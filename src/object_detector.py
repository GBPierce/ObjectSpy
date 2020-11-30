import sys
from cv2 import cv2
import numpy as np
from object import Object


class ObjectDetector:
    def __init__(self, size, confidence_threshold, nms_threshold, class_names, targets, path_model_cfg, path_model_weights):
        # Size of the image captured
        self._size = size
        # Confidence required for neural net to consider an object detected
        self._confidence_threshold = confidence_threshold
        # NMS Threshold
        self._nms_threshold = nms_threshold

        # All class names available
        self._class_names = class_names
        # Targets
        self._targets = targets

        # Create neural net with model config and weights
        self._net = cv2.dnn.readNetFromDarknet(path_model_cfg, path_model_weights)
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # Fetch camera
        self._camera = cv2.VideoCapture(0)

        # Image cache
        self._image = None
        # Found objects cache
        self._objects = None

        # Camera error checking
        if self._camera is None or not self._camera.isOpened():
            print("No video capture devices found, aborting.")
            sys.exit(-1)
    

    # Return either all objects recognized by the neural net or only ones the user specifically targets
    # This method is required to run prior to 'show_objects', "draw_objects", 'get_objects' and 'get_snapshot'
    def find_objects(self, targets_only):
        if targets_only:
            pass
        
        # Get image from camera
        success, self._image = self._camera.read()
        # Error checking
        if not success:
            print("Error retrieving image from camera. Has the camera been disconnected?")
            sys.exit(-2)

        # Convert image to blob for the network
        blob = cv2.dnn.blobFromImage(self._image, 1 / 255, (self._size, self._size), [0, 0, 0], 1, crop=False)

        # Set blob as network input
        self._net.setInput(blob)
        # Extract layers from network
        layer_names = self._net.getLayerNames()
        output_names = [layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]
        outputs = self._net.forward(output_names)

        # Find all object properties
        image_height, image_width, _image_channels = self._image.shape
        bounding_boxes = []
        class_ids = []
        confidence_values = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores) 
                confidenceValue = scores[classID]

                if confidenceValue > self._confidence_threshold:
                    width, height = int(detection[2] * image_width), int(detection[3] * image_height)
                    pos_x, pos_y = int((detection[0] * image_width) - width / 2), int((detection[1] * image_height) - height / 2)

                    bounding_boxes.append([pos_x, pos_y, width, height])
                    class_ids.append(classID)
                    confidence_values.append(float(confidenceValue))

        # Remove all overlapping boxes
        indices = cv2.dnn.NMSBoxes(bounding_boxes, confidence_values, self._confidence_threshold, self._nms_threshold)

        # Clear objects array from previous iteration
        self._objects = []

        # Create object instances from remaining objects
        for i in indices:
            i = i[0]

            class_name = self._class_names[class_ids[i]]
            confidence = int(confidence_values[i] * 100)

            bounding_box = bounding_boxes[i]
            position_x = bounding_box[0]
            position_y = bounding_box[1]
            size_x = bounding_box[2]
            size_y = bounding_box[3]

            object = Object(class_name, confidence, position_x, position_y, size_x, size_y)
            self._objects.append(object)

        # Delay to keep raspberry pi's from blowing up
        cv2.waitKey(1)


    # Draws the found object's bounding boxes, names and confidence levels on the current image
    def draw_objects(self):
        for object in self._objects:
            cv2.rectangle(self._image, (object.pos_x, object.pos_y), (object.pos_x + object.size_x, object.pos_y + object.size_y), (255, 0, 255), 2)
            cv2.putText(self._image, f'{object.class_name.upper()} {object.confidence}%', 
                        (object.pos_x, object.pos_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)


    # Optionally displays the objects found
    def show_objects(self):
        cv2.imshow("Target Detector Live", self._image)


    def get_objects(self):
        return self._objects.copy()

    
    def get_image(self):
        return self._image.copy()