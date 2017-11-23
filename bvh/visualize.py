
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Visualize(MotionVariables):
    def __init__(self, file_dir, filename):
        super().__init__()
        self.motion = Motion(file_dir, filename)
        fig = plt.figure()
        self.ax = Axes3D(fig)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

        for i in range(len(self.motion.get_time())):
            for joint in self.motion.get_joint_names():
                self.set_motion(joint, i, 1)
            self.ax.set_xlim([-1.0,1.0])
            self.ax.set_ylim([-1.0,1.0])
            self.ax.set_zlim([-1.0,1.0])
            plt.pause(0.008)
            self.ax.clear()

    def set_motion(self, joint, frame, scale):
        pos = self.motion.get_position(joint, frame, scale)
        parent_pos = self.motion.get_position(self.motion.get_parent(joint), frame, scale)
        vec = [[parent_pos[0], pos[0]],[parent_pos[1], pos[1]],[parent_pos[2], pos[2]]]
        self.ax.plot(vec[0],vec[1],vec[2], "o-", color="#00aa00", ms=4, mew=0.5)

    def set_motion2(self, joint, scale):
        pos = self.motion.get_joint_position(joint, scale)
        parent_pos = self.motion.get_joint_position(self.motion.get_parent(joint), scale)
        vec = [[parent_pos[0], pos[0]],[parent_pos[1], pos[1]],[parent_pos[2], pos[2]]]
        self.ax.plot(vec[0],vec[1],vec[2], "o-", color="#00aa00", ms=4, mew=0.5)

viz = Visualize('./data/sample/','traverse_gentleslope_go_assist_1.bvh')

# class Animation():
