import warnings
from fractions import Fraction as frac
from typing import Set, List, Tuple, Union, Optional
from multimethod import multimethod
from .constants import ROMAN_NUMERAL_TO_SHIFT


# Time
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
    def __init__(self, onset: str, duration: str):
        self.onset = frac(onset)
        self.duration = frac(duration)

    @multimethod
    def __init__(self, onset_duration: Tuple[frac, frac]):
        self.onset, self.duration = onset_duration

    def __radd__(self, other: frac) -> 'Hit':
        return Hit(self.onset + other, self.duration)

    def __hash__(self):
        return hash((self.onset, self.duration))

    def __eq__(self, other):
        if not isinstance(other, Hit):
            return False
        return self.onset == other.onset and self.duration == other.duration

    def __repr__(self):
        return f"({self.onset}, {self.duration})"


class Rhythm:
    @multimethod
    def __init__(self):
        self.hits = set()

    @multimethod
    def __init__(self, rhythm: 'Rhythm'):
        self.hits = {h for h in rhythm.hits}

    @multimethod
    def __init__(self, hits: Set[Hit]):
        self.hits = hits

    @multimethod
    def __init__(self, *hits: Hit):
        self.hits = set(hits)

    @multimethod
    def __init__(self, hits: Set[Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    @multimethod
    def __init__(self, *hits: Tuple[frac, frac]):
        self.hits = {Hit(h) for h in hits}

    def __add__(self, shift: frac) -> 'Rhythm':
        return Rhythm({shift + Hit(hit.onset, hit.duration) for hit in self.hits})

    def __eq__(self, other):
        if not isinstance(other, Rhythm):
            return False
        return self.hits == other.hits

    def __repr__(self):
        return '{' + f"{', '.join([str(h) for h in self.hits])}" + '}'


class Texture:
    @multimethod
    def __init__(self):
        self.rhythms = []

    @multimethod
    def __init__(self, texture: 'Texture'):
        self.rhythms = [r for r in texture.rhythms]

    @multimethod
    def __init__(self, *rhythms: Rhythm):
        self.rhythms = [r for r in rhythms]

    @multimethod
    def __init__(self, rhythms: List[Rhythm]):
        self.rhythms = rhythms

    @multimethod
    def __mul__(self, harmony: 'Harmony') -> 'HarmonicTexture':
        return HarmonicTexture(harmony, self)

    @multimethod
    def __mul__(self, instrumentation: 'Instrumentation') -> 'InstrumentedTexture':
        return InstrumentedTexture(instrumentation, self)

    def __add__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + other.rhythms)

    def __sub__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + [r + self.endpoint for r in other.rhythms])

    def __eq__(self, other):
        if not isinstance(other, Texture):
            return False
        return self.rhythms == other.rhythms

    def __len__(self):
        return len(self.rhythms)

    def __repr__(self):
        return f"[{', '.join([str(r) for r in self.rhythms])}]"

    def __getitem__(self, key):
        return Texture(self.rhythms[key])

    @property
    def endpoint(self) -> frac:
        result = frac(0)
        for rhythm in self.rhythms:
            for hit in rhythm.hits:
                end = hit.onset + hit.duration
                if end > result:
                    result = end
        return result


# Frequency
class Pitch:
    @multimethod
    def __init__(self, pitch: 'Pitch'):
        self.number = pitch.number

    @multimethod
    def __init__(self, number: int):
        self.number = number

    @multimethod
    def __add__(self, other: 'Pitch') -> 'Pitch':
        return Pitch(self.number + other.number)

    @multimethod
    def __add__(self, other: 'Chord') -> 'Chord':
        return Chord({self + p for p in other.pitches})

    @multimethod
    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony([self + c for c in other.chords])

    @multimethod
    def __add__(self, other: 'TensorContraction') -> 'TensorContraction':
        return TensorContraction(self + other.harmony,
                                 other.texture,
                                 other.instrumentation)

    @multimethod
    def __add__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self + other.harmony, other.texture)

    def __eq__(self, other):
        if not isinstance(other, Pitch):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __repr__(self):
        return str(self.number)


class Chord:
    @multimethod
    def __init__(self):
        self.pitches = set()

    @multimethod
    def __init__(self, chord: 'Chord'):
        self.pitches = {p for p in chord.pitches}

    @multimethod
    def __init__(self, pitches: Set[Pitch]):
        self.pitches = pitches

    @multimethod
    def __init__(self, *pitches: Pitch):
        self.pitches = set(pitches)

    @multimethod
    def __init__(self, pitches: Set[int]):
        self.pitches = {Pitch(p) for p in pitches}

    def __radd__(self, other: Pitch):
        return Chord({other + p for p in self.pitches})

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.pitches == other.pitches

    def __repr__(self):
        return '{' + f"{', '.join([str(p) for p in self.pitches])}" + '}'

    @classmethod
    def from_roman_numeral(cls, roman_numeral: str,
                           inversion: int = 0,
                           octave: int = 0,
                           n_notes: Optional[int] = None
                           ) -> 'Chord':
        try:
            shifts = ROMAN_NUMERAL_TO_SHIFT[roman_numeral]
        except KeyError:
            raise ValueError(f"Roman numeral: {roman_numeral} not found.")

        n = len(shifts)
        shifts_spacing = [(shifts[(i + 1) % n] - shifts[i % n]) % 12 for i in range(len(shifts))]
        if n_notes is None:
            n_notes = n

        if inversion != 0:
            shifts = shifts[inversion:] + shifts[:inversion]
            shifts_spacing = shifts_spacing[inversion:] + shifts_spacing[:inversion]

        bass = shifts[0] + 12 * octave
        return cls({bass + sum(shifts_spacing[:i]) for i in range(n_notes)})


class Harmony:
    @multimethod
    def __init__(self):
        self.chords = []

    @multimethod
    def __init__(self, harmony: 'Harmony'):
        self.chords = [c for c in harmony.chords]

    @multimethod
    def __init__(self, chords: List[Chord]):
        self.chords = chords

    @multimethod
    def __init__(self, *chords: Chord):
        self.chords = list(chords)

    @multimethod
    def __init__(self, chords: List[Set[int]]):
        self.chords = [Chord(c) for c in chords]

    @multimethod
    def __init__(self, *chords: Union[Chord, Set[Pitch], Set[int]]):
        self.chords = [Chord(c) for c in chords]

    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony(self.chords + other.chords)

    @multimethod
    def __mul__(self, texture: Texture) -> 'HarmonicTexture':
        return HarmonicTexture(self, texture)

    @multimethod
    def __mul__(self, instrumentation: 'Instrumentation') -> 'HarmonicInstrumentation':
        return HarmonicInstrumentation(self, instrumentation)

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            return False
        return self.chords == other.chords

    def __getitem__(self, key):
        return Harmony(self.chords[key])

    def __len__(self):
        return len(self.chords)

    def __repr__(self):
        return f"[{', '.join([str(c) for c in self.chords])}]"

    @classmethod
    def from_chord(cls, chord: Chord):
        ordered_pitches = sorted(chord.pitches, key=lambda p: p.number)
        return Harmony([Chord(c) for c in ordered_pitches])


# Instruments
class Instrument:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Instrument):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Section:
    @multimethod
    def __init__(self):
        self.instruments = set()

    @multimethod
    def __init__(self, section: 'Section'):
        self.instruments = {i for i in section.instruments}

    @multimethod
    def __init__(self, instruments: Set[Instrument]):
        self.instruments = instruments

    @multimethod
    def __init__(self, *instruments: Instrument):
        self.instruments = set(instruments)

    def __eq__(self, other):
        if not isinstance(other, Section):
            return False
        return self.instruments == other.instruments

    def __repr__(self):
        return '{' + f"{', '.join([str(i) for i in self.instruments])}" + '}'


class Instrumentation:
    @multimethod
    def __init__(self):
        self.sections = []

    @multimethod
    def __init__(self, instrumentation: 'Instrumentation'):
        self.sections = [s for s in instrumentation.sections]

    @multimethod
    def __init__(self, sections: List[Section]):
        self.sections = sections

    @multimethod
    def __init__(self, *sections: Section):
        if len(sections) == 1 and isinstance(sections[0], list):
            self.sections = []
        else:
            self.sections = list(sections)

    def __getitem__(self, key):
        return Instrumentation(self.sections[key])

    def __len__(self):
        return len(self.sections)

    def __add__(self, other: 'Instrumentation') -> 'Instrumentation':
        return Instrumentation(self.sections + other.sections)

    @multimethod
    def __mul__(self, harmony: Harmony) -> 'HarmonicInstrumentation':
        return HarmonicInstrumentation(harmony, self)

    @multimethod
    def __mul__(self, texture: Texture) -> 'InstrumentedTexture':
        return InstrumentedTexture(self, texture)

    def __eq__(self, other):
        if not isinstance(other, Instrumentation):
            return False
        return self.sections == other.sections

    def __repr__(self):
        return f"[{', '.join([str(g) for g in self.sections])}]"


# Time-Frequency
class Note:
    def __init__(self, pitch: Pitch, onset: frac, duration: frac, instrument: Instrument):
        self.pitch = pitch
        self.onset = onset
        self.duration = duration
        self.instrument = instrument

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        same_pitch = self.pitch == other.pitch
        same_onset = self.onset == other.onset
        same_duration = self.duration == other.duration
        same_instrument = self.instrument == other.instrument
        return same_pitch and same_onset and same_duration and same_instrument

    def __hash__(self):
        return hash((self.pitch, self.onset, self.duration, self.instrument))

    def __repr__(self):
        return f"({self.pitch}, {self.onset}, {self.duration}, {self.instrument})"

    @property
    def start(self):
        return self.onset

    @property
    def end(self):
        return self.onset + self.duration

    @property
    def frequency(self):
        return self.pitch.number


class HarmonicTexture:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.texture = Texture()

    @multimethod
    def __init__(self, harmonic_texture: 'HarmonicTexture'):
        self.harmony = Harmony(harmonic_texture.harmony)
        self.texture = Texture(harmonic_texture.texture)

    @multimethod
    def __init__(self, harmony: Harmony, texture: Texture):
        same_length = len(harmony) == len(texture)
        if not same_length:
            warnings.warn("Harmony and texture have different lengths; " +
                          f"Harmony: {len(harmony)}, " +
                          f"Texture: {len(texture)}. " +
                          f"Clipping to the minimum length ({min(len(harmony), len(texture))}).")

        min_length = min(len(harmony), len(texture))

        self.harmony = harmony[:min_length]
        self.texture = texture[:min_length]

    def __or__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.harmony + other.harmony, self.texture + other.texture)

    def __sub__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.harmony + other.harmony, self.texture - other.texture)

    def __mul__(self, other: Instrumentation) -> 'TensorContraction':
        return TensorContraction(self.harmony, self.texture, other)

    def __eq__(self, other):
        if not isinstance(other, HarmonicTexture):
            return False
        return self.harmony == other.harmony and self.texture == other.texture

    def notes(self, instrument_name: str = 'Acoustic Grand Piano'):
        result = set()

        instrument = Instrument(instrument_name)

        for rhythm, chord in zip(self.texture.rhythms, self.harmony.chords):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    result.add(Note(pitch, hit.onset, hit.duration, instrument))
        return result

    def ordered_notes(self, instrument_name: str = 'Acoustic Grand Piano'):
        notes = self.notes(instrument_name)
        return sorted(notes, key=lambda note: (note.onset, note.pitch.number))

    def to_midi(self, velocity=64, bpm=100):
        from .midi import to_midi
        return to_midi(self.notes(), velocity, bpm)


class HarmonicInstrumentation:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.instrumentation = Instrumentation()

    @multimethod
    def __init__(self, harmonic_instrumentation: 'HarmonicInstrumentation'):
        self.harmony = Harmony(harmonic_instrumentation.harmony)
        self.instrumentation = Instrumentation(harmonic_instrumentation.instrumentation)

    @multimethod
    def __init__(self, harmony: Harmony, instrumentation: Instrumentation):
        same_length = len(harmony) == len(instrumentation)
        if not same_length:
            warnings.warn("Harmony and instrumentation have different lengths; "
                          f"Harmony: {len(harmony)}, "
                          f"Instrumentation: {len(instrumentation)}")

        self.harmony = harmony
        self.instrumentation = instrumentation

    def __or__(self, other: 'HarmonicInstrumentation') -> 'HarmonicInstrumentation':
        return HarmonicInstrumentation(self.harmony + other.harmony, self.instrumentation + other.instrumentation)

    def __eq__(self, other):
        if not isinstance(other, HarmonicInstrumentation):
            return False
        return self.harmony == other.harmony and self.instrumentation == other.instrumentation


class InstrumentedTexture:
    @multimethod
    def __init__(self):
        self.instrumentation = Instrumentation()
        self.texture = Texture()

    @multimethod
    def __init__(self, texture_instrumentation: 'InstrumentedTexture'):
        self.instrumentation = Instrumentation(texture_instrumentation.instrumentation)
        self.texture = Texture(texture_instrumentation.texture)

    @multimethod
    def __init__(self, instrumentation: Instrumentation, texture: Texture):
        same_length = len(texture) == len(instrumentation)
        if not same_length:
            warnings.warn("Texture and instrumentation have different lengths; "
                          f"Texture: {len(texture)}, "
                          f"Instrumentation: {len(instrumentation)}")

        self.instrumentation = instrumentation
        self.texture = texture

    def __or__(self, other: 'InstrumentedTexture') -> 'InstrumentedTexture':
        return InstrumentedTexture(self.instrumentation + other.instrumentation, self.texture + other.texture)

    def __sub__(self, other: 'InstrumentedTexture') -> 'InstrumentedTexture':
        return InstrumentedTexture(self.instrumentation + other.instrumentation, self.texture - other.texture)

    def __eq__(self, other):
        if not isinstance(other, InstrumentedTexture):
            return False
        return self.texture == other.texture and self.instrumentation == other.instrumentation


class TensorContraction:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.texture = Texture()
        self.instrumentation = Instrumentation()

    @multimethod
    def __init__(self, tensor_contraction: 'TensorContraction'):
        self.harmony = Harmony(tensor_contraction.harmony)
        self.texture = Texture(tensor_contraction.texture)
        self.instrumentation = Instrumentation(tensor_contraction.instrumentation)

    @multimethod
    def __init__(self, harmony: Harmony, texture: Texture, instrumentation: Instrumentation):
        same_length = len(harmony) == len(texture) == len(instrumentation)
        if not same_length:
            warnings.warn("Harmony, texture and instrumentation have different lengths; "
                          f"Harmony: {len(harmony)}, "
                          f"Texture: {len(texture)}, "
                          f"Instrumentation: {len(instrumentation)}")
        min_length = min(len(harmony), len(texture), len(instrumentation))
        self.texture = texture[:min_length]
        self.harmony = harmony[:min_length]
        self.instrumentation = instrumentation[:min_length]

    def __or__(self, other: 'TensorContraction') -> 'TensorContraction':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture + other.texture if self.texture is not None else other.texture
        new_instrumentation = self.instrumentation + other.instrumentation \
            if self.instrumentation is not None else other.instrumentation
        return TensorContraction(new_harmony, new_texture, new_instrumentation)

    def __sub__(self, other: 'TensorContraction') -> 'TensorContraction':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture - other.texture if self.texture is not None else other.texture
        new_instrumentation = self.instrumentation + other.instrumentation \
            if self.instrumentation is not None else other.instrumentation
        return TensorContraction(new_harmony, new_texture, new_instrumentation)

    def __eq__(self, other):
        if not isinstance(other, TensorContraction):
            return False
        same_texture = self.texture == other.texture
        same_harmony = self.harmony == other.harmony
        same_instrumentation = self.instrumentation == other.instrumentation
        return same_texture and same_harmony and same_instrumentation

    def notes(self) -> Set['Note']:
        result = set()

        for rhythm, chord, group in zip(self.texture.rhythms, self.harmony.chords, self.instrumentation.sections):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    for instrument in group.instruments:
                        result.add(Note(pitch, hit.onset, hit.duration, instrument))
        return result

    def ordered_notes(self) -> List['Note']:
        notes = self.notes()
        return sorted(notes, key=lambda note: (note.onset, note.pitch.number))

    def to_midi(self, velocity=64, bpm=100):
        from .midi import to_midi
        return to_midi(self.notes(), velocity, bpm)
