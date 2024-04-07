import numpy as np
import chess

def map_pieces_to_squares(results, model, all_centers):
    piece_square_map = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0].cpu().numpy()
            c = box.cls
            bottom_center_x = (b[0] + b[2]) / 2
            bottom_center_y = b[3]
            assigned_square = min(range(len(all_centers)), key=lambda i: np.sqrt((bottom_center_x - all_centers[i][0]) ** 2 + (bottom_center_y - all_centers[i][1]) ** 2))
            piece_square_map.append((model.names[int(c)], assigned_square))
    return piece_square_map

def generate_fen_from_mapped_pieces(piece_square_map):
    board = [[" " for _ in range(8)] for _ in range(8)]
    piece_symbols = {
        'white_king': 'K', 'white_queen': 'Q', 'white_rook': 'R',
        'white_bishop': 'B', 'white_knight': 'N', 'white_pawn': 'P',
        'black_king': 'k', 'black_queen': 'q', 'black_rook': 'r',
        'black_bishop': 'b', 'black_knight': 'n', 'black_pawn': 'p'
    }
    for piece, square in piece_square_map:
        row, col = divmod(square, 8)
        board[row][col] = piece_symbols.get(piece, " ")
    
    fen_rows = []
    for row in board:
        empty = 0
        fen_row = ''
        for cell in row:
            if cell == " ":
                empty += 1
            else:
                if empty > 0:
                    fen_row += str(empty)
                    empty = 0
                fen_row += cell
        if empty > 0:
            fen_row += str(empty)
        fen_rows.append(fen_row)
    
    return "/".join(fen_rows) + " w - - 0 1"

def make_move_and_update_fen(board, move_uci):
    """
    Makes a move on the given board and returns the updated FEN string.
    """
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        return board.fen()
    else:
        return "Illegal move"
    
def create_board_from_fen(fen):
    """
    Creates a chess board from a given FEN string.
    """
    return chess.Board(fen)

def find_difference_in_fen_squares(original_fen, updated_fen):
    """
    Finds the original and new square numbers where the difference between the original and updated FEN occurs.
    Squares are numbered from 0 (top left) to 63 (bottom right).
    """
    original_board = chess.Board(original_fen)
    updated_board = chess.Board(updated_fen)

    original_square = None
    new_square = None

    for square in chess.SQUARES:
        original_piece = original_board.piece_at(square)
        updated_piece = updated_board.piece_at(square)

        if original_piece != updated_piece:
            if original_piece is not None and updated_piece is None:
                original_square = 63 - square
            elif original_piece is None and updated_piece is not None:
                new_square = 63 - square

    return original_square, new_square