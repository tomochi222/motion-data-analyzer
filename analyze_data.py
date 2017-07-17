
# coding: utf-8

from motion import Motion
from motion_variables import MotionVariables

class BioAnalyze(MotionVariables):
    def __init__(self, file_dir, filename, file_dir2='', filename2=''):
        super().__init__()
        self.motion1 = Motion(file_dir, filename)
        self.compare_available = False
        if not file_dir2 == '' and  not filename2 == '':
            self.motion2 = Motion(file_dir2, filename2)
            self.compare_available = True

    def compare_two_data():
        if not self.compare_available == True:
            print('Data to be compared is not set...')
