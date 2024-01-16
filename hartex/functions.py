from hartex import Texture, Harmony, Instrumentation, TensorContraction


def contraction(h: Harmony, t: Texture, o: Instrumentation) -> TensorContraction:
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
