from fractions import Fraction as frac
from typing import Set, List, Tuple, Union
from multimethod import multimethod


class Pitch(int):
    pass


class Hit:
    @multimethod
    def __init__(self, hit: 'Hit'):
        self.onset = hit.onset
        self.duration = hit.duration

    @multimethod
    def __init__(self, onset: frac, duration: frac):
        self.onset = onset
        self.duration = duration

    @multimethod
    def __init__(self, onset_duration: Tuple[frac, frac]):
        self.onset, self.duration = onset_duration

    def __hash__(self):
        return hash((self.onset, self.duration))

    def __eq__(self, other):
        if not isinstance(other, Hit):
            return False
        return self.onset == other.onset and self.duration == other.duration


class Chord:
    @multimethod
    def __init__(self, chord: 'Chord'):
        self.pitches = {p for p in chord.pitches}

    @multimethod
    def __init__(self, pitches: Set[Pitch]):
        self.pitches = pitches

    @multimethod
    def __init__(self, *pitches: Union[Pitch, int]):
        self.pitches = {Pitch(p) for p in pitches}

    @multimethod
    def __init__(self, pitches: Set[int]):
        self.pitches = {Pitch(p) for p in pitches}

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.pitches == other.pitches


class Rhythm:
    @multimethod
    def __init__(self, rhythm: 'Rhythm'):
        self.hits = {h for h in rhythm.hits}

    @multimethod
    def __init__(self, hits: Set[Hit]):
        self.hits = hits

    @multimethod
    def __init__(self, *hits: Union[Hit, Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    @multimethod
    def __init__(self, hits: Set[Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    def __add__(self, shift: frac) -> 'Rhythm':
        return Rhythm({Hit(hit.onset + shift, hit.duration) for hit in self.hits})

    def __eq__(self, other):
        if not isinstance(other, Rhythm):
            return False
        return self.hits == other.hits


class Harmony:
    @multimethod
    def __init__(self, harmony: 'Harmony'):
        self.chords = [c for c in harmony.chords]

    @multimethod
    def __init__(self, chords: List[Chord]):
        self.chords = chords

    @multimethod
    def __init__(self, chords: List[Set[int]]):
        self.chords = [Chord(c) for c in chords]

    @multimethod
    def __init__(self, *chords: Union[Chord, Set[Pitch], Set[int]]):
        self.chords = [Chord(c) for c in chords]

    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony(self.chords + other.chords)

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            return False
        return self.chords == other.chords


class Texture:
    @multimethod
    def __init__(self, texture: 'Texture'):
        self.rhythms = [r for r in texture.rhythms]

    @multimethod
    def __init__(self, *rhythms: Rhythm):
        self.rhythms = [r for r in rhythms]

    @multimethod
    def __init__(self, rhythms: List[Rhythm]):
        self.rhythms = rhythms

    def __mul__(self, harmony: Harmony) -> 'HarmonicTexture':
        return HarmonicTexture(self, harmony)

    def __add__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + other.rhythms)

    def __sub__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + [r + self.endpoint for r in other.rhythms])

    def __eq__(self, other):
        if not isinstance(other, Texture):
            return False
        return self.rhythms == other.rhythms

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

    def __eq__(self, other):
        if not isinstance(other, HarmonicTexture):
            return False
        return self.texture == other.texture and self.harmony == other.harmony
