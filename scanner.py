import cv2
import numpy as np


def reorder(points):

    points = points.reshape((4, 2))

    ordered = np.zeros((4, 2), dtype=np.float32)

    s = points.sum(axis=1)

    ordered[0] = points[np.argmin(s)]
    ordered[3] = points[np.argmax(s)]

    d = np.diff(points, axis=1)

    ordered[1] = points[np.argmin(d)]
    ordered[2] = points[np.argmax(d)]

    return ordered


def scan_document(image_path):

    img = cv2.imread(image_path)

    img = cv2.resize(img, (800, 800))

    original = img.copy()

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        30,
        120
    )

    contours, hierarchy = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    largest = max(
        contours,
        key=cv2.contourArea
    )

    perimeter = cv2.arcLength(
        largest,
        True
    )

    approx = cv2.approxPolyDP(
        largest,
        0.02 * perimeter,
        True
    )

    if len(approx) == 4:

        pts1 = reorder(approx)

        width = 800
        height = 800

        pts2 = np.float32([
            [0, 0],
            [width, 0],
            [0, height],
            [width, height]
        ])

        matrix = cv2.getPerspectiveTransform(
            pts1,
            pts2
        )

        warped = cv2.warpPerspective(
            original,
            matrix,
            (width, height)
        )

        warped_gray = cv2.cvtColor(
            warped,
            cv2.COLOR_BGR2GRAY
        )

        scan = cv2.adaptiveThreshold(
            warped_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        output_path = 'static/outputs/scanned.jpg'

        cv2.imwrite(output_path, scan)

        return output_path

    return None