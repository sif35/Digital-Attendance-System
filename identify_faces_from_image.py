import dlib
import numpy as np
import pickle
import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
import encoding_functions
from face_alignment import FaceAligner
import main_names


class IdentifyImage:
    predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desired_face_width=256)

    with open("Classifier/classifier_mine_knn_32_class_main.clf", 'rb') as f:
        knn_clf = pickle.load(f)

    def __init__(self, path_of_selected_image):

        self.image_path = path_of_selected_image
        
    def show_image(self, face_predictions):

        img = Image.open(self.image_path)
        img = np.array(img.convert("RGB"))

        for face_name, (top_cord, right_cord, bottom_cord, left_cord) in face_predictions:
            # co-ordinates are: (left(1st), top(2nd)) and (right(3rd), bottom(4th))
            # All the addition subtraction are nothing just to place the rectangle nicely
            img = cv2.rectangle(img, (left_cord - 5, bottom_cord + 5), (right_cord + 5, top_cord - 20), (0, 255, 0), 3)
            img = cv2.rectangle(img, (left_cord - 7, bottom_cord + 5),
                                (right_cord + 7, bottom_cord + 20), (0, 255, 0), -1)
            img = cv2.putText(img, face_name, (left_cord - 5, bottom_cord + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 2)

        plt.imshow(img)
        plt.show()
    
    
    def save_faces_from_image(self, face_predictions):

        img = Image.open(self.image_path)
        img = np.array(img.convert("RGB"))

        for files in os.listdir("Students"):
            os.remove(os.path.join("Students", files))

        for name, (top_cord, right_cord, bottom_cord, left_cord) in face_predictions:

            face = img[top_cord:bottom_cord, left_cord:right_cord]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            roll = main_names.name_dict[name][1]

            cv2.imwrite("Students/{}.jpg".format(roll), face)
            
    
    def classify_faces(self):

        face_predictions = []  # To store prediction results
        predicted_name_list = []  # To store predicted names for attendance sheet

        image = Image.open(self.image_path)
        image = np.array(image.convert("RGB"))

        face_bounding_boxes = encoding_functions.face_locations(image)
        landmarks = encoding_functions.raw_face_landmarks(image, image_face_locations=face_bounding_boxes)

        if len(face_bounding_boxes) == 0:
            return []

        encodings = encoding_functions.extract_encodings(image, facial_landmarks=landmarks)

        # Use the KNN model to find the best matches for the test face
        closest_distances = self.knn_clf.kneighbors(encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= 0.6 for i in
                       range(len(face_bounding_boxes))]  # distance_threshold = 0.6

        for pred, loc, rec in zip(self.knn_clf.predict(encodings), face_bounding_boxes, are_matches):

            if rec:
                face_predictions.append((pred, loc))
            else:
                face_predictions.append(("unknown", loc))

        for i in range(len(face_predictions)):
            predicted_name_list.append(face_predictions[i][0])

        return predicted_name_list

        # return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
        # zip(self.knn_clf.predict(encodings), face_bounding_boxes, are_matches)]
