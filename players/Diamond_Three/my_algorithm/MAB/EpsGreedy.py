import random


class EpsGreedy:
    def __init__(self, epsilon):
        """Initial the epsilon greedy with a epsilon value

        Args:
            epsilon: explore probability
        """
        self.epsilon = epsilon


    def FindBestChildNode(self, node, q_func):
        """Find the best node using Epsilon Greedy

        Attributes:
            node: expand_node
            q_func: how to calculate the q value, the child node would be its parameter.

        Returns:
            The node chosen by Epsilon Greedy
        """
        if random.random() > self.epsilon:
            # if rand() > epsilon, exploit
            max_q_value = float('-inf')
            best_child = None
            for child in node.children:
                if child.state.visited_count == 0:
                    return child
                else:
                    tmp = q_func(child)
                    if tmp > max_q_value:
                        max_q_value = tmp
                        best_child = child
            return best_child
        else:
            # if rand() < epsilon, explore
            return random.choice(node.children)
