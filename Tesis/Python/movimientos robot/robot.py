#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import time
from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Moving around:
   u    i    o
   j    k    l
   m    ,    .
"""

moveBindings = {
		'a':(1,0),
		'i':(0,1),
		'd':(0,-1),
		}
speed = .1
turn = 1

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('teleop_twist_keyboard')

	x = 0
	th = 0
	
	try:
		while(1):
			key = 'i'
			x = moveBindings[key][0]
			th = moveBindings[key][1]
			twist = Twist()
			twist.linear.x  = x*speed
			twist.linear.y  = 0 
			twist.linear.z  = 0
			twist.angular.x = 0
			twist.angular.y = 0
			twist.angular.z = th*turn
			pub.publish(twist)
			time.sleep(2)
			x = 0
			th = 0
			twist.linear.x  = 0
			twist.linear.y  = 0 
			twist.linear.z  = 0
			twist.angular.x = 0 
			twist.angular.y = 0 
			twist.angular.z = 0
			break 
			
	finally:
		twist = Twist()
		pub.publish(twist)
  		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
