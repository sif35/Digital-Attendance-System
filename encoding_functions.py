import cv2
import dlib
import numpy as np
from face_alignment import FaceAligner

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = "models/shape_predictor_68_face_landmarks.dat"
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = "models/shape_predictor_5_face_landmarks.dat"
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)

face_recognition_model = "models/dlib_face_recognition_resnet_model_v1.dat"
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

cnn_model = "models/mmod_human_face_detector.dat"
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_model)

fa = FaceAligner(pose_predictor_68_point, desired_face_width=256)


def rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()


def css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


def raw_face_locations(img, number_of_times_to_upsample=1, model="hog"):
    if model == "cnn":
        return cnn_face_detector(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


def face_locations(img, number_of_times_to_upsample=1, model="hog"):
    if model == "cnn":
        return [trim_css_to_bounds(rect_to_css(face.rect), img.shape) for face in
                raw_face_locations(img, number_of_times_to_upsample, "cnn")]
    else:
        return [trim_css_to_bounds(rect_to_css(face), img.shape) for face in
                raw_face_locations(img, number_of_times_to_upsample, model)]


def raw_face_landmarks(face_image, image_face_locations=None, model="large"):
    image_face_locations = [css_to_rect(face_location) for face_location in image_face_locations]

    pose_predictor = pose_predictor_68_point

    if model == "small":
        pose_predictor = pose_predictor_5_point

    return [pose_predictor(face_image, face_location) for face_location in image_face_locations]


def extract_encodings(face_image, facial_landmarks, num_of_jitters=1, model="large"):
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_of_jitters)) for
            raw_landmark_set in facial_landmarks]


def face_locations_with_alignment(image_with_faces, model="hog"):
    face_list = []

    if model == "cnn":
        face_rects = cnn_face_detector(image_with_faces, 1)
        for rect in face_rects:

            aligned_face = fa.align(image_with_faces, cv2.cvtColor(image_with_faces, cv2.COLOR_BGR2GRAY), rect)
            face = cnn_face_detector(aligned_face, 1)

            for r in face:
                face_list.append(trim_css_to_bounds(rect_to_css(r), image_with_faces.shape))

    else:
        face_rects = face_detector(image_with_faces, 2)
        for rect in face_rects:

            aligned_face = fa.align(image_with_faces, cv2.cvtColor(image_with_faces, cv2.COLOR_BGR2GRAY), rect)
            face = face_detector(aligned_face, 1)

            for r in face:
                face_list.append(trim_css_to_bounds(rect_to_css(r), image_with_faces.shape))

    return face_list
