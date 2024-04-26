import cv2
import numpy as np

def draw_square_centers(img, corners, pattern_size):
    centers = []
    for y in range(pattern_size[1] - 1):
        for x in range(pattern_size[0] - 1):
            top_left, top_right, bottom_left, bottom_right = \
                corners[y * pattern_size[0] + x][0], \
                corners[y * pattern_size[0] + (x + 1)][0], \
                corners[(y + 1) * pattern_size[0] + x][0], \
                corners[(y + 1) * pattern_size[0] + (x + 1)][0]
            center = (top_left + top_right + bottom_left + bottom_right) / 4
            centers.append(center)
            center_int = tuple(np.int32(center))
            cv2.circle(img, center_int, radius=5, color=(0, 0, 255), thickness=-1)
    return centers, img

def draw_move_arrow(img, start_square, end_square, centers):
    if start_square is not None and end_square is not None and centers is not None:
        start_point = square_number_to_center_coordinate(start_square, centers)
        end_point = square_number_to_center_coordinate(end_square, centers)
        cv2.arrowedLine(img, start_point, end_point, (0, 255, 0), 2, tipLength=0.01)
    else:
        print("No Squares Detected")

def square_number_to_center_coordinate(square_number, centers):
    center = centers[square_number]
    return int(center[0]), int(center[1])


def infer_outer_centers(centers):
    """
    Infer the centers of the outer squares of the chessboard based on detected inner square centers.
    
    Parameters:
        centers (list): Detected centers of the inner squares.
        
    Returns:
        list: Complete list of centers for all 64 squares of the chessboard.
    """
    centers_np = np.array(centers).reshape((6, 6, 2))
    horizontal_diffs, vertical_diffs = np.diff(centers_np, axis=1), np.diff(centers_np, axis=0)
    avg_horizontal_vector = np.mean(horizontal_diffs, axis=1)
    avg_vertical_vector = np.mean(vertical_diffs, axis=0)
    full_centers = np.zeros((8, 8, 2))
    full_centers[1:-1, 1:-1, :] = centers_np
    full_centers[0, 1:-1, :] = centers_np[0, :, :] - avg_vertical_vector[np.newaxis, 0, :]
    full_centers[-1, 1:-1, :] = centers_np[-1, :, :] + avg_vertical_vector[np.newaxis, -1, :]
    for i in range(1, 7):
        full_centers[i, 0, :] = full_centers[i, 1, :] - avg_horizontal_vector[i-1, :]
        full_centers[i, -1, :] = full_centers[i, -2, :] + avg_horizontal_vector[i-1, :]
    full_centers[0, 0, :] = full_centers[1, 0, :] - avg_vertical_vector[0, :]
    full_centers[0, -1, :] = full_centers[1, -1, :] - avg_vertical_vector[0, :]
    full_centers[-1, 0, :] = full_centers[-2, 0, :] + avg_vertical_vector[-1, :]
    full_centers[-1, -1, :] = full_centers[-2, -1, :] + avg_vertical_vector[-1, :]
    return full_centers.reshape(-1, 2).tolist()

from collections import defaultdict

def validate_chess_pieces(mapped_pieces):
    counts = defaultdict(int)
    for piece, _ in mapped_pieces:
        counts[piece] += 1
    
    errors = {}

    expected_counts = {
        'white_king': 1, 'black_king': 1,
        'white_queen': 1, 'black_queen': 1,
        'white_rook': 2, 'black_rook': 2,
        'white_bishop': 2, 'black_bishop': 2,
        'white_knight': 2, 'black_knight': 2,
        'white_pawn': 8, 'black_pawn': 8
    }

    for piece, expected_count in expected_counts.items():
        if counts[piece] > expected_count:
            errors[piece] = (counts[piece], 'too many')

    for king in ['white_king', 'black_king']:
        if counts[king] != 1:
            errors[king] = (counts[king], 'incorrect number')

    if errors:
        return False, errors
    return True, None

