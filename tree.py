from constants import *
import math


class Node:
    """
    node of Monte Carlo Tree Search
    """
    def __init__(self, parent=None, p=1.0):
        """

        :param parent: parent node
        :param p: prior probability
        """

        self.parent = parent
        self.p = p

        self.children = {}  # key: action, value: child node

        # MCTS variables
        self.W = 0  # total value of this node
        self.Q = 0  # mean value of this node
        self.N = 0  # number of times searching this node


class Tree:
    """
    basic features of a search tree
    """
    def __init__(self):
        self.root = Node(None, 1.0)

    @staticmethod
    def _is_leaf(node):
        """
        check if a node is a leaf node
        :param node:
        :return:
        """
        return node.children == {}

    @staticmethod
    def _expand(node, m_p):
        """
        expand the node
        :param m_p: list of (move, prior_probability) pairs of available actions
        :param node: node to be expanded
        :return: the expanded node
        """
        for m, p in m_p:
            if m not in node.children:
                node.children[m] = Node(node, p)

    @staticmethod
    def _cal_uct(node):
        """
        compute the uct value which we use to decide the next node searched
        :param node:
        :return: uct value of the node
        """
        uct = C_PUCT * node.P * math.sqrt(node.parent.N / (1 + node.N))
        uct += node.Q

        return uct

    @staticmethod
    def _select(node):
        """
        from the children of the node, select one to continue searching
        :param node:
        :return: the position and the node selected
        """
        return max(node.children.items(), key=lambda child: Tree._cal_uct(child[1]))

    @staticmethod
    def _update_node(node, value):
        """
        update the information of the node
        :param node:
        :param value: the value to be added to the total value of the node
        :return:
        """
        node.N += 1
        node.W += value
        node.Q = node.W / node.N

    @staticmethod
    def _back_propagation(node, value):
        """
        update the node of the searching route using the value of the leaf node
        :param node:
        :param value: value of the leaf node
        :return:
        """
        if node.parent:
            Tree._back_propagation(node.parent, -value)
        Tree._update_node(node, value)


# testing
if __name__ == "__main__":
    pass
