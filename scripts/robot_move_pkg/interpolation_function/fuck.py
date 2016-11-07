#!/usr/bin/env python

import matplotlib.pyplot as plot
import growth_curve as gc
goal = 2.5
def main():
    shit = gc.growth_curve()
    shit.set_goal_distance(goal)
    dis = 0.0
    vel = 0.0
    bitch = 100.0
    x = list()
    y = list()  
    for i in range(5000):
#        if dis > goal:
#            break
        dis += vel / bitch
        vel = shit.cal(dis)
        x.append(dis)
        y.append(vel)
    print dis
    plot.xlabel('dis_has_move')
    plot.ylabel('spline_vel')
    plot.plot(x,y)
    plot.savefig('growth_curve_demo.jpg')
    plot.show()
main()
