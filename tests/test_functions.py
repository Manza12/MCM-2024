from harmtex import frac, Hit, Harmony, Rhythm, Texture, contraction, parallelization, concatenation, plot_notes


t_acc = Texture(
    Rhythm(Hit(frac('0'), frac('1/8'))),
    Rhythm(Hit(frac('1/8'), frac('1/8'))),
    Rhythm(Hit(frac('1/4'), frac('1/8'))),
)
t_mel = Texture(
    Rhythm(Hit(frac('-1/8'), frac('1/8'))),
    Rhythm(Hit(frac('9/8'), frac('2/8'))),
    Rhythm(Hit(frac('4/8'), frac('1/8')), Hit(frac('6/8'), frac('3/8'))),
    Rhythm(Hit(frac('0/8'), frac('4/8')), Hit(frac('5/8'), frac('1/8'))),
)

h_13 = Harmony({39}, {55, 63}, {58, 63, 67})
h_2 = Harmony({51}, {56, 62}, {59, 62, 65})
h_4 = Harmony({38}, {55, 63}, {58, 63, 67})
h_mel = Harmony({70}, {75}, {77}, {79})

melody = contraction(h_mel, t_mel)

harmony_1 = contraction(h_13, t_acc)
harmony_2 = contraction(h_2, t_acc)
harmony_3 = contraction(h_13, t_acc)
harmony_4 = contraction(h_4, t_acc)
harmony = concatenation(harmony_1, harmony_2, harmony_3, harmony_4)

fragment = parallelization(harmony, melody)

# Print notes
for note in fragment.ordered_notes():
    print(note)

# Write to MIDI
midi = fragment.to_midi(bpm=36)
midi.write('data/test_functions.mid')

# Plot
x_ticks = {
    'x_tick_start': frac('-1/8'),
    'x_tick_end': frac('12/8'),
    'x_tick_step': frac('1/8')
}
plot_notes(melody, show=True, **x_ticks)
plot_notes(harmony, show=True, **x_ticks)

plot_notes(fragment, show=True, **x_ticks)

