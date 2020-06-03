import copy


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

    def ExpandChildren(self, moves=None):
        """Expand all the possible children of the node

        Generate all the possible children of the node, the next node belong to the opponent,
        We do self play to train ourselves
        """
        opponent_id = 1 - self.state.player_id
        # Get all move based on the current game state
        if moves is None:
            moves = self.state.game_state.players[self.state.player_id].GetAvailableMoves(self.state.game_state)
        # Reduce the num of moves, do more iteration on the meaningful moves
        # print("Move:", len(moves))
        moves = _simplyMoves(moves)
        # print("Move:", len(moves))
        for move in moves:
            # Get the next game_state: deep copy the current game_state and then execute the move.
            next_gs = copy.deepcopy(self.state.game_state)
            next_gs.ExecuteMove(self.state.player_id, move)
            # Add the new node to its children
            self.children.append(Node(State(opponent_id, next_gs, move), self))


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


def CalculateFutureReward(game_state, player_id):
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
    """Estimate Future Bonus"""
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
    """Simplify move action list, remove all move that would only move tile to floor line"""
    ans = []
    for move in moves:
        if len(moves) > 50:
            # Not allow picking one tile to fourth and fifth line at the beginning
            if move[2].pattern_line_dest > 2 and move[2].num_to_pattern_line == 1:
                continue
        if len(moves) > 30:
            # Not allow picking all the thing to the floor_line at the beginning
            if move[2].num_to_floor_line == move[2].number:
                continue
        ans.append(move)
    return ans
