import rosbag
import sys
import yaml
import json 
import ntpath

"""arg 1: path to .bag file, arg 2: robot name"""

bag = rosbag.Bag(sys.argv[1])


message_dict = {'/' + sys.argv[2] + '/wheels_driver_node/wheels_cmd' : []}

for topic, msg, t in bag.read_messages(topics=['/' + sys.argv[2] + '/wheels_driver_node/wheels_cmd']):
    s = {'vel_left' : str(msg.vel_left), 'vel_right' : str(msg.vel_right),'timestamp' : str(t)}
    message_dict['/' + sys.argv[2] + '/wheels_driver_node/wheels_cmd'].append(s)

message_dict['/' + sys.argv[2] + '/kinematics_node/velocity'] = []

for topic, msg, t in bag.read_messages(topics=['/' + sys.argv[2] + '/kinematics_node/velocity']):
    s = {'v' : str(msg.v), 'omega' : str(msg.omega),'timestamp' : str(t)}
    message_dict['/' + sys.argv[2] + '/kinematics_node/velocity'].append(s)

message_dict['/' + sys.argv[2] + '/camera_node/image/compressed'] = []

for topic, msg, t in bag.read_messages(topics=['/' + sys.argv[2] + '/camera_node/image/compressed']):
    s = {'timestamp' : str(t), 'deserialize' : 'image', 'deserialize_numpy' : 'numpy_image', 'data' : 'garbage'}
    message_dict['/' + sys.argv[2] + '/camera_node/image/compressed'].append(s)

with open(sys.argv[1][:-3]+'json', 'w+') as json_file:
    json.dump(message_dict, json_file, indent=4)

bag.close()