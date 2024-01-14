from hartex import Texture, Harmony, HarmonicTexture


def product(t: Texture, h: Harmony) -> HarmonicTexture:
    return t * h


def parallel(*args: HarmonicTexture) -> HarmonicTexture:
    harmonic_texture = HarmonicTexture()
    for arg in args:
        harmonic_texture = harmonic_texture | arg
    return harmonic_texture


def concatenate(*args: HarmonicTexture) -> HarmonicTexture:
    harmonic_texture = HarmonicTexture()
    for arg in args:
        harmonic_texture = harmonic_texture - arg
    return harmonic_texture
