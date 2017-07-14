
# coding: utf-8

import bvh_parser as bp
from coordinate_transform import *

class Motion(object):
    def __init__(self, file_dir, filename):
        self.file_dir = file_dir
        self.filename = filename
        ext = filename.split('.')
        ext = ext[len(ext)-1]
        if ext == 'bvh':
            motion = bp.bvh(file_dir+filename)
        print(motion.data)

# class Animation():
