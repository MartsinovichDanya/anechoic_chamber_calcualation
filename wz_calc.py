from calc_rays import *
from calc_amps import *
from params import *
import numpy as np


"""
LAMBDA = 0.1  # wavelength in m (10 cm)

CHL = 50 * LAMBDA  # chamber length in m (not chamber length, but the distance between antenna and measurement zone)
CHW = 20 * LAMBDA  # chamber width in m
CHH = 20 * LAMBDA  # chamber height in m

MZW = 10 * LAMBDA  # measurement zone width in m
MZH = 10 * LAMBDA  # measurement zone height in m

ANT_POINT = (0, 0, 0)
MZ_CENTER = (CHL, 0, 0)
"""


class MesurePoint:
    def __init__(self, x, y, z):
        self.pos = (x, y, z)
        self.refl_rays_amp = None
        self.dir_ray_amp = None
        self.anechoic_coef = None
        self.rays_data = {
            "ray1": None,
            "ray2": None,
            "ray3": None,
            "ray4": None,
            "dir": None,
        }


mz_y_lims = (-MZH/2, MZH/2)
# mz_y_lims = (0, MZH/2)
mz_z_lims = (-MZW/2, MZW/2)


def get_mz_points():
    mesure_points = []

    for y in np.arange(mz_y_lims[0], mz_y_lims[1], LAMBDA/2):
        for z in np.arange(mz_z_lims[0], mz_z_lims[1], LAMBDA/2):
            if float(y) == 0.0 and float(z) == 0.0:
                mesure_points.append(MesurePoint(CHL, -LAMBDA/4, -LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, LAMBDA/4, LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, -LAMBDA / 4, LAMBDA / 4))
                mesure_points.append(MesurePoint(CHL, LAMBDA / 4, -LAMBDA / 4))
                continue
            if float(y) == 0.0 and float(z) != 0.0:
                mesure_points.append(MesurePoint(CHL, -LAMBDA/4, round(float(z), 3)))
                mesure_points.append(MesurePoint(CHL, LAMBDA/4, round(float(z), 3)))
                continue
            if float(y) != 0.0 and float(z) == 0.0:
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), -LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), LAMBDA/4))
                continue
            if float(y) != 0.0 and float(z) != 0.0:
                if round(float(y), 3) == 0.0 or round(float(z), 3) == 0.0:
                    continue
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), round(float(z), 3)))

    return mesure_points


def get_mz_points_matrix():
    mesure_points = []

    for y in np.arange(mz_y_lims[0], mz_y_lims[1], LAMBDA/2):
        y_mesure_points = []
        for z in np.arange(mz_z_lims[0], mz_z_lims[1], LAMBDA/2):
            if float(y) == 0.0 and float(z) == 0.0:
                mesure_points.append(MesurePoint(CHL, -LAMBDA/4, -LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, LAMBDA/4, LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, -LAMBDA / 4, LAMBDA / 4))
                mesure_points.append(MesurePoint(CHL, LAMBDA / 4, -LAMBDA / 4))
                continue
            if float(y) == 0.0 and float(z) != 0.0:
                mesure_points.append(MesurePoint(CHL, -LAMBDA/4, round(float(z), 3)))
                mesure_points.append(MesurePoint(CHL, LAMBDA/4, round(float(z), 3)))
                continue
            if float(y) != 0.0 and float(z) == 0.0:
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), -LAMBDA/4))
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), LAMBDA/4))
                continue
            if float(y) != 0.0 and float(z) != 0.0:
                if round(float(y), 3) == 0.0 or round(float(z), 3) == 0.0:
                    continue
                mesure_points.append(MesurePoint(CHL, round(float(y), 3), round(float(z), 3)))

    return mesure_points


if __name__ == '__main__':
    mps = get_mz_points()
    for el in mps:
        print(el.pos)
    print(len(mps))

