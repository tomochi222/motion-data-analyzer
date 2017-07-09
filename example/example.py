# coding: utf-8
## bvh parser sample script
from bvh import bvh_parser as bp

if __name__ == "__main__":
	# parse bvh file
	bvh_parser = bp.bvh("Example1.bvh")
	# print first frame motion data
	print(bvh_parser.motions[0])
