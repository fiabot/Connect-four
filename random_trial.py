#random trial AI
from connect4_v1 import GamePlay
from copy import deepcopy
import random 

#currently messed up
#most likely something with copies
#also we still need to fix input for moves
class RandomTrialAI:
    def __init__(self, player = 1, opp = 2):
        self.auto_AI = "best_rand"
        self.player = player
        self.opp = opp
        self.game = GamePlay()

    # uses offense only 
    def offense (self,board,piece,opp):
        copy = deepcopy(board)
        cur_wins = 0
        most_wins = 0
        
        moves = self.game.moves_avail(copy)
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        best_move = self.game.random.choice(moves) 
        #repeat for each move
        for i in moves: 
            cur_wins = 0 
            copy = deepcopy(board)
            play = self.game.add_play(i,copy,piece)
            copy= play[0] 
            if self.game.check_win(copy,piece) == "Winner":
                return i
            if play == "too many players in row":
                print("too many players in row") 
                continue 
            if self.game.opp_wins(copy,piece,opp):
                
                continue  
            
            #repeat for number of trails 
            for p in range(100):
                
                # reset board with current piece
                copy = deepcopy(board)
                play = self.game.add_play(i,copy,piece)
                copy= play[0]
                 
                #repeat for number of future moves
                for n in range(5):
                    #add random opponent play
                    moves = self.game.moves_avail(copy)
                    if moves == "no moves available":
                        print("no moves", board)
                        break
                    play = self.game.add_play(random.choice(moves),copy,opp)
                    if copy == "t":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,opp)  
                        copy = play[0]
                    copy = play[0]
                    if copy == "t":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,opp)  
                        copy = play[0] 
                    #add random AI play
                    if self.game.moves_avail(copy) == "no moves available":
                        break
                    play = self.game.add_play(random.choice(moves),copy,piece)
                    if play == "too many players in row":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,piece)
                        copy = play[0] 
                    copy = play[0]
                    
                    #if AI won add points
                    if self.game.check_win(copy,piece) == "Winner":
                        cur_wins += 1
                        break
            #if this move is better then the highest so far  
            if cur_wins > most_wins:
                most_wins = cur_wins
                best_move = i  
         
        if self.game.add_play(best_move,copy,opp) == "too many players in row":
            best_move = random.choice(moves)   
                
        return best_move

    #uses defense only
    # uses a combination of offense and deffense 
    def defense(self,board,piece,opp):
        copy = deepcopy(board)
        cur_wins = 0
        most_wins = 0
        
        moves = self.game.moves_avail(copy)
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        best_move = random.choice(moves) 
        #repeat for each move
        for i in moves: 
            cur_wins = -100 
            copy = deepcopy(board)
            play = add_play(i,copy,piece)
            copy= play[0] 
            if self.game.check_win(copy,piece) == "Winner":
                return i
            if play == "too many players in row":
                print("too many players in row") 
                continue 
            if self.game.opp_wins(copy,piece,opp):
                    continue  
            
            #repeat for number of trails 
            for p in range(100):
                
                # reset board with current piece
                copy = deepcopy(board)
                play = self.game.add_play(i,copy,piece)
                copy= play[0]
                 
                #repeat for number of future moves
                for n in range(5):
                    #add random opponent play
                    moves = self.game.moves_avail(copy)
                    if moves == "no moves available":
                        print("no moves in future moves", copy)
                        break
                    play = self.game.add_play(random.choice(moves),copy,opp)
                    if copy == "t":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,opp)  
                        copy = play[0]
                    copy = play[0]
                    if copy == "t":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,opp)  
                        copy = play[0] 
                    #add random AI play
                    if moves_avail(copy) == "no moves available":
                        break
                    play = self.game.add_play(random.choice(moves),copy,piece)
                    if play == "too many players in row":
                        while play == "too many players in row":
                            play = self.game.add_play(random.choice(moves),copy,piece)
                        copy = play[0] 
                    copy = play[0]
                    
                    # if opponent won subtract points 
                    if self.game.check_win(copy,opp) == "Winner":
                        cur_wins -= 1
                        break
            #if this move is better then the highest so far  
            if cur_wins > most_wins:
                most_wins = cur_wins
                best_move = i  
         
        if self.game.add_play(best_move,copy,opp) == "too many players in row":
            best_move = random.choice(moves)   
                
        return best_move

    # uses a combination of offense and deffense 
    def best_rand(self,board,piece,opp):
        copy = deepcopy(board)
        cur_wins = 0
        most_wins = 0
        
        moves = self.game.moves_avail(copy)
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        best_move = random.choice(moves)
        #prevent_win = deepcopy(moves) #list of moves that can prevent opp win
        do_not_play = [] 
        #if winning moves exists, win, remove any where opp wins 
        for i in moves:
            cur_wins = 0 
            copy = deepcopy(board)
            play = self.game.add_play(i,copy,self.player)
            copy= play[0]
            
            if self.game.check_win(copy,self.player) == "Winner":
                print("choosing the winning move")
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
        #repeat for each move
        for i in do_play:
            cur_wins = -100 
            copy = deepcopy(board)
            play = self.game.add_play(i,copy,piece)
            copy= play[0]  
            
            #repeat for number of trails 
            for p in range(200):
                
                # reset board with current piece
                copy = deepcopy(board)
                play = self.game.add_play(i,copy,piece)
                copy= play[0]
                 
                #repeat for number of future moves
                for n in range(5):
                        #add random opponent play
                        moves = self.game.moves_avail(copy)
                        if moves == "no moves available":
                            break
                        play = self.game.add_play(random.choice(moves),copy,opp)
                        if copy == "t":
                            while play == "too many players in row":
                                play = self.game.add_play(random.choice(moves),copy,opp)  
                            copy = play[0]
                        copy = play[0]
                        if copy == "t":
                            while play == "too many players in row":
                                play = self.game.add_play(random.choice(moves),copy,opp)  
                            copy = play[0] 
                        #add random AI play
                        if self.game.moves_avail(copy) == "no moves available":
                            break
                        play = self.game.add_play(random.choice(moves),copy,piece)
                        if play == "too many players in row":
                            while play == "too many players in row":
                                play = self.game.add_play(random.choice(moves),copy,piece)
                            copy = play[0] 
                        copy = play[0]
                        
                        #if AI won add points
                        if self.game.check_win(copy,piece) == "Winner":
                            cur_wins += 28
                            break
                        # if opponent won subtract points 
                        if self.game.check_win(copy,opp) == "Winner":
                            cur_wins -= 1
                            break
                #if this move is better then the highest so far  
                if cur_wins > most_wins:
                    most_wins = cur_wins
                    best_move = i  
         
            if self.game.add_play(best_move,copy,opp) == "too many players in row":
                best_move = random.choice(moves)
        print(best_move)
        return best_move
    def pick_move(self, board):
        return self.best_rand(board,self.player,self.opp)
