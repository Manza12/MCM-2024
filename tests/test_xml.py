from pathlib import Path
from hartex.compiler import ScoreTree

score_tree = ScoreTree(Path('../xml/test.xml'))
midi = score_tree.to_midi(velocity=50)
midi.write('data/test_xml.mid')
