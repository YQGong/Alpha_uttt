from MC.MCTS import MCTS
from Game.GameLogic import Board
from tqdm import tqdm
from multiprocessing import Pool,Manager
from copy import deepcopy as copy
import numpy as np
from random import choice as randchoice
import time

def show_best(mcts,b,current_color,debug=False): # from 0 to 8
    Ns_list = []
    Qs_list = []
    for move in b.get_legal_moves(current_color):
        btmp = copy(b).execute_move(move, current_color)
        s = btmp.tostring()
        if s in mcts.Qs:
            value = mcts.Qs[s]
            Ns_list.append(value[1])
            Qs_list.append(value[0])
        elif btmp.finished and btmp.winner==current_color:
            if debug:
                print('win move found,',move)
            return move
        else:
            Ns_list.append(1)
            Qs_list.append(-1)

    value_list=[Qs_list[i]*10000//Ns_list[i] for i in range(len(Qs_list))]
    move_list=[i[0]*10+i[1]+11 for i in b.get_legal_moves(current_color)]
    max_move = np.array(value_list).argmax()
    next_move = b.get_legal_moves(current_color)[max_move]
    if debug:
        print(next_move +1, Ns_list[max_move], Qs_list[max_move], value_list[max_move])
        print(np.array([Ns_list, Qs_list, value_list, move_list]))
    return next_move


class Exception111(BaseException):
    pass


if __name__=='__main__':
    times_num=10
    process_num=30
    cparameter=1
    mcts=MCTS(cparameter,times_num,process_num)
    pool=Pool(process_num)
    cmd='init'
    while cmd!='exit':
        try:
            if cmd=='self play with random':
                win=[0,0,0]
                while True:
                    b=Board(9)
                    current_color=1
                    b.execute_move(np.array([6,5]) - 1, current_color)
                    current_color *= -1
                    # b.execute_move(np.array([9,5]) - 1, current_color)
                    # current_color *= -1

                    while not b.finished:
                        endtime=time.time()+1
                        while time.time()<endtime:
                            mcts.search(b, current_color, pool)

                        next_move = np.array(show_best(mcts,b,current_color)) +1

                        print('color {} move : {}'.format(current_color, next_move))
                        b.execute_move(np.array(next_move) - 1, current_color)
                        current_color *= -1

                        if b.finished:
                            break

                        next_move=np.array(randchoice(b.get_legal_moves(current_color)))+1

                        print('color {} move : {}'.format(current_color,next_move))
                        b.execute_move(np.array(next_move) - 1, current_color)
                        current_color *= -1

                    print(b.pieces)
                    print('winner:',b.winner)
                    win[b.winner]+=1
                    total=sum(win)
                    print('1 win {} times,-1 win {} times,draw {} times,'.format(win[1],win[-1],win[0]))
                    print('1 win rate {} ,-1 win rate {} ,draw rate {} ,'.format(win[1]/total,win[-1]/total,win[0]/total))
        except Exception as e:
            print(b.pieces)
            print(b.activation_zone)
            print(b.finished, b.winner)
            print(b.main_pieces)
            print(b.main_pieces_finished)
            print(e)
            cmd='error'

        if cmd=='init':
            b=Board(9)
            current_color=1
            b.execute_move(np.array([6,5]) - 1, current_color)
            current_color *= -1
            b.execute_move(np.array([9,5]) - 1, current_color)
            current_color *= -1
            # b.execute_move(np.array([8,4]) - 1, current_color)
            # current_color *= -1
            # b.execute_move(np.array([6,3]) - 1, current_color)
            # current_color *= -1
            # b.execute_move(np.array([9,9]) - 1, current_color)
            # current_color *= -1
            # b.execute_move(np.array([8,9]) - 1, current_color)
            # current_color *= -1
        if cmd=='do':
            for i in tqdm(range(10)):
                for j in range(100):
                    mcts.search(b, current_color, pool)
        if cmd=='show best':
            next_move = show_best(mcts,b,current_color,debug=True)
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
