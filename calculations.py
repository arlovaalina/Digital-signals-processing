from math import *
from constants import *

def get_signal():
    for i in range(N):
        yield 10 * cos(2 * pi * i / N)

def get_amplitude_cos(signal, harmonic_index = 1):
    _sum = sum(x * cos(2 * pi * i * harmonic_index / N) for i, x in enumerate(signal))
    return (2 / N) * _sum
    
def get_amplitude_sin(signal, harmonic_index = 1):
    _sum = sum(x * sin(2 * pi * i * harmonic_index / N) for i, x in enumerate(signal))
    return (2 / N) * _sum
    
def get_amplitude(amplitude_sin, amplitude_cos):
    return hypot(amplitude_sin, amplitude_cos)
    
def get_phase(amplitude_sin, amplitude_cos):
    return atan2(amplitude_sin, amplitude_cos)
    
def fourier_transform(signal, harmonic_amount = 1):
    def get_amplitude_params():
        for harmonic_index in range(harmonic_amount):
            amplitude_sin = get_amplitude_sin(signal, harmonic_index + 1)
            amplitude_cos = get_amplitude_cos(signal, harmonic_index + 1)
            yield amplitude_sin, amplitude_cos
            
    def get_tuples():
        for a_sin, a_cos in get_amplitude_params():
            amplitude = get_amplitude(a_sin, a_cos)
            phase = get_phase(a_sin, a_cos)
            yield amplitude, phase if abs(amplitude) > THRESHOLD else 0
            
    harmonic_tuples = list(get_tuples())
    amplitudes = [amplitude for amplitude, _ in harmonic_tuples]
    phases = [phase for (_, phase) in harmonic_tuples]
    return amplitudes, phases   
    
def get_restored_signal(amplitude, phase):
    for i in range(N):
        yield amplitude * cos(2 * pi * i / N - phase)
        
def get_restored_poly_signal(amplitudes, phases, harmonic_amount):
    def signal(amplitude, phase, i, harmonic_index):
        return amplitude * cos(2 * pi * i * harmonic_index / N - phase)
        
    for i in range(N):
        yield sum(signal(amplitudes[index], phases[index], i, index + 1) for index in range(harmonic_amount))
        
def get_restored_poly_signal_2(amplitudes, harmonic_amount):
    def signal(amplitude, i, harmonic_index):
        return amplitude * cos(2 * pi * i * harmonic_index / N)
        
    for i in range(N):
        yield sum(signal(amplitudes[index], i, index + 1) for index in range(harmonic_amount))

def get_polyharmonic_signal(test_spectrum):
    def signal(i, harmonic_index, spectrum):
        amplitude, phase = spectrum
        return amplitude * cos(2 * pi * i * harmonic_index / N - phase)

    for i in range(N):
        yield sum(signal(i, harmonic_index + 1, spectrum) for harmonic_index, spectrum in enumerate(test_spectrum))
            

def filter_signal(amplitudes, phases, filter_predicate):
    spectrum = [(amplitudes[i], phases[i]) for i in range(len(amplitudes))]

    def filter_helper(item):
        print(item)
        index, value = item
        return value if filter_predicate(index) else (0, 0)

    result = list(map(filter_helper, enumerate(spectrum)))
    print(result)
    a = [amplitude for amplitude, _ in result]
    p = [phase for (_, phase) in result]
    return (a, p)