import numpy as np


class Body:
    def __init__(self, id_No, pos, vel, spin, **kwarg):
        self.id_No = id_No                          # integer
        self.pos = pos                              # [float, float], np.array
        self.vel = vel                              # [float, float], np.array
        self.spin = spin                            # float, np.array
        self.tail = [self.pos]                      # [[pos0],[pos1],...]
        self.survive = True

        if 'color' not in kwarg:
            self.color = np.array([
                np.random.randint(0,255)/255,
                np.random.randint(0,255)/255,
                np.random.randint(0,255)/255
                ])                                  # [0-1, 0-1, 0-1], np.array
        else:
            self.color = kwarg['color']

        # tail length
        if not 'tail_length' in kwarg:
            self.tail_length = 1
        else:
            self.tail_length = kwarg['tail_length'] # integer

        # name
        if 'name' in kwarg:
            self.name = kwarg['name']
        else:
            self.name = str(self.id_No)

        # MASS RADIUS DENSITY
        # mass x radius density
        if 'mass' in kwarg and 'r' not in kwarg and 'density' not in kwarg:
            self.density = 1
            self.mass = kwarg['mass']
            self.r = ((3*self.mass)/(4*self.density*np.pi))**(1/3)
        # radius x mass density
        elif 'mass' not in kwarg and 'r' in kwarg and 'density' not in kwarg:
            self.density = 1
            self.r = kwarg['r']
            self.mass = 4*self.density*np.pi*self.r**3/3
        # mass radius x density
        elif 'mass' in kwarg and 'r' in kwarg and 'density' not in kwarg:
            self.mass = kwarg['mass']
            self.r = kwarg['r']
            self.density = 1
        # mass density x radius
        elif 'mass' in kwarg and 'r' not in kwarg and 'density' in kwarg:
            self.mass = kwarg['mass']
            self.density = kwarg['density']
            self.r = ((3*self.mass)/(4*self.density*np.pi))**(1/3)
        # radius density x mass
        elif 'mass' not in kwarg and 'r' in kwarg and 'density' in kwarg:
            self.density = kwarg['density']
            self.r = kwarg['r']
            self.mass = 4*self.density*np.pi*self.r**3/3
        else:
            raise ValueError('Need 1 or 2 arguments in "mass", "radius" and "density".')

        # momentum & angular momentum
        M = self.mass
        self.momentum = M * self.vel
        J = 2 * M * self.r**2 / 5
        self.amomentum = J * spin

        # energy
        self.energy = 0.5*M*(self.vel[0]**2+self.vel[1]**2) + 0.5*J*spin**2

        # movement cache
        self.dp = np.zeros(2)
        self.dv = np.zeros(2)

    def move(self):
        self.pos += self.dp
        self.vel += self.dv
