import time
import copy
import random


class MAB_only:
    """ Monte Carlo Tree Search (Light version)
    Use UTC to find the next move, but only consider one expand layer. Give it more iteration.

    Attributes:
        player_id: the ID of the player
        game_state: global information about the game, provided by the game manager
        time_limit: the time limit of each step, should be lower than the setting in the game
        mab: the Multi-armed bandits algorithm used in the Selection process.
        root: the root node of the tree
    """

    def __init__(self, player_id, game_state, time_limit, mab, discount_factor):
        """Init the Monte Carlo Tree Search algorithm

        Args:
            player_id: the ID of the player
            game_state: global information about the game, provided by the game manager
            time_limit: the time limit of each step, should be lower than the setting in the game
            mab: the Multi-armed bandits algorithm used in the Selection process.
            discount_factor: Use for discount the value in the future
        """
        self.player_id = player_id
        self.time_limit = time_limit
        self.mab = mab
        self.discount_factor = discount_factor
        # Initial tree
        self.root = Node(State(player_id, copy.deepcopy(game_state), None), None)
        # Here we expand the root directly to prevent empty selection
        self.root.ExpandChildren()

    def FindNextMove(self, first_q_func, second_q_func):
        """Find the best move using UTC

        Args:
            first_q_func: The Q function used to calculate UTB and to select move
            second_q_func: The Q function used to break the tie

        Returns:
             The best move with the highest scores
        """
        test_count = 0
        begin_time = time.time()
        while time.time() - begin_time < self.time_limit:
            test_count += 1
            # Select the leaf node with the higher UCB1 value
            # No expansion, only consider one layer
            child = self._Selection(self.root, first_q_func)
            # Simulation
            rewards, move_count = self._Simulation(child)
            # Actually, much like just using bandit, but we get the reward by simulation
            self._Update(child, rewards, move_count, self.discount_factor)
        # Find the best move with the highest win score
        print(test_count)
        # Choose the move that can bring the max Q value

        best_child = self._ChooseBestChildWithTieBreaker(self.root.children, first_q_func, second_q_func)
        return best_child.state.pre_move

    def _Selection(self, root, q_func):
        """ Select the leaf node with the highest UCB to expand"""
        return self.mab.FindBestChildNode(root, q_func)

    @staticmethod
    def _Simulation(child):
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
            selected = random.choice(moves)
            # Strategy 2 -- naive select:
            # selected = MCTS_Light._NaiveMoveSelected(moves)
            gs_copy.ExecuteMove(current_player_id, selected)
            # Change to the opponent
            current_player_id = 1 - current_player_id
            move_count += 1
        # TODO: reward can be change to improve
        reward0 = gs_copy.players[0].ScoreRound()[0] + _CalculateFutureReward(gs_copy, 0)
        reward1 = gs_copy.players[1].ScoreRound()[0] + _CalculateFutureReward(gs_copy, 1)
        return [reward0, reward1], move_count

    @staticmethod
    def _Update(leaf_node, rewards, move_count, discount_factor):
        """ Back propagation """
        # Get the rewards after discount
        real_rewards = [reward * (discount_factor ** move_count) for reward in rewards]
        # Increase the visited count
        leaf_node.state.visited_count += 1
        leaf_node.parent.state.visited_count += 1
        # Instead change the win score directly, add it into it.
        leaf_node.state.win_scores_sum[0] += real_rewards[0]
        leaf_node.state.win_scores_sum[1] += real_rewards[1]
        leaf_node.parent.state.win_scores_sum[0] += real_rewards[0]
        leaf_node.parent.state.win_scores_sum[1] += real_rewards[1]

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


def _CalculateFutureReward(game_state, player_id):
    """Use to calculate the reward of the future round

    Args:
        game_state: Current game state, the game state should be a end of a round
        player_id: The id of the player

    Returns:
        The estimation value
    """
    player_state = game_state.players[player_id]
    return _CalculateFutureBonus(game_state, player_id) - _CalculateFuturePenalty(player_state)


def _CalculateFuturePenalty(player_state):
    """Estimate the penalty in the future

    Args:
        player_state: Player state

    Returns:
        The estimation value
    """
    future_penalty = 0
    # Punish unfinished pattern line
    for i in range(1, 5):
        if player_state.lines_number[i] > 0:
            future_penalty += 1
    # Extra Punishment for fourth pattern line
    if player_state.lines_number[3] == 1:
        future_penalty += 1.5
    if player_state.lines_number[3] == 2:
        future_penalty += 0.5
    # Extra Punishment for fifth pattern line
    if player_state.lines_number[4] == 1:
        future_penalty += 2
    elif player_state.lines_number[4] == 2:
        future_penalty += 1
    return future_penalty


def _CalculateFutureBonus(game_state, player_id):
    """Use some domain knowledge to calculate the bonus"""
    # TODO: provide a more accurate estimation
    future_bonus = 0
    player_state = game_state.players[player_id]
    # Only consider cols and sets
    cols = player_state.GetCompletedColumns()
    sets = player_state.GetCompletedSets()
    bonus = (cols * player_state.COL_BONUS) + (sets * player_state.SET_BONUS)
    # Discount factor
    # bonus *= 0.5
    # It is ok to get the first player, however, since we can't get enough iteration, not consider this now.
    if game_state.next_first_player == player_id:
        future_bonus += 1
    future_bonus += bonus
    return future_bonus


def _simplyMoves(moves):
    """Simply moves list based on some policy
    May have negative effect

    Args:
        moves: a move action list

    Returns:
        a simplified move action list
    """
    for i in range(len(moves) - 1, -1, -1):
        curr_tile_grap = moves[i][2]
        if curr_tile_grap.num_to_floor_line == curr_tile_grap.number:
            moves.pop(i)


class State:
    """Use to record information about the game. Used by Node.

    Attributes:
        pre_move: the move action that make the previous game state change to the current game state.
        player_id: current player's ID
        game_state: current game state
        visited_count: Record the visited time of the state.
        win_scores_sum: Contain information about the sum of reward of both players. Index match the id.
    """

    def __init__(self, player_id, game_state, pre_move):
        """
        State constructor, create state to record the game state
        Args:
            player_id: current player_id, can only handle 1 or 0
            game_state: global game state, please deep copy before sending it inside
            pre_move: the move action that make the previous game state change to the current game state
        """
        # Record the move action that lead to the current state.
        self.pre_move = pre_move
        # Property relative to the game
        self.player_id = player_id
        self.game_state = game_state
        self.visited_count = 0
        # Record sum of win scores for all players
        self.win_scores_sum = [0, 0]


class Node:
    """Use for UTC Tree

    Attributes:
        state: Use to record the information about the game
        children: All the children that can generate by executing available move action, children state belong to
            opponent. We do self play. Children would only be generate through expansion process in MCTS.
        parent: The parent node of the current node.

    """

    def __init__(self, state, parent):
        """Init Node with state and parent, children would be generated in the expansion process in MCTS

        Args:
            state: Information about the game
            parent: The parent node of the current node. Use for back propagation.
        """
        # Property relative to the game
        self.state = state
        # Property for a tree node
        self.children = []
        self.parent = parent

    def ExpandChildren(self):
        """Expand all the possible children of the node

        Generate all the possible children of the node, the next node belong to the opponent,
        We do self play to train ourselves
        """
        opponent_id = 1 - self.state.player_id
        # Get all move based on the current game state
        moves = self.state.game_state.players[self.state.player_id].GetAvailableMoves(self.state.game_state)
        # Reduce the num of moves, do more iteration on the meaningful moves
        if len(moves) > 30:
            _simplyMoves(moves)
        for move in moves:
            # Get the next game_state: deep copy the current game_state and then execute the move.
            next_gs = copy.deepcopy(self.state.game_state)
            next_gs.ExecuteMove(self.state.player_id, move)
            # Add the new node to its children
            self.children.append(Node(State(opponent_id, next_gs, move), self))
