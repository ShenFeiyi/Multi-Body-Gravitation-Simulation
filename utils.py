import numpy as np
from classes import Body


def collide(stars, ALL_STARS, ORIGIN, CENTRIAL):
    survivors = []
    
    for center in stars:
        if center.survive:
            for star in stars:
                if star.survive:
                    if center.id_No == star.id_No:
                        continue
                    else:
                        d = np.linalg.norm(star.pos-center.pos)
                        if d > center.r + star.r:
                            continue
                        else:
                            center.survive = False
                            star.survive = False
                            ALL_STARS += 1
                            M = center.mass + star.mass
                            V = 4*np.pi*center.r**3/3 + 4*np.pi*star.r**3/3
                            R = ((3*V)/(4*np.pi))**(1/3)
                            pos = (center.mass*center.pos+star.mass*star.pos)/M
                            energy = center.energy + star.energy
                            ratio = 0.9
                            if (center.momentum+star.momentum == np.array([0,0])).all():
                                vel = np.array([0,0])
                            else:
                                direction = (center.momentum+star.momentum)/np.linalg.norm(center.momentum+star.momentum)
                                amplitude = np.sqrt(2*ratio*energy/M)
                                vel = direction * amplitude
                            if center.amomentum+star.amomentum == 0:
                                spin = 0
                            else:
                                direction = (center.amomentum+star.amomentum)/np.linalg.norm(center.amomentum+star.amomentum)
                                amplitude = np.sqrt(2*(1-ratio)*energy/(2*M*R**2/5))
                                spin = direction * amplitude
                            color = (center.color+star.color)/2
                            new = Body(ALL_STARS, pos, vel, spin, mass=M, r=R, color=color)
                            if center.id_No is CENTRIAL or star.id_No is CENTRIAL:
                                CENTRIAL = ALL_STARS
                                ORIGIN = new.pos
                            survivors.append(new)
                else:
                    continue
        else:
            continue

    for star in stars:
        if star.survive:
            survivors.append(star)

    return survivors, ALL_STARS, ORIGIN, CENTRIAL

def accelerate(stars, G, ORIGIN, CENTRIAL, dt=1e-3):

    for center in stars:
        force = np.zeros(2)
        for star in stars:
            if center.id_No == star.id_No:
                continue
            else:
                d = np.linalg.norm(center.pos-star.pos)
                amplitude = (G*center.mass*star.mass)/(d**2)
                direction = (star.pos-center.pos)/np.linalg.norm(star.pos-center.pos)
                f = amplitude * direction
                force += f
        a = force/center.mass
        center.dp = center.vel * dt
        center.dv = a * dt

    for star in stars:
        star.move()
        if star.id_No is CENTRIAL:
            ORIGIN = star.pos
        star.dp = np.zeros(2)
        star.dv = np.zeros(2)

    return stars, ORIGIN, CENTRIAL
