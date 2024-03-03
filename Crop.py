import cv2
import numpy as np
import os

def crop_chessboard(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    board_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            board_contour = cnt

    x, y, w, h = cv2.boundingRect(board_contour)

    margin = int(min(w, h) * 0.025)  
    cropped_image = image[y+margin:y+h-margin, x+margin:x+w-margin]

    cv2.imwrite('cropped_board.jpg', cropped_image)

image_path = 'transformed_chessboard.jpg'

crop_chessboard(image_path)