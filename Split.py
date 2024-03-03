import cv2
import os

def split_image_into_squares(img_path, output_dir, grid_size=(8, 8)):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    square_height = h // grid_size[0]
    square_width = w // grid_size[1]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            square = img[i*square_height:(i+1)*square_height, j*square_width:(j+1)*square_width]
            square_name = f"{output_dir}/square_{i*grid_size[1]+j}.jpg"
            cv2.imwrite(square_name, square)

#split_image_into_squares('cropped_board.jpg', 'outputs')