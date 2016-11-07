#!/usr/bin/env python
import math
import matplotlib.pyplot as pp
import matplotlib.pylab as sss

import cubic_spline

goal  = 3
def shit():
    fuck = cubic_spline.cubic_spline()

    dis = 0
    times = list()
    velocities = list()
    distance = list()
    pp.figure(1)
#    ax1 = pp.subplot(211)
#    ax2 = pp.subplot(212)
    bitch= 100.0
    fuck.set_mode(goal)
    print "mode:" + str(fuck.mode)
    for time in range(0,1500):
        #if dis < goal:
            if fuck.mode == 0:
                vel = fuck.get_first_func(time/bitch)
            elif fuck.mode == 1:
                vel = fuck.get_second_func(time/bitch)
            else:
                vel = fuck.get_third_func(time/bitch)
            dis += (vel/bitch)
           # print  dis
            velocities.append(vel)
            times.append(time/bitch)
            distance.append(dis)
    print dis
    #pp.sca(ax1)
    pp.plot(times, velocities)
    #pp.sca(ax2)
    #pp.plot(times, distance)
    pp.show()
def shit2():
    fuck = cubic_spline.cubic_spline()

    dis = 0
    times = list()
    velocities = list()
    distance = list()
    pp.figure(1)
#    ax1 = pp.subplot(211)
#   ax2 = pp.subplot(212)
    bitch= 100.0
    fuck.set_mode(goal)
    for time in range(0,2000):
        if dis <= goal:
#            if fuck.mode ==0:
#                vel = fuck.get_first_func(time/bitch)
#            elif fuck.mode == 1:
#                vel = fuck.get_second_func(time/bitch)
#            else:
#                vel = fuck.get_third_func(time/bitch)
            vel = fuck.cal(time/bitch, dis)
            dis+= (vel/bitch)
            velocities.append(vel)
            times.append(time/bitch)
    print "mode: "+str(fuck.mode)
    print dis
    #pp.sca(ax1)
    pp.plot(times, velocities)
    #pp.sca(ax2)
    #pp.plot(times, distance)
    pp.show()
if __name__ == '__main__':
    shit()
    #shit2()
