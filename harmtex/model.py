# import warnings
from fractions import Fraction as frac
from typing import Set, List, Tuple, Union
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

    def __mul__(self, harmony: 'Harmony') -> 'TensorContraction':
        return TensorContraction(harmony, self, Instrumentation([Section({Instrument("Acoustic Grand Piano")})]))

    def __rmul__(self, harmony: 'Harmony') -> 'TensorContraction':
        return TensorContraction(harmony, self, Instrumentation([Section({Instrument("Acoustic Grand Piano")})]))

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
        return Harmony({self + c for c in other.chords})

    @multimethod
    def __add__(self, other: 'TensorContraction') -> 'TensorContraction':
        return TensorContraction(self + other.harmony,
                                 other.texture,
                                 other.instrumentation)

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
    def from_roman_numeral(cls, roman_numeral: str, inversion: int = 0, octave: int = 0) -> 'Chord':
        try:
            shifts = ROMAN_NUMERAL_TO_SHIFT[roman_numeral]
        except KeyError:
            raise ValueError(f"Roman numeral: {roman_numeral} not found.")

        return cls({Pitch(p + 12 * octave) for p in shifts})


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

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            return False
        return self.chords == other.chords

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
        self.sections = list(sections)

    def __eq__(self, other):
        if not isinstance(other, Instrumentation):
            return False
        return self.sections == other.sections

    def __add__(self, other: 'Instrumentation') -> 'Instrumentation':
        return Instrumentation(self.sections + other.sections)

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
    def __init__(self, harmony: Harmony = None, texture: Texture = None, instrumentation: Instrumentation = None):
        # if len(texture) != len(harmony):
        #     warnings.warn("Texture and harmony have different lengths")
        # if instrumentation is None:
        #     instrumentation = Instrumentation(*[Section() for _ in range(len(texture))])
        # else:
        #     if len(instrumentation.sections) != len(texture):
        #         warnings.warn("Texture and instrumentation have different lengths")
        self.texture = texture
        self.harmony = harmony
        self.instrumentation = instrumentation

    def __or__(self, other: 'TensorContraction') -> 'TensorContraction':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture + other.texture if self.texture is not None else other.texture
        new_instrumentation = self.instrumentation + other.instrumentation \
            if self.instrumentation is not None else other.instrumentation
        return TensorContraction(new_harmony, new_texture, new_instrumentation)

    def __sub__(self, other: 'TensorContraction') -> 'TensorContraction':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture - other.texture if self.texture is not None else None
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
        if self.texture is None and self.harmony is None and self.instrumentation is None:
            return result

        len_texture = len(self.texture.rhythms) if self.texture is not None else 0
        len_harmony = len(self.harmony.chords) if self.harmony is not None else 0
        len_instrumentation = len(self.instrumentation.sections) if self.instrumentation is not None else 0
        max_len = max(len_texture, len_harmony, len_instrumentation)

        if self.texture is None:
            unit_rhythm = Rhythm(Hit('0', '1'))
            self.texture = Texture([unit_rhythm for _ in range(max_len)])
        if self.harmony is None:
            unit_chord = Chord()
            self.harmony = Harmony([unit_chord for _ in range(max_len)])
        if self.instrumentation is None:
            unit_section = Section(Instrument('Acoustic Grand Piano'))
            self.instrumentation = Instrumentation([unit_section for _ in range(max_len)])

        for rhythm, chord, group in zip(self.texture.rhythms, self.harmony.chords, self.instrumentation.sections):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    for instrument in group.instruments:
                        result.add(Note(pitch, hit.onset, hit.duration, instrument))
        return result

    def ordered_notes(self) -> List['Note']:
        return sorted(self.notes(), key=lambda note: (note.onset, note.pitch.number))

    def to_midi(self, velocity=64, bpm=100):
        import pretty_midi
        notes = self.notes()
        start = min(note.onset for note in notes)
        midi = pretty_midi.PrettyMIDI()

        instruments = set(note.instrument for note in notes)
        for instrument in instruments:
            instrument_program = pretty_midi.instrument_name_to_program(instrument.name)
            track = pretty_midi.Instrument(program=instrument_program)
            notes_instrument = [note for note in notes if note.instrument == instrument]
            for note in notes_instrument:
                onset_s = float((note.onset-start) * 240 / bpm)
                duration_s = float(note.duration * 240 / bpm)
                end_s = onset_s + duration_s
                note = pretty_midi.Note(velocity=velocity, pitch=note.pitch.number, start=onset_s, end=end_s)
                track.notes.append(note)
            midi.instruments.append(track)
        return midi
