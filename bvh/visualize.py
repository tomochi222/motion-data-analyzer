
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.animation import ArtistAnimation

class Visualize(MotionVariables):
    def __init__(self, file_dir, filename, interval=100, devise="optitrack", re_load=False):
        super().__init__()
        self.motion = Motion(file_dir, filename, devise=devise, re_load=re_load)
        time = np.array(self.motion.get_time())
        time_diff = np.diff(time)
        time_diff_mean = np.mean(time_diff)
        draw_frame = int((interval/1000)/time_diff_mean)
        print("draw_frame : ", draw_frame, "diff time : ", time_diff_mean)

        fig = plt.figure()
        self.ax = Axes3D(fig)
        self.ax.azim = self.motion.motion_variables.azim
        self.ax.elev = self.motion.motion_variables.elev
        self.frames = []
        
        print("Realtime loading plot data ...", end="", flush=True)
        try:
            for i in range(len(self.motion.get_time())):
                if i%100 == 0:
                    print("..", end="", flush=True)
                if i%draw_frame == 0:
                    if i != 0:
                        self.ax.azim = old_azim
                        self.ax.elev = old_elev
                    self.ax.set_xlabel('x')
                    self.ax.set_ylabel('y')
                    self.ax.set_zlabel('z')
                    self.ax.set_xlim([-1.0,1.0])
                    self.ax.set_ylim([0.,2.0])
                    self.ax.set_zlim([-1.0,1.0])
                    for joint in self.motion.get_joint_names():
                        frame = self.set_motion(joint, i, self.motion.motion_variables.scale)
                    plt.pause(float(interval/1000))
                    old_azim = self.ax.azim
                    old_elev = self.ax.elev
                    self.ax.clear()

            print("")
            input("Enter to close")
            plt.close()
            print("end")
        except KeyboardInterrupt:
            plt.close()
            print("KeyboardInterrupt... close figure.")

    def set_motion(self, joint, frame, scale):
        pos = self.motion.get_position(joint, frame, scale)
        parent_pos = self.motion.get_position(self.motion.get_parent(joint), frame, scale)
        vec = [[parent_pos[0], pos[0]],[parent_pos[1], pos[1]],[parent_pos[2], pos[2]]]
        self.ax.plot(vec[0],vec[1],vec[2], "o-", color="#00aa00", ms=4, mew=0.5)

viz = Visualize('./data/','test_optitrack.bvh', interval=100, devise="optitrack", re_load=False)
# viz = Visualize('./data/','test_neuron.bvh', interval=100, devise="perception_neuron", re_load=False)

# class Animation():
