
# coding: utf-8

class MotionVariables(object):
    def __init__(self):
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

    def get_common_elemants(self, list1, list2):
        matched_list = []
        for element1 in list1:
            matched_list+=filter(lambda element2: element2 == element1, list2)
        return matched_list
