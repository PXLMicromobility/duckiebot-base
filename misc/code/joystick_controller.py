#!/usr/bin/env python

"""
Comes from the Duckietown/gym-duckietown repository
This script allows you to manually control the duckiebot
"""

import sys
import pyglet
import rospy
import numpy as np
from sensor_msgs.msg import Joy


class Joyboy:

    def __init__(self):
        self.header = None
        self.msg = Joy()
        self.pub = rospy.Publisher("/greta/joy", Joy, queue_size=1)
        #amount of millisecods of wait between updates
        self.interval = 100 

    def on_joybutton_press(self, joystick, button):
        """
        Event Handler for Controller Button Inputs
        Relevant Button Definitions:
        1 - A - Starts / Stops Recording
        0 - X - Deletes last Recording
        2 - Y - Resets Env.

        Triggers on button presses to control recording capabilities
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
        This function is called at every frame to handle
        movement/stepping and redrawing
        """
        global recording, positions, actions
		
        x = joystick.x
        y = joystick.y

        # No actions took place
        if abs(x) < 0.07 and abs(y) < 0.07:
            return



        self.msg.axes = [0.0, -x, 0.0, -y, 0.0, 0.0, 0.0, 0.0]
        self.pub.publish(self.msg)

if __name__ == "__main__":

    rospy.init_node('joyboi', anonymous=True)

    joyboy = Joyboy()

    pyglet.clock.schedule_interval(joyboy.update, joyboy.interval*0.030)

    # Registers joysticks and recording controls
    joysticks = pyglet.input.get_joysticks()
    assert joysticks, 'No joystick device is connected'
    joystick = joysticks[0]
    joystick.open()
    joystick.push_handlers(joyboy.on_joybutton_press)

    # Enter main event loop
    pyglet.app.run()

    rospy.spin()
