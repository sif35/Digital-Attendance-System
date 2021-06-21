from helpers import FACIAL_LANDMARKS_IDXS
from helpers import shape_to_np
import numpy as np
import cv2


class FaceAligner:
    def __init__(self, predictor, desired_left_eye=(0.35, 0.35),
                 desired_face_width=256, desired_face_height=None):
        # store the facial landmark predictor, desired output left
        # eye position, and desired output face width + height
        self.predictor = predictor
        self.desiredLeftEye = desired_left_eye
        self.desiredFaceWidth = desired_face_width
        self.desiredFaceHeight = desired_face_height
        # if the desired face height is None, set it to be the
        # desired face width (normal behavior)
        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth

    def align(self, image, gray, rect):
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = self.predictor(gray, rect)
        shape = shape_to_np(shape)
        # extract the left and right eye (x, y)-coordinates
        (lStart, lEnd) = FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = FACIAL_LANDMARKS_IDXS["right_eye"]
        left_eye_pts = shape[lStart:lEnd]
        right_eye_pts = shape[rStart:rEnd]

        # compute the center of mass for each eye
        left_eye_center = left_eye_pts.mean(axis=0).astype("int")
        right_eye_center = right_eye_pts.mean(axis=0).astype("int")
        # compute the angle between the eye centroids
        dy = right_eye_center[1] - left_eye_center[1]
        dx = right_eye_center[0] - left_eye_center[0]
        angle = np.degrees(np.arctan2(dy, dx)) - 180

        # compute the desired right eye x-coordinate based on the
        # desired x-coordinate of the left eye
        desired_right_eye_x = 1.0 - self.desiredLeftEye[0]
        # determine the scale of the new resulting image by taking
        # the ratio of the distance between eyes in the *current*
        # image to the ratio of distance between eyes in the
        # *desired* image
        dist = np.sqrt((dx ** 2) + (dy ** 2))
        desired_dist = (desired_right_eye_x - self.desiredLeftEye[0])
        desired_dist *= self.desiredFaceWidth
        scale = desired_dist / dist

        # compute center (x, y)-coordinates (i.e., the median point)
        # between the two eyes in the input image
        eyes_center = ((left_eye_center[0] + right_eye_center[0]) // 2,
                       (left_eye_center[1] + right_eye_center[1]) // 2)
        # grab the rotation matrix for rotating and scaling the face
        m = cv2.getRotationMatrix2D(eyes_center, angle, scale)
        # update the translation component of the matrix
        tx = self.desiredFaceWidth * 0.5
        ty = self.desiredFaceHeight * self.desiredLeftEye[1]
        m[0, 2] += (tx - eyes_center[0])
        m[1, 2] += (ty - eyes_center[1])

        # apply the affine transformation
        (w, h) = (self.desiredFaceWidth, self.desiredFaceHeight)
        output = cv2.warpAffine(image, m, (w, h),
                                flags=cv2.INTER_CUBIC)
        # return the aligned face
        return output
