class Object:
    def __init__(self, class_name, confidence, pos_x, pos_y, size_x, size_y):
        self.class_name = class_name
        self.confidence = confidence
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
    
    def log(self):
        print("Class name: " + self.class_name)
        print("Confidence: " + str(self.confidence))
        print("Position X: " + str(self.pos_x))
        print("Position Y: " + str(self.pos_y))
        print("Size X: " + str(self.size_x))
        print("Size Y: " + str(self.size_y))