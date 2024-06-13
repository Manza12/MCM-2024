import warnings
from fractions import Fraction as frac
from typing import Set, List, Tuple, Union
from multimethod import multimethod


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
    def __init__(self, onset_duration: Tuple[frac, frac]):
        self.onset, self.duration = onset_duration

    def __hash__(self):
        return hash((self.onset, self.duration))

    def __eq__(self, other):
        if not isinstance(other, Hit):
            return False
        return self.onset == other.onset and self.duration == other.duration

    def __str__(self):
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
    def __init__(self, hits: Set[Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    def __add__(self, shift: frac) -> 'Rhythm':
        return Rhythm({Hit(hit.onset + shift, hit.duration) for hit in self.hits})

    def __eq__(self, other):
        if not isinstance(other, Rhythm):
            return False
        return self.hits == other.hits

    def __str__(self):
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

    def __str__(self):
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

    def __eq__(self, other):
        if not isinstance(other, Pitch):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __str__(self):
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
    #
    # @multimethod
    # def __init__(self, *pitches: Union[Pitch, int]):
    #     self.pitches = {Pitch(p) for p in pitches}

    @multimethod
    def __init__(self, pitches: Set[int]):
        self.pitches = {Pitch(p) for p in pitches}

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.pitches == other.pitches

    def __str__(self):
        return '{' + f"{', '.join([str(p) for p in self.pitches])}" + '}'


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

    def __str__(self):
        return f"[{', '.join([str(c) for c in self.chords])}]"


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

    def __str__(self):
        return self.name


class Section:
    @multimethod
    def __init__(self):
        self.instruments = set()

    @multimethod
    def __init__(self, group: 'Section'):
        self.instruments = {i for i in group.instruments}

    @multimethod
    def __init__(self, instruments: Set[Instrument]):
        self.instruments = instruments

    def __eq__(self, other):
        if not isinstance(other, Section):
            return False
        return self.instruments == other.instruments

    def __str__(self):
        return '{' + f"{', '.join([str(i) for i in self.instruments])}" + '}'


class Instrumentation:
    @multimethod
    def __init__(self):
        self.groups = []

    @multimethod
    def __init__(self, instrumentation: 'Instrumentation'):
        self.groups = [g for g in instrumentation.groups]

    @multimethod
    def __init__(self, groups: List[Section]):
        self.groups = groups

    def __eq__(self, other):
        if not isinstance(other, Instrumentation):
            return False
        return self.groups == other.groups

    def __add__(self, other: 'Instrumentation') -> 'Instrumentation':
        return Instrumentation(self.groups + other.groups)

    def __str__(self):
        return f"[{', '.join([str(g) for g in self.groups])}]"


# Time-Frequency
class Note:
    def __init__(self, pitch: Pitch, onset: frac, duration: frac, instrument: Instrument = None):
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

    def __str__(self):
        return f"({self.pitch}, {self.onset}, {self.duration}, {self.instrument})"


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
    def __init__(self, harmony: Harmony, texture: Texture, instrumentation: Instrumentation = None):
        if len(texture) != len(harmony):
            warnings.warn("Texture and harmony have different lengths")
        if instrumentation is None:
            instrumentation = Instrumentation([Section() for _ in range(len(texture))])
        else:
            if len(instrumentation.groups) != len(texture):
                warnings.warn("Texture and instrumentation have different lengths")
        self.texture = texture
        self.harmony = harmony
        self.instrumentation = instrumentation

    def __or__(self, other: 'TensorContraction') -> 'TensorContraction':
        return TensorContraction(self.harmony + other.harmony,
                                 self.texture + other.texture,
                                 self.instrumentation + other.instrumentation)

    def __sub__(self, other: 'TensorContraction') -> 'TensorContraction':
        return TensorContraction(self.harmony + other.harmony,
                                 self.texture - other.texture,
                                 self.instrumentation + other.instrumentation)

    def __eq__(self, other):
        if not isinstance(other, TensorContraction):
            return False
        same_texture = self.texture == other.texture
        same_harmony = self.harmony == other.harmony
        same_instrumentation = self.instrumentation == other.instrumentation
        return same_texture and same_harmony and same_instrumentation

    def notes(self) -> Set['Note']:
        result = set()
        for rhythm, chord, group in zip(self.texture.rhythms, self.harmony.chords, self.instrumentation.groups):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    for instrument in group.instruments:
                        result.add(Note(pitch, hit.onset, hit.duration, instrument))
        return result

    def to_midi(self, instrument='Acoustic Grand Piano', velocity=64, bpm=100):
        import pretty_midi
        notes = self.notes()
        start = min(note.onset for note in notes)
        midi = pretty_midi.PrettyMIDI()
        instrument_program = pretty_midi.instrument_name_to_program(instrument)
        track = pretty_midi.Instrument(program=instrument_program)
        for note in notes:
            onset_s = float((note.onset-start) * 240 / bpm)
            duration_s = float(note.duration * 240 / bpm)
            end_s = onset_s + duration_s
            note = pretty_midi.Note(velocity=velocity, pitch=note.pitch.number, start=onset_s, end=end_s)
            track.notes.append(note)
        midi.instruments.append(track)
        return midi
