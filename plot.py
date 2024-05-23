from calc_rays import *
from calc_amps import *
from params import *
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


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

mz_y_lims = (-MZH/2, MZH/2)
mz_z_lims = (-MZW/2, MZW/2)

dir_amp_map = []
refl_amp_map = []
coef_map = []

for y in np.arange(mz_y_lims[0], mz_y_lims[1], LAMBDA/2):
    if round(float(y), 3) == 0:
        continue
    y_temp_dir = []
    y_temp_refl = []
    y_temp_coef = []
    for z in np.arange(mz_z_lims[0], mz_z_lims[1], LAMBDA/2):
        if round(float(z), 3) == 0:
            continue

        p = (CHL, round(float(y), 3), round(float(z), 3))

        try:
            dir_ray = calc_dir_ray(p)
            ray1 = calc_ray_1(p)
            ray2 = calc_ray_2(p)
            ray3 = calc_ray_3(p)
            ray4 = calc_ray_4(p)
            dir_amp = calc_e_amp_dir(dir_ray["ray_phi_proj_xz"], dir_ray["ray_phi_proj_xy"], dir_ray["ray_len"])
            # y_temp_dir.append(norm(dir_amp.real))
            y_temp_dir.append(abs(dir_amp))

            e_amp_refl_arr = [
                norm(calc_e_amp_refl(ray1["ray_phi_proj_xz"], ray1["ray_phi_proj_xy"], ray1["ray_len"], ray1["ray_phi"])),
                norm(calc_e_amp_refl(ray2["ray_phi_proj_xz"], ray2["ray_phi_proj_xy"], ray2["ray_len"], ray2["ray_phi"])),
                norm(calc_e_amp_refl(ray3["ray_phi_proj_xz"], ray3["ray_phi_proj_xy"], ray3["ray_len"], ray3["ray_phi"])),
                norm(calc_e_amp_refl(ray4["ray_phi_proj_xz"], ray4["ray_phi_proj_xy"], ray4["ray_len"], ray4["ray_phi"]))
            ]
            sigma_amp_refl = calc_sigma_e_amp_refl(e_amp_refl_arr)
            # y_temp_refl.append(sigma_amp_refl.real)
            y_temp_refl.append(abs(sigma_amp_refl))

            anec_coef = calc_anec_coef(dir_amp, e_amp_refl_arr)
            y_temp_coef.append(anec_coef)
        except Exception:
            pass
            # y_temp_dir.append(0)
            # y_temp_refl.append(0)
            # y_temp_coef.append(0)
    dir_amp_map.append(y_temp_dir)
    refl_amp_map.append(y_temp_refl)
    coef_map.append(y_temp_coef)


# dir_amp_map = np.asarray(dir_amp_map)
# cmap = sns.color_palette("Blues", as_cmap=True)
# ax = sns.heatmap(dir_amp_map, cmap=cmap, linewidth=0.5)

# refl_amp_map = np.asarray(refl_amp_map)
# cmap = sns.color_palette("Blues", as_cmap=True)
# ax = sns.heatmap(refl_amp_map, cmap=cmap,  linewidth=0.5)

coef_map = np.asarray(coef_map)
cmap = sns.color_palette("Blues", as_cmap=True)
ax = sns.heatmap(coef_map, cmap=cmap,  linewidth=0.5)

plt.show()
