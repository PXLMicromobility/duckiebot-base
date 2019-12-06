#!/usr/bin/env python

"""
Comes from the Duckietown/gym-duckietown repository
This script allows you to manually control the duckiebot using a joystick

"""

import sys, signal
import pyglet
import rospy
import numpy as np

from functools import partial
from sensor_msgs.msg import Joy


jb = None

class Joyboy:

    def __init__(self):
        self.header = None
        self.msg = Joy()
        self.pub = rospy.Publisher("/greta/joy", Joy, queue_size=1)
        #amount of millisecods of wait between updates
        self.interval = 30
        self.stopped = True

    def on_joybutton_press(self, joystick, button):
        """
        Event Handler for Controller Button Inputs
        Relevant Button Definitions:
        """
        global recording, positions, actions

        # A Button
        if button == 1:
            print('A')

        # X Button
        elif button == 0:
            print('X')

        # Y Button
        elif button == 3:
            print('Y')

        # Any other button thats not boost prints help
        elif button != 5:
            helpstr1 = "A - Starts / Stops Recording\nX - Deletes last Recording\n"
            helpstr2 = "Y - Resets Env.\nRB - Hold for Boost"

            print("Help:\n{}{}".format(helpstr1, helpstr2))

    def update(self, dt):
        """
        This function is called at every frame to handle movement
        """
		
        x = joystick.y
        y = joystick.x * 0.5

        # No actions took place
        if abs(x) < 0.07 and abs(y) < 0.07:
            if self.stopped:
                return
            else:
                self.msg.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                self.stopped = True
                self.pub.publish(self.msg)
                return

        
        self.stopped = False
        self.msg.axes = [0.0, -x, 0.0, -y, 0.0, 0.0, 0.0, 0.0]
        self.pub.publish(self.msg)

def on_close(sig, frame):
    print("Closing")
    stop_message = Joy()
    stop_message.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    jb.pub.publish(stop_message)
    rospy.signal_shutdown("Closed")
    pyglet.app.exit()
    sys.exit()


if __name__ == "__main__":

    rospy.init_node('joyboi', anonymous=True)

    joyboy = Joyboy()
    jb = joyboy

    signal.signal(signal.SIGINT, on_close)

    pyglet.clock.schedule_interval(joyboy.update, joyboy.interval*0.01)

    # Registers joysticks and recording controls
    joysticks = pyglet.input.get_joysticks()
    assert joysticks, 'No joystick device is connected'
    joystick = joysticks[0]
    joystick.open()
    joystick.push_handlers(joyboy.on_joybutton_press)

    # Enter main event loop
    pyglet.app.run()
    rospy.spin()
