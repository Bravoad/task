"""

6.2. Распознавание автомобильных номеров на фото с камеры видеонаблюдения;


"""
import cv2
import easyocr
from typing import Optional


def recognize_license_plate(image_path: str) -> Optional[str]:
    # Загрузка изображения
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Обнаружение контуров
    contours, _ = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    plate_contour = None

    # Нахождение контура номерного знака
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2 < aspect_ratio < 5:
            plate_contour = contour
            break

    if plate_contour is None:
        return None

    x, y, w, h = cv2.boundingRect(plate_contour)
    plate_image = gray_image[y:y + h, x:x + w]

    # Распознавание текста
    reader = easyocr.Reader(['en'])
    result = reader.readtext(plate_image)

    if len(result) > 0:
        return result[0][-2]
    else:
        return None


license_plate = recognize_license_plate(input('Введите файл с номером машины'))
