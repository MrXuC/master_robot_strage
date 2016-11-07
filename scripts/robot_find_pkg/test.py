#!/usr/bin/python
#coding=utf-8
import rospy
# from cylinder_detector.srv  import *
from object_detect.srv import *
from cylinder_find.srv import *
import geometry_msgs.msg as g_msgs 

if __name__ == '__main__':
    #cylinder_client = rospy.ServiceProxy('cylinder_data',cylinderdata)
    cylinder_client_theta = rospy.ServiceProxy('cylinder_data_theta',cylinder_find)
    #self.cmd_vel_pub = rospy.Publisher('cmd_move_robot' , g_msgs.Twist , queue_size=100)
    rospy.loginfo('[cylinder_state_pkg]->waiting cylinderdata service')
    cylinder_client_theta.wait_for_service()
    rospy.loginfo('[cylinder_state_pkg] -> connected to cylinder service')
    res_theta = cylinder_client_theta()
