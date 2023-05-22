import os
import PIL.Image
import dlib
import numpy as np
from PIL import ImageFile
from sklearn import neighbors
import cv2
import math
import pickle
import encoding_functions

ImageFile.LOAD_TRUNCATED_IMAGES = True

print("[INFO] Loading face detector and recognition models...")
face_detector = dlib.get_frontal_face_detector()

protoPath = "./face_detection_model/deploy.prototxt"
modelPath = "./face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

predictor_68_point_model = "models/shape_predictor_68_face_landmarks.dat"
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = "models/shape_predictor_5_face_landmarks.dat"
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

cnn_face_detection_model = "models/mmod_human_face_detector.dat"
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

face_recognition_model = "models/dlib_face_recognition_resnet_model_v1.dat"
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

Dataset_dir = "./Augmented Dataset"

encodings_array = []
class_names = []

bounding_boxes = list()
facial_landmarks = list()

number_of_images = 0
print("[INFO] Extracting face encodings...")
for classes in os.listdir(Dataset_dir):

    class_name = classes
    classes = os.path.join(Dataset_dir, classes)
    print("[INFO] Encoding class {}...".format(class_name))

    for (i, image_path) in enumerate(os.listdir(classes)):
        image_path = os.path.join(classes, image_path)

        image = PIL.Image.open(image_path)
        img = np.array(image.convert("RGB"))

        face_bounding_boxes = encoding_functions.face_locations(img)
        landmarks = encoding_functions.raw_face_landmarks(img, image_face_locations=face_bounding_boxes)

        if len(face_bounding_boxes) != 1:
            # If there are no people (or too many people) in a training image, skip the image.
            print("Image {} not suitable for training: {}".format(image_path, "Didn't find a face" if len(
                face_bounding_boxes) < 1 else "Found more than one face"))
        else:
            # Add face encoding for current image to the training set
            encodings_array.append(encoding_functions.extract_encodings(img, facial_landmarks=landmarks)[0])
            class_names.append(class_name)

        number_of_images = i + number_of_images + 1

print(f'[INFO] Number of faces encoded: {len(encodings_array)}')
print(f'[INFO] Number of images: {number_of_images}')

print("[INFO] Saving face encodings...")
with open("Face Encodings/encodings_main_32_class.pkl", "wb") as f:
    pickle.dump(encodings_array, f)
with open("Face Encodings/class_names_main_32_class.pkl", "wb") as f:
    pickle.dump(class_names, f)
