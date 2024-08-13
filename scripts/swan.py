from harmtex.functions import concatenation, parallelization
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrumentation, Instrument, Section
from harmtex.plot import plot_notes, plt


# Tonic
G3 = Pitch(55)

# Textures
t_bass = Texture(
    Rhythm(Hit('0', '1/8'), Hit('4/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8'), Hit('5/8', '1/8')),
    Rhythm(Hit('2/8', '1/8'))
)

t_accompaniment = Texture(
    Rhythm(Hit('0', '1/16')),
    Rhythm(Hit('1/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
    Rhythm(Hit('2/16', '1/16'))
)

t_accompaniment_3 = t_accompaniment - t_accompaniment - t_accompaniment

# Orquestration
piano = Section(Instrument('Acoustic Grand Piano'))
o_bass = Instrumentation(piano, piano, piano)
o_accompaniment = Instrumentation(*(piano for _ in range(12)))


# Blocks
def generate_dotted_half_block(harmony: Harmony, tonic: Pitch = G3):
    h_bass = harmony[:3]
    h_accompaniment = harmony[3:]

    block_bass = tonic + t_bass * h_bass * o_bass

    h_accompaniment_3 = h_accompaniment + h_accompaniment + h_accompaniment
    block_accompaniment = tonic + t_accompaniment_3 * h_accompaniment_3 * o_accompaniment

    block = parallelization(block_bass, block_accompaniment)
    return block


# Harmony
h_I = Harmony.from_chord(Chord({-12, -5, 0, 4, 7, 12, 16}))
h_ii7 = Harmony.from_chord(Chord({-12, -3, 2, 5, 9, 14, 17}))
h_V_ton = Harmony.from_chord(Chord({-12, -5, 2, 5, 11, 14, 17}))
h_viio7_of_ii = Harmony.from_chord(Chord({-12, -3, 3, 6, 9, 15, 18}))
h_V7_of_ii = Harmony.from_chord(Chord({-13, -3, 3, 6, 9, 15, 18}))

piano_part_1 = generate_dotted_half_block(h_I)
piano_part_2 = generate_dotted_half_block(h_ii7)
piano_part_3 = generate_dotted_half_block(h_V_ton)
piano_part_4 = generate_dotted_half_block(h_viio7_of_ii)
piano_part_5 = generate_dotted_half_block(h_V7_of_ii)
piano_part = concatenation(piano_part_1, piano_part_1,
                           piano_part_1, piano_part_1,
                           piano_part_2, piano_part_2,
                           piano_part_2, piano_part_3,
                           piano_part_1, piano_part_1,
                           piano_part_1, piano_part_1,
                           piano_part_4, piano_part_5,)

# # Melody
# half = Texture(Rhythm(Hit('0', '1/2')))
# quarter = Texture(Rhythm(Hit('0', '1/4')))
# eighth = Texture(Rhythm(Hit('0', '1/8')))
# sixteenth = Texture(Rhythm(Hit('0', '1/16')))
# dotted_quarter = Texture(Rhythm(Hit('0', '3/8')))
# trino = Texture(Rhythm(Hit('0', '1/24')))
#
# t_melody_1 = half - quarter - quarter - dotted_quarter - sixteenth - sixteenth - quarter - quarter
# t_melody_2 = half - quarter - quarter - quarter - trino - trino - trino - sixteenth - sixteenth - quarter - quarter
#
# leading = Harmony(Chord({-1}))
# tonic = Harmony(Chord({0}))
# super_tonic = Harmony(Chord({2}))
# mediant = Harmony(Chord({4}))
# subdominant = Harmony(Chord({5}))
# dominant = Harmony(Chord({7}))
# sub_mediant = Harmony(Chord({9}))
# tonic_1 = Harmony(Chord({12}))
# silence = Harmony(Chord())
#
# h_melody_1 = tonic + mediant + dominant + leading + tonic + super_tonic + tonic + silence
# h_melody_2 = sub_mediant + dominant + tonic_1 + dominant + subdominant + \
#              dominant + subdominant + mediant + subdominant + mediant + silence
#
# o_meoldy_1 = Instrumentation([piano for _ in range(8)])
# o_meoldy_2 = Instrumentation([piano for _ in range(11)])
#
# melody_1 = octave_1 + t_melody_1 * h_melody_1 * o_meoldy_1
# melody_2 = octave_1 + t_melody_2 * h_melody_2 * o_meoldy_2
# melody = concatenation(melody_1, melody_2)

piece = parallelization(piano_part)

# Write MIDI
midi = piece.to_midi(bpm=120)
midi.write('../midi/swan.mid')

# Plot
plot_notes(piece,
           figsize=(12, 6),
           x_tick_start=0,
           x_tick_step=1.5,)
plt.show()
