from MC.MCTS import MCTS
from Game.GameLogic import Board
from tqdm import tqdm
from multiprocessing import Pool,Manager
from copy import deepcopy as copy
import numpy as np
import time

if __name__=='__main__':
    b=Board(9)
    current_color=1
    mcts=MCTS(1,10,30)
    pool=Pool(30)
    cmd='init'
    while cmd!='exit':
        if cmd=='init':
            b.execute_move(np.array([6,5]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([8,6]) - 1, current_color)
            current_color *= -1
        if cmd=='do':
            for i in tqdm(range(20)):
                for j in range(100):
                    mcts.search(b, current_color, pool)
        if cmd=='show best':
            Ns_list = []
            Qs_list = []
            for move in b.get_legal_moves(current_color):
                s = copy(b).execute_move(move, current_color).tostring()
                Ns_list.append(mcts.Ns[s])
                Qs_list.append(mcts.Qs[s])
            max_move = np.array(Ns_list).argmax()
            next_move = b.get_legal_moves(current_color)[max_move]
            print(next_move + 1, Ns_list[max_move], Qs_list[max_move])
            print(np.array([Ns_list, Qs_list]))
        if cmd=='next move':
            str=input('position:')
            next_move=[int(i) for i in str.split(' ')]
            b.execute_move(np.array(next_move) - 1, current_color)
            current_color *= -1
        if cmd=='show':
            print(b.pieces)
        cmd=input('command:')

if False:
    time_start=time.time()
    mcts.search(b,current_color,pool)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')

    time_start=time.time()
    mcts.search(b,current_color,pool)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')

    time_start=time.time()
    mcts.search(b,current_color,pool)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')

    time_start=time.time()
    mcts.search(b,current_color,pool)
    time_end=time.time()
    print('time cost',time_end-time_start,'s')


    print(mcts.Qs,mcts.Ns)