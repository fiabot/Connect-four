#goal: find the ratio of offense to deffense in a game of connect 4 
import random
from operator import itemgetter
from copy import deepcopy

#note in board[a][b] a is rows from the top and b is columns from the left
#ps COLUMNS ARE VERTICAL and ROWS ARE HORAZONTAL
# create an empty board to work with
board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,]]

#a function that takes a column numer and adds it to the next row number 
def add_play (col,board,player):
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
def check_win(board,piece):
    #check for horazontal win
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
 
# returns a list of moves available 
def moves_avail(board):
    copy = deepcopy(board)
    moves = []
    for i in range(7):
        play = add_play(i,copy,1)
        if not play == "too many players in row":
            moves.append(i)
    if moves == []:
        return "no moves available"
    else: return moves

# returns true if opponent can win next turn    
def opp_wins(board,piece,opp):
    
    for i in range(7):
        copy = deepcopy(board)
        play = add_play(i,copy,opp)
        if play == "too many players in row":
            return False 
        copy = play[0]
        
        if check_win(copy,opp) == "Winner": 
            return True
    else: return False
    
# uses offense only 
def offense (board,piece,opp):
    copy = deepcopy(board)
    cur_wins = 0
    most_wins = 0
    
    moves = moves_avail(copy)
    if moves == "no moves available":
        print("no moves available") 
        return "no moves available"
    best_move = random.choice(moves) 
    #repeat for each move
    for i in moves: 
        cur_wins = 0 
        copy = deepcopy(board)
        play = add_play(i,copy,piece)
        copy= play[0] 
        if check_win(copy,piece) == "Winner":
            return i
        if play == "too many players in row":
            print("too many players in row") 
            continue 
        if opp_wins(copy,piece,opp):
            
            continue  
        
        #repeat for number of trails 
        for p in range(100):
            
            # reset board with current piece
            copy = deepcopy(board)
            play = add_play(i,copy,piece)
            copy= play[0]
             
            #repeat for number of future moves
            for n in range(5):
                #add random opponent play
                moves = moves_avail(copy)
                if moves == "no moves available":
                    print("no moves")
                    break
                play = add_play(random.choice(moves),copy,opp)
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0]
                copy = play[0]
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0] 
                #add random AI play
                if moves_avail(copy) == "no moves available":
                    break
                play = add_play(random.choice(moves),copy,piece)
                if play == "too many players in row":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,piece)
                    copy = play[0] 
                copy = play[0]
                
                #if AI won add points
                if check_win(copy,piece) == "Winner":
                    cur_wins += 1
                    break
        #if this move is better then the highest so far  
        if cur_wins > most_wins:
            most_wins = cur_wins
            best_move = i  
     
    if add_play(best_move,copy,opp) == "too many players in row":
        best_move = random.choice(moves)   
            
    return best_move
#uses defense only
# uses a combination of offense and deffense 
def deffense(board,piece,opp):
    copy = deepcopy(board)
    cur_wins = 0
    most_wins = 0
    
    moves = moves_avail(copy)
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
        if check_win(copy,piece) == "Winner":
            return i
        if play == "too many players in row":
            print("too many players in row") 
            continue 
        if opp_wins(copy,piece,opp):
                continue  
        
        #repeat for number of trails 
        for p in range(100):
            
            # reset board with current piece
            copy = deepcopy(board)
            play = add_play(i,copy,piece)
            copy= play[0]
             
            #repeat for number of future moves
            for n in range(5):
                #add random opponent play
                moves = moves_avail(copy)
                if moves == "no moves available":
                    print("no moves")
                    break
                play = add_play(random.choice(moves),copy,opp)
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0]
                copy = play[0]
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0] 
                #add random AI play
                if moves_avail(copy) == "no moves available":
                    break
                play = add_play(random.choice(moves),copy,piece)
                if play == "too many players in row":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,piece)
                    copy = play[0] 
                copy = play[0]
                
                # if opponent won subtract points 
                if check_win(copy,opp) == "Winner":
                    cur_wins -= 1
                    break
        #if this move is better then the highest so far  
        if cur_wins > most_wins:
            most_wins = cur_wins
            best_move = i  
     
    if add_play(best_move,copy,opp) == "too many players in row":
        best_move = random.choice(moves)   
            
    return best_move

# uses a combination of offense and deffense 
def best_rand (board,piece,opp):
    copy = deepcopy(board)
    cur_wins = 0
    most_wins = 0
    
    moves = moves_avail(copy)
    if moves == "no moves available":
        print("no moves available") 
        return "no moves available"
    best_move = random.choice(moves)
    #repeat for each move
    print("loading", end = "")
    for i in moves: 
        cur_wins = -100 
        copy = deepcopy(board)
        play = add_play(i,copy,piece)
        copy= play[0] 
        if check_win(copy,piece) == "Winner":
            print("") 
            return i
        if play == "too many players in row":
            print("too many players in row") 
            continue 
        if opp_wins(copy,piece,opp):
            #print("oppent won:" + str(i)) 
            continue  
        
        #repeat for number of trails 
        for p in range(200):
            if p % 100 == 0:
                print(".", end = "")
            # reset board with current piece
            copy = deepcopy(board)
            play = add_play(i,copy,piece)
            copy= play[0]
             
            #repeat for number of future moves
            for n in range(5):
                #add random opponent play
                moves = moves_avail(copy)
                if moves == "no moves available":
                    print("no moves")
                    break
                play = add_play(random.choice(moves),copy,opp)
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0]
                copy = play[0]
                if copy == "t":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,opp)  
                    copy = play[0] 
                #add random AI play
                if moves_avail(copy) == "no moves available":
                    break
                play = add_play(random.choice(moves),copy,piece)
                if play == "too many players in row":
                    while play == "too many players in row":
                        play = add_play(random.choice(moves),copy,piece)
                    copy = play[0] 
                copy = play[0]
                
                #if AI won add points
                if check_win(copy,piece) == "Winner":
                    cur_wins += 28
                    break
                # if opponent won subtract points 
                if check_win(copy,opp) == "Winner":
                    cur_wins -= 1
                    break
        #if this move is better then the highest so far  
        if cur_wins > most_wins:
            most_wins = cur_wins
            best_move = i  
     
    if add_play(best_move,copy,opp) == "too many players in row":
        best_move = random.choice(moves)
    print("")
    return best_move

def player_play(board,piece,opp):
    copy = deepcopy(board)
    moves = moves_avail(copy)
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
    if add_play(play,board,piece) == "too many players in row":
        while add_play(play,board,piece) == "too many players in row":
            print("invalid move please choose again")
            play = input("Choose a column:")
            play = int(play)
    return(play) 
#plays a game with x and y methods
def play_game(b,method_1, method_2):
    board = deepcopy(b)
    
    while not check_win(board,1) == "Winner" and not check_win(board,2) == "Winner":
        move_1 = method_1(board,1,2)
        if move_1 == "no moves available":
            break
        else: 
            play = add_play(move_1,board,1)
            board = play[0]
        if check_win(board,1):
            break 
        move_2 = method_2(board,2,1)
        if move_2 == "no moves available":
            break
        else: 
            play = add_play(move_2,board,2)
            board = play[0]
    print(board[0])
    print(board[1])
    print(board[2])
    print(board[3])
    print(board[4])
    print(board[5])
    if check_win(board,1) == "Winner":
        return 1 #method 1 won
    elif check_win(board,2) == "Winner":
        return 2 #method 2 won
    else: return 0 # there was a tie

                
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
##
print("You are player number 2") 
game = play_game(board,best_rand,player_play)
if game == 1:
    print("Computer won")
elif game == 2:
    print("Player won")
else:
    print ("tie")




