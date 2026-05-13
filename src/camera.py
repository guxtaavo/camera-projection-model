import numpy as np
def intrisic_matrix():
    f = 20
    w_ccd = 36
    h_ccd = 24
    w_pixels = 1280
    h_pixels = 720
    skew_factor = 0
    sx = w_pixels/w_ccd
    sy = h_pixels/h_ccd
    ox = w_pixels/2
    oy = h_pixels/2

    intrisic_matrix = np.array([[f*sx, f*skew_factor, ox], [0, f*sy, oy], [0, 0, 1]])

    return intrisic_matrix
