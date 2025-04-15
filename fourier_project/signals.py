import numpy as np
from svgpathtools import svg2paths

def unit_circle(N=1000):
    ts = np.linspace(0, 1, N, endpoint=False)
    return np.exp(2j * np.pi * ts)

def spiral(N=1000, turns=3):
    ts = np.linspace(0, 1, N, endpoint=False)
    return ts * np.exp(2j * 2 * np.pi * turns * ts)

def svg_to_complex_signal(name, N=1000, scale=1.0):
    paths, _ = svg2paths(f"assets\{name}.SVG")
    points = []
    
    for path in paths:
        for segment in path:
            num_samples = max(int(N * (segment.length() / path.length())), 1)
            for t in np.linspace(0, 1, num_samples, endpoint=False):
                point = segment.point(t)
                points.append(complex(point.real, point.imag))
    
    signal = np.array(points)
    signal -= np.mean(signal)
    signal /= np.abs(signal).max()
    signal *= scale
    indices = np.linspace(0, len(signal) - 1, N, dtype=int)
    return signal[indices]