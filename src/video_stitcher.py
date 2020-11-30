from cv2 import cv2
from datetime import datetime
import os

class VideoStitcher:
    def __init__(self, image_size, path_output):
        self._images = []
        self._image_size = image_size
        self._path_output = path_output


    def add_image(self, image):
        self._images.append(image)


    def create_video(self):
        if not os.path.exists(self._path_output):
            print("Output path does not exist, did you remove an external media device?")
            exit(-3)

        time = datetime.now().strftime("DAY-%d-%m-%Y-AT-%H-%M-%S")
        video_writer = cv2.VideoWriter(os.path.join(self._path_output, time + ".avi"), cv2.VideoWriter_fourcc(*'XVID'), 10.0, (640, 480))
        
        for image in self._images:
            video_writer.write(image)

        video_writer.release()


    # Clears all preexisting images
    def clear_buffer(self):
        self._images = []