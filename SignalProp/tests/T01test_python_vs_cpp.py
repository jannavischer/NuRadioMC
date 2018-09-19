import matplotlib.pyplot as plt
import numpy as np
import time
from NuRadioMC.SignalProp import analyticraytraycing as ray
from NuRadioMC.utilities import units, medium
import logging
from radiotools import helper as hp
from radiotools import plthelpers as php
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test_raytracing')

ice = medium.southpole_simple()

np.random.seed(0)  # set seed to have reproducible results
n_events = int(1e3)
rmin = 50. * units.m
rmax = 3. * units.km
zmin = 0. * units.m
zmax = -3. * units.km
rr = np.random.triangular(rmin, rmax, rmax, n_events)
phiphi = np.random.uniform(0, 2 * np.pi, n_events)
xx = rr * np.cos(phiphi)
yy = rr * np.sin(phiphi)
zz = np.random.uniform(zmin, zmax, n_events)

points = np.array([xx, yy, zz]).T
x_receiver = np.array([0., 0., -5.])

results_C0s_cpp = np.zeros((n_events, 2))
t_start = time.time()
for iX, x in enumerate(points):
    r = ray.ray_tracing(x, x_receiver, ice)
    r.find_solutions()
    if(r.has_solution()):
        for iS in range(r.get_number_of_solutions()):
            results_C0s_cpp[iX, iS] = r.get_results()[iS]['C0']
t_cpp = time.time() - t_start
print("CPP time = {:.1f} seconds = {:.2f}ms/event".format(t_cpp, 1000. * t_cpp / n_events))


results_C0s_python = np.zeros((n_events, 2))
ray.cpp_available = False
t_start = time.time()
for iX, x in enumerate(points):
    r = ray.ray_tracing(x, x_receiver, ice)
    r.find_solutions()
    if(r.has_solution()):
        for iS in range(r.get_number_of_solutions()):
            results_C0s_python[iX, iS] = r.get_results()[iS]['C0']
t_python = time.time() - t_start
print("Python time = {:.1f} seconds = {:.2f}ms/event".format(t_python, 1000. * t_python / n_events))