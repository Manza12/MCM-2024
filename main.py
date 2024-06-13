from pathlib import Path
from hartex.compiler import ScoreTree

score_tree = ScoreTree(Path('xml/symphony-mozart.xml'))
midi = score_tree.to_midi()
midi.write('midi/symphony-mozart.mid')
