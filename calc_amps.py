from calc_funcs import *
from params import *
import numpy as np
import cmath


"""
LAMBDA = 0.1  # wavelength in m (10 cm)

CHL = 50 * LAMBDA  # chamber length in m (not chamber length, but the distance between antenna and measurement zone)
CHW = 20 * LAMBDA  # chamber width in m
CHH = 20 * LAMBDA  # chamber height in m

ANT_POINT = (0, 0, 0)
"""


def norm(a):
    if a <= 0:
        a = -a
    return a


# calc_start_amp(ray_phi_proj_xz, ray_phi_proj_xy)
def calc_start_amp(phi, theta):
    f_xz = ((1 + cmath.cos(phi))/2) * (cmath.cos(((PI*ANT_A)/LAMBDA) * cmath.sin(phi))/(1 - (((2*PI*ANT_A*cmath.sin(phi))/(PI*LAMBDA))**2)))
    f_yz = ((1 + cmath.cos(theta))/2) * (cmath.sin(((PI*ANT_B)/LAMBDA)*cmath.sin(theta))/(((PI*ANT_B)/LAMBDA)*cmath.sin(theta)))
    e0 = f_xz * f_yz
    return e0


def calc_e_amp_dir(phi_xz, theta_xy, r):
    e0 = calc_start_amp(phi_xz, theta_xy)
    e_amp = (e0/r)*cmath.exp(-J*K*r)
    return e_amp


def calc_e_amp_refl(phi_xz, theta_xy, r, phi):
    e0 = calc_start_amp(phi_xz, theta_xy)
    g = calc_g_1_layer(EPS, TAN_DELTA, D, FREQ, phi, POL)
    e_amp = g*(e0/r)*cmath.exp(-J*K*r)
    return e_amp


def calc_sigma_e_amp_refl(e_amp_refl_arr):
    return sum(e_amp_refl_arr)


def calc_e1(e_amp_dir, sigma_e_amp_refl):
    return abs(sigma_e_amp_refl) / abs(e_amp_dir)


def calc_anec_coef(e_amp_dir, e_amp_refl_arr):
    sigma_e_amp_refl = calc_sigma_e_amp_refl(e_amp_refl_arr)
    e1 = calc_e1(e_amp_dir, sigma_e_amp_refl)
    return (20 * cmath.log10(e1)).real
