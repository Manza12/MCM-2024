from hartex import Texture, Harmony, TensorContraction


def product(t: Texture, h: Harmony) -> TensorContraction:
    return t * h


def parallel(*args: TensorContraction) -> TensorContraction:
    harmonic_texture = TensorContraction()
    for arg in args:
        harmonic_texture = harmonic_texture | arg
    return harmonic_texture


def concatenate(*args: TensorContraction) -> TensorContraction:
    harmonic_texture = TensorContraction()
    for arg in args:
        harmonic_texture = harmonic_texture - arg
    return harmonic_texture
