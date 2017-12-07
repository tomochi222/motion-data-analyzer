# -*- coding: utf-8 -*-

from coordinate_transform import *
import numpy as np

class MotionVariables(object):
    def __init__(self, devise="optitrack"):
        self.devise = devise
        self.devise_list = ["optitrack", "perception_neuron"]

        if self.devise in self.devise_list:
            if self.devise == "optitrack":
                # self.coordinate_trans_mat = get_simultaneous_rotation_matrix(get_rotation_x(np.pi/2))
                self.scale = 1.0
                self.azim = -90
                self.elev = 113
            elif self.devise == "perception_neuron":
                # self.coordinate_trans_mat = get_simultaneous_rotation_matrix(get_rotation_x(np.pi/2))        
                self.scale = 1/100
                self.azim = 90
                self.elev = -66.5
        else:
            print("Currently your sellect devise is not supporting")
            exit()

        self.MOTIVE_BONE_NAMES = ['Hips', 'Spine', 'Spine1', 'Neck', 'Head',
                             'LeftShoulder', 'LeftArm', 'LeftForeArm',
                             'LeftHand', 'RightShoulder', 'RightArm',
                             'RightForeArm', 'RightHand', 'LeftUpLeg',
                             'LeftLeg', 'LeftFoot', 'LeftToeBase',
                             'RightUpLeg', 'RightLeg', 'RightFoot',
                             'RightToeBase']

        self.PERCEPTION_NEURON_BONE_NAMES = ['Hips','RightUpLeg','RightLeg',
                                             'RightFoot','LeftUpLeg','LeftLeg',
                                             'LeftFoot','Spine','Spine1',
                                             'Spine1','Spine2','Spine3',
                                             'Neck','Head','RightShoulder',
                                             'RightArm','RightForeArm',
                                             'RightHand','RightHandThumb1',
                                             'RightHandThumb2','RightHandThumb3',
                                             'RightInHandIndex','RightHandIndex1',
                                             'RightHandIndex2','RightHandIndex3',
                                             'RightInHandMiddle','RightHandMiddle1',
                                             'RightHandMiddle2','RightHandMiddle3',
                                             'RightInHandRing','RightHnadRing1',
                                             'RightHandRing2','RightHandRing3',
                                             'RightInHandPinky','RightHandPinky1',
                                             'RightHandPinky2','RightHandPinky3',
                                             'LeftShoulder','LeftArm','LeftForeArm',
                                             'LeftHand','LeftHandThumb1',
                                             'LeftHandThumb2','LeftHandThumb3',
                                             'LeftInHandIndex','LeftHandIndex1',
                                             'LeftHandIndex2','LeftHandIndex3',
                                             'LeftInHandMiddle','LeftHandMiddle1',
                                             'LeftHandMiddle2','LeftHandMiddle3',
                                             'LeftInHandRing','LeftHnadRing1',
                                             'LeftHandRing2','LeftHandRing3',
                                             'LeftInHandPinky','LeftHandPinky1',
                                             'LeftHandPinky2','LeftHandPinky3',]

    def get_common_elements(self, list1, list2):
        matched_list = []
        for element1 in list1:
            matched_list+=filter(lambda element2: element2 == element1, list2)
        return matched_list
