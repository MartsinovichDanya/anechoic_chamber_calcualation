import cmath
import numpy as np
import random


"""
n_layers    - число слоев в диэлектрике
eps         - диэлектрическая проницаемость (1-10)
tan_delta   - тангенс угла диэлектрических потерь (1 - 0,0001) обычно 0.0001-0.001
d           - толщина каждого слоя в миллиметрах (суммарная толщина не больше 2мм)
freq        - частота электромагнитной волны в мегагерцах (3000 - 40000)
phi         - угол падения электромагнитной волны на слой в градусах (0 - 89) для теста взять 0
wave_pol    - поляризация падающей волны (параллельная - 0 или перпендикулярная - 1)
"""


PI = cmath.pi
J = complex(0, 1)
W0 = 120 * PI
C = 299792458  # speed of light m/s


def to_rad(x): return x*(PI/180)


def to_deg(x): return x*(180/PI)


def calc_rounded_abs_phase(x, n_round=3):
    return round(abs(x), n_round), round((cmath.phase(x)*(180/PI)), n_round)


def calc_check_coef(t, g, n_round=3):
    return round((abs(t)**2) + (abs(g)**2), n_round)


def round_complex(x, n):
    return complex(round(x.real, n), round(x.imag, n))


def calc_beta_i(d, eps, freq, tan_delta, phi):
    wave_l = C/(freq*(10**6))
    d = d*(10**(-3))
    beta_i = ((2*PI*d)/wave_l)*cmath.sqrt(eps*(1 - (J*tan_delta)))*cmath.cos(phi*(PI/180))
    # beta_i = ((2*PI*d)/wave_l)*cmath.sqrt(eps*(1 - tan_delta)) * cmath.cos(phi*(PI/180))
    return beta_i


def calc_phi_arr(n, phi_0, eps_arr, tan_delta_arr):
    phi_arr = [phi_0]
    for i in range(n):
        phi_arr.append((cmath.asin((cmath.sin(phi_arr[0]*(PI/180)))/float((cmath.sqrt(eps_arr[i]*(1 - (J*tan_delta_arr[i])))).real))).real*(180/PI))
    return phi_arr


def calc_layer_matrix(d, eps, freq, tan_delta, phi, phi_1, phi_0, wave_pol):
    cos_phi_1 = cmath.cos(phi_1*(PI/180))
    cos_phi_0 = cmath.cos(phi_0*(PI/180))
    cos_phi = cmath.cos(phi*(PI/180))
    beta_i = calc_beta_i(d, eps, freq, tan_delta, phi)
    sh_j_beta_i = cmath.sinh(J*beta_i)
    wi = W0/cmath.sqrt(eps*(1 - (J*tan_delta)))

    m11 = m22 = cmath.cosh(J * beta_i)

    if wave_pol == 0:
        m12 = ((W0*cos_phi_1)/(wi*cos_phi))*sh_j_beta_i
        m21 = ((wi*cos_phi)/(W0*cos_phi_0))*sh_j_beta_i
    elif wave_pol == 1:
        m12 = ((wi*cos_phi)/(W0*cos_phi_1))*sh_j_beta_i
        m21 = ((W0*cos_phi_0)/(wi*cos_phi))*sh_j_beta_i
    else:
        raise ValueError('incorrect value for wave polarization')

    return np.array([[m11, m12], [m21, m22]])


def get_layer_matrix_list(n_layers, eps_arr, tan_delta_arr, d_arr, freq, phi_arr, wave_pol):
    phi_0 = phi_arr[0]
    phi_1 = phi_arr[1]
    matrix_list = []

    for i in range(n_layers):
        eps = eps_arr[i]
        tan_delta = tan_delta_arr[i]
        d = d_arr[i]
        phi = phi_arr[i+1]

        matrix_list.append(calc_layer_matrix(d, eps, freq, tan_delta, phi, phi_1, phi_0, wave_pol))

    return matrix_list


def calc_sigma_matrix(layer_matrix_list):
    sigma_matrix = layer_matrix_list[0]
    if len(layer_matrix_list) > 1:
        for i in range(1, len(layer_matrix_list)):
            sigma_matrix = sigma_matrix.dot(layer_matrix_list[i])
    return sigma_matrix


def calc_coefs_1_layer(eps, tan_delta, d, freq, phi_0, wave_pol):
    phi_arr = calc_phi_arr(1, phi_0, [eps], [tan_delta])
    layer_matrix_list = get_layer_matrix_list(1, [eps], [tan_delta], [d], freq, phi_arr, wave_pol)
    sigma_matrix = calc_sigma_matrix(layer_matrix_list)
    sum_sigma_matrix_el = sigma_matrix[0, 0] + sigma_matrix[0, 1] + sigma_matrix[1, 0] + sigma_matrix[1, 1]
    t_sigma = 2 / sum_sigma_matrix_el
    g_sigma = ((sigma_matrix[0, 0] + sigma_matrix[0, 1]) - (sigma_matrix[1, 0] + sigma_matrix[1, 1])) / sum_sigma_matrix_el

    return phi_arr, layer_matrix_list, sigma_matrix, t_sigma, g_sigma


# phi_0 здесь передается в радианах
def calc_g_1_layer(eps, tan_delta, d, freq, phi_0, wave_pol):
    phi_0 = to_deg(phi_0)
    phi_arr = calc_phi_arr(1, phi_0, [eps], [tan_delta])
    layer_matrix_list = get_layer_matrix_list(1, [eps], [tan_delta], [d], freq, phi_arr, wave_pol)
    sigma_matrix = calc_sigma_matrix(layer_matrix_list)
    sum_sigma_matrix_el = sigma_matrix[0, 0] + sigma_matrix[0, 1] + sigma_matrix[1, 0] + sigma_matrix[1, 1]
    g_sigma = ((sigma_matrix[0, 0] + sigma_matrix[0, 1]) - (sigma_matrix[1, 0] + sigma_matrix[1, 1])) / sum_sigma_matrix_el

    return g_sigma

