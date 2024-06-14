from pathlib import Path
from harmtex.compiler import ScoreTree

score_tree = ScoreTree(Path('../xml/test.xml'))
midi = score_tree.to_midi()
midi.write('data/test_xml.mid')
