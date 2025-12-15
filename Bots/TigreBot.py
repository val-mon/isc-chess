from Bots.ChessBotList import register_chess_bot
from Bots.RandomBot import Pieces, find_best_move, get_pawn_directions, load_from_string


def chess_bot(player_sequence, board, time_budget, **kwargs):
    loaded_board = load_from_string(board)
    pawn_directions = get_pawn_directions(player_sequence)
    mycolor = Pieces.white if player_sequence[1] == "w" else Pieces.black
    return find_best_move(loaded_board, mycolor, 3, pawn_directions)


register_chess_bot("TigreBot", chess_bot)
