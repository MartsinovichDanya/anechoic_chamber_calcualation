from calc_rays import *
from calc_amps import *
from params import *
import numpy as np
import json


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
mz_z_lims = (-MZW/2, MZW/2)

mesure_points = []

for y in np.arange(mz_y_lims[0], mz_y_lims[1], LAMBDA/2):
    for z in np.arange(mz_z_lims[0], mz_z_lims[1], LAMBDA/2):
        mesure_points.append(MesurePoint(CHL, round(float(y), 3), round(float(z), 3)))

counter = 0
anec_coef_arr = []
for mp in mesure_points:
    try:
        dir_ray = calc_dir_ray(mp.pos)
        mp.rays_data["dir"] = dir_ray
        ray1 = calc_ray_1(mp.pos)
        mp.rays_data["ray1"] = ray1
        ray2 = calc_ray_2(mp.pos)
        mp.rays_data["ray2"] = ray2
        ray3 = calc_ray_3(mp.pos)
        mp.rays_data["ray3"] = ray3
        ray4 = calc_ray_4(mp.pos)
        mp.rays_data["ray4"] = ray4

        e_amp_dir = calc_e_amp_dir(dir_ray["ray_phi_proj_xz"], dir_ray["ray_phi_proj_xy"], dir_ray["ray_len"])
        e_amp_refl_arr = [
            calc_e_amp_refl(ray1["ray_phi_proj_xz"], ray1["ray_phi_proj_xy"], ray1["ray_len"], ray1["ray_phi"]),
            calc_e_amp_refl(ray2["ray_phi_proj_xz"], ray2["ray_phi_proj_xy"], ray2["ray_len"], ray2["ray_phi"]),
            calc_e_amp_refl(ray3["ray_phi_proj_xz"], ray3["ray_phi_proj_xy"], ray3["ray_len"], ray3["ray_phi"]),
            calc_e_amp_refl(ray4["ray_phi_proj_xz"], ray4["ray_phi_proj_xy"], ray4["ray_len"], ray4["ray_phi"])
        ]

        anec_coef = calc_anec_coef(e_amp_dir, e_amp_refl_arr)
        anec_coef_arr.append(anec_coef)
        mp.dir_ray_amp = e_amp_dir
        mp.refl_rays_amp = calc_sigma_e_amp_refl(e_amp_refl_arr)
        mp.anechoic_coef = anec_coef
        counter+=1

    except Exception as e:
        pass
        # raise e
        print("error point", mp.pos, e)

# print()
# print(counter)
# print(min(anec_coef_arr))

for mp in mesure_points:
    if mp.pos in [(5.0, -0.4, -0.4), (5.0, -0.4, 0.4), (5.0, 0.4, -0.4), (5.0, 0.4, 0.4)]:
        print("pos:", mp.pos)
        print("anechoic_coef:", mp.anechoic_coef)
        print("dir_ray_amp:", mp.dir_ray_amp)
        print("refl_rays_amp:", mp.refl_rays_amp)
        json_str = json.dumps(mp.rays_data, indent=4)
        print(json_str)
        print("==========================================")

