from manim import *
import numpy as np
import signals as sig
from fourier_utils import compute_fourier_coefs

class Amty(Scene):
    def construct(self):
        # ==== CONFIGURATION =====
        use_svg = True
        svg_path = "amity"
        signal_type = "spiral"  # or "circle"
        turns = 5
        n_terms = 1000
        N = 1000000  # number of samples
        scale = 2
        # ========================
        
        if use_svg:
            signal = sig.svg_to_complex_signal(svg_path, N, scale=2.0)
        elif signal_type == "circle":
            signal = sig.unit_circle(N)
        elif signal_type == "spiral":
            signal = sig.spiral(N, turns)
        else:
            raise ValueError("Unknown signal type.")
        fourier_terms = compute_fourier_coefs(signal, n_terms=n_terms)
        frequencies = [int(round(freq)) for freq, _ in fourier_terms]
        coefficients = [coef for _, coef in fourier_terms]
        
        t = ValueTracker(0)
        
        origin = np.array([0, 0, 0])
        prev_tip_func = lambda: origin
        vectors = VGroup()
        circles = VGroup()
        
        for coef, freq in zip(coefficients, frequencies):
            radius = abs(coef)
            current_start_func = prev_tip_func
            
            vector = always_redraw(lambda c = coef, f = freq, start = current_start_func:
                Line(start(), start() + self.to_point(c, f, t.get_value()),color=BLUE)
            )
            
            circle = always_redraw(lambda r = radius, start = current_start_func:
                Circle(radius = r, color = GRAY, stroke_opacity = 0.2).move_to(start())
            )
            
            vectors.add(vector)
            circles.add(circle)
            prev_tip_func = lambda v=vector: v.get_end()
        
        dot = always_redraw(lambda: Dot(prev_tip_func(), color=RED))
        path = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=2)
        text = Tex(rf"$n={n_terms}$").rotate_about_origin(PI)
        self.play(Write(text))
        self.wait(0.5)
        self.play(FadeOut(text))
        self.add(circles, vectors, dot, path)
        self.play(t.animate.set_value(1), run_time=5, rate_func=linear) 
        
    def to_point(self, coef, freq, t):
        z = coef * np.exp(1j * TAU * freq * t)
        return np.array([z.real, z.imag, 0])

