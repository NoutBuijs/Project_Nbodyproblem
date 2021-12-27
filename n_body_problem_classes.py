import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D

class body:

    def __init__(self, pos=np.array([0,0,0]),
                 v = np.array([0,0,0]),
                 mu = 0,
                 name = "None",
                 id = np.nan,
                 color = "None"):

        self.position = pos * 1.495978707*10**11
        self.pos = pos * 1.495978707*10**11
        self.velocity = v
        self.v = v
        self.mu = mu
        self.name = name
        self.id = id
        self.color = color


class enviroment:

    def __init__(self,
                 framesize = np.array([10,6]),
                 contents = np.nan):

        self.size = framesize
        self.contents = contents
        self.ncontents = int(np.size(contents))
        self.names = np.zeros(self.ncontents,dtype=object)

        for i,content in enumerate(contents):
            self.names[i] = content.name


    def setup(self):
        plt.style.use("dark_background")
        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1,projection='3d')
        ax.set_facecolor("k")
        plt.axis('off')

    def plotpos(self, states):

        for i,content in enumerate(self.contents):

            x = np.array(states.iloc[:,i*3+0])
            y = np.array(states.iloc[:,i*3+1])
            z = np.array(states.iloc[:,i*3+2])
            plt.plot(x, y, z, c = content.color, label=content.name)

    def show(self):
        plt.legend()
        plt.show()


class physics:

    def __init__(self,
                 bodies = np.nan):

        self.bodies = bodies
        self.locations = np.zeros(np.size(bodies), dtype=object)
        self.names = np.zeros(np.size(bodies), dtype=object)
        self.velocities = np.zeros(np.size(bodies), dtype=object)
        self.sysmatrix = np.zeros((np.size(bodies), np.size(bodies)), dtype=object)
        self.nbodies = int(np.size(bodies))

        for i,body in enumerate(self.bodies):
            self.locations[i] = self.bodies[i].pos
            self.names[i] = self.bodies[i].name
            self.velocities[i] = self.bodies[i].v

        self.state = np.concatenate(np.hstack((self.locations, self.velocities)))


    def simulate(self, t_end = 0, dt = 1):

        time = np.arange(0,t_end,dt)
        self.states = np.zeros(np.size(time), dtype=object)

        for ti,t in enumerate(tqdm(time)):

            self.states[ti] = np.copy(self.state)

            for i,bodyi in enumerate(self.bodies):
                for j,bodyj in enumerate(self.bodies):
                    if i != j:

                        self.sysmatrix[i,j] = np.array(bodyj.mu/np.sqrt(np.sum((bodyj.pos-bodyi.pos)**2))**3 \
                                                       *(bodyj.pos-bodyi.pos))

            self.sysmatrixa = np.concatenate(np.sum(self.sysmatrix, axis=1))
            self.sysmatrixa = np.hstack((self.state[self.nbodies*3:], self.sysmatrixa))
            self.state += self.sysmatrixa*dt

            for i,body in enumerate(self.bodies):
                body.pos = self.state[i*3:i*3+3]
                body.v = self.state[(self.nbodies+1)*3:(self.nbodies+1)*3+3]

        self.data = np.reshape(np.concatenate(self.states),
                               (np.size(time),np.size(self.state)))

        self.columns = np.zeros(np.size(self.state), dtype=object)

        for i,body in enumerate(self.bodies):
                self.columns[i*3:i*3+3] = np.array([f"X{body.name}",
                                                    f"Y{body.name}",
                                                    f"Z{body.name}"],dtype=object)
                self.columns[(self.nbodies+i)*3:(self.nbodies+i)*3+3] = np.array([f"Vx{body.name}",
                                                                              f"Vy{body.name}",
                                                                              f"Vz{body.name}"],dtype=object)

        self.data = pd.DataFrame(self.data, columns=self.columns)