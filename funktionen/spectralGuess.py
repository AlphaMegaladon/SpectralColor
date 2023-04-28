from funktionen import spectralTrafo
from scipy.optimize import minimize
import numpy as np

def srgb2spec(srgb, ill = 'd65', obs = '2'):
    initalSpectrum = [0.5 for _ in range(50)]

    def loss4srgb2spec(specGuess, ill = ill, obs = obs):
        specGuess = specGuess.clip(0,1)
        xyzGuess = spectralTrafo.spec2xyz(specGuess, ill=ill, obs=obs)
        rgbGuess = spectralTrafo.xyz2rgb(xyzGuess)
        srgbGuess = np.clip(spectralTrafo.gamma_correction(rgbGuess)*255, 0, 255)
        #print(srgb, srgbGuess, (srgb-srgbGuess), (srgb-srgbGuess)**2, np.sum((srgb-srgbGuess)**2))
        return np.sum((srgb-srgbGuess)**2)

    res = minimize(loss4srgb2spec, x0=initalSpectrum, method='L-BFGS-B')
    # Nelder-Mead: Relativ gezacktes Spectrum
    # Powell: Spectrum schöner und Werte besser als bei Nelder-Mead, aber langsamer
    # CG: Sehr schönes Spektrum, aber reproduzierte rgb werte nicht unbedingt korrekt
    # BFGS: Normale Farben sehr gut, bei "Randfarben" keine gute reproduktion
    # Newton-CG: Jacobial is required ...
    # L-BFGS-B: Der funktioniert ziemlich nice ;-)
    return res.x
    