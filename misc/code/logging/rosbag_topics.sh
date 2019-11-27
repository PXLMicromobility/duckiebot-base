#!/bin/bash
# USAGE: record_sensors.sh <duckiebot_name>

if [ -z "$1" ]
  then 
    echo "Need robot name as argument!"
    exit 1
fi

rosrun topic_tools throttle messages /$1/camera_node/image/compressed 1.0 &

sleep 5

rosbag record /$1/camera_node/image/compressed_throttle -o /data/logs/$1_camera &
rosbag record /$1/wheels_driver_node/wheels_cmd -o /data/logs/$1_wheels &
rosbag record /$1/kinematics_node/velocity -o /data/logs/$1_velocity &

wait $!

exit 0