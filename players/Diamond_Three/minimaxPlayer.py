from advance_model import *
from .my_algorithm. Minimax import *


class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectMove(self, moves, game_state):
        # No need to think if only one move is provided
        print('------------')
        selector = Minimax(self.id, game_state, moves)
        return selector.FindNextMove()
