
# coding: utf-8

from motion import Motion

class Visualize(Motion):
    def __init__(self, file_dir, filename):
        super().__init__(file_dir,filename)

viz = Visualize('data\\','Example1.bvh')
print(viz.motion.data)

# class Animation():
