import unittest
from hartex import frac, Pitch, Hit, Chord, Rhythm, Harmony, Texture, HarmonicTexture


class TestObjects(unittest.TestCase):
    def test_pitch(self):
        Pitch(60)

    def test_hit(self):
        Hit(frac('1/4'), frac('1/4'))
        Hit(frac(1, 4), frac(1, 4))
        Hit((frac(1, 4), frac(1, 4)))

    def test_chord(self):
        Chord({Pitch(60), Pitch(64), Pitch(67)})
        Chord(Pitch(60), Pitch(64), Pitch(67))
        Chord({60, 64, 67})
        Chord(60, 64, 67)

    def test_rhythm(self):
        Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))})
        Rhythm(Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4)))
        Rhythm({(frac(1, 4), frac(1, 4)), (frac(1, 2), frac(1, 4))})
        Rhythm((frac(1, 4), frac(1, 4)), (frac(1, 2), frac(1, 4)))


if __name__ == '__main__':
    test_objects = TestObjects()
    test_objects.test_pitch()
    test_objects.test_hit()
    test_objects.test_chord()
    test_objects.test_rhythm()
