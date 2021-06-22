import cv2
import dlib
import encoding_functions
import pickle


class IdentifyVideo:

    with open("Classifier/Classifier_Model.clf", 'rb') as f:
        knn_clf = pickle.load(f)

    def __init__(self):
        pass

    def classify_face_for_video(self, image):

        face_name = "Unknown"

        face_bounding_boxes = encoding_functions.face_locations(image)
        landmarks = encoding_functions.raw_face_landmarks(image, image_face_locations=face_bounding_boxes)

        if len(face_bounding_boxes) == 0:
            return "Unknown"

        encodings = encoding_functions.extract_encodings(image, facial_landmarks=landmarks)

        # Use the KNN model to find the best matches for the test face
        closest_distances = self.knn_clf.kneighbors(encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= 0.6 for i in
                       range(len(face_bounding_boxes))]  # distance_threshold = 0.6

        for pred, loc, rec in zip(self.knn_clf.predict(encodings), face_bounding_boxes, are_matches):

            if rec:
                face_name = pred
            else:
                face_name = "Unknown"

        return face_name

    def classify_faces(self):

        face_detector = dlib.get_frontal_face_detector()

        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        face_name_list = []
        while True:
            ret, frame = capture.read()

            faces = face_detector(frame, 1)

            for face in faces:
                left = face.left()
                top = face.top()
                right = face.right()
                bottom = face.bottom()

                width = right - left
                height = bottom - top

                image_crop = frame[top:top + height, left:left + width]

                face_name = (self.classify_face_for_video(image_crop))
                face_name_list.append(face_name)

                cv2.rectangle(frame, (left - 5, bottom + 5), (right + 5, top - 20), (0, 255, 0), 3)
                cv2.rectangle(frame, (left - 7, bottom + 5),
                              (right + 7, bottom + 20), (0, 255, 0), -1)
                cv2.putText(frame, face_name, (left - 5, bottom + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 255), 2)

            cv2.imshow("Live Camera", frame)

            if cv2.waitKey(100) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return face_name_list
