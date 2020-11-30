import os
import time
from object_detector import ObjectDetector
from video_stitcher import VideoStitcher
from noise_maker import NoiseMaker

# Configuration options
SIZE = 320
CONFIDENCE_THRESHOLD = 0.3
NMS_THRESHOLD = 0.3
TIME_RECORDING_MIN = 5 * 60
ALARM = False

# Paths
path_dir = os.path.dirname(__file__)
path_model_cfg = os.path.join(path_dir, "../models/yolov3-tiny.cfg")
path_model_weights = os.path.join(path_dir, "../models/yolov3-tiny.weights")
path_output = os.path.join(path_dir, "../output")
path_sound = os.path.join(path_dir, "../sounds/beep-2.wav")
path_class_names = os.path.join(path_dir, "../coco.names")

# Targets
targets = ["cat", "dog", "bird", "person"]


def load_class_names(path):
    with open(path, 'rt') as file:
        return file.read().rstrip('\n').split('\n')


if __name__ == "__main__":
    class_names = load_class_names(path_class_names)
    object_detector = ObjectDetector(SIZE, CONFIDENCE_THRESHOLD, NMS_THRESHOLD, class_names, targets, path_model_cfg, path_model_weights)
    video_stitcher = VideoStitcher(SIZE, path_output)
    noise_maker = NoiseMaker(path_sound)

    is_recording = False
    recording_time = 0

    while True:
        # Time at the beginning of the frame
        iteration_time = time.time()

        # Find draw and display objects on screen
        object_detector.find_objects(False)
        object_detector.draw_objects()
        object_detector.show_objects()
        
        # Flag to be set when a target was found within all network recognized objects
        target_found = False

        for object in object_detector.get_objects():
            for target in targets:
                if object.class_name == target:
                    #print("Target found! - " + object.class_name)
                    target_found = True

        # If Alarm is desired and target has been found
        if target_found and ALARM:
            noise_maker.play()

        # Toggle recording
        if target_found and not is_recording:
            is_recording = True
        elif not target_found and is_recording and recording_time > TIME_RECORDING_MIN:
            is_recording = False
            recording_time = 0
            video_stitcher.create_video()
            video_stitcher.clear_buffer()


        # Time taken to complete this iteration
        iteration_time = time.time() - iteration_time

        # If we are recording
        if is_recording:
            # Update recording time
            recording_time += iteration_time
            
            # Add new image to video stitcher
            video_stitcher.add_image(object_detector.get_image())