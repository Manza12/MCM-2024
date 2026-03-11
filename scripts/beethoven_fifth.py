from pathlib import Path

from harmtex.audio import render_midi_to_audio
from harmtex.functions import concatenation, parallelization
from harmtex.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrumentation, Instrument, Section
from harmtex.plot import plot_notes, plt


# Tonic
C4 = Pitch(60)

# Octaves
octave_4 = C4
octave_3 = C4 - 12
octave_2 = C4 - 12 * 2

# Textures
t_main_head = Texture(
    Rhythm(Hit('1/8', '1/8'), Hit('2/8', '1/8'), Hit('3/8', '1/8'))
)
t_half = Texture(Rhythm(Hit('0', '1/2')))
t_whole = Texture(Rhythm(Hit('0', '1/1')))

t_main_1 = t_main_head - t_half
t_main_2 = t_main_head - t_whole

# Orquestration
s_1_high = Section(Instrument('Clarinet'), Instrument('Violin'))
s_1_medi = Section(Instrument('Viola'))
s_1_bass = Section(Instrument('Cello'), Instrument('Contrabass'))

o_1_high = Instrumentation(s_1_high, s_1_high)
o_1_medi = Instrumentation(s_1_medi, s_1_medi)
o_1_bass = Instrumentation(s_1_bass, s_1_bass)

# Harmony
h_1 = Harmony(Chord({7}), Chord({3}))
h_2 = Harmony(Chord({5}), Chord({2}))

# Phrases
m_1_high = t_main_1 * (octave_4 + h_1) * o_1_high
m_1_medi = t_main_1 * (octave_3 + h_1) * o_1_medi
m_1_bass = t_main_1 * (octave_2 + h_1) * o_1_bass
m_1 = parallelization(m_1_high, m_1_medi, m_1_bass)

m_2_high = t_main_2 * (octave_4 + h_2) * o_1_high
m_2_medi = t_main_2 * (octave_3 + h_2) * o_1_medi
m_2_bass = t_main_2 * (octave_2 + h_2) * o_1_bass
m_2 = parallelization(m_2_high, m_2_medi, m_2_bass)

phrase_1 = concatenation(m_1, m_2)

# Full piece
piece = concatenation(phrase_1)

# Paths
name = 'beethoven_fifth'
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')
sf2_path = Path("../../../SoundFonts/FluidR3_GM2-2.sf2")

# Write MIDI
fragment = phrase_1
midi = fragment.to_midi(bpm=108*2)
midi.write(midi_path)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(fragment,
           figsize=(12, 6),
           x_tick_start=0,
           x_tick_step=1,)
plt.show()
