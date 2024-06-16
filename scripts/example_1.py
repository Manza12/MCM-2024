from harmtex.functions import concatenation
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch
from harmtex.plot import plot_notes, plt

t_alberti = Texture(
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

h_I = Harmony.from_chord(Chord.from_roman_numeral('I'))
h_V_2 = Harmony.from_chord(Chord.from_roman_numeral('V7', 2))
h_IV_2 = Harmony.from_chord(Chord.from_roman_numeral('IV', 2))
h_V_1 = Harmony.from_chord(Chord.from_roman_numeral('V', 1, -1))

harmony_theme_A = [h_I, h_I, h_V_2, h_I, h_IV_2, h_I, h_V_1, h_I]
texture_theme_A = [t_alberti for _ in harmony_theme_A]
harmonic_textures = [h * t for h, t in zip(harmony_theme_A, texture_theme_A)]
accompaniment_theme_A = concatenation(*harmonic_textures)

C4 = Pitch(60)
accompaniment_theme_A_in_C4 = C4 + accompaniment_theme_A

# Print
print('Notes:')
fragment = accompaniment_theme_A_in_C4.ordered_notes()
for note in fragment:
    print(note)

print('\nTexture:')
print(accompaniment_theme_A_in_C4.texture)

print('\nHarmony:')
print(accompaniment_theme_A_in_C4.harmony)

# Write MIDI
midi = accompaniment_theme_A_in_C4.to_midi(bpm=120)
midi.write('../midi/example_1.mid')

# Plot
plot_notes(accompaniment_theme_A_in_C4,
           x_tick_start=0,
           x_tick_step=0.5)
plt.show()
