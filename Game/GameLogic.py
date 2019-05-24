'''
Author: Miaozha
Date: 5 23, 2019.
Board class.
Board data:
  1=cricle, -1=cross, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
import numpy as np
import pickle
class Board():

    def __init__(self,n):
        "Set up initial board configuration."
        self.pieces = np.zeros([9,9],dtype=np.int8)
        self.main_pieces= np.zeros([3,3],dtype=np.int8)
        self.main_pieces_finished= np.zeros([3,3],dtype=np.int8)
        self.last_move=None
        self.activation_zone=None
        self.finished=False
        self.winner=0
        
    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color"""
        return np.sum(self.pieces)

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        """
        moves = set()  # stores the legal moves.
        
        if self.activation_zone==None:
            return np.asarray(np.where(self.pieces==0),dtype=np.int8).transpose()
        
        sub_board=self.get_sub_board(self.activation_zone)
        legal_indices_sub=np.where(sub_board==0)
        return self.to_board_index(legal_indices_sub,self.activation_zone).transpose()

    def has_legal_moves(self, color):
        return not self.finished

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play 
        """
        if self.finished:
            raise Exception('execute move while the game is already finished!')
        # update board
        x,y=move
        self.pieces[x,y]=color
        
        self.last_move=[[x//3,y//3],[x%3,y%3]]
        last_move_zone_x,last_move_zone_y=self.last_move[0]
        last_move_sub_x,last_move_sub_y=self.last_move[1]
        
        # update the status of the current subboard to the main board
        if self.sub_board_win(self.get_sub_board(self.last_move[0]),self.last_move[1]):
            self.main_pieces[last_move_zone_x,last_move_zone_y]=color
            self.main_pieces_finished[last_move_zone_x,last_move_zone_y]=1
            # check whether the current color wins:
            if self.sub_board_win(self.main_pieces,self.last_move[0]):
                self.finished=True
                self.winner=color
                return self
        elif len(np.where(self.get_sub_board(self.last_move[0])==0)[0])==0:
            self.main_pieces_finished[last_move_zone_x,last_move_zone_y]=1
        
        if len(np.nonzero(self.main_pieces_finished.reshape(-1))[0])==9:
            self.finished=True
            return self
        
        # update the new activation zone
        if self.main_pieces_finished[last_move_sub_x,last_move_sub_y]==0:
            self.activation_zone=self.last_move[1]
        else:
            self.activation_zone=None
        return self

    def get_sub_board(self,move):
        x,y=move
        return self.pieces[3*x:3*x+3,3*y:3*y+3]

    def to_board_index(self,index_at_sub_board,sub_board_index):
        index_at_sub_board_x,index_at_sub_board_y=index_at_sub_board
        sub_board_x,sub_board_y=sub_board_index
        return np.asarray([index_at_sub_board_x+3*sub_board_x,index_at_sub_board_y+3*sub_board_y],dtype=np.int8)

    def fill_test_pattern(self):
        for i in range(9):
            for j in range(9):
                next_move(self.pieces,i,j,i*10+j)

    def sub_board_win(self,sub_board,last_move):
        last_x,last_y=last_move
        last_c=sub_board[last_x,last_y]
        if len(set(sub_board[last_x]))==1:
            return True
        if len(set(sub_board[:,last_y]))==1:
            return True
        if last_x==last_y and len(set([sub_board[0,0],sub_board[1,1],sub_board[2,2]]))==1:
            return True
        if last_x+last_y==2 and len(set([sub_board[0,2],sub_board[1,1],sub_board[2,0]]))==1:
            return True
        return False
    
    def tostring(self):
#         return pickle.dumps(self)
#         return self.pieces.tostring()
        return str(self.pieces)+str(self.activation_zone)