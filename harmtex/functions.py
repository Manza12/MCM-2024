from .model import Texture, Harmony, Instrumentation, TensorContraction, Section, Instrument


def contraction(h: Harmony, t: Texture, o: Instrumentation = None) -> TensorContraction:
    if o is None:
        piano_section = Section(Instrument('Acoustic Grand Piano'))
        o = Instrumentation([piano_section for _ in range(len(h))])
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
