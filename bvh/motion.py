
# coding : utf-8

import bvh_parser as bp
from coordinate_transform import *

class Motion(object):
    def __init__(self, file_dir, filename):
        self.file_dir = file_dir
        self.filename = filename

        channels = ['Xposition', 'Yposition', 'Zposition',
                    'Xrotation', 'Yrotation', 'Zrotation']

        ext = filename.split('.')
        ext = ext[len(ext)-1]
        if ext == 'bvh':
            self.motion = bp.bvh(file_dir+filename)
            self.data_size = len(self.motion.data)

        self.add_rotation_info()

    def add_rotation_info(self):
        for joint in self.motion.skeleton:
            order = self.motion.skeleton[joint]['channels']
            mat = []
            for i in range(self.data_size):
                mat.append(np.identity(3))
            for channel in order:
                if 'rotation' in channel:
                    column_name = joint+'-'+channel
                    for j in range(self.data_size):
                        if channel == 'Xrotation':
                            mat[j] = get_rotation_x(deg2rad(self.motion.data[column_name].values[j]))*mat[j]
                        if channel == 'Yrotation':
                            mat[j] = get_rotation_y(deg2rad(self.motion.data[column_name].values[j]))*mat[j]
                        if channel == 'Zrotation':
                            mat[j] = get_rotation_z(deg2rad(self.motion.data[column_name].values[j]))*mat[j]

            degree_list = []
            for one_mat in mat:
                vec,deg = get_rotation_info(one_mat)
                degree_list.append(deg)
            self.motion.data[joint+'-rotation'] = degree_list
        print(self.motion.data)

motion = Motion('data\\','Example1.bvh')
