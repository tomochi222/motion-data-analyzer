
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.animation import ArtistAnimation

class Visualize(MotionVariables):
    def __init__(self, file_dir, filename, interval=100):
        super().__init__()
        self.motion = Motion(file_dir, filename)
        time = np.array(self.motion.get_time())
        time_diff = np.diff(time)
        time_diff_mean = np.mean(time_diff)
        draw_frame = int((interval/1000)/time_diff_mean)
        print("draw_frame : ", draw_frame, "diff time : ", time_diff_mean)

        fig = plt.figure()
        self.ax = Axes3D(fig)
        self.frames = []
        
        print("Realtime loading plot data ...", end="", flush=True)
        for i in range(len(self.motion.get_time())):
            if i%100 == 0:
                print("..", end="", flush=True)
            if i%draw_frame == 0:
                for joint in self.motion.get_joint_names():
                    self.ax.set_xlabel('x')
                    self.ax.set_ylabel('y')
                    self.ax.set_zlabel('z')
                    self.ax.set_xlim([-1.0,1.0])
                    self.ax.set_ylim([-1.0,1.0])
                    self.ax.set_zlim([-1.0,1.0])
                    frame = self.set_motion(joint, i, 1)
                plt.pause(float(interval/1000))
                self.ax.clear()

        print("")
        input("Enter to close")
        plt.close()
        print("end")

    def set_motion(self, joint, frame, scale):
        pos = self.motion.get_position(joint, frame, scale)
        parent_pos = self.motion.get_position(self.motion.get_parent(joint), frame, scale)
        vec = [[parent_pos[0], pos[0]],[parent_pos[1], pos[1]],[parent_pos[2], pos[2]]]
        self.ax.plot(vec[0],vec[1],vec[2], "o-", color="#00aa00", ms=4, mew=0.5)

    def set_motion2(self, joint, scale):
        pos = self.motion.get_joint_position(joint, scale)
        parent_pos = self.motion.get_joint_position(self.motion.get_parent(joint), scale)
        vec = [[parent_pos[0], pos[0]],[parent_pos[1], pos[1]],[parent_pos[2], pos[2]]]
        tmp_frame, = self.ax.plot(vec[0],vec[1],vec[2], "o-", color="#00aa00", ms=4, mew=0.5)
        self.frames.append([tmp_frame])

viz = Visualize('./data/','test_optitrack.bvh')

# class Animation():
