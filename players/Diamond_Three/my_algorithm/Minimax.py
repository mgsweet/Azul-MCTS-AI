import copy
from .game_tree import Node, State
from .MCTS import MonteCarloTreeSearch
import time

count = 1


def _SetDepth(moves_size):
    if moves_size > 17:
        return 0
    elif moves_size > 7:
        return 1
    else:
        return 100


class Minimax:
    def __init__(self, player_id, game_state, moves):
        self.root = Node(State(player_id, game_state, None), None)
        print("Before Simplify: ", len(moves))
        self.root.ExpandChildren(moves)
        print("After Simplify: ", len(self.root.children))
        self.depth = _SetDepth(len(self.root.children))
        print("Depth: ", self.depth)
        self.count = 0

    def minimax(self, node, depth, alpha, beta, player_id):
        self.count += 1
        father_player_id = 1 - player_id
        if depth == 0 or node.state.game_state.TilesRemaining() is False:
            # Reuse the simulation in MonteCarloTreeSearch
            rewards, move_count = MonteCarloTreeSearch.Simulation(node)
            father_player_reward = rewards[father_player_id]
            if father_player_id == 1:
                father_player_reward *= -1
            return father_player_reward, rewards
        if player_id == 0:
            max_eval = float('-inf')
            max_rewards = None
            if len(node.children) == 0:
                node.ExpandChildren()
            for child in node.children:
                evaluation, rewards = self.minimax(child, depth - 1, alpha, beta, 1)
                if evaluation > max_eval or (
                        evaluation == max_eval and rewards[0] - rewards[1] > max_rewards[0] - max_rewards[1]):
                    max_eval = evaluation
                    max_rewards = rewards
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return -max_rewards[1], max_rewards
        else:
            min_eval = float('inf')
            min_rewards = None
            if len(node.children) == 0:
                node.ExpandChildren()
            for child in node.children:
                evaluation, rewards = self.minimax(child, depth - 1, alpha, beta, 0)
                if evaluation < min_eval or (
                        evaluation == min_eval and rewards[0] - rewards[1] < min_rewards[0] - min_rewards[1]):
                    min_eval = evaluation
                    min_rewards = rewards
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_rewards[0], min_rewards

    def _ChooseBestChild(self):
        best_child = None
        best_rewards = None
        if self.root.state.player_id == 0:
            max_eval = float('-inf')
            for child in self.root.children:
                evaluation, rewards = self.minimax(child, self.depth, float('-inf'), float('inf'), 1)
                if evaluation > max_eval or (
                        evaluation == max_eval and rewards[0] - rewards[1] > best_rewards[0] - best_rewards[1]):
                    max_eval = evaluation
                    best_child = child
                    best_rewards = rewards
        else:
            min_eval = float('inf')
            for child in self.root.children:
                evaluation, rewards = self.minimax(child, self.depth, float('-inf'), float('inf'), 0)
                if evaluation < min_eval or (
                        evaluation == min_eval and rewards[0] - rewards[1] < best_rewards[0] - best_rewards[1]):
                    min_eval = evaluation
                    best_child = child
                    best_rewards = rewards
        print("best_rewards: ", best_rewards[0], best_rewards[1])
        return best_child

    def FindNextMove(self):
        begin = time.time()
        best_child = self._ChooseBestChild()
        print("Time cost: ", time.time() - begin)
        print("Iteration: ", self.count)
        return best_child.state.pre_move
