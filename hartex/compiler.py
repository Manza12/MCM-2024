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
            start = self.decode(element[0])
            duration = self.decode(element[1])
            return Hit(start, duration)
        elif element.tag == 'rhythm':
            hits = []
            for child in element:
                hit = self.decode(child)
                hits.append(hit)
            return Rhythm(*hits)
        elif element.tag == 'texture':
            rhythms = []
            for child in element:
                rhythm = self.decode(child)
                rhythms.append(rhythm)
            texture = Texture(*rhythms)
            return texture
        elif element.tag == 'number':
            return int(element.text)
        elif element.tag == 'pitch':
            number = self.decode(element[0])
            return Pitch(number)
        elif element.tag == 'chord':
            pitches = []
            for child in element:
                pitch = self.decode(child)
                pitches.append(pitch)
            chord = Chord(*pitches)
            return chord
        elif element.tag == 'harmony':
            chords = []
            for child in element:
                chord = self.decode(child)
                chords.append(chord)
            harmony = Harmony(*chords)
            return harmony
        elif element.tag == 'product':
            harmony = self.decode(element[0])
            texture = self.decode(element[1])
            harmonic_texture = HarmonicTexture(harmony, texture)
            return harmonic_texture
        elif element.tag == 'parallel':
            harmonic_texture = HarmonicTexture()
            for child in element:
                harmonic_texture = harmonic_texture | self.decode(child)
            return harmonic_texture
        elif element.tag == 'concatenate':
            harmonic_texture = HarmonicTexture()
            for child in element:
                harmonic_texture = harmonic_texture - self.decode(child)
            return harmonic_texture
        else:
            raise NotImplementedError("Tag '%s' not implemented." % element.tag)
