#goal: find the ratio of offense to deffense in a game of connect 4 
import random
from operator import itemgetter
from copy import deepcopy
import pygame

#note in board[a][b] a is rows from the top and b is columns from the left
#ps COLUMNS ARE VERTICAL and ROWS ARE HORAZONTAL

class GamePlay:
    def __init__(self):
        self.board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],[0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,]]
    #a function that takes a column numer and adds the move
    #returns new board and row number 
    def add_play (self,col,board,player): 
        copy = deepcopy(board) 
        row_num = 5
        placed = False
        for i in range(0,6): 
            if copy[row_num][col] == 0:
                copy[row_num][col] = player
                placed = True
            if placed:
                return (copy,row_num) 
            row_num -= 1 
            
        return "too many players in row"


    #checks to see if there is a winner 
    def check_win(self,board,piece):
        #check for horazontal win
        if not isinstance(board, str):
            for i in range(6):
                #print(i) 
                #win 1, start with first piece to the left
                if board[i][0] == piece and board[i][1] == piece and board[i][2] == piece and board[i][3] == piece:
                    return "Winner"
                #win 2, start with second piece to the left 
                if board[i][1] == piece and board[i][2] == piece and board[i][3] == piece and board[i][4] == piece:
                    return "Winner"
                #win 3, start with third piece to the left
                if board[i][2] == piece and board[i][3]== piece and board[i][4] == piece and board[i][5] == piece:
                    return "Winner"
                #win 4, start with forth piece to the left 
                if board[i][3] == piece and board[i][4] == piece and board[i][5] == piece and board[i][6] == piece:
                    return "Winner"
            #check for vertical win
            for i in range(7):
                #win 1, start with first piece to the top
                if board[0][i] == piece and board[1][i] == piece and board[2][i] == piece and board[3][i] == piece:
                    return "Winner"
                #win 2, start with second piece to the top 
                if board[1][i] == piece and board[2][i] == piece and board[3][i] == piece and board[4][i] == piece:
                    return "Winner"
                #win 3, start with third piece to the top
                if board[2][i] == piece and board[3][i]== piece and board[4][i] == piece and board[5][i] == piece:
                    return "Winner"
            #check for positive diagonal win
            for i in range(4):
                start= 3
                for g in range(3):
                    if board[start][i] == piece and board[start-1][i+1] == piece and board[start-2][i+2] == piece and board[start-3][i+3] == piece:
                        return "Winner"
                    start += 1 
            #check for negitve diagonal win
            for i in range(4):
                start= 0
                for g in range(3):
                    if board[start][i] == piece and board[start+1][i+1] == piece and board[start+2][i+2] == piece and board[start+3][i+3] == piece:
                        return "Winner"
                    start += 1
        else: return None 
     
    # returns a list of moves available 
    def moves_avail(self,board):
        copy = deepcopy(board)
        moves = []
        for i in range(7):
            play = self.add_play(i,copy,1)
            if not play == "too many players in row":
                moves.append(i)
        if moves == []:
            return "no moves available"
        else: return moves

    # returns true if opponent can win next turn    
    def opp_wins(self,board,piece,opp):
        
        for i in range(7):
            copy = deepcopy(board)
            play = self.add_play(i,copy,opp)
            if play == "too many players in row":
                return False 
            copy = play[0]
            
            if self.check_win(copy,opp) == "Winner": 
                return True
        else: return False

    
"""class HumanPlayer:
    def __init__(self, piece = 2, opp= 1):
        self.piece = piece
        self.opp = opp
    def pick_move(self, board):
        game = GamePlay()
        copy = deepcopy(board)
        moves = game.moves_avail(copy)
        print(board[0])
        print(board[1])
        print(board[2])
        print(board[3])
        print(board[4])
        print(board[5])
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        play = input("Choose a column:")
        play = int(play)
        if play > 6:
            while play > 6:
                print("Not a Valid Column, please enter a number between 0-6")
                play = input("Choose a Column:")
        if game.add_play(play,board,self.piece) == "too many players in row":
            while game.add_play(play,board,self.piece) == "too many players in row":
                print("invalid move please choose again")
                play = input("Choose a column:")
                play = int(play)
        return(play)  """   



"""board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,]]
display = Display()
display.draw_board(board) 
game = GamePlay(display)
AI = ComputerAI()
human = HumanPlayer(2,1,display)

game.play_game(board, AI, human)


                
board_copy = deepcopy(board)
fake_board = [[],[],[],[],[],[]]
fake_board[0] = [0,0,0,1,0,0,0]
fake_board[1] = [0,0,0,2,0,0,0]
fake_board[2] = [0,0,0,2,0,0,0]
fake_board[3] = [0,0,0,2,0,0,0]
fake_board[4] = [0,0,0,1,0,0,0]
fake_board[5] = [2,2,1,1,0,0,0]


##print(best_rand(fake_board,1,2)) 
#print(moves_avail(fake_board)) 
#print(offensive(fake_board,1,2))
#print(dig_moves(1,2,False))
#print(board)            
#print(best_rand(fake_board,1,2))

win_1 = 0
win_2 = 0
tie = 0

##for i in range(5):
##    game = (play_game(board,offense,deffense))
##    if game == 1:
##        win_1 += 1
##    elif game == 2:
##        win_2 += 1
##    elif game == 0:
##        tie += 1
##    game = (play_game(board,deffense,offense))
##    if game == 1:
##        win_2 += 1
##    elif game == 2:
##        win_1 += 1
##    elif game == 0:
##        tie += 1
##    print(win_1)
##    print(win_2) 
##
##print("offense:" + str(win_1))
##print("deffense:" + str(win_2))
##print("Tie:" + str(tie))
##'
print("You are player number 2")
game = GamePlay()
AI = RandomTrialAI()
score = game.play_game(board,player_play,player_play)
if score == 1:
    print("Player 1 won")
elif score == 2:
    print("Player 2 won")
else:
    print ("tie")"""
