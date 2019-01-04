import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from math import *
from tkinter import *
from tkinter.ttk import *

from helper import *
from constants import *
from calculations import *
from fft import *

TEST_SPECTRUM = list(zip(list(randoms_from(TEST_AMPLITUDES, POLY_COUNT)), list(randoms_from(TEST_PHASES, POLY_COUNT))))

def show_charts(page, signal, restored_signal, restored_signal_2, amplitude, phase):
    figure = Figure(figsize = (10, 7))
    a = figure.add_subplot(311)
    a.plot([i/len(signal) for i in range(len(signal))], signal)
    a.plot([i/len(restored_signal) for i in range(len(restored_signal))], restored_signal)
    a.plot([i/len(restored_signal_2) for i in range(len(restored_signal_2))], restored_signal_2)
    a = figure.add_subplot(312)
    a.stem([i + 1 for i in range(len(amplitude))], amplitude)
    a = figure.add_subplot(313)
    a.stem([i + 1 for i in range(len(phase))], phase)
    canvas = FigureCanvasTkAgg(figure, page)
    canvas.show()
    canvas.get_tk_widget().place(x = 10, y = 10)
    
def show_filter_charts(page, signal, amplitudes, high_spectrum_restored, high_amplitudes, low_spectrum_restored, low_amplitudes):
    figure = Figure(figsize = (10, 7))
    a = figure.add_subplot(231)
    a.plot([i/len(signal) for i in range(len(signal))], signal)
    a = figure.add_subplot(232)
    a.plot([i/len(high_spectrum_restored) for i in range(len(high_spectrum_restored))], high_spectrum_restored)
    a = figure.add_subplot(233)
    a.plot([i/len(low_spectrum_restored) for i in range(len(low_spectrum_restored))], low_spectrum_restored)
    a = figure.add_subplot(234)
    a.stem([i + 1 for i in range(len(amplitudes))], amplitudes)
    a = figure.add_subplot(235)
    a.stem([i + 1 for i in range(len(high_amplitudes))], high_amplitudes)
    a = figure.add_subplot(236)
    a.stem([i + 1 for i in range(len(low_amplitudes))], low_amplitudes)
    canvas = FigureCanvasTkAgg(figure, page)
    canvas.show()
    canvas.get_tk_widget().place(x = 10, y = 10)
    
def first_task(page):
    signal = list(get_signal())
    amplitudes, phases = fourier_transform(signal)
    restored_signal = list(get_restored_signal(amplitudes[0], phases[0]))
    show_charts(page, signal, restored_signal, [], amplitudes, phases)

def second_task(page):
    signal = list(get_polyharmonic_signal(TEST_SPECTRUM))
    amplitudes, phases = fourier_transform(signal, POLY_COUNT)
    restored_signal = list(get_restored_poly_signal(amplitudes, phases, POLY_COUNT))
    # restored_signal_2 = list(get_restored_poly_signal_2(amplitudes, POLY_COUNT))
    show_charts(page, signal, restored_signal, [], amplitudes, phases)
    
def third_task(page):
    signal = list(get_polyharmonic_signal(TEST_SPECTRUM))
    fft_spectrum = get_fft_spectrum(signal, POLY_COUNT)
    amplitudes = [amplitude for amplitude, _ in fft_spectrum]
    phases = [phase for (_, phase) in fft_spectrum]
    restored_signal = list(get_restored_poly_signal(amplitudes, phases, POLY_COUNT))
    show_charts(page, signal, restored_signal, [], amplitudes, phases)
    
def fourth_task(page):
    signal = list(get_polyharmonic_signal(TEST_SPECTRUM))
    amplitudes, phases = fourier_transform(signal, POLY_COUNT)
    
    high_amplitudes, high_phases = filter_signal(amplitudes, phases, lambda x: x < 15)
    high_spectrum_restored = list(get_restored_poly_signal(high_amplitudes, high_phases, POLY_COUNT))
    
    low_amplitudes, low_phases  = filter_signal(amplitudes, phases, lambda x: x > 15)
    low_spectrum_restored = list(get_restored_poly_signal(low_amplitudes, low_phases, POLY_COUNT))
    
    show_filter_charts(page, signal, amplitudes, high_spectrum_restored, high_amplitudes, low_spectrum_restored, low_amplitudes)
    

def initialize_window():
    root = Tk()
    root.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
    
    notebook = Notebook(root)
    page1 = Frame(notebook, width = 850, height = 630)
    page2 = Frame(notebook, width = 850, height = 630)
    page3 = Frame(notebook, width = 850, height = 630)
    page4 = Frame(notebook, width = 850, height = 630)
    notebook.add(page1, text = "Задание 2")
    notebook.add(page2, text = "Задание 3")
    notebook.add(page3, text = "Задание 4")
    notebook.add(page4, text = "Задание 5")
    notebook.pack()

    first_task(page1)
    second_task(page2)
    third_task(page3)
    fourth_task(page4)

    root.mainloop()

if __name__ == "__main__":
    initialize_window()
