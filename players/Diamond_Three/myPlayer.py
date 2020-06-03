from advance_model import *
from .my_algorithm import MCTS
from .my_algorithm import Qfunctions
from .my_algorithm.MAB.UCB import *


class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)
        # Initialize the Multi-armed bandit algorithm
        self.mab = UCB(0.5)

    def SelectMove(self, moves, game_state):
        # No need to think if only one move is provided
        if len(moves) == 1:
            return moves[0]
        # Reduce the number of moves, to get more iteration
        mcts = MCTS.MonteCarloTreeSearch(self.id, game_state, moves, 0.9, self.mab, 1)
        return mcts.FindNextMove(Qfunctions.AverageQfunc, Qfunctions.AggressiveQfunc)
