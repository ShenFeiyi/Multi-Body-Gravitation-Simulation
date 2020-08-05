import numpy as np
from matplotlib import pyplot as plt


filename = 'estimate.txt'
with open(filename, 'r') as file:
    lines = file.readlines()

epochs = []
stars = []
time = []
for line in lines:
    data = line.split(' ')
    epochs.append(int(data[0]))
    stars.append(int(data[1]))
    time.append(int(data[2]))

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

# 创建系数矩阵A
a = 0
A = np.ones((len(lines), 3))
for i in range(0, len(lines)):
    A[i, 0] = epochs[a]
    A[i, 1] = stars[a]
    a += 1
 
# 创建矩阵b
b = np.zeros((len(lines), 1))
a = 0
for i in range(0, len(lines)):
    b[i, 0] = time[a]
    a += 1
 
# 通过X=(AT*A)-1*AT*b直接求解
A_T = A.T
A1 = np.dot(A_T, A)
A2 = np.linalg.inv(A1)
A3 = np.dot(A2, A_T)
X = np.dot(A3, b)
print('平面拟合结果为：time = %.3f * epochs + %.3f * stars + %.3f' % (X[0,0],X[1,0],X[2,0]))
 
# 计算方差
R = 0
for i in range(0,len(lines)):
    R += (X[0, 0] * epochs[i] + X[1, 0] * stars[i] + X[2, 0] - time[i])**2
print ('方差为：%.*f' % (3,R))

x_p = np.linspace(min(epochs)-1, max(epochs)+1)
y_p = np.linspace(min(stars)-1, max(stars)+1)
x_p, y_p = np.meshgrid(x_p, y_p)
z_p = X[0, 0] * x_p + X[1, 0] * y_p + X[2, 0]
ax.plot_wireframe(x_p, y_p, z_p, alpha=0.5)

ax.scatter(epochs, stars, time, color='r')
ax.set_xlabel('epochs')
ax.set_ylabel('stars')
ax.set_zlabel('time')

plt.show()
