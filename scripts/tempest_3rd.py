from harmtex.functions import concatenation, parallelization
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, TensorContraction
from harmtex.plot import plot_notes, plt


# Tonic
D4 = Pitch(62)

# Octaves
octave_0 = D4
octave_minus_1 = D4 - 12
octave_1 = D4 + 12

# Textures
t_anacrusis = Texture(
    Rhythm(Hit('-3/16', '1/16')),
    Rhythm(Hit('-2/16', '1/16')),
    Rhythm(Hit('-1/16', '1/16')),
)

t_motif_1 = Texture(
    Rhythm(Hit('-3/16', '1/16')),
    Rhythm(Hit('-2/16', '1/16')),
    Rhythm(Hit('-1/16', '1/16')),
    Rhythm(Hit('0/16', '2/16')),
    Rhythm(Hit('2/16', '1/16')),
)

t_arpeggio_1 = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('1/16', '1/16')),
    Rhythm(Hit('2/16', '1/16')),
    Rhythm(Hit('3/16', '1/16')),
    Rhythm(Hit('4/16', '2/16')),
)

t_bass_1 = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('1/16', '5/16')),
)

t_motif_2 = Texture(
    Rhythm(Hit('3/16', '1/16')),
    Rhythm(Hit('4/16', '1/16')),
    Rhythm(Hit('0/16', '2/16'), Hit('5/16', '1/16')),
)

t_arpeggio_2 = Texture(
    Rhythm(Hit('0/16', '1/16')),
    Rhythm(Hit('1/16', '5/16')),
    Rhythm(Hit('2/16', '4/16')),
)

t_bass_2 = Texture(
    Rhythm(Hit('0/16', '6/16')),
)

# Phrase A.1
h_motif_1 = Harmony.from_chord(Chord({-5, 0, 2, 3})).extend(1)
h_motif_2 = Harmony.from_chord(Chord({-5, 2, 3, 5})).extend(1)

motif_1_1 = octave_1 + t_motif_1 * h_motif_1.permute([0, 3, 2, 1, 4])
arpeggio_1_1 = octave_0 + t_arpeggio_1 * Harmony.from_chord(Chord({-12, -5, 0, 3})).extend(1)
bass_1_1 = octave_minus_1 + t_bass_1 * Harmony.from_chord(Chord({0, 7}))

motif_1_2_a = octave_1 + t_motif_1 * h_motif_1.permute([0, 3, 1, 2, 4])
motif_1_2_b = octave_1 + t_motif_1 * h_motif_2.permute([0, 3, 2, 1, 4])
motif_1_2_c = octave_1 + t_motif_1 * h_motif_2.permute([0, 3, 1, 2, 4])
arpeggio_1_2 = octave_minus_1 + t_arpeggio_1 * Harmony.from_chord(Chord({-5, 7, 11, 14})).extend(1)
bass_1_2 = octave_minus_1 + t_bass_1 * Harmony.from_chord(Chord({-5, 7}))

block_A_1_1 = parallelization(motif_1_1, arpeggio_1_1, bass_1_1)
block_A_1_2 = block_A_1_1
block_A_1_3 = block_A_1_1
block_A_1_4 = parallelization(motif_1_2_a, arpeggio_1_2, bass_1_2)
block_A_1_5 = parallelization(motif_1_2_b, arpeggio_1_2, bass_1_2)
block_A_1_6 = block_A_1_5
block_A_1_7 = block_A_1_5
block_A_1_8 = parallelization(motif_1_2_c, arpeggio_1_1, bass_1_1)

# Phrase A.2
motif_2_1_pre = octave_1 + t_anacrusis * Harmony.from_chord(Chord({0, 7, 12}))

t_block_2 = t_bass_2 + t_arpeggio_2 + t_motif_2
h_block_2_1 = Harmony.from_roman_numeral('iv', [
    '1',
    '-', '5', '1',
    '3', '5', '3',
])
h_block_2_2 = Harmony.from_roman_numeral('N', [
    '1',
    '-', '5', '1',
    '3', '5', '3',
])
h_block_2_3 = Harmony.from_roman_numeral('V', [
    '3',
    '-', '1', '3',
    '5', '1', '5',
], -1)
h_block_2_4 = Harmony.from_roman_numeral('i', [
    '1',
    '-', '5', '1',
    '3', '5', '3',
])
h_block_2_5 = Harmony.from_roman_numeral('i', [
    '5',
    '-', '3', '5',
    '1', '5', '1',
], -1)
h_block_2_6 = Harmony.from_roman_numeral('V7', [
    '1',
    '-', '5', '7',
    '3', '1', '3',
], -1)

block_A_2_1 = t_block_2 * (octave_minus_1 + h_block_2_1)
block_A_2_2 = t_block_2 * (octave_minus_1 + h_block_2_2)
block_A_2_3 = t_block_2 * (octave_minus_1 + h_block_2_3)
block_A_2_4 = t_block_2 * (octave_minus_1 + h_block_2_4)
block_A_2_5 = t_block_2 * (octave_minus_1 + h_block_2_5)
block_A_6_6 = t_block_2 * (octave_minus_1 + h_block_2_6)

# Structure
phrase_A_1 = concatenation(block_A_1_1, block_A_1_2, block_A_1_3, block_A_1_4,
                           block_A_1_5, block_A_1_6, block_A_1_7, block_A_1_8)
phrase_A_2_a = concatenation(motif_2_1_pre,
                             block_A_2_1, block_A_2_2, block_A_2_3,
                             block_A_2_4, block_A_2_5, block_A_6_6)
phrase_A_2_b = TensorContraction()
phrase_A_2_c = TensorContraction()
phrase_A_2 = concatenation(phrase_A_2_a, phrase_A_2_b, phrase_A_2_c)
theme_A = concatenation(phrase_A_1, phrase_A_2)
fragment = theme_A

# Write MIDI
midi = fragment.to_midi(bpm=110)
midi.write('../midi/tempest_3rd.mid')

# Plot
plot_notes(fragment,
           x_tick_start=0,
           x_tick_step=3/8)
plt.show()
