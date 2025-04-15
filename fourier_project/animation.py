from manim import *
import numpy as np

class ComplexFourierSeries(Scene):
    def construct(self):
        # Example complex Fourier coefficients and frequencies
        N = 500
        ts = np.linspace(0, 1, N, endpoint=False)
        signal = np.exp(2j * np.pi * ts) + 2*np.exp(1j * np.pi * ts)
        
        fourier_terms = self.compute_fourier_coefs(signal, n_terms=10)
        
        frequencies = [int(round(freq)) for freq, coef in fourier_terms]
        coefficients = [coef for freq, coef in fourier_terms]

        t = ValueTracker(0)

        origin = np.array([0, 0, 0])
        prev_tip_func = lambda: origin
        vectors = VGroup()
        circles = VGroup()

        # Store the final tip for the traced path

        for coef, freq in zip(coefficients, frequencies):
            # Define the vector as a line from previous tip to new tip
            radius = abs(coef)
            
            vector = always_redraw(lambda c=coef, f=freq, start=prev_tip_func:
                Line(
                    start(),
                    start() + self.get_vector_endpoint(c, f, t.get_value()),
                    color=BLUE
                )
            )
            current_start_func = prev_tip_func
            circle = always_redraw(lambda r=radius, start=current_start_func:
                Circle(radius=r, color=GRAY, stroke_opacity=0.4).move_to(start())
            )
            vectors.add(vector)
            circles.add(circle)
            prev_tip_func = lambda v=vector: v.get_end()

        # The final tip for tracing
        dot = always_redraw(lambda: Dot(prev_tip_func(), color=RED))
        path = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=2)

        self.add(circles, vectors, dot, path)
        self.play(t.animate.set_value(1), run_time=10, rate_func=linear)
        self.wait()
    
    def compute_fourier_coefs(self, signal, n_terms=None):
        N = len(signal)
        
        freqs = np.fft.fftfreq(N, d=1.0 / N)
        coefs = np.fft.fft(signal) / N
        
        indices = np.argsort(np.abs(freqs))
        if n_terms:
            indices = np.argsort(-np.abs(coefs))[:n_terms]
            
        pairs = list(zip(freqs[indices], coefs[indices]))
        
        return sorted(pairs, key=lambda p: p[0])

    def get_vector_endpoint(self, coef, freq, t):
        return np.array([
            (coef * np.exp(1j * TAU * freq * t)).real,
            (coef * np.exp(1j * TAU * freq * t)).imag,
            0
        ])
