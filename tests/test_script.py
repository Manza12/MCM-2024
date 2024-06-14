from harmtex.model import frac, Hit, Harmony, Rhythm, Texture

t_acc = Texture(
    Rhythm({Hit(frac('0'), frac('1/8'))}),
    Rhythm({Hit(frac('1/8'), frac('1/8'))}),
    Rhythm({Hit(frac('1/4'), frac('1/8'))}),
)
t_mel = Texture(
    Rhythm({Hit(frac('-1/8'), frac('1/8'))}),
    Rhythm({Hit(frac('9/8'), frac('1/4'))}),
    Rhythm({Hit(frac('4/8'), frac('1/4')), Hit(frac('6/8'), frac('3/8'))}),
    Rhythm({Hit(frac('0'), frac('1/2')), Hit(frac('5/8'), frac('1/8'))}),
)

h_13 = Harmony({39}, {55, 63}, {58, 63, 67})
h_2 = Harmony({51}, {56, 62}, {59, 62, 65})
h_4 = Harmony({38}, {55, 63}, {58, 63, 67})
h_mel = Harmony({70}, {75}, {77}, {79})

ht = ((t_acc * h_13) - (t_acc * h_2) - (t_acc * h_13) - (t_acc * h_4)) | (t_mel * h_mel)

# Print
print('Notes:')
fragment = ht.notes()
for note in fragment:
    print(note)

print('\nTexture:')
print(ht.texture)

print('\nHarmony:')
print(ht.harmony)

# Write MIDI
midi = ht.to_midi(bpm=36)
midi.write('data/test_script.mid')
