import cv2
import numpy as np
import time

class Object_Detector(object):
    
    def __init__(self, configPath, weightsPath, labelsPath, confidence=0.5, threshold=0.8):
        #  you'll need at least OpenCV 3.4.2  for dnn module 
        self.configPath = configPath
        self.weightsPath = weightsPath
        self.labelsPath = labelsPath
        self.conf = confidence
        self.thresh = threshold
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        
        self.ln = self.net.getLayerNames()
        # determine only the *output* layer names that we need from YOLO
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
        self.LABELS = open(labelsPath).read().strip().split("\n") # strip() removes leading and trailing whitespaces
#         np.random.seed(42)
#         COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
        return
    
    def detect_object(self, image):
        (H, W) = image.shape[:2]
        cv2.imwrite("readImage.jpg", image)
        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        # show timing information on YOLO
#         print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        boxes = []
        confidences = []
        classIDs = []
        
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.conf:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.conf, self.thresh)
        return idxs, boxes, confidences, classIDs
        # ensure at least one detection exists
    
    def return_tags(self,image):
        
        idxs, boxes, confidences, classIDs = self.detect_object(image)
        if(len(idxs)>0):
            tags = [int(i) for i in idxs.flatten()]
            tags = list(dict.fromkeys(tags))
            names = [self.LABELS[i] for i in tags]
        else:
            names= []
        return set(names)
    
    def add_tags(self, tubes, step=0.1):
        
        for tube in tubes:
            length = len(tube['color_tube'])
            tube['tags'] = set()
            for inc in range(0,1,step):
                frame  = tube['color_tube'][int(length*inc)]
                tube['tags'].union(self.return_tags(frame))
            # print("tags are " + str(tags))
        return tubes

    
    def draw_boxes(self, idxs, boxes, confidences, classIDs, image):
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                print("label is " + text)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.imwrite("Image.jpg", image)
        return
        
    def select_tubes(self, tubes, query): #update function to consider time durations also
        selected = []
        qset = query['tags']
        for tube in tubes:
            tset = tube['tags']
            if(bool(qset.intersection(tset))):
                selected.append(tube)
                # cv2.imshow(str(qset.intersection(tset)), tube['color_tube'][int(0.5*len(tube['color_tube']))])
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        return selected

# example usage
'''
c = "../Yolo/yolov3.cfg"
w = "../Yolo/yolov3.weights"
l = "../Yolo/coco.names"
conf = 0.5
thresh = 0.8
obj = Object_Detector(c,w,l, 0.9)
img = cv2.imread("../Images/run.png")
print(obj.return_tags(img))
idxs, boxes, confidences, classIDs = obj.detect_object(img)
obj.draw_boxes(idxs, boxes, confidences, classIDs, img)
'''
