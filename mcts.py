import numpy as np
import copy
from constants import *
from tree import *
from board import *
from policies import *


class MCTS(Tree):
    def __init__(self, policy_function, n_search=N_SEARCH):
        """

        :param policy_function: the function that calculates
            the probability distribution of available actions
        :param n_search: number of searching per action
        """
        Tree.__init__(self)

        self.policy_function = policy_function
        self.n = n_search

    def _search(self, _board):
        """

        :param _board:
        :return:
        """
        node = self.root

        # board will be modified during searching, so make a deep copy
        search_board = copy.deepcopy(_board)

        # search all the way done to a leaf node
        while not MCTS.is_leaf(node):
            position, node = MCTS._select(node)
            search_board.place_stone(position)

        # check if the leaf node is the end of the game
        has_winner, winner = search_board.check_winner()

        # if it is not a leaf node, expand
        if not has_winner:
            # get the prior probabilities of the children and the value of this node
            a_p, _value = self.policy_function(search_board)  # a_p: actions_probabilities

            MCTS._expand(node, a_p)

        else:
            if winner == 0:
                _value = 0.0
            elif winner == search_board.last_player.get_number():
                _value = 1.0
            else:
                _value = -1.0

        MCTS.back_propagation(node, _value)

    def solve(self, _board):
        """
        given a board, solve the prior probability of its child nodes
        :param _board:
        :return:
        """

        search_board = copy.deepcopy(_board)

        for _ in range(N_SEARCH):
            self._search(search_board)

        action_number = [(action, node.N) for action, node in self.root.children.items()]
        _actions, _numbers = zip(*action_number)

        _probs = MCTS._pi(_numbers)

        return _actions, _probs

    @staticmethod
    def _pi(x):
        """

        :param x:
        :return:
        """
        log_x = (1 / TEMPERATURE) * np.log(np.array(x) + 1e-10)
        return MCTS._softmax(log_x)

    @staticmethod
    def _softmax(x):
        p = np.exp(x - np.max(x))
        p /= np.sum(p)
        return p


# testing
if __name__ == "__main__":
    mcts = MCTS(uniform_policy)
    board = Board()

    actions, probs = mcts.solve(board)

    print(actions[:5])
    print(probs[:5])
