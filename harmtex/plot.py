from harmtex.model import TensorContraction
import matplotlib.pyplot as plt


def plot_notes(tensor_contraction: TensorContraction,
               linewidth: float = 5,
               eps: float = 0.3,
               ):
    notes = tensor_contraction.notes()

    fig = plt.figure()
    for note in notes:
        plt.hlines(note.frequency, float(note.start), float(note.end), color='black', linewidth=linewidth)

    for note in notes:
        plt.vlines(float(note.start), note.frequency - eps, note.frequency + eps, color='red', linewidth=linewidth)

    return fig
