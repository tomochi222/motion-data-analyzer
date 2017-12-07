# -*- coding: utf-8 -*-
# parse bvh(BioVision Hierarchical) file for python 3
import re
import pandas as pd
import copy

##################################################
##################################################
class bvh:

##################################################
	def __init__(self, bvh_file = ''):
		if bvh_file == '':
			print('Please set bvh file path and name')
			return 0
		self.bvh_file = bvh_file
		self.current_token = 0
		self.skeleton = {}
		self.bone_context = []
		self.motion_channels = []
		self.motions = []
		self.reserved      = [ "HIERARCHY", "ROOT", "OFFSET", "CHANNELS", "MOTION" ]
		self.channel_names = [ "Xposition", "Yposition", "Zposition",  "Zrotation", "Xrotation",  "Yrotation" ]
		self.joints_channel_names = []
		self.data = 0
		self.df_columns = []

		print(type(self.bone_context))

		scanner = re.Scanner([
		    (r"[a-zA-Z_]\w*", self.identifier),
		    (r"-*[0-9]+(\.[0-9]+)?", self.digit),
			(r"}", self.close_brace),
			(r"{", self.open_brace),
			(r":", None),
		    (r"\s+", None),
		    ])

		bvh_file = open(bvh_file, "r")
		bvh = bvh_file.read()
		bvh_file.close()
		tokens, remainder = scanner.scan(bvh)
		self.parse_hierarchy(tokens)
		self.current_token = self.current_token + 1
		self.parse_motion(tokens)
		self.create_name_for_pandas()
		self.create_dataframe()

##################################################
	def new_bone(self, parent, name):
		bone = { "parent" : parent, "channels" : [], "offsets" : []}
		return bone

##################################################
	def push_bone_context(self, name):
		self.bone_context.append(name)

##################################################
	def get_bone_context(self):
		return self.bone_context[len(self.bone_context)-1]

##################################################
	def pop_bone_context(self):
		self.bone_context = self.bone_context[:-1]
		return self.bone_context[len(self.bone_context)-1]

##################################################
	def identifier(self, scanner, token):  return "IDENT", token
##################################################
	def operator(self, scanner, token):    return "OPERATOR", token
##################################################
	def digit(self, scanner, token):       return "DIGIT", token
##################################################
	def open_brace(self, scanner, token):  return "OPEN_BRACE", token
##################################################
	def close_brace(self, scanner, token): return "CLOSE_BRACE", token

##################################################
	def read_offset(self, bvh, token_index):
		if (bvh[token_index] != ("IDENT", "OFFSET")):
			return None, None
		token_index = token_index + 1
		offsets = [ 0.0 ] * 3
		for i in range(0,3):
			offsets[i] = float(bvh[token_index][1])
			token_index = token_index + 1
		return  offsets, token_index

##################################################
	def read_channels(self, bvh, token_index):
		if (bvh[token_index] != ("IDENT", "CHANNELS")):
			return None, None
		token_index = token_index + 1
		channel_count = int(bvh[token_index][1])
		token_index = token_index+1
		channels = [ "" ] * channel_count
		for i in range(0, channel_count):
			channels[i] = bvh[token_index][1]
			token_index = token_index+1
		return channels, token_index

##################################################
	def parse_joint(self, bvh, token_index):
		end_site = False
		joint_id = bvh[token_index][1]
		token_index = token_index + 1
		joint_name = bvh[token_index][1]
		token_index = token_index + 1
		if (joint_id == "End"): # end site
			joint_name = self.get_bone_context() + "_Nub"
			end_site = True
		joint = self.new_bone(self.get_bone_context(), joint_name)
		if bvh[token_index][0] != "OPEN_BRACE":
			print("Was expecting brace, got ", bvh[token_index])
			return None
		token_index = token_index + 1
		offsets, token_index = self.read_offset(bvh, token_index)
		joint["offsets"] = offsets
		if (not(end_site)):
			channels, token_index = self.read_channels(bvh, token_index)
			joint["channels"] = channels
			for channel in channels:
				self.motion_channels.append((joint_name, channel))
		self.skeleton[joint_name] = joint
		while (((bvh[token_index][0] == "IDENT") and (bvh[token_index][1] == "JOINT")) or
			  ((bvh[token_index][0] == "IDENT") and (bvh[token_index][1] == "End"))):
			self.push_bone_context(joint_name)
			token_index = self.parse_joint(bvh, token_index)
			self.pop_bone_context()
		if (bvh[token_index][0]) == "CLOSE_BRACE":
			return token_index + 1
		print("Unexpected token ", bvh[token_index])

##################################################
	def parse_hierarchy(self, bvh):
		self.current_token = 0
		if (bvh[self.current_token] != ("IDENT", "HIERARCHY")):
			return None
		self.current_token = self.current_token + 1
		if (bvh[self.current_token] != ("IDENT", "ROOT")):
			return None
		self.current_token = self.current_token + 1
		if (bvh[self.current_token][0] != "IDENT"):
			return None
		root_name =bvh[self.current_token][1]
		root_bone = self.new_bone(None, root_name)
		self.current_token = self.current_token + 1
		if bvh[self.current_token][0] != "OPEN_BRACE":
			return None
		self.current_token = self.current_token + 1
		offsets, self.current_token = self.read_offset(bvh, self.current_token)
		channels, self.current_token = self.read_channels(bvh, self.current_token)
		root_bone["offsets"]  = offsets
		root_bone["channels"] = channels
		for channel in channels:
			self.motion_channels.append((root_name, channel))
		self.skeleton[root_name] = root_bone
		self.push_bone_context(root_name)
		while(bvh[self.current_token][1] == "JOINT"):
			self.current_token = self.parse_joint(bvh, self.current_token)

##################################################
	def parse_motion(self, bvh):
		if (bvh[self.current_token][0] != "IDENT"):
			print("Unexpected text")
			return None
		if (bvh[self.current_token][1] != "MOTION"):
			print("No motion section")
			return None
		self.current_token = self.current_token + 1
		if (bvh[self.current_token][1] != "Frames"):
			return None
		self.current_token = self.current_token  + 1
		frame_count = int(bvh[self.current_token][1])
		self.current_token = self.current_token  + 1
		if (bvh[self.current_token][1] != "Frame"):
			return None
		self.current_token = self.current_token  + 1
		if (bvh[self.current_token][1] != "Time"):
			return None
		self.current_token = self.current_token  + 1
		frame_rate = float(bvh[self.current_token][1])
		frame_time = 0.0
		self.motions = [ () ] * frame_count
		print('Parsing now ...')
		self.current_token += 1

		for i in range(0, frame_count):
			channel_values = []
			for channel in self.motion_channels:
				channel_values.append((channel[0], channel[1], float(bvh[self.current_token][1])))
				self.current_token += 1
			self.motions[i] = (frame_time, channel_values)
			frame_time = frame_time + frame_rate
		print('bvh parsing complete !!!!')
##################################################

	def create_name_for_pandas(self):
		motion_data = self.motions[0][1]
		self.df_columns.append('time')
		for joint_name, channel_name, tmp in motion_data:
			tmp_array = [joint_name, channel_name]
			self.joints_channel_names.append(tmp_array)
			tmp_name = joint_name+'-'+channel_name
			self.df_columns.append(tmp_name)

	def create_dataframe(self):
		df_array = []
		tmp_array = []
		motion_data = self.motions[0][1]
		for i in range(len(motion_data)+1):
			tmp_array.append(0)

		for motion_data_array in self.motions:
			tmp_array_copy = copy.deepcopy(tmp_array)
			tmp_array_copy[0] = motion_data_array[0]
			for joint_name, channel_name, tmp in motion_data_array[1]:
				index = self.joints_channel_names.index([joint_name,channel_name])
				tmp_array_copy[index+1] = tmp
			df_array.append(tmp_array_copy)
		self.data = pd.DataFrame(df_array,columns=self.df_columns)
##################################################
