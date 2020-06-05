import time
import copy
import random
from .game_tree import Node, State, CalculateFutureReward


class MonteCarloTreeSearch:
    """ Monte Carlo Tree Search
    Use UTC to find the next move

    Attributes:
        player_id: the ID of the player
        game_state: global information about the game, provided by the game manager
        time_limit: the time limit of each step, should be lower than the setting in the game
        mab: the Multi-armed bandits algorithm used in the Selection process.
        root: the root node of the tree
    """

    def __init__(self, player_id, game_state, moves, time_limit, mab, discount_factor):
        """Init the Monte Carlo Tree Search algorithm

        Args:
            player_id: the ID of the player
            game_state: global information about the game, provided by the game manager
            moves: the move action list
            time_limit: the time limit of each step, should be lower than the setting in the game
            mab: the Multi-armed bandits algorithm used in the Selection process.
            discount_factor: Use for discount the value in the future
        """
        self.moves = moves
        self.player_id = player_id
        self.time_limit = time_limit
        self.mab = mab
        self.discount_factor = discount_factor
        # Initial tree
        self.root = Node(State(player_id, game_state, None), None)
        # Here we expand the root directly to prevent empty selection
        self.root.ExpandChildren(moves)

    def FindNextMove(self, first_q_func, second_q_func):
        """Find the best move using UTC

        Use two Q function to break the tie to select a better move.

        Args:
            first_q_func: The Q function used to calculate UTB and to select move
            second_q_func: The Q function used to break the tie

        Returns:
             The best move with the highest scores
        """
        begin_time = time.time()
        while time.time() - begin_time < self.time_limit:
            # Select the leaf node with the higher UCB1 value
            expand_node = self.Selection(self.root, first_q_func)
            # Expand the node, only expand if it is visited more than one times before.
            # This encourage breath search one more time instead of expanding nodes.
            # If the node is the end of the game, use the expand_node to simulate.
            child = expand_node
            # A higher visited_count would lead to more simulation. Not enough computing power provided!
            if expand_node.state.visited_count > 1 and expand_node.state.game_state.TilesRemaining() is True:
                children = self.Expansion(expand_node)
                # It may not have children. Also, for the first time, it would not expand its children.
                if len(children) > 0:
                    child = self.Choose(children)
            # Simulation
            rewards, move_count = self.Simulation(child)
            # Back propagation, backup both our reward and our opponent's reward (Self training)
            self.Backup(child, rewards, move_count, self.discount_factor)
        # Find the best move with the highest win score
        # Choose the move that can bring the max Q value
        best_child = self._ChooseBestChildWithTieBreaker(self.root.children, first_q_func, second_q_func)
        return best_child.state.pre_move

    def Selection(self, root, q_func):
        """ Select the leaf node with the highest UCB to expand"""
        node = root
        while len(node.children) > 0:
            node = self.mab.FindBestChildNode(node, q_func)
        return node

    @staticmethod
    def Expansion(node):
        """ Expand the node, add children into its leaves """
        node.ExpandChildren()
        return node.children

    @staticmethod
    def Choose(children):
        """ Randomly choose a child to do simulation """
        # TODO: can be improve using some costless method to avoid Impossible choice
        return random.choice(children)

    @staticmethod
    def Simulation(child):
        """ Use some simple and costless strategy to simulate """
        # Deep copy first to avoid change the game_state in the node
        gs_copy = copy.deepcopy(child.state.game_state)
        current_player_id = child.state.player_id
        move_count = 0
        while gs_copy.TilesRemaining():
            # Update move
            plr_state = gs_copy.players[current_player_id]
            moves = plr_state.GetAvailableMoves(gs_copy)
            # TODO: provide different strategy for simulation the future
            # Strategy 1 -- random select:
            # selected = random.choice(moves)
            # Strategy 2 -- naive select:
            selected = MonteCarloTreeSearch._NaiveMoveSelected(moves)
            gs_copy.ExecuteMove(current_player_id, selected)
            # Change to the opponent
            current_player_id = 1 - current_player_id
            move_count += 1
        # TODO: reward can be change to improve
        reward0 = gs_copy.players[0].ScoreRound()[0] + CalculateFutureReward(gs_copy, 0)
        reward1 = gs_copy.players[1].ScoreRound()[0] + CalculateFutureReward(gs_copy, 1)
        return [reward0, reward1], move_count

    @staticmethod
    def Backup(node, rewards, move_count, discount_factor):
        """ Back propagation """
        # Get the rewards after discount
        real_rewards = [reward * (discount_factor ** move_count) for reward in rewards]
        # Back propagation
        p_node = node
        while p_node is not None:
            # Increase the visited count
            p_node.state.visited_count += 1
            # Instead change the win score directly, add it into it.
            p_node.state.win_scores_sum[0] += real_rewards[0]
            p_node.state.win_scores_sum[1] += real_rewards[1]
            p_node = p_node.parent

    @staticmethod
    def _NaiveMoveSelected(moves):
        """ Use for simulation to provide more reasonable choice"""
        most_to_line = -1
        corr_to_floor = 0
        best_moves = []
        for mid, fid, tgrab in moves:
            if most_to_line == -1:
                best_moves.append((mid, fid, tgrab))
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
            elif tgrab.num_to_pattern_line > most_to_line:
                best_moves.clear()
                best_moves.append((mid, fid, tgrab))
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
            elif tgrab.num_to_pattern_line == most_to_line:
                if tgrab.num_to_floor_line < corr_to_floor:
                    best_moves.clear()
                    best_moves.append((mid, fid, tgrab))
                    most_to_line = tgrab.num_to_pattern_line
                    corr_to_floor = tgrab.num_to_floor_line
                elif tgrab.num_to_floor_line == corr_to_floor:
                    best_moves.append((mid, fid, tgrab))
        return random.choice(best_moves)

    @staticmethod
    def _ChooseBestChildWithTieBreaker(children, first_q_func, second_q_func):
        """ Choose the best child based on the Q value
        Choose the best child from a bunch of children with two Q function, the second one is used to break the tie

        Args:
            children: All the children that can be chosen, a Node object
            first_q_func: Main Q function for child selection
            second_q_func: Used for tie breaker

        Returns:
            the best child
        """
        if second_q_func is None:
            return max(children, key=first_q_func)
        else:
            best_child = None
            max_first_q_value = float('-inf')
            best_second_q_value = float('-inf')
            for child in children:
                first_q_value = first_q_func(child)
                if first_q_value > max_first_q_value:
                    best_child = child
                    max_first_q_value = first_q_value
                    best_second_q_value = second_q_func(child)
                elif first_q_value == max_first_q_value:
                    # Use the second Q value to break the first tie
                    curr_second_q_value = second_q_func(child)
                    if curr_second_q_value > best_second_q_value:
                        best_child = child
                        best_second_q_value = curr_second_q_value
                    elif best_second_q_value == curr_second_q_value:
                        # Use Naive way to break the second tie
                        _, _, best_tgrab = best_child.state.pre_move
                        _, _, curr_tgrab = child.state.pre_move
                        if curr_tgrab.num_to_pattern_line > best_tgrab.num_to_pattern_line:
                            best_child = child
                        elif curr_tgrab.num_to_pattern_line == best_tgrab.num_to_pattern_line:
                            if curr_tgrab.num_to_floor_line < best_tgrab.num_to_floor_line:
                                best_child = child
            # TODO: Can still be improved
            return best_child