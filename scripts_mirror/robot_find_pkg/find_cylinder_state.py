#!/usr/bin/python
#coding=utf-8
#Author: Xu

#为状态机模块提供找定位柱的接口
#kinect的坐标系与机器人坐标系不同！

import rospy
from object_detect.srv import *
from cylinder_find.srv import *
import geometry_msgs.msg as g_msgs

class find_cylinder_state(object):
    def __init__(self):
        self.cylinder_client = rospy.ServiceProxy('cylinder_data',cylinderdata)
        self.cylinder_theta_client = rospy.ServiceProxy('cylinder_data_theta',cylinder_find)
        self.cmd_vel_pub = rospy.Publisher('cmd_move_robot' , g_msgs.Twist , queue_size=100)
        rospy.loginfo('[cylinder_state_pkg]->waiting cylinderdata service')
        self.cylinder_client.wait_for_service()
        self.cylinder_theta_client.wait_for_service()
        rospy.loginfo('[cylinder_state_pkg] -> connected to cylinder service')


    #边转动边检测定位柱，检测到后停止
    def get_cylinder_status(self):
        self.cylinder_client.wait_for_service()
        res = self.cylinder_client(True)
        move_velocity = g_msgs.Twist()
        move_velocity.angular.z = 0.13
        x = res.z
        theta = res.theta
        iscylinder = res.has_cylinder
        r = rospy.Rate(50)
        while not rospy.is_shutdown() and not iscylinder:
            self.cmd_vel_pub.publish(move_velocity)
            res = self.cylinder_client(True)
            x = res.z
            theta = res.theta
            iscylinder = res.has_cylinder
            if iscylinder == 1:
                self.brake()
                break
            r.sleep()
        return (x,theta)

    #直接获取定位柱的位置信息
    def find_cylinder(self):
        res_theta = self.cylinder_theta_client()
        x = 0
        theta = res_theta.theta
        return (x,theta)

    def brake(self):
        self.cmd_vel_pub.publish(g_msgs.Twist())


if __name__ == '__main__':
    rospy.init_node('find_cylinder')
    test = find_cylinder_state()
    print test.get_cylinder_status()
