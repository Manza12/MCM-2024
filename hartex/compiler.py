from pathlib import Path
import xml.etree.ElementTree as ET
from .objects import frac, Hit, Rhythm, Texture, Pitch, Chord, Harmony, HarmonicTexture


class ScoreTree:
    def __init__(self, file_path: Path):
        self.file_path = file_path

        self.objects = {}

        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

        self.harmonic_texture = self.decode(self.root)

    def to_midi(self, instrument: str = 'Acoustic Grand Piano', bpm: int = 64, velocity: int = 50):
        return self.harmonic_texture.to_midi(instrument, velocity, bpm)

    def decode(self, element: ET.Element):
        if element.tag == 'start':
            return frac(int(element.attrib['num']), int(element.attrib['den']))
        elif element.tag == 'duration':
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
        elif element.tag == 'id':
            return self.objects[element.text]
        else:
            raise NotImplementedError("Tag '%s' not implemented." % element.tag)