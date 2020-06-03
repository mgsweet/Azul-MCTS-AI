import math
from .MAB import *


class UCB(MAB):
    """
    Epsilon-Greedy multi-armed bandit

    Attributes
        exploration_constant : explore probability
    """

    def __init__(self, exploration_constant):
        """Initialize UCB

        Args:
            exploration_constant: explore-exploit trade-off controler
        """
        self.exploration_constant = exploration_constant

    def FindBestChildNode(self, node, q_func):
        """Find the best node through comparing the highest UCB

        Args:
            node: expand_node
            q_func: how to calculate the q value, the child node would be its parameter.

        Returns:
            The node with the max UCB
        """
        parent_visited_count = node.state.visited_count
        max_ucb = float('-inf')
        best_child = None
        # Child state belong to the opponent, we need to find one with the best win_scores_sum of ourselves
        for child in node.children:
            if child.state.visited_count == 0:
                return child
            else:
                tmp = self._CalculateUCB(parent_visited_count, q_func(child), child.state.visited_count)
                if tmp > max_ucb:
                    max_ucb = tmp
                    best_child = child
        return best_child

    def _CalculateUCB(self, total_visit, q_value, node_visited_count):
        """Calculate UCB

        Args:
            total_visit: the visit count of the parent node
            q_value: the Q value of the node
            node_visited_count: the visit count of the current node

        Returns:
            The UCB value
        """
        if node_visited_count == 0:
            return float('inf')
        return q_value + self.exploration_constant * math.sqrt(math.log(total_visit) / node_visited_count)
