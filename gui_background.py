from identify_faces_from_image import IdentifyImage
from attendance_maintain import Attendance
from identify_faces_from_video import IdentifyVideo
import attendance_maintain
from attendance_percentage import Percentage


def classify_image(image_path, attendance_path):

    attendance_update = Attendance(attendance_file_path=attendance_path)
    image_identification = IdentifyImage(path_of_selected_image=image_path)

    face_name_list = image_identification.classify_faces()
    attendance_update.modify_attendance_sheet(face_name_list)


def classify_video(attendance_file_path):

    attendance_update = Attendance(attendance_file_path=attendance_file_path)
    video_identification = IdentifyVideo()

    name_list = video_identification.classify_faces()
    attendance_update.modify_attendance_sheet(name_list)


def create_attendance(path, name):
    attendance_maintain.create_new_attendance_sheet(path, name)


def percentage_works(attendance_file):

    percentage_files = Percentage()
    percentage_files.calculate_percentage_and_update(attendance_file)
