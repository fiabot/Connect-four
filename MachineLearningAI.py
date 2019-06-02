#Machine Learning AI
import pickle
import pandas
from connect4_v1 import GamePlay
from copy import deepcopy
from sklearn.neural_network import MLPClassifier
import numpy
import random


class MachineLearningAI:
    def __init__(self, player = 1, opp = 2):
        
        #load the models
        forest_name = '/home/fiabot/Desktop/connect_4/forest_model_stable.sav'
        self.forest_model = pickle.load(open(forest_name, 'rb'))

        svc_name = '/home/fiabot/Desktop/connect_4/svc_model_stable.sav'
        self.svc_model = pickle.load(open(svc_name, 'rb'))

        neigh_name = '/home/fiabot/Desktop/connect_4/neigh_model_stable.sav'
        self.neigh_model = pickle.load(open(neigh_name, 'rb'))

        neural_name = '/home/fiabot/Desktop/connect_4/neural_model_stable.sav'
        self.neural_model = pickle.load(open(neural_name, 'rb'))

        #current accuracies
        self.forest_ac =  0.7874764510630663
        self.svc_ac = 0.6587422624921504
        self.neigh_ac = 0.7239616040190185
        self.neural_ac = 0.8131784336592806

        self.highest_ac = self.neural_model

        #extra information about current models 
        self.test_sample = 0.33
        self.tree_samples= 1000 
        self_neigh_k = 4
        self.hidden_layers = (64,64)
        self.max_iter = 500

        #enter blank board
        self.board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

        #general game function
        self.game = GamePlay()

        #which player computer plays as 
        self.player = player
        self.opp = opp
        
    #convert board to be read by model 
    def convert_board(self, board):
        board_expanded = [[]]
        column_names = ["a1","a2"," a3"," a4","a5"," a6"," b1","b2"," b3"," b4"," b5"
                   ," b6"," c1"," c2","c3","c4","c5","c6"," d1","d2","d3","d4"
                   ,"d5","d6","e1","e2","e3","e4","e5","e6","f1","f2","f3","f4"
                   ,"f5","f6","g1","g2","g3","g4","g5","g6"]
        row = [5,4,3,2,1,0]
        for r in row:
            for c in range(7):
                board_expanded[0].append(board[r][c])
        
        formatted_board = pandas.DataFrame(numpy.array(board_expanded),
                                                    columns = column_names)
        return(formatted_board) 

    def predict_future_outcomes(self,model,board, moves): 
        outcomes = []
        for i in moves:
            b = deepcopy(board)
            b = self.game.add_play(i,b,self.player)
            b = b[0]
            b = self.convert_board(b)
            prediction = model.predict(b)
            outcomes.append(prediction[0])
        return outcomes
    def pick_move(self,board):
        copy = deepcopy(board)
        
        #find available moves 
        moves = self.game.moves_avail(copy) 
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        print("available moves", moves ) 

        #choice random move just in case 
        random_move = random.choice(moves)

        #prevent_win = deepcopy(moves) #list of moves that can prevent opp win
        do_not_play = [] 
        #if winning moves exists, win, remove any where opp wins 
        for i in moves:
            cur_wins = 0 
            copy = deepcopy(board)
            play = self.game.add_play(i,copy,self.player)
            copy= play[0]
            
            if self.game.check_win(copy,self.player) == "Winner":
                return i
            if play == "too many players in row":
                print("too many players in row") 
                continue 
            if self.game.opp_wins(copy,self.player,self.opp):
                do_not_play.append(i)
        do_play = []
        
        for i in moves:
            if i not in do_not_play:
                do_play.append(i)
        print(do_play) 
                
                
        #if loss cannot be prevented, choose randomly
        if len(do_play) == 0:
            return random.choice(moves)
        #if there is one way to block, do so
        elif len(do_play) == 1:
            return do_play[0] 
        else:
            #predict outcomes of all possible moves
            outcomes = self.predict_future_outcomes(self.highest_ac ,
                                                    board,do_play) 
            good_moves = []
            ok_moves = []
            bad_moves = []
            count = 0
            #sort predictions into wins, draws, or losses
            for i in outcomes:
                if i == self.player:
                    good_moves.append(do_play[count])
                elif i == 0:
                    ok_moves.append(do_play[count])
                else:
                    bad_moves.append(do_play[count]) 
                count += 1
            #if available good move, choice that, otherwise ok move
            #if all is lost, choice bad move 
            if len(good_moves) == 0:
                if len(ok_moves) == 0:
                    return random.choice(bad_moves)
                else:
                    return random.choice(ok_moves)
            else:
                return random.choice(good_moves)
        #if all goes horribly wrong return random move
        return random_move  
                           
            
        


