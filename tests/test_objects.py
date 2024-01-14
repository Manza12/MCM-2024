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
        r_1 = Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))})
        r_2 = Rhythm(Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4)))
        r_3 = Rhythm({(frac(1, 4), frac(1, 4)), (frac(1, 2), frac(1, 4))})
        r_4 = Rhythm((frac(1, 4), frac(1, 4)), (frac(1, 2), frac(1, 4)))
        assert r_1 == r_2 == r_3 == r_4

    def test_harmony(self):
        h_1 = Harmony([Chord({Pitch(60), Pitch(64), Pitch(67)}), Chord({Pitch(62), Pitch(65), Pitch(69)})])
        h_2 = Harmony(Chord({Pitch(60), Pitch(64), Pitch(67)}), Chord({Pitch(62), Pitch(65), Pitch(69)}))
        h_3 = Harmony([{60, 64, 67}, {62, 65, 69}])
        h_4 = Harmony({60, 64, 67}, {62, 65, 69})
        assert h_1 == h_2 == h_3 == h_4

    def test_texture(self):
        Texture([Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))}),
                 Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))})])
        Texture(Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))}),
                Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))}))

    def test_harmonic_texture(self):
        texture = Texture(Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))}),
                          Rhythm({Hit(frac(1, 4), frac(1, 4)), Hit(frac(1, 2), frac(1, 4))}))
        harmony = Harmony([Chord({Pitch(60), Pitch(64), Pitch(67)}), Chord({Pitch(62), Pitch(65), Pitch(69)})])
        assert HarmonicTexture(texture, harmony) == texture * harmony


if __name__ == '__main__':
    test_objects = TestObjects()
    tests = [method for method in dir(TestObjects) if method.startswith('test_')]

    for test_name in tests:
        test = getattr(test_objects, test_name)
        test()
