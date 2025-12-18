from Bots.ChessBotList import register_chess_bot

import random

class Pieces:
    none = 0

    king = 1
    pawn = 2
    knight = 3
    bishop = 4
    rook = 5
    queen = 6

    white = 8
    black = 16

class Move:
    def __init__(self, start_square, target_square):
        self.start_square = start_square
        self.target_square = target_square

def load_from_string(board):
    squares = [tuple()] * 64
    for y in range(8):
        for x in range(8):
            symbol = board[y][x]
            index = (7 - y) * 8 + (7 - x)
            if symbol == "":
                squares[index] = Pieces.none, Pieces.none
            else:
                color = Pieces.white if symbol[1] == "w" else Pieces.black
                piece = MoveUtils.piece_type_from_symbol.get(symbol[0])
                squares[index] = piece, color
    return squares

def precompute_move_data():
    num_square_to_edge = [None] * 64
    for file in range(8):
        for rank in range(8):
            num_up = 7 - rank
            num_down = rank
            num_left = file
            num_right = 7 - file
            square_index = rank * 8 + file

            num_square_to_edge[square_index] = [
                num_up,  # 0: up
                num_down,  # 1: down
                num_left,  # 2: left
                num_right,  # 3: right
                min(num_up, num_left),  # 4: up_left
                min(num_down, num_left),  # 5: down_left
                min(num_up, num_right),  # 6: up_right
                min(num_down, num_right),  # 7: down_right
            ]
    return num_square_to_edge

class MoveUtils:
    direction_offsets = [8, -8, -1, 1, 7, -9, 9, -7]

    num_squares_to_edges = precompute_move_data()

    piece_type_from_symbol = {
        "k": Pieces.king,
        "q": Pieces.queen,
        "n": Pieces.knight,
        "b": Pieces.bishop,
        "r": Pieces.rook,
        "p": Pieces.pawn,
    }

    up = 8
    down = -8
    left = -1
    right = 1
    up_left = 7
    up_right = 9
    down_left = -9
    down_right = -7

def get_pawn_directions(player_sequence) -> dict[int, int]:
    """
    player_sequence
        0w0 : 
        - 0 = ID de l'équipe
        - w = couleur : white
        - 0 = orientation du plateau
    
        1b2
        - 1 = ID de l'équipe
        - b = couleur : black
        - 2 = orientation du plateau
    
    orientation
        '0': White Down (-8), Black Up (+8)
        '2': White Up (+8), Black Down (-8) (Assumed standard)
    """
    orientation = player_sequence[2]
    if orientation == "0":
        return {Pieces.white: MoveUtils.down, Pieces.black: MoveUtils.up}
    else:
        return {Pieces.white: MoveUtils.up, Pieces.black: MoveUtils.down}

def generate_pawn_moves(squares, start_square, piece, pawn_directions):
    moves = list()
    piece_type, piece_color = piece
    (
        max_up,
        max_down,
        max_left,
        max_right,
        max_up_left,
        max_down_left,
        max_up_right,
        max_down_right,
    ) = MoveUtils.num_squares_to_edges[start_square]
    direction = pawn_directions[piece_color]

    if direction == MoveUtils.down:
        # Down (Move)
        if max_down > 0:
            target_square = start_square + MoveUtils.down
            target_piece, target_color = squares[target_square]
            if target_piece == Pieces.none:
                moves.append(Move(start_square, target_square))
        # Down-Left (Capture)
        if max_down_left > 0:
            target_square = start_square + MoveUtils.down_left
            target_piece, target_color = squares[target_square]
            if target_piece != Pieces.none and target_color != piece_color:
                moves.append(Move(start_square, target_square))
        # Down-Right (Capture)
        if max_down_right > 0:
            target_square = start_square + MoveUtils.down_right
            target_piece, target_color = squares[target_square]
            if target_piece != Pieces.none and target_color != piece_color:
                moves.append(Move(start_square, target_square))

    elif direction == MoveUtils.up:
        # Up (Move)
        if max_up > 0:
            target_square = start_square + MoveUtils.up
            target_piece, target_color = squares[target_square]
            if target_piece == Pieces.none:
                moves.append(Move(start_square, target_square))
        # Up-Left (Capture)
        if max_up_left > 0:
            target_square = start_square + MoveUtils.up_left
            target_piece, target_color = squares[target_square]
            if target_piece != Pieces.none and target_color != piece_color:
                moves.append(Move(start_square, target_square))
        # Up-Right (Capture)
        if max_up_right > 0:
            target_square = start_square + MoveUtils.up_right
            target_piece, target_color = squares[target_square]
            if target_piece != Pieces.none and target_color != piece_color:
                moves.append(Move(start_square, target_square))

    return moves

def generate_king_moves(squares, start_square, piece):
    moves = list()
    piece_type, piece_color = piece

    for i in range(8):
        max_steps = MoveUtils.num_squares_to_edges[start_square][i]
        if max_steps > 0:
            target = start_square + MoveUtils.direction_offsets[i]
            target_piece, target_color = squares[target]
            if target_color != piece_color:
                moves.append(Move(start_square, target))
    return moves

def generate_knight_moves(squares, start_square, piece):
    moves = list()
    piece_type, piece_color = piece
    max_up, max_down, max_left, max_right = MoveUtils.num_squares_to_edges[
        start_square
    ][:4]

    # big : up-left (2 left, 1 up)
    if max_left >= 2 and max_up >= 1:
        target_square = start_square - 2 + MoveUtils.up
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # big : up-right (2 right, 1 up)
    if max_right >= 2 and max_up >= 1:
        target_square = start_square + 2 + MoveUtils.up
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # big : down-left (2 left, 1 down)
    if max_left >= 2 and max_down >= 1:
        target_square = start_square - 2 + MoveUtils.down
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # big : down-right (2 right, 1 down)
    if max_right >= 2 and max_down >= 1:
        target_square = start_square + 2 + MoveUtils.down
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # small : up-left (1 left, 2 up)
    if max_left >= 1 and max_up >= 2:
        target_square = start_square - 1 + 2 * MoveUtils.up
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # small : up-right (1 right, 2 up)
    if max_right >= 1 and max_up >= 2:
        target_square = start_square + 1 + 2 * MoveUtils.up
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # small : down-left (1 left, 2 down)
    if max_left >= 1 and max_down >= 2:
        target_square = start_square - 1 + 2 * MoveUtils.down
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    # small : down-right (1 right, 2 down)
    if max_right >= 1 and max_down >= 2:
        target_square = start_square + 1 + 2 * MoveUtils.down
        target_piece, target_color = squares[target_square]
        if target_color != piece_color:
            moves.append(Move(start_square, target_square))

    return moves

def generate_sliding_moves(squares, start_square, piece):
    moves = list()
    piece_type, piece_color = piece

    start_dir_index = 0
    end_dir_index = 0

    match piece_type:
        case Pieces.bishop:
            start_dir_index = 4
            end_dir_index = 7
        case Pieces.rook:
            start_dir_index = 0
            end_dir_index = 3
        case Pieces.queen:
            start_dir_index = 0
            end_dir_index = 7

    for direction_index in range(start_dir_index, end_dir_index + 1):
        for n in range(MoveUtils.num_squares_to_edges[start_square][direction_index]):
            target_square = start_square + MoveUtils.direction_offsets[
                direction_index
            ] * (n + 1)
            piece_on_target, color_on_target = squares[target_square]

            # blocked by friendly piece
            if color_on_target == piece_color:
                break

            moves.append(Move(start_square, target_square))

            # blocked by enemy piece (can capture but stop after)
            if color_on_target != Pieces.none:
                break
    return moves

def generate_moves(squares, mycolor, pawn_directions):
    moves = list()
    for start_square, piece in enumerate(squares):
        piece_type, piece_color = piece
        if piece_type and piece_color == mycolor:
            match piece_type:
                case Pieces.king:
                    moves.extend(generate_king_moves(squares, start_square, piece))
                case Pieces.pawn:
                    moves.extend(
                        generate_pawn_moves(
                            squares, start_square, piece, pawn_directions
                        )
                    )
                case Pieces.knight:
                    moves.extend(generate_knight_moves(squares, start_square, piece))
                case Pieces.bishop | Pieces.rook | Pieces.queen:
                    moves.extend(generate_sliding_moves(squares, start_square, piece))
                case _:
                    print("INFO : problem generating moves")
    return moves

def generate_legal_moves(squares, moves, mycolor, pawn_directions):
    legal_moves = []

    for move_to_verify in moves:
        new_squares = make_move(squares, move_to_verify)
        new_color = Pieces.white if mycolor == Pieces.black else Pieces.black

        check_king = False
        opponent_responses = generate_moves(new_squares, new_color, pawn_directions)

        for move in opponent_responses:
            piece_targeted, color_targeted = new_squares[move.target_square]
            if piece_targeted == Pieces.king and color_targeted == mycolor:
                check_king = True
                break

        if not check_king:
            legal_moves.append(move_to_verify)

    return legal_moves

def make_move(squares, move):
    # copy the board
    new_squares = squares[:]

    # get the piece at start square
    piece = new_squares[move.start_square]

    # if piece is pawn and at last square, transform to queen
    target_y = index_to_xy(move.target_square)[0]
    if piece[0] == Pieces.pawn and (target_y == 7 or target_y == 0):
        piece = (Pieces.queen, piece[1])

    # move piece to target square
    new_squares[move.target_square] = piece

    # clear the start square
    new_squares[move.start_square] = (Pieces.none, Pieces.none)

    return new_squares

def index_to_xy(n: int):
    y = 7 - (n // 8)
    x = 7 - (n % 8)
    return y, x
     
def chess_bot(player_sequence, board, time_budget, **kwargs):
    mycolor = Pieces.white if player_sequence[1] == "w" else Pieces.black
    squares = load_from_string(board)
    pawn_directions = get_pawn_directions(player_sequence)

    moves = generate_moves(squares, mycolor, pawn_directions)
    legal_moves = generate_legal_moves(squares, moves, mycolor, pawn_directions)

    random_move = random.choice(legal_moves)
    return index_to_xy(random_move.start_square), index_to_xy(random_move.target_square)

register_chess_bot("RandomBot", chess_bot)
