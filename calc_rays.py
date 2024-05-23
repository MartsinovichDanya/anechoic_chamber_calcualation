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


def calc_ray_len(start, end):
    ray_len = cmath.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2 + (end[2] - start[2])**2)
    return ray_len.real


def calc_dir_ray(mz_point):
    dir_ray_len = calc_ray_len(ANT_POINT, mz_point)
    phi = cmath.asin(1 / cmath.sqrt(mz_point[0] ** 2 + mz_point[1] ** 2 + mz_point[2] ** 2))
    s_dir_xz = cmath.sqrt(CHL ** 2 + mz_point[2] ** 2)
    phi_xz = cmath.acos(CHL / s_dir_xz)
    s_dir_xy = cmath.sqrt(CHL ** 2 + mz_point[1] ** 2)
    phi_xy = cmath.acos(CHL / s_dir_xy)
    return {"ray_len": dir_ray_len,
            "ray_phi": phi.real,
            "ray_phi_proj_xy": phi_xy.real,
            "ray_phi_proj_xz": phi_xz.real}


def calc_ray_1(mz_point):
    s_dir_xz = cmath.sqrt(CHL**2 + mz_point[2]**2)
    phi_xz = cmath.acos(CHL/s_dir_xz)
    tan_phi_xz = cmath.tan(phi_xz)

    yc = CHH - mz_point[1]
    s_top_xy = cmath.sqrt(CHL**2 + yc**2)
    phi_top_xy = cmath.acos(CHL/s_top_xy)

    xp = (2 * CHL)/(CHH * yc)
    yp = CHH / 2
    zp = (xp * tan_phi_xz).real
    p = (xp, yp, zp)

    ray_len_bp = calc_ray_len(ANT_POINT, p)
    ray_len_ap = calc_ray_len(p, mz_point)

    phi = cmath.asin(1/cmath.sqrt(xp**2 + yp**2 + zp**2))

    return {"refl_p": p,
            "ray_len_bp": ray_len_bp,
            "ray_len_ap": ray_len_ap,
            "ray_len": ray_len_bp + ray_len_ap,
            "ray_phi": phi.real,
            "ray_phi_proj_xy": phi_top_xy.real,
            "ray_phi_proj_xz": phi_xz.real}


def calc_ray_2(mz_point):
    s_dir_xz = cmath.sqrt(CHL ** 2 + mz_point[2] ** 2)
    phi_xz = cmath.acos(CHL / s_dir_xz)
    tan_phi_xz = cmath.tan(phi_xz)

    yd = -CHH - mz_point[1]
    s_bottom_xy = cmath.sqrt(CHL ** 2 + yd ** 2)
    phi_bottom_xy = cmath.acos(CHL / s_bottom_xy)

    xp = (2 * CHL) / ((-CHH) * yd)
    yp = -CHH / 2
    zp = (xp * tan_phi_xz).real
    p = (xp, yp, zp)

    ray_len_bp = calc_ray_len(ANT_POINT, p)
    ray_len_ap = calc_ray_len(p, mz_point)

    phi = cmath.asin(1 / cmath.sqrt(xp ** 2 + yp ** 2 + zp ** 2))

    return {"refl_p": p,
            "ray_len_bp": ray_len_bp,
            "ray_len_ap": ray_len_ap,
            "ray_len": ray_len_bp + ray_len_ap,
            "ray_phi": phi.real,
            "ray_phi_proj_xy": phi_bottom_xy.real,
            "ray_phi_proj_xz": phi_xz.real}


def calc_ray_3(mz_point):
    s_dir_xy = cmath.sqrt(CHL ** 2 + mz_point[1] ** 2)
    phi_xy = cmath.acos(CHL / s_dir_xy)
    tan_phi_xy = cmath.tan(phi_xy)

    ze = CHW - mz_point[2]
    s_right_xz = cmath.sqrt(CHL ** 2 + ze ** 2)
    phi_right_xz = cmath.acos(CHL / s_right_xz)

    xp = (2 * CHL) / (CHW * ze)
    yp = (xp * tan_phi_xy).real
    zp = CHW / 2
    p = (xp, yp, zp)

    ray_len_bp = calc_ray_len(ANT_POINT, p)
    ray_len_ap = calc_ray_len(p, mz_point)

    phi = cmath.asin(1 / cmath.sqrt(xp ** 2 + yp ** 2 + zp ** 2))

    return {"refl_p": p,
            "ray_len_bp": ray_len_bp,
            "ray_len_ap": ray_len_ap,
            "ray_len": ray_len_bp + ray_len_ap,
            "ray_phi": phi.real,
            "ray_phi_proj_xy": phi_xy.real,
            "ray_phi_proj_xz": phi_right_xz.real}


def calc_ray_4(mz_point):
    s_dir_xy = cmath.sqrt(CHL ** 2 + mz_point[1] ** 2)
    phi_xy = cmath.acos(CHL / s_dir_xy)
    tan_phi_xy = cmath.tan(phi_xy)

    zf = -CHW - mz_point[2]
    s_left_xz = cmath.sqrt(CHL ** 2 + zf ** 2)
    phi_left_xz = cmath.acos(CHL / s_left_xz)

    xp = (2 * CHL) / ((-CHW) * zf)
    yp = (xp * tan_phi_xy).real
    zp = -CHW / 2
    p = (xp, yp, zp)

    ray_len_bp = calc_ray_len(ANT_POINT, p)
    ray_len_ap = calc_ray_len(p, mz_point)

    phi = cmath.asin(1 / cmath.sqrt(xp ** 2 + yp ** 2 + zp ** 2))

    return {"refl_p": p,
            "ray_len_bp": ray_len_bp,
            "ray_len_ap": ray_len_ap,
            "ray_len": ray_len_bp + ray_len_ap,
            "ray_phi": phi.real,
            "ray_phi_proj_xy": phi_xy.real,
            "ray_phi_proj_xz": phi_left_xz.real}


if __name__ == '__main__':
    print(calc_ray_1((5.0, 0.5, 0.7)))
    print(calc_ray_2((5.0, 0.5, 0.7)))
    print(calc_ray_3((5.0, 0.5, 0.7)))
    print(calc_ray_4((5.0, 0.5, 0.7)))
