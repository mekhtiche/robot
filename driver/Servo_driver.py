#!/usr/bin/env python


import rospy
from beginner_tutorials.msg import servoSet
from servo.Adafruit_PWM_Servo_Driver import PWM

hand = ['Right', 'Left']
DEBUG = 1
Lpwm = PWM(0x41, 4)
Rpwm = PWM(0x40, 4)
Lpwm.setPWMFreq(30)
Rpwm.setPWMFreq(30)




def doIt(Rcmd, Lcmd):
    Rpwm.setPWM(1, 0, Rcmd[0])
    Rpwm.setPWM(2, 0, Rcmd[1])
    Rpwm.setPWM(3, 0, Rcmd[2])
    Rpwm.setPWM(4, 0, Rcmd[3])
    Rpwm.setPWM(5, 0, Rcmd[4])
    Rpwm.setPWM(6, 0, Rcmd[5])
    Rpwm.setPWM(7, 0, Rcmd[6])
    Rpwm.setPWM(8, 0, Rcmd[7])
    Rpwm.setPWM(9, 0, Rcmd[8])

    Lpwm.setPWM(1, 0, Lcmd[0])
    Lpwm.setPWM(2, 0, Lcmd[1])
    Lpwm.setPWM(3, 0, Lcmd[2])
    Lpwm.setPWM(4, 0, Lcmd[3])
    Lpwm.setPWM(5, 0, Lcmd[4])
    Lpwm.setPWM(6, 0, Lcmd[5])
    Lpwm.setPWM(7, 0, Lcmd[6])
    Lpwm.setPWM(8, 0, Lcmd[7])
    Lpwm.setPWM(9, 0, Lcmd[8])



def callback(data):
    #print data
    doIt(data.right_cmd, data.left_cmd)





if __name__ == '__main__':

    rospy.init_node('Fingers_driver', anonymous=True)
    rospy.Subscriber('servo/cmd', servoSet, callback=callback)
    rospy.spin()
