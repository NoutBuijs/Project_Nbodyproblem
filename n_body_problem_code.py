import n_body_problem_classes as nb
import numpy as np
import pandas as pd

au  = 1.495978707*10**11

np.set_printoptions(precision=2)
pd.set_option('display.max_columns', None)

sun = nb.body(pos = np.array([1,0,0]),
                mu = 	1.32712440018*10**20,
                name = "Sun",
                id = 0,
                color = "y")

earth = nb.body(pos = np.array([0,0,0]),
                v = np.array([0,29.78*10**3,0]),
                mu = 3.986004418 * 10**14,
                name = "Earth",
                id = 1,
                color = "blue")

moon = nb.body(pos = np.array([0.002569,0,0]),
                v = np.array([0,1.022*10**3+29.78*10**3,0]),
                mu = 4.9048695 * 10**12,
                name = "Moon",
                id = 2,
                color = "gray")
planetA = nb.body(pos = np.array([0.002,0,0]),
                v = np.array([0,19*10**3,0]),
                mu = 3.986004418 * 10**14*10,
                name = "PlanetA",
                id = 1,
                color = "blue")

planetB = nb.body(pos = np.array([0,1.5,0]),
                v = np.array([0,0,80*10**2]),
                mu = 3.986004418 * 10**14*10000,
                name = "PlanetB",
                id = 1,
                color = "green")

planetC = nb.body(pos = np.array([2,0,0]),
                v = np.array([0,-10*10**3,10*10**3]),
                mu = 3.986004418 * 10**14 * 1000,
                name = "PlanetC",
                id = 1,
                color = "red")

bodies = np.array([moon, earth, sun, planetC, planetB, planetA])

sim = nb.physics(bodies = bodies)
sim.simulate(t_end=3600*24*70*4,dt = 1000)
space = nb.enviroment(contents = bodies)
states = sim.data

space.setup()
space.plotpos(states)
space.show()

