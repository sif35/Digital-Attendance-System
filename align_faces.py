from face_alignment import FaceAligner
import numpy as np
import cv2
import dlib
import os

print("[INFO] Loading Detector and Face Aligner...")
protoPath = "D:/3-2_Project/Demo/Face-Recognition-OpenCV-Facenet/face_detection_model/deploy.prototxt"
modelPath = "D:/3-2_Project/Demo/Face-Recognition-OpenCV-Facenet/face_detection_model/res10_300x300_ssd_iter_140000" \
            ".caffemodel "
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desired_face_width=256)


def face_aligning(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (h, w) = image.shape[:2]

    image_blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(image_blob)
    detections = detector.forward()

    if len(detections) > 0:
        # we're making the assumption that each image has only ONE
        # face, so find the bounding box with the largest probability
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        # ensure that the detection with the 50% probabilty thus helping filter out weak detections
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI and grab the ROI dimensions
            # face = image[startY:endY, startX:endX]
            # (fH, fW) = face.shape[:2]
            face_aligned = fa.align(image, gray, dlib.rectangle(startX, startY, endX, endY))
            return face_aligned


def face_aligning_from_dataset(dataset, aligned_dataset):

    if len(os.listdir(dataset)) is None:
        print("[ERROR: No Class] At least one class should be present in a dataset. Try aligning using class")
        return

    for class_name in os.listdir(dataset):
        # aligned_image_class_path = os.path.join(aligned_dataset, class_name)
        image_class_path = os.path.join(dataset, class_name)

        face_aligning_from_class(class_name, image_class_path, aligned_dataset)


def face_aligning_from_class(class_name, class_path, aligned_class_path):
    aligned_class_path = os.path.join(aligned_class_path, class_name)
    if os.path.isdir(aligned_class_path) is False:
        os.mkdir(aligned_class_path)

    for (i, image_path) in enumerate(os.listdir(class_path)):

        image_path = os.path.join(class_path, image_path)
        aligned_image_path = os.path.join(aligned_class_path, f'{class_name} - {i + 1}.jpg')

        img = cv2.imread(image_path)

        aligned_face = face_aligning(img)
        if aligned_face is None:
            print(f"No face found at {image_path}")
            continue
        cv2.imwrite(aligned_image_path, aligned_face)


if __name__ == "__main__":
    print("[INFO] Aligning Faces...")
    Dataset = "Dataset"
    align_dataset = "Aligned Dataset"
    # face_aligning_from_dataset(Dataset, align_dataset)
    face_aligning_from_class("Pranta", "Dataset/Pranta", align_dataset)
