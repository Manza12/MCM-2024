from .model import Texture, Harmony, Instrumentation, TensorContraction, Section, Instrument


def contraction(h: Harmony, t: Texture, o: Instrumentation = None) -> TensorContraction:
    return TensorContraction(h, t, o)


def parallelization(*args: TensorContraction) -> TensorContraction:
    harmonic_texture = TensorContraction()
    for arg in args:
        harmonic_texture = harmonic_texture | arg
    return harmonic_texture


def concatenation(*args: TensorContraction) -> TensorContraction:
    harmonic_texture = TensorContraction()
    for arg in args:
        harmonic_texture = harmonic_texture - arg
    return harmonic_texture
