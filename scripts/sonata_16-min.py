from harmtex.functions import concatenation, parallelization
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrumentation, Instrument, Section
from harmtex.plot import plot_notes, plt


# Tonic
C4 = Pitch(60)

# Octaves
octave_0 = C4
octave_minus_1 = C4 - 12
octave_1 = C4 + 12

# Textures
t_alberti = Texture(
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

# Orquestration
piano = Section(Instrument('Acoustic Grand Piano'))
o_harmony = Instrumentation(piano, piano, piano)

# Harmony
h_I = Harmony.from_chord(Chord({0, 3, 7}))
h_V_no_5 = Harmony.from_chord(Chord({2, 5, 7}))
h_IV = Harmony.from_chord(Chord({0, 5, 8}))
h_V = Harmony.from_chord(Chord({-1, 2, 7}))

block_1 = octave_0 + t_alberti * h_I * o_harmony
block_2 = block_1
block_3 = octave_0 + t_alberti * h_V_no_5 * o_harmony
block_4 = octave_0 + t_alberti * h_I * o_harmony
block_5 = octave_0 + t_alberti * h_IV * o_harmony
block_6 = octave_0 + t_alberti * h_I * o_harmony
block_7 = octave_0 + t_alberti * h_V * o_harmony
block_8 = octave_0 + t_alberti * h_I * o_harmony

harmony = concatenation(block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8)

# Melody
half = Texture(Rhythm(Hit('0', '1/2')))
quarter = Texture(Rhythm(Hit('0', '1/4')))
eighth = Texture(Rhythm(Hit('0', '1/8')))
sixteenth = Texture(Rhythm(Hit('0', '1/16')))
dotted_quarter = Texture(Rhythm(Hit('0', '3/8')))
trino = Texture(Rhythm(Hit('0', '1/24')))

t_melody_1 = half - quarter - quarter - dotted_quarter - sixteenth - sixteenth - quarter - quarter
t_melody_2 = half - quarter - quarter - quarter - trino - trino - trino - sixteenth - sixteenth - quarter - quarter

leading = Harmony(Chord({-1}))
tonic = Harmony(Chord({0}))
super_tonic = Harmony(Chord({2}))
mediant = Harmony(Chord({3}))
subdominant = Harmony(Chord({5}))
dominant = Harmony(Chord({7}))
sub_mediant = Harmony(Chord({8}))
tonic_1 = Harmony(Chord({12}))
silence = Harmony(Chord())

h_melody_1 = tonic + mediant + dominant + leading + tonic + super_tonic + tonic + silence
h_melody_2 = sub_mediant + dominant + tonic_1 + dominant + subdominant + \
             dominant + subdominant + mediant + subdominant + mediant + silence

o_meoldy_1 = Instrumentation([piano for _ in range(8)])
o_meoldy_2 = Instrumentation([piano for _ in range(11)])

melody_1 = octave_1 + t_melody_1 * h_melody_1 * o_meoldy_1
melody_2 = octave_1 + t_melody_2 * h_melody_2 * o_meoldy_2
melody = concatenation(melody_1, melody_2)

# Structure
phrase_1 = parallelization(harmony, melody)

# Write MIDI
fragment = phrase_1
midi = fragment.to_midi(bpm=120)
midi.write('../midi/sonata_16-min.mid')

# Plot
plot_notes(fragment,
           figsize=(12, 6),
           x_tick_start=0,
           x_tick_step=1,)
plt.show()
