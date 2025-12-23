import json
import pytest

from Bots.TigreBot import chess_bot

@pytest.mark.parametrize(
    "player_sequence,board,expected",
    json.load(open("./Tests/piece_move.json", "r"))
)
class TestsPieceMove:
    def tests_piece_move(self, player_sequence, board, expected):
        e = expected
        assert chess_bot(player_sequence,board,1) == ((e[0][0], e[0][1]), (e[1][0], e[1][1]))

@pytest.mark.parametrize(
    "player_sequence,board,expected",
    json.load(open("./Tests/eat_king_in_one.json", "r"))
)
class TestsEatKingInOne:
    def test_eat_king_in_one(self, player_sequence, board, expected):
        e = expected
        assert chess_bot(player_sequence,board,1) == ((e[0][0], e[0][1]), (e[1][0], e[1][1]))

@pytest.mark.parametrize(
    "player_sequence,board,expected",
    json.load(open("./Tests/checkmate_in_one.json", "r")),
)
class TestsCheckmateInOne:
    def test_checkmate_in_one(self, player_sequence, board, expected):
        e = expected
        assert chess_bot(player_sequence,board,1) == ((e[0][0], e[0][1]), (e[1][0], e[1][1]))

@pytest.mark.parametrize(
    "player_sequence,board,expected",
    json.load(open("./Tests/checkmate_in_two.json", "r")),
)
class TestsCheckmateInTwo:
    def test_checkmate_in_two(self, player_sequence, board, expected):
        e = expected
        assert chess_bot(player_sequence,board,2) == ((e[0][0], e[0][1]), (e[1][0], e[1][1]))

@pytest.mark.parametrize(
    "player_sequence,board,expected",
    json.load(open("./Tests/capture_attacker.json", "r")),
)
class TestsCaptureAttacker:
    def test_capture_attacker(self, player_sequence, board, expected):
        e = expected
        assert chess_bot(player_sequence,board,1) == ((e[0][0], e[0][1]), (e[1][0], e[1][1]))
