from advance_model import *
from .my_algorithm import MAB_only
from .my_algorithm import Qfunctions
from .my_algorithm.MAB.UCB import *


class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)
        # Initialize the Multi-armed bandit algorithm
        self.mab = UCB(0.5)

    def SelectMove(self, moves, game_state):
        # Reduce the number of moves, to get more iteration
        mcts_light = MAB_only.MAB_only(self.id, game_state, 0.95, self.mab, 1)
        return mcts_light.FindNextMove(Qfunctions.AverageQfunc, Qfunctions.AggressiveQfunc)
