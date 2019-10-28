import numpy as np
from board import *


# uniform policy
def uniform_policy(board):
    """
    this policy will choose the child nodes uniformly
    it will return a random number as the value
    :param board:
    :return:
    """

    actions = np.array(board.empty_places)

    probabilities = np.ones(actions.size) / actions.size

    a_c = list(zip(actions, probabilities))

    value = np.random.uniform(-1, 1)

    return a_c, value


# testing
if __name__ == "__main__":
    board = Board()

    for i in range(144):
        board.place_stone(i)
        if i % 10 == 0:
            a_c, value = uniform_policy(board)
            print(i)
            print(a_c)
            print(value)
