from pathlib import Path
from hartex.compiler import ScoreTree

score_tree = ScoreTree(Path('xml/nocturne-chopin.xml'))
midi = score_tree.to_midi()
midi.write('midi/nocturne-chopin.mid')
