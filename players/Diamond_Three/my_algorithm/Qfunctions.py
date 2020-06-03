def AverageQfunc(node):
    """average Q function
    Use the average reward in the node to defined whether it is good or not

    Args:
        node: a child node, contain a opponent state

    Returns:
        the Q value of the child node.
    """
    if node.state.visited_count == 0:
        return 0
    # (1 - node.state.player_id) is the ID of the father node,
    # Since this function is used by the father to select the best child for itself
    # We need to maximize the win_scores of the father
    father_id = 1 - node.state.player_id
    return node.state.win_scores_sum[father_id] / node.state.visited_count


def AggressiveQfunc(node):
    """Aggressive Q function
    Try to maximize the difference between us and our opponent.

    Args:
        node: a child node, contain a opponent state

    Returns:
        the Q value of the child node.
    """
    # (1 - node.state.player_id) is the ID of the father node,
    # Since this function is used by the father to select the best child for itself
    # We need to maximize the win_scores of the father
    if node.state.visited_count == 0:
        return 0
    father_id = 1 - node.state.player_id
    child_id = node.state.player_id
    return (node.state.win_scores_sum[father_id] - node.state.win_scores_sum[child_id]) / node.state.visited_count
