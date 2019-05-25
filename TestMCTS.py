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
    times_num=20
    process_num=30
    cparameter=0.3
    mcts=MCTS(cparameter,times_num,process_num)
    pool=Pool(process_num)
    cmd='init'
    while cmd!='exit':
        if cmd=='init':
            b.execute_move(np.array([6,5]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([9,5]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([8,4]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([6,3]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([9,9]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([8,9]) - 1, current_color)
            current_color *= -1
        if cmd=='do':
            for i in tqdm(range(10)):
                for j in range(100):
                    mcts.search(b, current_color, pool)
        if cmd=='show best':
            Ns_list = []
            Qs_list = []
            for move in b.get_legal_moves(current_color):
                s = copy(b).execute_move(move, current_color).tostring()
                Ns_list.append(mcts.Ns[s])
                Qs_list.append(mcts.Qs[s])
            value_list=[Qs_list[i]*10000//Ns_list[i] for i in range(len(Qs_list))]
            move_list=[i[0]*10+i[1]+11 for i in b.get_legal_moves(current_color)]
            max_move = np.array(value_list).argmax()
            next_move = b.get_legal_moves(current_color)[max_move]
            print(next_move + 1, Ns_list[max_move], Qs_list[max_move],value_list[max_move])
            print(np.array([Ns_list, Qs_list,value_list,move_list]))
        if cmd=='next move':
            str=input('position:')
            next_move=[int(i) for i in str.split(' ')]
            b.execute_move(np.array(next_move) - 1, current_color)
            current_color *= -1
        if cmd=='show':
            print(b.pieces)
        if cmd=='update times':
            value=input('value:')
            mcts.times=value
        if cmd=='update process':
            value=input('value:(less than {})'.format(process_num))
            mcts.process=value
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