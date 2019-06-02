#display board and control human player
import pygame
import time 
from connect4_v1 import GamePlay
from copy import deepcopy
board = [[0,0,0,0,2,0,0],[1,1,0,0,0,0,0],[0,0,0,0,0,0,2],
                      [0,0,0,2,0,0,0],[0,0,0,0,0,0,1],[0,1,0,0,0,0,2]]


class Display:
    def __init__(self,width = 800, height = 500, fill_color = (255,255,255),
                 border = 20, player1 = (255,0,0), player2 = (0,0,255),
                 select_color = (111, 239, 67),blank = (255, 221, 2),
                 top_space = 0, left_space = 0, text_space = 200,
                 inst_space = 200):
        #initialize pygame 
        pygame.init()

        #create screen 
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('connect 4')
        
        #start up screen setting
        self.centerx = width/2
        self.centery = height/2 
        self.player1_x = self.centerx - text_space
        self.player2_x = self.centerx + text_space
        self.inst_y = self.centery - inst_space
        
        #circle demensions 
        self.boarder = border
        self.square_width = (width-left_space)/7
        self.square_height = (height- top_space)/6
        self.permeter = 2*(self.square_width - self.boarder) +\
                        2*(self.square_height - self.boarder)
        self.diameter = self.permeter/8 #diameter of circle
        self.x_adder = -top_space
        self.y_adder = left_space

        #set up colors
        self.fill_color = fill_color
        self.py1_color = player1
        self.py2_color = player2
        self.bk_color = blank
        self.st_color = select_color
        self.black = (0,0,0)
        
    def set_up_screen(self,players):
        player1_index = 0
        player2_index = 0
        player_control = 1
        while True: 
            self.screen.fill(self.fill_color)
            
            largeText = pygame.font.Font('freesansbold.ttf',40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

            #use arrow keys to select players, enter to return 
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                player_control = 1
            if pressed[pygame.K_RIGHT]:
                player_control = 2
            if pressed[pygame.K_DOWN]:
                if player_control == 1:
                    if player1_index >= (len(players)-1):
                        player1_index = 0
                    else:
                        player1_index += 1
                if player_control == 2:
                    if player2_index >= (len(players) - 1):
                        player2_index = 0
                    else:
                        player2_index += 1
            if pressed[pygame.K_UP]:
                if player_control == 1:
                    if player1_index <= 0:
                        player1_index = len(players) -1 
                    else:
                        player1_index += -1
                if player_control == 2:
                    if player2_index <= 0:
                        player2_index = len(players) - 1
                    else:
                        player2_index += -1
            if pressed[pygame.K_SPACE]:
                break
            
            if player_control == 1:
                colors = [self.st_color, self.black]
            else:
                colors = [self.black, self.st_color]

            #display instructions 
            instructions = ["Use arrow keys to select players",
                            "press space when done"]
            
            inst1_surf = largeText.render(instructions[0], True, self.black)
            inst2_surf = largeText.render(instructions[1], True, self.black)

            inst1_rect = inst1_surf.get_rect()
            inst2_rect = inst2_surf.get_rect()

            inst1_rect.center = ((self.centerx),(self.inst_y))
            self.screen.blit(inst1_surf, inst1_rect)
            inst2_rect.center = ((self.centerx),(self.inst_y+30))
            self.screen.blit(inst2_surf, inst2_rect)

            #display players 
            player1_surf = largeText.render(str(players[player1_index]),
                                                True, colors[0])
            player1_rect = player1_surf.get_rect()
    
            player1_rect.center = ((self.player1_x),(self.centery))
            self.screen.blit(player1_surf, player1_rect)

            player2_surf = largeText.render(str(players[player2_index]),
                                                True, colors[1])
            player2_rect = player2_surf.get_rect()
                                           
            player2_rect.center = ((self.player2_x),(self.centery))
            self.screen.blit(player2_surf, player2_rect)

            pygame.display.flip()

            time.sleep(0.1)
        return [players[player1_index], players[player2_index]] 
            
    def draw_board(self, board):
        self.screen.fill(self.fill_color)
        row = 5
        for r in range(1,7):
            square_top = r*self.square_height
            square_bottom = (r-1)*self.square_height
            circle_y = (square_top + square_bottom)/2
            col = 6
            for c in range(1,8):
                #set up circle pos 
                square_right = c*self.square_width
                square_left = (c-1)*self.square_width
                circle_x = (square_right + square_left)/2

                #determine circle color
                if board[r-1][c-1] == 1:
                    color = self.py1_color
                elif board [r-1][c-1] == 2:
                    color = self.py2_color
                else:
                    color = self.bk_color
                
                
                pygame.draw.circle(self.screen, (color),
                                   (circle_x + self.x_adder,
                                    circle_y + self.y_adder), self.diameter)
    def show_selection(self, pos):
        #set up circle position
        square_top = 1*self.square_height
        square_bottom = 0
        circle_y = (square_top + square_bottom)/2
        
        square_right = (pos+1)*self.square_width
        square_left = (pos)*self.square_width
        circle_x = (square_right + square_left)/2

        pygame.draw.circle(self.screen, (self.st_color),
                                   (circle_x + self.x_adder,
                                    circle_y + self.y_adder), self.diameter)

    def player_select(self,moves, board):
        move_index = 0
        selected = None
        
        while selected is None:
            self.draw_board(board)
            self.show_selection(moves[move_index])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and not move_index == 0:
                move_index -= 1
                
            if pressed[pygame.K_RIGHT] and not move_index == (len(moves)-1):
                move_index += 1

            if pressed[pygame.K_DOWN]:
                selected = moves[move_index]
                
            pygame.display.flip()
            time.sleep(0.1) 
        return selected
    
    def end_screen(self, winner):
        time.sleep(2) 
        largeText = pygame.font.Font('freesansbold.ttf',35)
        play_again = True
        while True:
            self.screen.fill(self.fill_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

            #use arrow keys to select players, enter to return 
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                play_again = True
            if pressed[pygame.K_RIGHT]:
                play_again = False
            if pressed[pygame.K_SPACE]:
                break

            #print instructions 
            instructions = ["player "+ str(winner) + " won" , 
                                "Do you want to play again?" ]
            inst1_surf = largeText.render(instructions[0], True, self.black)
            inst2_surf = largeText.render(instructions[1], True, self.black)

            inst1_rect = inst1_surf.get_rect()
            inst2_rect = inst2_surf.get_rect()

            inst1_rect.center = ((self.centerx),(self.inst_y))
            self.screen.blit(inst1_surf, inst1_rect)
            inst2_rect.center = ((self.centerx),(self.inst_y+30))
            self.screen.blit(inst2_surf, inst2_rect)

            #display options
            if play_again:
                colors = [self.st_color, self.black]
            else:
                colors = [self.black, self.st_color]
                    
            yes_surf = largeText.render("Yes!", True, colors[0])
            yes_rect = yes_surf.get_rect()

            yes_rect.center = ((self.player1_x),(self.centery))
            self.screen.blit(yes_surf, yes_rect)

            no_surf = largeText.render("No", True, colors[1])
            no_rect = no_surf.get_rect()
                                           
            no_rect.center = ((self.player2_x),(self.centery))
            self.screen.blit(no_surf, no_rect)

            pygame.display.flip()

            time.sleep(0.1)
        if not play_again:
            pygame.display.quit()
        return play_again

        

class HumanPlayer:
    def __init__(self, player = 2, opp= 1, display = Display()):
        self.player = player
        self.opp = opp
        self.display = display 
    def pick_move(self, board):
        game = GamePlay()
        copy = deepcopy(board)
        moves = game.moves_avail(copy)
        
        if moves == "no moves available":
            print("no moves available") 
            return "no moves available"
        play = self.display.player_select(moves, board)
            
        return(play)     


                
                

"""display = Display() 

print(display.player_select([0,1,2,3,5,6], board))
display.draw_board(board)
pygame.display.flip()
"""
