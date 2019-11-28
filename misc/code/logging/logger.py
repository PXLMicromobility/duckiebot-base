#!/usr/bin/env python
import rospy
import numpy, sys, csv, datetime
from sensor_msgs.msg import CompressedImage, Joy
from duckietown_msgs.msg import WheelsCmdStamped 


# Joy [(0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
# Wheels_Cmd_Executed [-0.47752153873443604, -0.47752153873443604]
# Image/Compressed ['blob data.data', 'jpeg']

datetime = datetime.datetime.now()

class Logger:

    def __init__(self, destination, robot_name, time):
        
        rospy.init_node('logger', anonymous=True)
        self.seq = 0
        # This represents the last known image and joy message that will later be used in the wheels_executed_callback to write them to files.
        self.LKimage = None 
        self.LKjoy = None
        self.LKjoy = {"seq": self.seq, "axes": [0,0,0,0,0,0], "buttons": [0,0,0,0,0,0,0]}
        self.destination = destination
        self.robot_name = robot_name
        self.time_instatiated = str(time).replace(" ", "")[:-7]
        self.destination = destination
        self.file_name = destination + "/" + self.robot_name + "_" + self.time_instatiated
        with open(self.file_name + '.csv', mode='w') as csv_file:
            csv_file.write("seq,x,y,vel_left,vel_right\n")
        rospy.Subscriber("/" + self.robot_name + "/wheels_driver_node/wheels_cmd_executed", WheelsCmdStamped, self.wheels_executed_callback)
        rospy.Subscriber("/" + self.robot_name + "/camera_node/image/compressed", CompressedImage, self.camera_callback)
        rospy.Subscriber("/" + self.robot_name + "/joy", Joy, self.joy_callback)

    
    def wheels_executed_callback(self, data):
        with open(self.file_name + '.csv', mode='a') as csv_file:
            csv_file.write("{},{},{},{},{}\n".format(self.seq, self.LKjoy["axes"][1], self.LKjoy['axes'][3], data.vel_left, data.vel_right))
        self.write_image(self.seq, self.LKimage["format"], self.LKimage["data"])
        self.seq += 1

    def camera_callback(self, data):
        self.LKimage = {"seq": self.seq, "data": data.data, "format": data.format}
    
    def joy_callback(self, data):
        self.LKjoy = {"seq": self.seq, "axes": data.axes, "buttons": data.buttons}

    def write_image(self, name, format, data):
        with open(self.destination + "/images/" + str(name) + "." + format, "w") as file:
                file.write(data)

if __name__ == '__main__':
    if len(sys.argv) is 1:
        raise Exception("Destination Argument cannot be None or empty")
    if len(sys.argv) is 2:
        raise Exception("Robot Name cannot be None or empty")
    logger = Logger(destination=sys.argv[1], robot_name=sys.argv[2], time=datetime)
    rospy.spin()    

# scp thizzhead@172.16.104.139:/home/thizzhead/duckiebot-base/misc/code/logging/logger.py .