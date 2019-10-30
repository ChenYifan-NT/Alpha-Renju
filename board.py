from constants import SIZE, RENJU
import copy
import numpy as np


class Player:
    def __init__(self, number):
        """

        :param number: the number of the player
        """
        self.number = number  # 1 or 2

        # also record the last two actions of the player in the player object
        self.last_action = -1
        self.second_last_action = -1

    def get_number(self):
        """
        return the number of the player
        :return:
        """
        return self.number

    def update_actions(self, action):
        self.second_last_action = self.last_action
        self.last_action = action

    def get_last_actions(self):
        """
        return the last two actions of the player, the last one in the front
        :return:
        """
        return self.last_action, self.second_last_action


class Board:
    def __init__(self):
        # stones placed.
        # 0 if the place is empty, 1 if the stone is black, 2 is the stone is white.
        # initially all places are empty
        self.stones = np.zeros(SIZE ** 2)

        # list of empty places.
        self.empty_places = list(range(SIZE ** 2))

        # players
        self.players = {1: Player(1), 2: Player(2)}

        # the player who made the last action
        self.last_player = None
        # the player who is the next one to act
        self.next_player = self.players[1]

        # record the last action
        self.last_action = -1

    def place_stone(self, position):
        """
        place a stone on the board.
        :param position: the position to place the stone (the board is flattened)
        :return:
        """

        # stone is placed
        self.stones[position] = self.next_player.get_number()
        self.empty_places.remove(position)

        self.last_action = position

        # update the action history of the player
        self.next_player.update_actions(position)

        # change side
        self.last_player = self.next_player
        change_side = {1: 2, 2: 1}
        self.next_player = self.players[change_side[self.last_player.get_number()]]

    def check_winner(self):
        """
        check if there is a winner. return two numbers.
        the first is a bool telling if there is a winner,
        the second is the number of the winner. 0 for a tie or the game is not over.
        :return: has_winner, winner
        """

        if self.last_action == -1:
            return False, 0

        # starting from the position where the last stone is placed
        pos = self.last_action
        player = self.stones[pos]

        # transfer the position to coordinate
        col = pos % SIZE
        row = pos // SIZE

        # check horizontally
        count = 1
        # left
        c = copy.deepcopy(col) - 1
        r = copy.deepcopy(row)
        while c >= 0 and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c -= 1

        # right
        c = copy.deepcopy(col) + 1
        while c < SIZE and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c += 1

        if count >= RENJU:
            return True, player

        # check vertically
        count = 1
        # up
        c = copy.deepcopy(col)
        r = copy.deepcopy(row) - 1
        while r >= 0 and self.stones[Board._c2p(c, r)] == player:
            count += 1
            r -= 1
        # down
        c = copy.deepcopy(col)
        r = copy.deepcopy(row) + 1
        while r < SIZE and self.stones[Board._c2p(c, r)] == player:
            count += 1
            r += 1

        if count >= RENJU:
            return True, player

        # check back slash
        count = 1
        # up
        c = copy.deepcopy(col) - 1
        r = copy.deepcopy(row) - 1
        while c >= 0 and r >= 0 and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c -= 1
            r -= 1

        # down
        c = copy.deepcopy(col) + 1
        r = copy.deepcopy(row) + 1
        while c < SIZE and r < SIZE and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c += 1
            r += 1

        if count >= RENJU:
            return True, player

        # check forward slash
        count = 1
        # up
        c = copy.deepcopy(col) + 1
        r = copy.deepcopy(row) - 1
        while c < SIZE and r >= 0 and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c += 1
            r -= 1

        # down
        c = copy.deepcopy(col) - 1
        r = copy.deepcopy(row) + 1
        while c >= 0 and r < SIZE and self.stones[Board._c2p(c, r)] == player:
            count += 1
            c -= 1
            r += 1

        if count >= RENJU:
            return True, player

        # if the board is empty, then tie
        if len(self.empty_places) == 0:
            return True, 0
        else:
            return False, 0

    @staticmethod
    def _c2p(c, r):
        """
        transfer a coordinate to position, only used in Board.check_winner()
        :param c: col
        :param r: row
        :return: pos
        """
        return r * SIZE + c

    def draw(self):
        """
        draw the board
        :return:
        """

        print('The current player is ' + str(self.next_player.get_number()))

        # print the column numbers
        for x in range(SIZE):
            print('{0:8}'.format(x), end='')
        print()

        # print the row number
        for y in range(SIZE):
            print('{0:4d}'.format(y), end='')
            for x in range(SIZE):
                position = y * SIZE + x
                stone = self.stones[position]

                if stone == 1:
                    if position == self.last_action:
                        print('黑'.center(8), end='')
                    else:
                        print('B'.center(8), end='')
                elif stone == 2:
                    if position == self.last_action:
                        print('白'.center(8), end='')
                    else:
                        print('W'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')


# testing
if __name__ == "__main__":
    board = Board()

    for i in range(5):
        board.place_stone(SIZE * i + i)
        print(board.check_winner())
        board.place_stone(SIZE * SIZE - 1 - i)
        print(board.check_winner())
        board.draw()
