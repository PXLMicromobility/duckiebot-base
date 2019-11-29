#!/usr/bin/env python
import rospy
import zipfile
import numpy, sys, csv, datetime, os, signal
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
        self.LKjoy = {"seq": self.seq, "axes": [0,0,0,0,0,0], "buttons": [0,0,0,0,0,0,0]}
        self.destination = destination
        self.robot_name = robot_name
        self.time_instatiated = str(time).replace(" ", "")[:-7]
        self.destination = destination
        self.file_name = destination + "/" + self.robot_name + "_" + self.time_instatiated
        with open(self.file_name + '.csv', mode='w+') as csv_file:
            csv_file.write("seq,x,y,vel_left,vel_right\n")
        rospy.Subscriber("/" + self.robot_name + "/wheels_driver_node/wheels_cmd_executed", WheelsCmdStamped, self.wheels_executed_callback)
        rospy.Subscriber("/" + self.robot_name + "/camera_node/image/compressed", CompressedImage, self.camera_callback)
        rospy.Subscriber("/" + self.robot_name + "/joy", Joy, self.joy_callback)

    
    def wheels_executed_callback(self, data):
        with open(self.file_name + '.csv', mode='a+') as csv_file:
            csv_file.write("{},{},{},{},{}\n".format(self.seq, self.LKjoy["axes"][1], self.LKjoy['axes'][3], data.vel_left, data.vel_right))
        self.write_image(self.seq, self.LKimage["format"], self.LKimage["data"])
        self.seq += 1

    def camera_callback(self, data):
        self.LKimage = {"seq": self.seq, "data": data.data, "format": data.format}
    
    def joy_callback(self, data):
        self.LKjoy = {"seq": self.seq, "axes": data.axes, "buttons": data.buttons}

    def write_image(self, name, format, data):
        if not os.path.isdir(self.destination + "/images/"):
            os.mkdir(self.destination + "/images/")
        with open(self.destination + "/images/" + str(name) + "." + format, "w") as file:
            file.write(data)

def get_robot_name():
    if len(sys.argv) is 1:
        raise Exception("Robot Name cannot be None or empty")
    return sys.argv[1]

def signal_handler(sig, frame):
    print("\nZipping... Wait a second please.\n")
    folder_name = "/data/logs"
    zip_name = get_robot_name() + "_logs_" + str(datetime).replace(" ", "")

    if len(os.listdir(folder_name)) is 0:
        print("No files in directory")
        sys.exit()

    with zipfile.ZipFile(os.path.join(folder_name, zip_name) + '.zip', 'w') as zf:
        for item in os.listdir(folder_name):
            if item.endswith(".zip"):
                continue

            if os.path.isfile(os.path.join(folder_name, item)):
                zf.write(os.path.join(folder_name, item), item)
            else:
                for file in os.listdir(os.path.join(folder_name, item)):
                    zf.write(os.path.join(folder_name, item, file), os.path.join(item, file))
    
    for item in os.listdir(folder_name):
        if item.endswith(".zip"):
            continue
        if os.path.isfile(os.path.join(folder_name, item)):
            os.remove(os.path.join(folder_name, item))
        if os.path.isdir(os.path.join(folder_name, item)):
            for file in os.listdir(os.path.join(folder_name, item)):
                if os.path.isfile(os.path.join(folder_name, item, file)):
                    os.remove(os.path.join(folder_name, item, file))
            os.rmdir(os.path.join(folder_name, item)) 
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    logger = Logger(destination="/data/logs", robot_name=get_robot_name(), time=datetime)
    rospy.spin()