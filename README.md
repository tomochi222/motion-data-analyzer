# Analyze motion capture data
This library support to analyze motion capture data.

## Description

This is a module and sample script for motion data analysis.

## Features

- Easily analyze various motion data
	- Easy to parse
	- Get each joint information
		- joint rotation angle
		- joint rotation vector
		- joint position
	- Visualization
	- Absorb the difference between devices
- Implementing
	- Comparison of data measured simultaneously by different sensors
	- Convert to another supported format and another equipment-like export data

### Support equipment
- Now supporting
	- [Optitrack](http://optitrack.com/)
	- [Perception Neuron](https://www.noitom.com/index.php/solutions/perception-neuron)

### Supporting motion format
- Now supporting
	- BVH (BioVision Hierarchical) file
		- [About BVH (Biovision Hierarchical) format](https://en.wikipedia.org/wiki/Biovision_Hierarchy)
- Future support
	- C3D file
	- FBX
	- TRX
	- CSV

## Installation/Minimum Requirement

	$ pip install git+https://github.com/keit0222/motion-data-analyzer.git

### upgrade library

	$ pip install --upgrade git+https://github.com/keit0222/motion-data-analyzer.git

- python 3.x.x

### example

`$ python example.py`

## Author/Contributors

facebook: [Keita Tomochika](http://www.facebook.com/keita.tomochika)
qiita: [@tomochiii](http://qiita.com/tomochiii)

## License

This software is released under the MIT License, see LICENSE.txt.
