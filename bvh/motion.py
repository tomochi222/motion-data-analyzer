
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
        # print(self.motion.skeleton)
        for joint in self.get_joint_names():
        # for joint in ['LeftToeBase']:
            print('target joint',joint)
            self.joint_hierarchy = self.get_joint_hierarchy(joint)

            mat = []
            for i in range(self.data_size):
                mat.append(np.identity(4))

            for target in self.joint_hierarchy:
                order = self.get_channels(target)
                rotation_check = len([l for l in order if 'rotation' in l])

                rotation_mat_tmp = []
                for i in range(self.data_size):
                    rotation_mat_tmp.append(np.identity(3))

                rotation_order = []
                for channel in order:
                    if 'rotation' in channel:
                        rotation_order.append(target+'-'+channel)

                if rotation_check > 0:
                    for j in range(self.data_size):
                        for tmp in rotation_order:
                            # rotation_mat_tmp[j] = np.dot(get_rotation(tmp[len(tmp)-9],deg2rad(self.motion.data[tmp].values[j])),rotation_mat_tmp[j])
                            rotation_mat_tmp[j] = np.dot(rotation_mat_tmp[j],get_rotation(tmp[len(tmp)-9],deg2rad(self.motion.data[tmp].values[j])))
                        child_joint = self.get_child(target)
                        if child_joint == None:
                            mat[j] = np.dot(get_simultaneous_trans_matrix(rotation_mat_tmp[j],[0.,0.,0.]),mat[j])
                        else:
                            mat[j] = np.dot(get_simultaneous_trans_matrix(rotation_mat_tmp[j],self.get_offsets(child_joint)),mat[j])

                if target == self.get_parent(joint):
                    position_list = []
                    for one_mat in mat:
                        pos = get_position_info(one_mat)
                        position_list.append(pos)

            degree_list = []
            rotation_axis_vec = []
            for one_mat in mat:
                vec,deg = get_rotation_info(one_mat[0:3,0:3])
                degree_list.append(deg)
                rotation_axis_vec.append(vec)
            self.motion.data[joint+'-Rotation'] = degree_list
            self.motion.data[joint+'-Axis'] = rotation_axis_vec
            self.motion.data[joint+'-position'] = position_list

    def get_joint_hierarchy(self,joint):
        joint_hierarchy = [joint]
        # print('target joint : ',joint)
        parent_joint = joint
        while not parent_joint == None:
            parent_joint = self.motion.skeleton[parent_joint]['parent']
            joint_hierarchy.insert(0,parent_joint)
            # print('parent joint : ',parent_joint)
        return joint_hierarchy[1:len(joint_hierarchy)]

    def get_parent(self, child_joint):
        return self.get_joint_hierarchy(child_joint)[len(self.get_joint_hierarchy(child_joint))-2]

    def get_child(self, parent_joint):
        parent_index = self.joint_hierarchy.index(parent_joint)
        if not parent_index == len(self.joint_hierarchy)-1:
            child = self.joint_hierarchy[parent_index+1]
            return child
        else:
            return None

    def get_offsets(self, joint):
        return self.motion.skeleton[joint]['offsets']

    def get_axis(self, joint):
        return self.motion.data[joint+'-Axis'].values

    def get_angle(self, joint):
        return self.motion.data[joint+'-Rotation'].values

    def get_position(self, joint, frame, scale):
        return self.motion.data[joint+'-position'].values[frame]*scale

    def get_joint_names(self):
        joint_names = []
        for joint in self.motion.skeleton:
            joint_names.append(joint)
        return joint_names

    def get_channels(self,joint):
        return self.motion.skeleton[joint]['channels']

    def get_time(self):
        return self.motion.data['time'].values

    def save_to_csv(self):
        self.motion.data.to_csv('tmp.csv')
