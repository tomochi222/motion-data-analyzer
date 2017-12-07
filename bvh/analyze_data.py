
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

class BioAnalyze(MotionVariables):
    def __init__(self, file_dir, filename, file_dir2='', filename2='', save_dir="", devise="optitrack", re_load=False, bone_names=None):
        super().__init__()

        if bone_names is None:
            self.COMMON_BONE_NAMES = self.get_common_elements(self.MOTIVE_BONE_NAMES,self.PERCEPTION_NEURON_BONE_NAMES)
        else:
            self.COMMON_BONE_NAMES = bone_names

        self.motion1 = Motion(file_dir, filename, devise, re_load, bone_names=self.COMMON_BONE_NAMES)
        savename = save_dir + filename.split('.')[0] + ".csv"
        self.motion1.save_angle_data_to_csv(savename=savename)
        self.compare_available = False
        if not file_dir2 == '' and  not filename2 == '':
            self.motion2 = Motion(file_dir2, filename2)
            self.compare_available = True
            self.compare_two_data()

    def compare_two_data(self):
        if not self.compare_available == True:
            print('Data to be compared is not set...')
        for joint_name in self.COMMON_BONE_NAMES:
            print(joint_name,len(self.motion1.get_angle(joint_name)),len(self.motion2.get_angle(joint_name)))
            print(self.motion1.get_angle(joint_name),self.motion1.get_axis(joint_name))
            print(self.motion2.get_angle(joint_name),self.motion2.get_axis(joint_name))

    def get_common_bone_names(self):
        return self.COMMON_BONE_NAMES