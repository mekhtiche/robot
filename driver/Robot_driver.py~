#!/usr/bin/env python

import thread
import time
import rospy
from beginner_tutorials.msg import motorStat
from beginner_tutorials.msg import motorStatList
from beginner_tutorials.msg import motorSet
from std_msgs.msg import String
import pypot.robot
print 'succiful import'

robot = pypot.robot.from_config(pypot.robot.config.robot_config, True, True, False, activemotors={})


pupStat = rospy.Publisher('Robot_status', String, queue_size=10)
motorStatus = rospy.Publisher('All_motors', motorStatList, queue_size=10)

pub = dict()




def Openning():
    print('Starting the ROBOT')
    try:
        for m in robot.motors:
            m.compliant = False
        for m in robot.motors:
            m.goal_position = 0
        print('Robot started')
        robot_status = 'Ready'
        pupStat.publish(robot_status)

    except Exception, err:
        print 'Robot can not start, error is '
        print  err
        robot_status = err.message
        pupStat.publish(robot_status)



def Closing():

    try:
        print 'Closing the robot'
        for m in robot.motors:
            m.compliant = True
        robot.close()
        robot_status = 'Closed'
        pupStat.publish(robot_status)
        print 'Robot Closed'
    except Exception, err:
        print err


def callback(data, m):
    m.compliant = data.compliant
    m.direct = data.direct
    m.goal_position = data.goal_position
    m.offset = data.offset
    m.torque_limit = data.max_load

def publisher():
    motor = motorStat()
    while not rospy.is_shutdown():
        motors = motorStatList()
        for m in robot.motors:
            motor.id = m.id
            motor.name = m.name
            motor.present_position = m.present_position
            motor.goal = m.goal_position
            motor.present_error = m.goal_position - m.present_position
            motor.present_speed = m.present_speed
            motor.present_load = m.present_load
            motor.present_voltage = m.present_voltage
            motor.present_temperature = m.present_temperature
            motor.compliant = m.compliant
            motor.max_angle = m.angle_limit[0]
            motor.min_angle = m.angle_limit[1]
            motor.direction = m.direct
            motor.model = m.model
            motor.offset = m.offset
            motor.max_load = m.torque_limit
            pub[m.name].publish(motor)
            motors.motorList.append(motor)# = motors.motorList + [motor]
        motorStatus.publish(motors)
        time.sleep(0.1)

if __name__ == '__main__':

    rospy.init_node('robot_node', anonymous=True)
    Openning()
    for m in robot.motors:
        pub[m.name] = rospy.Publisher('poppy/get/'+m.name, motorStat, queue_size=10)
        rospy.Subscriber('poppy/set/'+m.name, motorSet, callback=callback, callback_args=m)
    print 'ROBOT publishers & subscribers'
    thread.start_new_thread(publisher, ())
    rospy.spin()
    Closing()


