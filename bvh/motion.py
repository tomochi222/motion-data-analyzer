
# coding : utf-8

import bvh_parser as bp
from coordinate_transform import *

try:
    from graphviz import Digraph
except:
    print("Can't import graphviz. graphviz is not existance")
from collections import defaultdict
from pprint import pprint

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

        # self.export_joint_hierarchy()
        # self.get_joint_info(0)
        # self.add_rotation_info()


    def get_joint_info(self, frame):
        self.get_joint_hierarchy_tree()
        self.joint_info_mat = defaultdict(list)
        self.joint_info = defaultdict(list)
        self.get_joint_info_matrix(self.joint_hierarchy_tree, frame)
        self.pos_dict = {}
        self.extract_joint_position()

    def extract_joint_position(self):
        for joint in self.joint_info:
            mat = dict(self.joint_info)[joint][0]
            self.pos_dict[joint] = get_position_info(mat)

    def get_joint_info_matrix(self, joint_tree, frame):
        for target in joint_tree:
            # print('target',target)

            #
            self.joint_hierarchy = self.get_joint_hierarchy(target)

            # 処理のコード
            # Check order list have 'Rotation' information
            order = self.get_channels(target)
            rotation_check = len([l for l in order if 'rotation' in l])

            # Initialize transformation matrix
            rotation_mat_tmp = np.identity(3)
            mat_tmp = np.identity(4)
            mat = np.identity(4)

            # Get rotation order information for target joint
            rotation_order = []
            for channel in order:
                if 'rotation' in channel:
                    rotation_order.append(target+'-'+channel)

            # Prepare simultaneous transformation matrix for target joint
            if any(('rotation' in x for x in order)) == True:
                for tmp in rotation_order:
                    rotation_mat_tmp = np.dot(get_rotation(tmp[len(tmp)-9],deg2rad(self.motion.data[tmp].values[frame])),rotation_mat_tmp)

            mat_tmp = np.dot(get_simultaneous_matrix(rotation_mat_tmp,self.get_offsets(target)),mat_tmp)
            self.joint_info_mat[target].append([mat_tmp])

            for joint in self.joint_hierarchy:
                mat = np.dot(dict(self.joint_info_mat)[joint][0][0],mat)
            self.joint_info[target].append(mat)

            self.get_joint_info_matrix(joint_tree[target],frame)

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
                            rotation_mat_tmp[j] = np.dot(get_rotation(tmp[len(tmp)-9],deg2rad(self.motion.data[tmp].values[j])),rotation_mat_tmp[j])
                            # rotation_mat_tmp[j] = np.dot(rotation_mat_tmp[j],get_rotation(tmp[len(tmp)-9],deg2rad(self.motion.data[tmp].values[j])))
                        child_joint = self.get_child(target)
                        if child_joint == None:
                            # mat[j] = np.dot(get_simultaneous_trans_matrix([0.,0.,0.]),mat[j])
                            mat[j] = np.dot(get_simultaneous_matrix(rotation_mat_tmp[j],[0.,0.,0.]),mat[j])
                        else:
                            # mat[j] = np.dot(get_simultaneous_trans_matrix(self.get_offsets(child_joint)),mat[j])
                            mat[j] = np.dot(get_simultaneous_matrix(rotation_mat_tmp[j],self.get_offsets(child_joint)),mat[j])

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

    def get_joint_hierarchy_tree(self):
        self.joint_hierarchy_tree = self.tree()
        added_pair = []
        for joint in self.get_joint_names():
            hierarchy = self.get_joint_hierarchy(joint)
            self.add(self.joint_hierarchy_tree, hierarchy)
        self.joint_hierarchy_tree = self.dicts(self.joint_hierarchy_tree)
        # pprint(self.joint_hierarchy_tree)

    def tree(self):
        return defaultdict(self.tree)

    def add(self,t, keys):
        for key in keys:
            t = t[key]

    def dicts(self,t):
        return {k: self.dicts(t[k]) for k in t}

    def print_dict_keys(self, t):
        for key in t:
            if t[key] == {}:
                print(key,t[key])
            self.print_dict_keys(t[key])

    def get_joint_hierarchy(self,joint):
        joint_hierarchy = [joint]
        # print('target joint : ',joint)
        parent_joint = joint
        while not parent_joint == None:
            parent_joint = self.motion.skeleton[parent_joint]['parent']
            joint_hierarchy.insert(0,parent_joint)
            # print('parent joint : ',parent_joint)
        return joint_hierarchy[1:len(joint_hierarchy)]

    def export_joint_hierarchy(self,export_name='joint_hierarchy'):
        # formatはpngを指定(他にはPDF, PNG, SVGなどが指定可)
        G = Digraph(format='png') #　有向グラフ初期化
        G.attr('node', shape='circle') # ノードの形

        added_pair = []
        # ノードの追加
        for joint in self.get_joint_names():
            G.node(joint, joint) # ノード作成
        # 辺の追加
        for joint in self.get_joint_names():
            hierarchy = self.get_joint_hierarchy(joint)
            for i in range(len(hierarchy)-1):
                if any((x == [hierarchy[i],hierarchy[i+1]] for x in added_pair)) == False:
                    G.edge(hierarchy[i],hierarchy[i+1])
                    added_pair.append([hierarchy[i],hierarchy[i+1]])
        G.render(export_name)

    def get_parent(self, child_joint):
        return self.get_joint_hierarchy(child_joint)[len(self.get_joint_hierarchy(child_joint))-2]

    def get_child(self, parent_joint):
        parent_index = self.joint_hierarchy.index(parent_joint)
        print(self.joint_hierarchy,'parent index', parent_index)
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

    def get_joint_position(self, joint, scale):
        return self.pos_dict[joint]*scale

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
