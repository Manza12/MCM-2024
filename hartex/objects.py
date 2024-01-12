from fractions import Fraction as frac
from typing import Set, List, Tuple
from multimethod import multimethod


class Pitch(int):
    pass


class Hit:
    @multimethod
    def __init__(self, onset: frac, duration: frac):
        self.onset = onset
        self.duration = duration

    @multimethod
    def __init__(self, onset_duration: Tuple[frac, frac]):
        self.onset, self.duration = onset_duration


class Chord:
    @multimethod
    def __init__(self, pitches: Set[Pitch]):
        self.pitches = pitches

    @multimethod
    def __init__(self, *pitches: Pitch):
        self.pitches = set(pitches)

    @multimethod
    def __init__(self, pitches: Set[int]):
        self.pitches = {Pitch(p) for p in pitches}

    @multimethod
    def __init__(self, *pitches: int):
        self.pitches = {Pitch(p) for p in pitches}


class Rhythm:
    @multimethod
    def __init__(self, hits: Set[Hit]):
        self.hits = hits

    @multimethod
    def __init__(self, *hits: Hit):
        self.hits = hits

    @multimethod
    def __init__(self, hits: Set[Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    @multimethod
    def __init__(self, *hits: Tuple[frac, frac]):
        self.hits = {Hit(h) for h in hits}

    def __add__(self, shift: frac) -> 'Rhythm':
        return Rhythm({Hit(hit.onset + shift, hit.duration) for hit in self.hits})


class Harmony:
    def __init__(self, chords: List[Chord]):
        self.chords = chords

    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony(self.chords + other.chords)


class Texture:
    def __init__(self, rhythms: List[Rhythm]):
        self.rhythms = rhythms

    def __mul__(self, harmony: Harmony) -> 'HarmonicTexture':
        return HarmonicTexture(self, harmony)

    def __add__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + other.rhythms)

    def __sub__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + [r + self.endpoint for r in other.rhythms])

    @property
    def endpoint(self) -> frac:
        result = frac(0)
        for rhythm in self.rhythms:
            for hit in rhythm.hits:
                end = hit.onset + hit.duration
                if end > result:
                    result = end
        return result


class HarmonicTexture:
    def __init__(self, texture: Texture, harmony: Harmony):
        self.texture = texture
        self.harmony = harmony

    def __or__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.texture + other.texture, self.harmony + other.harmony)

    def __sub__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.texture - other.texture, self.harmony + other.harmony)
