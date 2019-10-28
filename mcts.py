import numpy as np
import copy
from constants import *
from tree import *


class MCTS(Tree):
    def __init__(self, policy_function, n_search=N_SEARCH):
        """

        :param policy_function: the function that calculates
            the probability distribution of available actions
        :param n_search: number of searching per action
        """
        Tree.__init__()

        self.policy_function = policy_function
        self.n = n_search

    def _search(self, board):
        """

        :param board:
        :return:
        """
        node = self.root

        # board will be modified during searching, so make a deep copy
        search_board = copy.deepcopy(board)

        # search all the way done to a leaf node
        while not MCTS._is_leaf(node):
            position, node = MCTS._select(node)
            search_board.place_stone(position)

        # check if the leaf node is the end of the game


