
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

class BioAnalyze(MotionVariables):
    def __init__(self, file_dir, filename, file_dir2='', filename2=''):
        super().__init__()

        self.COMMON_BONE_NAMES = self.get_common_elemants(self.MOTIVE_BONE_NAMES,self.PERCEPTION_NEURON_BONE_NAMES)

        self.motion1 = Motion(file_dir, filename)
        self.motion1.save_to_csv()
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

analysis = BioAnalyze('data\\','test_optitrack.bvh')
# analysis = BioAnalyze('data\\','test_neuron.bvh')
# analysis = BioAnalyze('data\\','test_optitrack.bvh','data\\','test_neuron.bvh')
