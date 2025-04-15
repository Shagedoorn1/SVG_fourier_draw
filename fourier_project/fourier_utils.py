import numpy as np

def compute_fourier_coefs(signal, n_terms=None):
    N = len(signal)
    freqs = np.fft.fftfreq(N, d= 1.0 / N)
    coefs = np.fft.fft(signal) / N
    
    if n_terms:
        indices = np.argsort(-np.abs(coefs))[:n_terms]
    else:
        indices = np.arange(n_terms)
    
    pairs = list(zip(freqs[indices], coefs[indices]))
    return sorted(pairs, key=lambda p: p[0])