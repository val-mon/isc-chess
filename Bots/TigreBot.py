from Bots.ChessBotList import register_chess_bot
from Bots.RandomBot import *

def chess_bot(player_sequence, board, time_budget, **kwargs):
    b = [
      ["","","","pw","pw","pw","",""],
      ["","","","","","","",""],
      ["","","","","","","",""],
      ["","","","","","","",""],
      ["","","","","","","",""],
      ["","","","","","","",""],
      ["","","","","","","",""],
      ["","","","","","","",""]
    ]
    loaded_board = load_from_string(board)
    return find_best_move(loaded_board, Pieces.white if player_sequence[1] == 'w' else Pieces.black, 4)

register_chess_bot("TigreBot", chess_bot)
