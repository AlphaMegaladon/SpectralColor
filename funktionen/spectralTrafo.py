import numpy as np

def gamma_correction(rgb):
    srgb = rgb
    for idx, value in enumerate(rgb):
        if value <= 0.0031308:
            srgb[idx] = 12.92*value
        else:
            srgb[idx] = 1.055*(value**(1/2.4)) - 0.055
    return srgb

def xyz2rgb(lab):
    """
    transformation from CIELab to rgb via 3x3 matrix
    """
    M_inv = np.array([[3.2404542, -1.5371385, -0.4985314],
                      [-0.9692660, 1.8760108,  0.0415560], 
                      [0.0556434, -0.2040259, 1.0572252]])
    return np.matmul(M_inv, lab.ravel())

# wahrscheinlich falsch
#def xyz2srgb(lab, ill='d50'):
#    """
#    transformation from CIELab to srgb via 3x3 matrix
#    """
#    if ill == 'd50':
#        M_inv = np.array([[3.1338561, -1.6168667, -0.4906146],
#                      [-0.9787684,  1.9161415,  0.0334540], 
#                      [0.0719453, -0.2289914,  1.4052427]])
#        res = np.matmul(M_inv, lab.ravel())
#        return res
#    elif ill == 'd65':
#        M_inv = np.array([[3.2404542, -1.5371385, -0.4985314],
#                          [-0.9692660, 1.8760108,  0.0415560], 
#                          [0.0556434, -0.2040259, 1.0572252]])
#        return np.matmul(M_inv, lab.ravel())
#    else:
#        raise "ill has to be either 'd50' or 'd65'"

def xyz2Lab(xyz, obs = '2', ill = 'd50'):
    """
    Converts XYZ to Lab.
    """
    labs = xyz.copy()
    
    CIE_E = 216.0 / 24389.0
    ILLUMINANTS = {
        # 2 Degree Functions
        "2": {
            "d50": (0.96422, 1.00000, 0.82521),
            "d65": (0.95047, 1.00000, 1.08883),
        },
        # 10 Degree Functions
        "10": {
            "d50": (0.9672, 1.000, 0.8143),
            "d65": (0.9481, 1.000, 1.073),
        },
    }
    illum = ILLUMINANTS[obs][ill]
    
    labs[:,0] /= illum[0]
    labs[:,1] /= illum[1]
    labs[:,2] /= illum[2]
    
    condition = labs>CIE_E
    labs[condition] = labs[condition]**(1./3.)
    labs[~condition] = 7.787*labs[~condition] + 16./116.

    temp = labs.copy()
    labs[:,0] = 116.*temp[:,1] - 16.
    labs[:,1] = 500.*(temp[:,0] - temp[:,1])
    labs[:,2] = 200.*(temp[:,1] - temp[:,2])

    return labs

def spec2xyz(spec, obs = '2', ill = 'd50'):
    
    if obs == '2':
        std_obs = STDOBSERV('2')
    elif obs == '10':
        std_obs = STDOBSERV('10')
    else:
        raise "Standard Observer has to be '2' or '10' Degree"
    if ill == 'd50':
        ref_ill = REFERENCE_ILLUM('d50')
    elif ill == 'd65':
        ref_ill = REFERENCE_ILLUM('d65')
    else:
        raise "Reference Illumination has to be 'd50' or 'd65'"
        
    coefs = std_obs.copy()
    coefs[:,0] = std_obs[:,0]*ref_ill
    coefs[:,1] = std_obs[:,1]*ref_ill
    coefs[:,2] = std_obs[:,2]*ref_ill
    
    teiler = coefs[:,1].sum()
    
    res = np.matmul(spec, coefs)
    res /= teiler
    
    return res 

def STDOBSERV(degree):
    if degree == '2':
        return np.array([[0.000000e+00, 0.000000e+00, 0.000000e+00],
                       [0.000000e+00, 0.000000e+00, 0.000000e+00],
                       [1.299000e-04, 3.917000e-06, 6.061000e-04],
                       [4.149000e-04, 1.239000e-05, 1.946000e-03],
                       [1.368000e-03, 3.900000e-05, 6.450001e-03],
                       [4.243000e-03, 1.200000e-04, 2.005001e-02],
                       [1.431000e-02, 3.960000e-04, 6.785001e-02],
                       [4.351000e-02, 1.210000e-03, 2.074000e-01],
                       [1.343800e-01, 4.000000e-03, 6.456000e-01],
                       [2.839000e-01, 1.160000e-02, 1.385600e+00],
                       [3.482800e-01, 2.300000e-02, 1.747060e+00],
                       [3.362000e-01, 3.800000e-02, 1.772110e+00],
                       [2.908000e-01, 6.000000e-02, 1.669200e+00],
                       [1.953600e-01, 9.098000e-02, 1.287640e+00],
                       [9.564000e-02, 1.390200e-01, 8.129501e-01],
                       [3.201000e-02, 2.080200e-01, 4.651800e-01],
                       [4.900000e-03, 3.230000e-01, 2.720000e-01],
                       [9.300000e-03, 5.030000e-01, 1.582000e-01],
                       [6.327000e-02, 7.100000e-01, 7.824999e-02],
                       [1.655000e-01, 8.620000e-01, 4.216000e-02],
                       [2.904000e-01, 9.540000e-01, 2.030000e-02],
                       [4.334499e-01, 9.949501e-01, 8.749999e-03],
                       [5.945000e-01, 9.950000e-01, 3.900000e-03],
                       [7.621000e-01, 9.520000e-01, 2.100000e-03],
                       [9.163000e-01, 8.700000e-01, 1.650001e-03],
                       [1.026300e+00, 7.570000e-01, 1.100000e-03],
                       [1.062200e+00, 6.310000e-01, 8.000000e-04],
                       [1.002600e+00, 5.030000e-01, 3.400000e-04],
                       [8.544499e-01, 3.810000e-01, 1.900000e-04],
                       [6.424000e-01, 2.650000e-01, 4.999999e-05],
                       [4.479000e-01, 1.750000e-01, 2.000000e-05],
                       [2.835000e-01, 1.070000e-01, 0.000000e+00],
                       [1.649000e-01, 6.100000e-02, 0.000000e+00],
                       [8.740000e-02, 3.200000e-02, 0.000000e+00],
                       [4.677000e-02, 1.700000e-02, 0.000000e+00],
                       [2.270000e-02, 8.210000e-03, 0.000000e+00],
                       [1.135916e-02, 4.102000e-03, 0.000000e+00],
                       [5.790346e-03, 2.091000e-03, 0.000000e+00],
                       [2.899327e-03, 1.047000e-03, 0.000000e+00],
                       [1.439971e-03, 5.200000e-04, 0.000000e+00],
                       [6.900786e-04, 2.492000e-04, 0.000000e+00],
                       [3.323011e-04, 1.200000e-04, 0.000000e+00],
                       [1.661505e-04, 6.000000e-05, 0.000000e+00],
                       [8.307527e-05, 3.000000e-05, 0.000000e+00],
                       [4.150994e-05, 1.499000e-05, 0.000000e+00],
                       [2.067383e-05, 7.465700e-06, 0.000000e+00],
                       [1.025398e-05, 3.702900e-06, 0.000000e+00],
                       [5.085868e-06, 1.836600e-06, 0.000000e+00],
                       [2.522525e-06, 9.109300e-07, 0.000000e+00],
                       [1.251141e-06, 4.518100e-07, 0.000000e+00]])
    elif degree == '10':
        return np.array([[0.00000e+00, 0.00000e+00, 0.00000e+00],
                       [0.00000e+00, 0.00000e+00, 0.00000e+00],
                       [1.22200e-07, 1.33980e-08, 5.35027e-07],
                       [5.95860e-06, 6.51100e-07, 2.61437e-05],
                       [1.59952e-04, 1.73640e-05, 7.04776e-04],
                       [2.36160e-03, 2.53400e-04, 1.04822e-02],
                       [1.91097e-02, 2.00440e-03, 8.60109e-02],
                       [8.47360e-02, 8.75600e-03, 3.89366e-01],
                       [2.04492e-01, 2.13910e-02, 9.72542e-01],
                       [3.14679e-01, 3.86760e-02, 1.55348e+00],
                       [3.83734e-01, 6.20770e-02, 1.96728e+00],
                       [3.70702e-01, 8.94560e-02, 1.99480e+00],
                       [3.02273e-01, 1.28201e-01, 1.74537e+00],
                       [1.95618e-01, 1.85190e-01, 1.31756e+00],
                       [8.05070e-02, 2.53589e-01, 7.72125e-01],
                       [1.61720e-02, 3.39133e-01, 4.15254e-01],
                       [3.81600e-03, 4.60777e-01, 2.18502e-01],
                       [3.74650e-02, 6.06741e-01, 1.12044e-01],
                       [1.17749e-01, 7.61757e-01, 6.07090e-02],
                       [2.36491e-01, 8.75211e-01, 3.04510e-02],
                       [3.76772e-01, 9.61988e-01, 1.36760e-02],
                       [5.29826e-01, 9.91761e-01, 3.98800e-03],
                       [7.05224e-01, 9.97340e-01, 0.00000e+00],
                       [8.78655e-01, 9.55552e-01, 0.00000e+00],
                       [1.01416e+00, 8.68934e-01, 0.00000e+00],
                       [1.11852e+00, 7.77405e-01, 0.00000e+00],
                       [1.12399e+00, 6.58341e-01, 0.00000e+00],
                       [1.03048e+00, 5.27963e-01, 0.00000e+00],
                       [8.56297e-01, 3.98057e-01, 0.00000e+00],
                       [6.47467e-01, 2.83493e-01, 0.00000e+00],
                       [4.31567e-01, 1.79828e-01, 0.00000e+00],
                       [2.68329e-01, 1.07633e-01, 0.00000e+00],
                       [1.52568e-01, 6.02810e-02, 0.00000e+00],
                       [8.12606e-02, 3.18004e-02, 0.00000e+00],
                       [4.08508e-02, 1.59051e-02, 0.00000e+00],
                       [1.99413e-02, 7.74880e-03, 0.00000e+00],
                       [9.57688e-03, 3.71774e-03, 0.00000e+00],
                       [4.55263e-03, 1.76847e-03, 0.00000e+00],
                       [2.17496e-03, 8.46190e-04, 0.00000e+00],
                       [1.04476e-03, 4.07410e-04, 0.00000e+00],
                       [5.08258e-04, 1.98730e-04, 0.00000e+00],
                       [2.50969e-04, 9.84280e-05, 0.00000e+00],
                       [1.26390e-04, 4.97370e-05, 0.00000e+00],
                       [6.45258e-05, 2.54860e-05, 0.00000e+00],
                       [3.34117e-05, 1.32490e-05, 0.00000e+00],
                       [1.76115e-05, 7.01280e-06, 0.00000e+00],
                       [9.41363e-06, 3.76473e-06, 0.00000e+00],
                       [5.09347e-06, 2.04613e-06, 0.00000e+00],
                       [2.79531e-06, 1.12809e-06, 0.00000e+00],
                       [1.55314e-06, 6.29700e-07, 0.00000e+00]])

def REFERENCE_ILLUM(light):
    if light == 'd50':
        return np.array((17.92, 20.98, 23.91, 25.89, 24.45,
                         29.83, 49.25, 56.45, 59.97, 57.76,
                         74.77, 87.19, 90.56, 91.32, 95.07,
                         91.93, 95.70, 96.59, 97.11, 102.09,
                         100.75, 102.31, 100.00, 97.74, 98.92,
                         93.51, 97.71, 99.29, 99.07, 95.75,
                         98.90, 95.71, 98.24, 103.06, 99.19,
                         87.43, 91.66, 92.94, 76.89, 86.56,
                         92.63, 78.27, 57.72, 82.97, 78.31,
                         79.59, 73.44, 63.95, 70.81, 74.48))
    elif light == 'd65':
        return np.array((39.90, 44.86, 46.59, 51.74, 49.92,
                         54.60, 82.69, 91.42, 93.37, 86.63,
                         104.81, 116.96, 117.76, 114.82, 115.89,
                         108.78, 109.33, 107.78, 104.78, 107.68,
                         104.40, 104.04, 100.00, 96.34, 95.79,
                         88.69, 90.02, 89.61, 87.71, 83.30,
                         83.72, 80.05, 80.24, 82.30, 78.31,
                         69.74, 71.63, 74.37, 61.62, 69.91,
                         75.11, 63.61, 46.43, 66.83, 63.40,
                         64.32, 59.47, 51.97, 57.46, 60.33))
