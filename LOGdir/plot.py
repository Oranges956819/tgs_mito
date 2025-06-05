import numpy as np
import sys
import matplotlib.pyplot as plt

#filename = "filelog_2024-09-17_10h04m00s.txt"
filename = sys.argv[1]
filelog = "/home/massimiliano/Desktop/workdir/Programmi_Solaris/movimento_telescopi/armadietto_unimi/otf_v1/LOGdir/log_2024-09-17/filelog_2024-09-17_13h38m13s.txt"

x1 = np.loadtxt(filename, dtype=float, delimiter=',', skiprows=1, unpack='true',usecols=1)
y1 = np.loadtxt(filename, dtype=float, delimiter=',', skiprows=1, unpack='true',usecols=2)

x2 = np.loadtxt(filelog, dtype=float, delimiter=',', skiprows=3, unpack='true',usecols=3)
y2 = np.loadtxt(filelog, dtype=float, delimiter=',', skiprows=3, unpack='true',usecols=4)

fig, ax = plt.subplots(1,1)

ax.plot(y1,x1,color='b')
ax.scatter(y2,x2,color='r')
ax.set_ylabel('elevation [deg]')
ax.set_xlabel('azimuth [deg]')

plt.show()

