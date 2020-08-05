import os
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Ellipse

import cv2 as cv

from classes import Body
from utils import collide, accelerate


frame_path = 'frame-continue'
file_name = 'simulation-continue.mp4'
if not os.path.exists(os.path.join('.',frame_path)):
    # frame cache folder
    os.mkdir(os.path.join('.',frame_path))

# Read logged data
with open('simulation.txt', 'r') as f:
    content = f.readlines()

# Read origin and centrial id
origin_and_centrial = content[2]
ORIGIN = np.array([float(origin_and_centrial.split(' ')[0]), float(origin_and_centrial.split(' ')[1])])
CENTRIAL = int(origin_and_centrial.split(' ')[2])
ALL_STARS = int(origin_and_centrial.split(' ')[3])

# Read stars' data
datatxt = content[3:]
stars = []
for data in datatxt:
    d = data.split(' ')
    id_No = int(d[0])
    pos0 = float(d[1])
    pos1 = float(d[2])
    vel0 = float(d[3])
    vel1 = float(d[4])
    spin = float(d[5][:-1][1:])
    tail_length = int(d[6])
    color0 = float(d[7])
    color1 = float(d[8])
    color2 = float(d[9])
    name = d[10]
    mass = float(d[11][:-1][1:])
    r = float(d[12][:-1][1:])
    stars.append(
        Body(id_No, np.array([pos0,pos1]), np.array([vel0,vel1]), np.array(spin),
             tail_length=tail_length, color=np.array([color0,color1,color2]), name=name, mass=mass, r=r)
        )


exp = 3.432
epoch = 0
epochs = 10**exp

G = 10
all_stars = ALL_STARS

# Plot frames
start = datetime.now()
print('Simulating...')
while True:
    stars, ALL_STARS, ORIGIN, CENTRIAL = collide(stars, ALL_STARS, ORIGIN, CENTRIAL)
    stars, ORIGIN, CENTRIAL = accelerate(stars, G, ORIGIN, CENTRIAL, dt=1e-3)

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis([-100+ORIGIN[0],100+ORIGIN[0],-100+ORIGIN[1],100+ORIGIN[1]])

    for star in stars:
        circle = Circle(star.pos, star.r, color=star.color)
        ellipse = Ellipse(star.pos, star.r, star.r/2, star.spin*epoch, color=1-star.color)
        ax.add_patch(circle)
        ax.add_patch(ellipse)

    plt.savefig(os.path.join('.',frame_path,str(epoch).zfill(int(exp)+1)+'.jpg'))
    plt.close()

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
# Read former video
cap = cv.VideoCapture('simulation.mp4')
success, img0 = cap.read()
while success:
    try:
        video.write(img0)
        success, img0 = cap.read()
    except:
         break
# Write new video
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
with open('simulation-continue.txt', 'w') as f:
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
engine.say('all work done.')
engine.runAndWait()
engine.stop()
