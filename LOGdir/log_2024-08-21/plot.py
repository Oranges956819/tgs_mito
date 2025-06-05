import numpy as np
import sys
import matplotlib.pyplot as plt

filename = "filelog_2024-08-21_11:39.txt"
filepath = "240821_133927_path.txt"
#filename = sys.argv[1]


az = np.loadtxt(filename, dtype=float, delimiter='\t', skiprows=1, unpack='true',usecols=2)
el = np.loadtxt(filename, dtype=float, delimiter='\t', skiprows=1, unpack='true',usecols=1)

az_enc = 250 + np.loadtxt(filepath, dtype=float, delimiter='\t', skiprows=0, unpack='true',usecols=0)
el_enc = 180 - np.loadtxt(filepath, dtype=float, delimiter='\t', skiprows=0, unpack='true',usecols=1)

fig, ax = plt.subplots(1,1)

ax.plot(az,el,color='b')
ax.plot(az_enc,el_enc,color='r')
ax.set_ylabel('elevation [deg]')
ax.set_xlabel('azimuth [deg]')

plt.show()

