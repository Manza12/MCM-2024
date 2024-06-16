from harmtex.functions import concatenation
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrumentation, Section, Instrument
from harmtex.plot import plot_notes, plt

h_a_0 = Harmony(
    Chord.from_roman_numeral('i', 0, -1, 1),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 1, 0, 3)[0, 2],
)

h_a_1 = Harmony(
    Chord(),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 1, 0, 3)[0, 2],
)

h_a_2 = Harmony(
    Chord.from_roman_numeral('i', 0, 0, 1),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 1, 0, 3)[0, 2],
)

h_a_3 = h_a_1

h_a_4 = Harmony(
    Chord.from_roman_numeral('i', 0, -1, 1),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 2, 0, 2),
)

h_a_5 = Harmony(
    Chord(),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 2, 0, 2),
)

h_a_6 = Harmony(
    Chord.from_roman_numeral('i', 0, 0, 1),
    Chord.from_roman_numeral('i', 0, 0, 2),
    Chord.from_roman_numeral('i', 1, 0, 2),
)

h_a_7 = h_a_1

h_a_8 = Harmony(
    Chord.from_roman_numeral('iio7', 0, -1, 1),
    Chord.from_roman_numeral('iio7', 0, 0, 3)[0, 2],
    Chord.from_roman_numeral('iio7', 2, 0, 3)[0, 2],
)

h_a_9 = Harmony(
    Chord(),
    Chord.from_roman_numeral('iio7', 0, 0, 3)[0, 2],
    Chord.from_roman_numeral('iio7', 2, 0, 3)[0, 2],
)

h_a_10 = Harmony(
    Chord.from_roman_numeral('iio7', 0, 0, 1),
    Chord.from_roman_numeral('iio7', 0, 0, 3)[0, 2],
    Chord.from_roman_numeral('iio7', 2, 0, 3)[0, 2],
)

h_a_11 = h_a_9

h_a_12 = Harmony(
    Chord.from_roman_numeral('V7', 1, -1, 1),
    Chord.from_roman_numeral('V7', 2, 0, 3)[0, 2],
    Chord.from_roman_numeral('V7', 0, 0, 4)[0, 3],
)


h_a_13 = Harmony(
    Chord(),
    Chord.from_roman_numeral('V7', 2, 0, 3)[0, 2],
    Chord.from_roman_numeral('V7', 0, 0, 4)[0, 3],
)


harmonies = [h_a_0, h_a_1, h_a_2, h_a_3, h_a_4, h_a_5, h_a_6, h_a_7,
             h_a_8, h_a_9, h_a_10, h_a_11, h_a_12, h_a_13]

t_a = Texture(
    Rhythm(Hit('0/8', '1/4')),
    Rhythm(Hit('0/8', '1/8'), Hit('1/8', '1/8')),
    Rhythm(Hit('2/8', '1/8'), Hit('3/8', '1/8')),
)

o_a = Instrumentation(
    Section({Instrument('Contrabass'), Instrument('Cello')}),
    Section({Instrument('Viola')}),
    Section({Instrument('Viola')}),
)

blocks = [t_a * h * o_a for h in harmonies]
first_phrase = concatenation(*blocks)

G3 = Pitch(55)
first_phrase_in_G3 = G3 + first_phrase

# Print
print('Notes:')
fragment = first_phrase_in_G3.ordered_notes()
for note in fragment:
    print(note)

print('\nTexture:')
print(first_phrase_in_G3.texture)

print('\nHarmony:')
print(first_phrase_in_G3.harmony)

# Write MIDI
midi = first_phrase_in_G3.to_midi(bpm=220)
midi.write('../midi/example_2.mid')

# Plot
plot_notes(first_phrase_in_G3,
           x_tick_start=0,
           x_tick_step=0.5)
plt.show()
