#!/usr/bin/env python

import rospy
import os
import time
import threading
import Adafruit_PCA9685
from std_msgs.msg import String

os.system("sudo pigpiod")
time.sleep(1)
import pigpio


def robot_init():
	
	pwm = Adafruit_PCA9685.PCA9685()	
	
	#GPIO04
	ESC = 4

	pi = pigpio.pi()
	pi.set_servo_pulsewidth(ESC, 0)

	max_value = 2000
	min_value = 700


class engine_listener(thread.Thread):
	
	def __init__(self, sub):
		threading.Thread.__init__(self)
		self.sub = sub
		self.speed = 1500
	
	def sent_command(self, data):
		self.drive(data.data)

	def drive(self, data):
		
		if data == 'forward' and self.speed != 1588:
			self.speed += 1
		elif data == 'reverse' and self.speed != 1417:
			self.speed -= 1
		else:
			pass
		pi.set_servo_pulsewidth(ESC, self.speed)

	def run(self):
		rospy.Subscriber(self.sub, String, self.sent_command)
		rospy.spin()

	
	

class steering_listener(threading.Thread):

	#Init-function
	def __init__(self, sub):
		threading.Thread.__init__(self)
		self.sub = sub
		self.turn = 425

	def sent_command(self, data):
		self.drive(data.data)
			
	
	def drive(self, data):
		
		print(self.turn)
		if data == 'left' and self.turn != 510:
			self.turn += 5
		elif data == 'right' and self.turn != 335:
			self.turn -= 5
		else:
			pass
		pwm.set_pwm(0,0,self.turn)
			

	def run(self):
		rospy.Subscriber(self.sub, String, self.sent_command)
		rospy.spin()

class robot_kinetics:

	def __init__(self):
		self.controlEnabled = False
		self.calibrateEnabled = False

	
	def calibrate(self):
		pi.set_servo_pulsewidth(ESC, 0)
		time.sleep(5)
		pi.set_servo_pulsewidth(ESC, max_value)
		time.sleep(5)
		pi.set_servo_pulsewidth(ESC, min_value)
		time.sleep(5)
		pi.set_servo_pulsewidth(ESC, 0)
		time.sleep(5)
		pi.set_servo_pulsewidth(ESC, 0)
		time.sleep(1)
	

	def callback(self,data):
		rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		if data.data == 'control' and not self.controlEnabled:
			self.thread_starter()
			self.controlEnabled = True

		elif data.data == 'calibrate' and not self.calibrateEnabled:
			print("calibration initiating....")
			#self.calibrate
			self.calibrateEnabled = True
			self.thread_starter()
		else: 
			print("TESTING INIT_COMMAND FUNCTION")

		

	def initial_command(self):
		rospy.Subscriber('function', String, self.callback)
		rospy.spin()

	def thread_starter(self):
		self.eThread = engine_listener('engine')
		self.sThread = steering_listener('steering')
		self.eThread.start()
		self.sThread.start()

	def main(self):
		rospy.init_node('listener', anonymous=True)
		self.initial_command()

def run():
	robot_init()
	ROBOT = robot_kinetics()
	ROBOT.main()

if __name__ == '__main__':
	try:
		run()
	except rospy.ROSInterruptException:
		ROBOT.engine_thread.terminate()
		ROBOT.steerng_thread.terminate()
		pass




