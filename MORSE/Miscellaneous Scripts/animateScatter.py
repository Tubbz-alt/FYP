import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def main():
    numframes = 100
    numpoints = 10
    color_data = np.random.random((numframes, numpoints))
    f = open("pathPlots(175 laps).txt","r")
    xar = []
    yar = []

    for line in f:
        x, y = line.split(' ')
        xar.append(int(x))
        yar.append(int(y))

    fig = plt.figure()
    plt.xlim(-73, 73)
    plt.ylim(-60, 60)
    scat = plt.scatter(xar, yar, s=1)

    ani = animation.FuncAnimation(fig, update_plot, fargs=(color_data, scat))
    plt.show()

def update_plot(i, data, scat):
    scat.set_array(data[i])
    return scat,

main()