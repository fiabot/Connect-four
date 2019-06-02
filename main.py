#play game
from MachineLearningAI import MachineLearningAI
from display import Display
from display import HumanPlayer
from random_trial import RandomTrialAI
from connect4_v1 import GamePlay
import pygame
import time 
class main:
    def __init__(self): 
        self.gameplay = GamePlay()
        self.display = Display()
        self.board = board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,]]
        self.display.draw_board(board)
        self.machine_AI = MachineLearningAI(1,2)
        self.random_AI = RandomTrialAI(1,2)
        self.human_player = HumanPlayer(2,1,self.display)
        self.show = True
    def start(self):
        choice = self.display.set_up_screen(["human player",
                                             "Neural Net AI",
                                             "Random Trial AI"])
        if choice[0] == "human player":
            choice[0] = self.human_player
        elif choice[0] == "Random Trial AI":
            choice[0] = self.random_AI
        else:
            choice[0] = self.machine_AI
        if choice[1] == "human player":
            choice[1] = self.human_player
        elif choice[1] == "Random Trial AI":
            choice[1] = self.random_AI
        else:

            choice[1] = self.machine_AI

        choice[0].player = 1
        choice[0].opp = 2
        choice[1].player = 2
        choice[1].opp = 1
        self.method_1 = choice[0]
        self.method_2 = choice[1]
                                
    #plays a game with x and y methods
    def play_game(self):
        board = self.board
        while not self.gameplay.check_win(board,1) == "Winner" and \
              not self.gameplay.check_win(board,2) == "Winner":
            self.display.draw_board(board)
            pygame.display.flip()
            move_1 = self.method_1.pick_move(board)
            if move_1 == "no moves available":
                break
            else: 
                play = self.gameplay.add_play(move_1,board,1)
                board = play[0]
            if self.gameplay.check_win(board,1):
                break
            self.display.draw_board(board)
            pygame.display.flip()
            move_2 = self.method_2.pick_move(board)
            if move_2 == "no moves available":
                break
            else: 
                play = self.gameplay.add_play(move_2,board,2)
                board = play[0]
        if self.show:
            self.display.draw_board(board)
            pygame.display.flip()
        if self.gameplay.check_win(board,1) == "Winner":
            return 1 #method 1 won
        elif self.gameplay.check_win(board,2) == "Winner":
            return 2 #method 2 won
        else: return 0 # there was a tie
    def play_again(self,winner):
        return self.display.end_screen(winner) 

game = main()

while True:
    game.start()
    winner = game.play_game()
    if not game.play_again(winner):
        break
    time.sleep(0.1) 


