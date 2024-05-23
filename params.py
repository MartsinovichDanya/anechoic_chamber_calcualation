import cmath


PI = cmath.pi
C = 299792458

LAMBDA = 0.1  # wavelength in m (10 cm)
K = (2*PI)/LAMBDA
FREQ = C/LAMBDA

CHL = 50 * LAMBDA  # chamber length in m (not chamber length, but the distance between antenna and measurement zone)
CHW = 20 * LAMBDA  # chamber width in m
CHH = 20 * LAMBDA  # chamber height in m

MZW = 10 * LAMBDA  # measurement zone width in m
MZH = 10 * LAMBDA  # measurement zone height in m

ANT_A = 5 * LAMBDA
ANT_B = 5 * LAMBDA

D = 2 * LAMBDA
POL = 1
TAN_DELTA = 0.0
EPS = 1.7

ANT_POINT = (0, 0, 0)
MZ_CENTER = (CHL, 0, 0)
