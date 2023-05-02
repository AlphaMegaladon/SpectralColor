from funktionen import spectralTrafo
from scipy.optimize import minimize
import numpy as np

def srgb2spec(srgb, ill = 'd65', obs = '2'):
    initalSpectrum = [0.5 for _ in range(50)]
    bounds = [(0,1) for _ in range(50)]

    def loss4srgb2spec(specGuess, ill = ill, obs = obs):
        xyzGuess = spectralTrafo.spec2xyz(specGuess, ill=ill, obs=obs)
        rgbGuess = spectralTrafo.xyz2rgb(xyzGuess)
        srgbGuess = np.clip(spectralTrafo.gamma_correction(rgbGuess)*255, 0, 255)
        #print(srgb, srgbGuess, (srgb-srgbGuess), (srgb-srgbGuess)**2, np.sum((srgb-srgbGuess)**2))
        return np.sum((srgb-srgbGuess)**2)

    res = minimize(loss4srgb2spec, x0=initalSpectrum, method='L-BFGS-B', bounds = bounds,
                   options = {'ftol': 1e-7, 
                              'maxiter': 200})
                              
    # Nelder-Mead: Relativ gezacktes Spectrum
    # Powell: Spectrum schöner und Werte besser als bei Nelder-Mead, aber langsamer
    # CG: Sehr schönes Spektrum, aber reproduzierte rgb werte nicht unbedingt korrekt
    # BFGS: Normale Farben sehr gut, bei "Randfarben" keine gute reproduktion
    # Newton-CG: Jacobial is required ...
    # L-BFGS-B: Der funktioniert ziemlich nice ;-)
    # TNC: Untauglich, viel zu wild und ungenau
    # COBYLA: Nicht wirklich smooth und auch nocht akkurat
    # SLSQP: Erzeugt sehr scharfe Kannten, generiert praktisch nur 1 oder 0 im Reflektionsspektrum
    # trust-constr: Bisschen langsam, erzeut abe schöne Spektren
    # dogleg: Jacobian is required
    # trust-ncg: Jacobian is required
    # trust-exact: Jacobian is required
    # trust-krylov: Jacobian is required
    # Hot candidats: BFGS, trust-constr
    return res.x
    