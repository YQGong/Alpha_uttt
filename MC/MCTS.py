from random import choice as randchoice
from copy import deepcopy as copy
import math


class MCTS:

    def __init__(self, cucpt=1, times=1, process=1):
        self.Qs = {}
        self.cpuct = cucpt
        self.times = times
        self.process = process

    def one_search(self, board, color):
        b = copy(board)
        current_color = copy(color)
        while not b.finished:
            move = randchoice(b.get_legal_moves(current_color))
            b.execute_move(move, current_color)
            current_color *= -1
        return b.winner

    def one_search_MP(self, board, color):
        return sum([self.one_search(board, color) for i in range(self.times)])

    def search(self, board, color,pool=None):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propogated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propogated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        Returns:
            v: the negative of the value of the current canonicalBoard / the previous move
        """

        s = board.tostring()
        # terminal node : return the value of the game
        if board.finished:
            return -board.winner * color  # the negative of the value of the previous move

        # leaf node : return the value given by the nnet
        if s not in self.Qs:
            result=[]
            if not pool:
                print('single core mode ')
                rand = sum([self.one_search(board, color) for i in range(self.times)])
            else:
                for i in range(self.process):
                    result.append(pool.apply_async(func=self.one_search_MP, args=(board, color,)))
                [i.wait() for i in result]
                rand=sum([i.get() for i in result])
            v = rand * color  # the value of the next color
            self.Qs[s] = [-v,self.times*self.process]  # Qs : the value of the previous move
            return -v

        # non-leaf node
        cur_best = -float('inf')
        best_move = []

        # pick the action with the highest upper confidence bound
        for move in board.get_legal_moves(color):
            bmove = copy(board).execute_move(move, color)
            smove = bmove.tostring()
            value=self.Qs[s]
            if smove in self.Qs:
                value_move=self.Qs[smove]
                u = value_move[0] / value_move[1] + self.cpuct * math.sqrt(2 * math.log(value[1]) / value_move[1])
            elif bmove.finished and bmove.winner==-color:
                continue
            else:
                best_move = move
                break

            if u > cur_best:
                cur_best = u
                best_move = move
        if len(best_move) != 0:
            board_next = copy(board).execute_move(best_move, color)
        else:
            raise Exception('no best action found!')

        # next recursion
        v = self.search(board_next, -color,pool)  # the value of the current color

        # back propagation for non-leaf node
        value=self.Qs[s]
        value[0]-=v
        value[1]+=self.times*self.process
        self.Qs[s] = value  # Qs : the value of the previous move
        return -v
