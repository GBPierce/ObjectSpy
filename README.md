# ObjectSpy
Detects, records and produces 5 minute videos of desired objects. \
Optionally plays a desired sound upon object detection until the object exits the camera's fov.

## Dependencies

#### Python
* python 3.8.6

#### Python modules
* opencv-python 4.4.0.46
* numpy 1.19.3
* playsound 1.2.2

#### Models
* configs and weights from https://pjreddie.com/darknet/yolo/
* coco.names file from https://github.com/pjreddie/darknet/blob/master/data/coco.names

## Setup
1. Copy configs and weights into the models folder
2. Copy coco.names file into the project root
3. Copy desired sound file into the sounds folder
4. Alter paths in src/main.py to reflect copied file names
5. Set targets in src/main.py to desired targets from coco.names
6. Make sure you have a camera connected
7. Run src/main.py

#### License
Do whatever you want
