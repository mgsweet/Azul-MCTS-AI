from abc import ABC, abstractmethod


class MAB(ABC):
    """
    Abstract class that represents a multi-armed bandit (MAB)
    """
    @abstractmethod
    def FindBestChildNode(self, node, q_func):
        """Find the best child node of a node using MAB algorithm

        Args:
            node: A Tree Node containing information about the game.
            q_func: A function used to provide Q value

        Returns:
            The best child
        """
        pass
