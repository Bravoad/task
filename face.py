"""
6.1. Распознавание лиц на фото с камеры видеонаблюдения;

"""
import cv2
import face_recognition
import os
from typing import List, Tuple


def recognize_faces(image_path: str, known_faces_dir: str) -> Tuple[List[Tuple[int, int, int, int]], List[str]]:
    # Загрузка изображения
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Обнаружение лиц
    face_locations: List[Tuple[int, int, int, int]] = face_recognition.face_locations(rgb_image)
    face_encodings: List = face_recognition.face_encodings(rgb_image, face_locations)

    known_face_encodings: List = []
    known_face_names: List[str] = []

    # Загрузка известных лиц
    for name in os.listdir(known_faces_dir):
        for img_file in os.listdir(os.path.join(known_faces_dir, name)):
            known_image = face_recognition.load_image_file(os.path.join(known_faces_dir, name, img_file))
            known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
            known_face_names.append(name)

    # Распознавание лиц
    face_names: List[str] = []
    for face_encoding in face_encodings:
        matches: List[bool] = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name: str = "Unknown"

        if True in matches:
            first_match_index: int = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    return face_locations, face_names

# Пример использования
face_locations, face_names = recognize_faces(input('введите файл:'), input('введите путь к папкам'))
