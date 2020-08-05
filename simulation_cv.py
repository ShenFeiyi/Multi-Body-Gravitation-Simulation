import os
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Ellipse

import cv2 as cv

from classes import Body
from utils import collide, accelerate


frame_path = 'frame'
file_name = 'simulation.mp4'
if not os.path.exists(os.path.join('.',frame_path)):
    # frame cache folder
    os.mkdir(os.path.join('.',frame_path))

exp = 4.21
epoch = 0
epochs = 10**exp

# Generate stars
G = 10
ALL_STARS = 255
all_stars = ALL_STARS

stars = [Body(1, np.zeros(2), np.zeros(2), np.array(0.1), mass=np.array(3333.3333), r=np.array(111.111))]
'''
# Original size
sun_mass = 333000 # unit: Earth
distance = [0, 0.38, 0.723, 1.001, 1.5235, 5.204, 9.582, 19.23, 30.1085] # unit: AU
stars = [
    # Body(id_No, pos,                 vel,                                           spin,             mass,                    r,                         name)
    Body(1, np.zeros(2),               np.zeros(2),                                   np.array( 0.040), mass=np.array(333299.9), r=np.array(0.005000*50),   name='Sun'),
    Body(2, np.array([distance[1],0]), np.array([0,np.sqrt(G*sun_mass/distance[1])]), np.array( 0.017), mass=np.array(0.055000), r=np.array(0.000018*1000), name='Mercury'),
    Body(3, np.array([distance[2],0]), np.array([0,np.sqrt(G*sun_mass/distance[2])]), np.array(-0.004), mass=np.array(0.815000), r=np.array(0.000044*1000), name='Venus'),
    Body(4, np.array([distance[3],0]), np.array([0,np.sqrt(G*sun_mass/distance[3])]), np.array( 1.001), mass=np.array(1.000001), r=np.array(0.000046*1000), name='Earth'),
    Body(5, np.array([distance[4],0]), np.array([0,np.sqrt(G*sun_mass/distance[4])]), np.array( 0.975), mass=np.array(0.107000), r=np.array(0.000024*1000), name='Mars'),
    Body(6, np.array([distance[5],0]), np.array([0,np.sqrt(G*sun_mass/distance[5])]), np.array( 2.439), mass=np.array(317.8000), r=np.array(0.000498*1000), name='Jupiter'),
    Body(7, np.array([distance[6],0]), np.array([0,np.sqrt(G*sun_mass/distance[6])]), np.array( 2.347), mass=np.array(95.15200), r=np.array(0.000433*1000), name='Saturn'),
    Body(8, np.array([distance[7],0]), np.array([0,np.sqrt(G*sun_mass/distance[7])]), np.array( 2.347), mass=np.array(14.53600), r=np.array(0.000184*1000), name='Uranus'),
    Body(9, np.array([distance[8],0]), np.array([0,np.sqrt(G*sun_mass/distance[8])]), np.array( 1.502), mass=np.array(17.14700), r=np.array(0.000178*1000), name='Neptune')
    ]
'''

ORIGIN = stars[0].pos
CENTRIAL = stars[0].id_No
for i in range(len(stars),ALL_STARS):
    stars.append(
        Body(i+1, 150*np.random.rand(2)-75, 200*np.random.rand(2)-100, 2*np.random.rand(1)-1, mass=100*np.random.rand(1), density=10*np.random.rand(1))
        )

# Plot frames
start = datetime.now()
print('Simulating...')
while True:
    fig = plt.figure(figsize=(16,16))
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis([-333+ORIGIN[0],333+ORIGIN[0],-333+ORIGIN[1],333+ORIGIN[1]])

    for star in stars:
        circle = Circle(star.pos, star.r, color=star.color)
        ellipse = Ellipse(star.pos, star.r, star.r/2, star.spin*epoch, color=1-star.color)
        ax.add_patch(circle)
        ax.add_patch(ellipse)

    plt.savefig(os.path.join('.',frame_path,str(epoch).zfill(int(exp)+1)+'.jpg'))
    plt.close()

    stars, ALL_STARS, ORIGIN, CENTRIAL = collide(stars, ALL_STARS, ORIGIN, CENTRIAL)
    stars, ORIGIN, CENTRIAL = accelerate(stars, G, ORIGIN, CENTRIAL, dt=1e-3)

    epoch += 1
    if epoch >= epochs:
        break

# Read frames
print('Analysing...')
dirs = os.listdir(os.path.join('.',frame_path))
imgnames = [ os.path.join('.',frame_path,img) for img in dirs if img.endswith('jpg') ]
imgnames.sort()

# Generate video
fps = 60
sample = cv.imread(imgnames[0])
size = (sample.shape[0],sample.shape[1])
fourcc = cv.VideoWriter_fourcc(*'XVID')
video = cv.VideoWriter(file_name, fourcc, fps, size)
for img in imgnames:
    frame = cv.imread(img)
    video.write(frame)
video.release()
for img in imgnames:
    os.remove(img)
os.rmdir(os.path.join('.',frame_path))
finish = datetime.now()
time = (finish-start).seconds

# Log data for time estimate
filename = 'estimate.txt'
content = []
if os.path.exists(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
with open(filename, 'w') as file:
    if not content == []:
        file.writelines(content)
    log = str(int(epochs)) + ' ' + str(all_stars) + ' ' + str(time)
    file.writelines(log)
    file.write('\n')

# Log data for further simulation
with open('simulation.txt', 'w') as f:
    f.write('ORIGIN[0] ORIGIN[1] CENTRIAL ALL_STARS\n')
    f.write('id_No pos[0] pos[1] vel[0] vel[1] spin tail_length color[0] color[1] color[2] name mass r\n')
    f.write(str(ORIGIN[0])+' '+str(ORIGIN[1])+' '+str(CENTRIAL)+' '+str(ALL_STARS)+'\n')
    for star in stars:
        data = [
            star.id_No, star.pos[0], star.pos[1], star.vel[0], star.vel[1],
            star.spin, star.tail_length, star.color[0], star.color[1], star.color[2],
            star.name, star.mass, star.r
            ]
        for item in data:
            f.write(str(item))
            f.write(' ')
        f.write('\n')

# Alarm me that all work's done
import pyttsx3
engine = pyttsx3.init()
engine.say('All work done.')
engine.runAndWait()
engine.stop()
