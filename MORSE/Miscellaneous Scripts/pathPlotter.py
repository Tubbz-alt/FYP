#Created by: Miguel Sancho

import matplotlib.pyplot as plt

f = open("paths.txt","r")
xar = []
yar = []

for line in f:
	x, y = line.split(' ')
	xar.append(int(x))
	yar.append(int(y))

plt.xlim(-73, 73)
plt.ylim(-60, 60)
plt.scatter(xar, yar, s=2)
#plt.plot(xar, yar)
plt.show()
