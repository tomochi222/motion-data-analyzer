# -*- coding: utf-8 -*-
## bvh visualizer sample script
from bvh.visualize import Visualize

devise = "optitrack"
# devise = "perception_neuron"
viz = Visualize('./data/','test_optitrack.bvh', interval=100, devise=devise, re_load=False)