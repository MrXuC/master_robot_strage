#!/usr/bin/python
# -*- coding:utf-8 -*-
#进行三次样条插值
#自变量为时间
from math import *
import spline_config

class cubic_spline(object):
    def __init__(self,v_m = spline_config.velocity_max):
        self.vel_max = v_m
        self.acc_max = spline_config.acceleration_max
        self.rateAcc_max = spline_config.rate_of_acceleration__max
        self.first_mode_distance = spline_config.first_mode_dis
        self.second_mode_distance = spline_config.second_mode_dis
    def set_mode(self,goal_distance):
        self.goal = goal_distance
        self.get_first_func(0)
        self.get_second_func(0)
        self.get_third_func(0)
        if goal_distance <= self.first_mode_distance:
            self.mode = 0
        elif goal_distance <= self.second_mode_distance:
            self.mode = 1
        else:
            self.mode = 2

    def cal(self, time = 0.0,dis = 0.0):
        if self.mode == 2:
            if dis < self.third_s1:
                return self.third_function[0](time)
            elif dis < self.third_s2:
                return self.third_function[1](time)
            elif dis < self.third_s3:
                return self.third_function[2](time)
            elif dis < (self.goal - self.third_s3):
                return self.third_function[3](time)
            elif dis < (self.goal - self.third_s2):
                return self.third_function[4](time)
            elif dis < (self.goal - self.third_s1):
                return self.third_function[5](time)
            elif dis < self.goal:
                return self.third_function[6](time)
            else:
                return 0.0
        if self.mode == 1:
            if dis < self.second_s1:
                return self.second_function[0](time)
            elif dis < self.second_s2:
                return self.second_function[1](time)
            elif dis < self.second_s3:
                return self.second_function[2](time)
            elif dis < (self.goal - self.second_s2):
                return self.second_function[3](time)
            elif dis < (self.goal - self.second_s1):
                return self.second_function[4](time)
            elif dis < self.goal:
                return self.second_function[5](time)
            else:
                return  0.0

        if self.mode == 0:
            if dis < self.first_s1:
                return self.first_function[0](time)
            elif dis < self.first_s2:
                return self.first_function[1](time)
            elif dis < (self.goal - self.first_s1):
                return self.first_function[2](time)
            elif dis < self.goal :
                return self.first_function[3](time)
            else:
                return  0.0

    def get_third_func(self,time):
        time = float(time)
        self.third_function = list()
        a1 = self.rateAcc_max / 6.0
        b1 = 0.0
        c1 = 0.0
        d1 = 0.0
        t1 = self.acc_max / self.rateAcc_max
        self.third_function.append(lambda t: a1 * t ** 3 + b1 * t ** 2 + c1 * t + d1)
        s1 = self.third_function[0](t1)

        a2 = self.acc_max       /   2.0
        b2 = -self.acc_max ** 2 /   (2.0 * self.rateAcc_max)
        c2 = self.acc_max**3    /   (6.0*self.rateAcc_max**2)
        t2 = self.vel_max / self.acc_max
        self.third_function.append(lambda t: a2 * t ** 2 + b2 * t + c2)
        s2 = self.third_function[1](t2) - s1

        a3 = -self.rateAcc_max / 6.0
        b3 = 0.5 * (self.acc_max + self.rateAcc_max * self.vel_max / self.acc_max)
        c3 = -self.rateAcc_max * self.vel_max ** 2 / (2 * self.acc_max ** 2) \
             - self.acc_max ** 2/(2 * self.rateAcc_max)
        d3 = ( self.acc_max ** 3 / (6 * self.rateAcc_max ** 2) +
                0.5 * self.acc_max ** 2 / self.rateAcc_max +
                self.rateAcc_max * self.vel_max**3  / (self.rateAcc_max**2 * 6))
#        a3 = self.rateAcc_max / 6.0
#        b3 = -0.5 * (self.acc_max + self.rateAcc_max * self.vel_max / self.acc_max)
#        c3 = 2*self.vel_max \
#             +self.rateAcc_max * self.vel_max ** 2 / (2.0 * self.acc_max **2) \
#             -self.acc_max**2/(2*self.rateAcc_max)
#        d3 = self.acc_max**3 /(6.0*self.rateAcc_max**2) \
#            -self.rateAcc_max * self.vel_max**3/(6.0*self.acc_max**3) \
#            -self.vel_max**2/self.acc_max
        t3 = t1 + t2
        self.third_function.append(lambda t: a3 * t ** 3 + b3 * t ** 2 + c3 * t + d3)
        s3 = 0.5*self.vel_max*t3
        fixed_velocity_time = (self.goal -2*s3)/self.vel_max
        self.third_function[0] = (lambda t: t**2 * 3 * a1 + 2.0*b1 * t + c1)
        self.third_function[1] = lambda t: 2*a2 * t + b2
        self.third_function[2] = lambda t: 3*a3 * t ** 2 + 2*b3 * t + c3
        self.third_function.append(lambda t: self.vel_max)
        self.third_function.append(lambda t: self.third_function[2](fixed_velocity_time + 2*t3 - t))
        self.third_function.append(lambda t: self.third_function[1](fixed_velocity_time + 2*t3 - t))
        self.third_function.append(lambda t: self.third_function[0](fixed_velocity_time + 2*t3 - t))
        self.third_s1 = s1
        self.third_s2 = s2
        self.third_s3 = s3
#        print s1,s2,s3
#        print "third_time 1,2,3:%lf; %lf; %lf"%(t1,t2,t3)
#        print "fuck" + str(fixed_velocity_time)
#        print type(time)
        if time < t1:
            return self.third_function[0](time)
        elif time < t2:
            return self.third_function[1](time)
        elif time < t3:
            return self.third_function[2](time)
        elif time < (fixed_velocity_time + t3):
            return self.third_function[3](time)
        elif time < (fixed_velocity_time + 2*t3 - t2):
            return self.third_function[4](time)
        elif time < (fixed_velocity_time + 2*t3 - t1):
            return self.third_function[5](time)
        elif time < (fixed_velocity_time + 2*t3):
            return self.third_function[6](time)
        else:
            return 0.0


    def get_second_func(self,time):
        self.second_function = list()
        a1 = self.rateAcc_max / 6.0
        time = float(time)
        b1 = 0.0
        c1 = 0.0
        d1 = 0.0
        t1 = self.acc_max / self.rateAcc_max
        self.second_function.append(lambda t: a1 * t ** 3 + b1 * t ** 2 + c1 * t + d1)
        s1 = self.second_function[0](t1)
        a2 = self.acc_max / 2.0
        b2 = -self.acc_max ** 2 / (2 * self.rateAcc_max)
        c2 = s1
        t2 =  0.5*(sqrt(self.acc_max**2/self.rateAcc_max**2 + 4* self.goal/self.acc_max)
                   - self.acc_max / self.rateAcc_max)
        self.second_function.append(lambda t: a2 * t ** 2 + b2 * t ** 1 + c2)
        s2 = self.second_function[1](t2)
        a3 = -self.rateAcc_max / 6.0
        b3 = 0
        c3 = 0.5 * (sqrt(self.acc_max ** 4 / self.rateAcc_max ** 2 + 4 * self.goal * self.acc_max)
                    - self.acc_max**2 / self.rateAcc_max)
        d3 = -self.goal / 2.0
        t3 = 0.5 * (sqrt(self.acc_max ** 2 / self.rateAcc_max ** 2 + 4 * self.goal / self.acc_max)
                    + self.acc_max / self.rateAcc_max)
        self.second_function.append(lambda t: a3 * (t - t3) ** 3 + b3 * t ** 2 + c3 * t + d3)
        s3 = self.second_function[2](t3)
        self.second_function[0] = lambda t: 3*a1 * t ** 2 + 2 * b1 * t + c1
        self.second_function[1] = lambda t: 2*a2 * t + b2
        self.second_function[2] = lambda t: 3*a3 * (t - t3) ** 2 +2 * b3 * t  + c3
        self.second_function.append(lambda t: self.second_function[2]((2 * t3 - t)))
        self.second_function.append(lambda t: self.second_function[1]((2 * t3 - t)))
        self.second_function.append(lambda t: self.second_function[0]((2 * t3 - t)))
        self.second_s1 = s1
        self.second_s2 = s2
        self.second_s3 = s3
#        print "second_time 1,2,3:%lf; %lf; %lf" % (t1, t2, t3)
        if time < t1:
            return self.second_function[0](time)
        elif time < t2:
            return self.second_function[1](time)
        elif time < t3:
            return self.second_function[2](time)
        elif time < t3*2 - t2:
            return self.second_function[3](time)
        elif time < t3*2 - t1:
            return self.second_function[4](time)
        elif time < t3*2:
            return self.second_function[5](time)
        else:
            return 0

    def get_first_func(self,time):
        self.first_function = list()
        a1 = self.rateAcc_max / 6.0
        b1 = 0
        c1 = 0
        d1 = 0
        t1 = pow(0.5*self.goal/self.rateAcc_max, 1/3.0)
        self.first_function.append(lambda t: a1 * t ** 3 + b1 * t ** 2 + c1 * t + d1)
        s1 = self.first_function[0](t1)

        a2 = -self.rateAcc_max / 6.0
        b2 = 0
        c2 = self.rateAcc_max*pow(0.5*self.goal / self.rateAcc_max, 2.0 / 3.0)
        d2 = -0.5*self.goal
        t2 = 2 * pow(0.5*self.goal/self.rateAcc_max, 1.0/3.0)
        self.first_function.append(lambda t: a2 * (t - t2) ** 3 + b2 * t ** 2 + c2*t+d2)
        s2 = self.first_function[1](t2)

        self.first_function[0] = lambda t: 3*a1 * t ** 2 + 2*b1 * t + c1
        self.first_function[1] = lambda t: 3*a2 * (t - t2) ** 2 + 2*b2 * t + c2
        self.first_function.append(lambda t: self.first_function[1]((2 * t2 - t)))
        self.first_function.append(lambda t: self.first_function[0]((2 * t2 - t)))
        self.first_s1 = s1
        self.first_s2 = s2
        #print "first_time 1,2,3:%lf,%lf" % (t1, t2)
        if time < t1:
            return self.first_function[0](time)
        elif time < t2:
            return self.first_function[1](time)
        elif time < t2*2 - t1:
            return self.first_function[2](time)
        elif time < t2*2:
            return self.first_function[3](time)
        else:
            return 0
