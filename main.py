import cv2
import time
import math 
from ultralytics import YOLO
from chess_utils import draw_square_centers, draw_move_arrow, square_number_to_center_coordinate, infer_outer_centers
from chess_fen import map_pieces_to_squares, generate_fen_from_mapped_pieces, make_move_and_update_fen, create_board_from_fen, find_difference_in_fen_squares
from chess_api import send_fen_to_server

model = YOLO('best3.pt')
chessboard_size = (7, 7)
cap = cv2.VideoCapture(0)
last_FEN = ""
original_square = None
updated_square = None
last_FEN_time = time.time()
all_centers = None
classNames = [
    "black_bishop",
    "black_king",
    "black_knight",
    "black_pawn",
    "black_queen",
    "black_rook",
    "white_bishop",
    "white_king",
    "white_knight",
    "white_pawn",
    "white_queen",
    "white_rook"
]
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (640,640))
    img_with_centers = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCornersSB(gray, chessboard_size, None)
    results = model.predict(frame, conf=0.73, stream=True)
    
    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        centers, img_with_centers = draw_square_centers(frame, corners2, chessboard_size)
        all_centers = infer_outer_centers(centers)
        
        if len(all_centers) == 64:
            
            piece_square_map = map_pieces_to_squares(results, model, all_centers)
            fen_string = generate_fen_from_mapped_pieces(piece_square_map)
            print(fen_string)
            if last_FEN != "" and fen_string != last_FEN:
                move = send_fen_to_server(fen_string)
                if move:
                    updated_fen = make_move_and_update_fen(create_board_from_fen(fen_string), move)
                    original_square, updated_square = find_difference_in_fen_squares(last_FEN, updated_fen)
                    draw_move_arrow(img_with_centers, original_square, updated_square, all_centers)
                    last_FEN_time = time.time()
            last_FEN = fen_string
    draw_move_arrow(frame, original_square, updated_square, all_centers)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
