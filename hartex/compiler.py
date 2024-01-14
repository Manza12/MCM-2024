from pathlib import Path
import xml.etree.ElementTree as ET
from .objects import frac, Hit, Rhythm, Texture, Pitch, Chord, Harmony, HarmonicTexture, Instrument


class ScoreTree:
    def __init__(self, file_path: Path):
        # File path
        self.file_path = file_path

        # Metadata
        self.title = ''
        self.composer = ''
        self.tempo = ScoreTree.Tempo(frac(1, 4), 100)
        self.time_signature = ScoreTree.TimeSignature(4, 4)
        self.anacrusis = frac(0, 1)

        # Objects
        self.objects = {}

        # Parse XML
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

        # Decode XML
        self.instruments = []
        self.decode(self.root)

    class Tempo:
        def __init__(self, beat: frac, bpm: int):
            self.beat = beat
            self.bpm = bpm

        def __str__(self):
            return f'{self.beat} = {self.bpm}'

    class TimeSignature:
        def __init__(self, numerator: int, denominator: int):
            self.numerator = numerator
            self.denominator = denominator

        def __str__(self):
            return f'{self.numerator}/{self.denominator}'

    def to_midi(self, velocity: int = 50):
        import pretty_midi

        bpm = self.tempo.bpm * self.tempo.beat / frac(1, 4)

        start = -self.anacrusis

        midi = pretty_midi.PrettyMIDI()

        for instrument in self.instruments:
            notes = instrument.harmonic_texture.notes()
            instrument_program = pretty_midi.instrument_name_to_program(instrument.name)
            track = pretty_midi.Instrument(program=instrument_program)
            for note in notes:
                onset_s = float((note.onset - start) * 240 / bpm)
                duration_s = float(note.duration * 240 / bpm)
                end_s = onset_s + duration_s
                note = pretty_midi.Note(velocity=velocity, pitch=note.pitch.number, start=onset_s, end=end_s)
                track.notes.append(note)
            midi.instruments.append(track)
        return midi

    def decode(self, element: ET.Element):
        # Root
        if element.tag == 'score-tree':
            for child in element:
                self.decode(child)
        # Metadata
        elif element.tag == 'title':
            self.title = element.text
        elif element.tag == 'composer':
            self.composer = element.text
        elif element.tag == 'tempo':
            self.tempo = ScoreTree.Tempo(self.decode(element[0]), int(element[1].text))
        elif element.tag == 'time-signature':
            self.time_signature = ScoreTree.TimeSignature(int(element[0].text), int(element[1].text))
        elif element.tag == 'anacrusis':
            self.anacrusis = frac(int(element.attrib['num']), int(element.attrib['den']))
        # Ids
        elif element.tag in ['hits', 'rhythms', 'textures', 'pitches', 'chords', 'harmonies']:
            for child in element:
                assert child.attrib.get('id') is not None
                self.objects[child.attrib['id']] = self.decode(child)
        elif element.tag == 'id':
            return self.objects[element.text]
        # Objects
        elif element.tag in ['onset', 'duration', 'beat']:
            return frac(int(element.attrib['num']), int(element.attrib['den']))
        elif element.tag == 'hit':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode hit
            start = self.decode(element[0])
            duration = self.decode(element[1])
            hit = Hit(start, duration)

            # Save the hit if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = hit

            return hit
        elif element.tag == 'rhythm':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode rhythm
            hits = []
            for child in element:
                hit = self.decode(child)
                hits.append(hit)
            rhythm = Rhythm(*hits)

            # Save the rhythm if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = rhythm

            return rhythm
        elif element.tag == 'texture':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode texture
            rhythms = []
            for child in element:
                rhythm = self.decode(child)
                rhythms.append(rhythm)
            texture = Texture(*rhythms)

            # Save the texture if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = texture

            return texture
        elif element.tag == 'number':
            return int(element.text)
        elif element.tag == 'pitch':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode pitch
            number = self.decode(element[0])
            pitch = Pitch(number)

            # Save the pitch if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = pitch

            return pitch
        elif element.tag == 'chord':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode chord
            pitches = []
            for child in element:
                pitch = self.decode(child)
                pitches.append(pitch)
            chord = Chord(*pitches)

            # Save the chord if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = chord

            return chord
        elif element.tag == 'harmony':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode harmony
            chords = []
            for child in element:
                chord = self.decode(child)
                chords.append(chord)
            harmony = Harmony(*chords)

            # Save the harmony if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = harmony

            return harmony
        # Operators
        elif element.tag == 'product':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode product
            texture = self.decode(element[0])
            harmony = self.decode(element[1])
            harmonic_texture = HarmonicTexture(texture, harmony)

            # Save the harmonic texture if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = harmonic_texture

            return harmonic_texture
        elif element.tag == 'parallel':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode parallel
            harmonic_texture = HarmonicTexture()
            for child in element:
                harmonic_texture = harmonic_texture | self.decode(child)

            # Save the harmonic texture if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = harmonic_texture

            return harmonic_texture
        elif element.tag == 'concatenate':
            # Check if it's a reference
            if len(element) != 0 and element[0].tag == 'id':
                return self.decode(element[0])

            # Decode concatenate
            harmonic_texture = HarmonicTexture()
            for child in element:
                harmonic_texture = harmonic_texture - self.decode(child)

            # Save the harmonic texture if it has an id
            if element.attrib.get('id') is not None:
                self.objects[element.attrib['id']] = harmonic_texture

            return harmonic_texture
        elif element.tag == 'instrument':
            name = element.attrib['name']
            harmonic_texture = self.decode(element[0])
            instrument = Instrument(name, harmonic_texture)
            self.instruments.append(instrument)
        # Not implemented
        else:
            raise NotImplementedError("Tag '%s' not implemented." % element.tag)
