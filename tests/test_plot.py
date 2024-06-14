from harmtex.plot import plot_notes, plt
from harmtex.model import Harmony, Chord, Texture, Rhythm, Hit, Instrumentation, Section, Instrument, TensorContraction

h = Harmony(Chord({60}), Chord({64, 67}))
t = Texture(Rhythm(Hit('0/8', '1/8')),
            Rhythm(Hit('1/8', '1/8'), Hit('2/8', '1/8')))
i = Instrumentation(Section(Instrument('Tuba')), Section(Instrument('Horn'), Instrument('Trumpet')))

tensor_contraction = TensorContraction(h, t, i)
plot_notes(tensor_contraction)

plt.show()
