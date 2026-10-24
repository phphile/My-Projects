""" Pong game using pygame"""

__author__ = "le_p"


import pygame, sys, random
from pygame.locals import *

pygame.init()

# Clock
FPS = 30 
FPSClock = pygame.time.Clock()

# Couleurs
BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Surface 
flag = pygame.SCALED
WIDTH = 1000
HEIGHT = 500
GAMESURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# 2 rectangles for 2 players
bar_width = 20
bar_height = 150

bar1_width, bar1_height = bar_width, bar_height
bar1_x, bar1_y = 30, HEIGHT/2 - bar1_height/2


bar2_width, bar2_height = bar_width, bar_height
bar2_x, bar2_y = 950, HEIGHT/2 - bar2_height/2

bar1_y_move, bar2_y_move = bar1_y, bar2_y

attack_for_left, attack_for_right = False, False
fired_right, fired_left = False, False 
attempt_left, attempt_right = 0, 0


def attack():
    """
    Faire dispaitre un morceau de la barre adversaire, 
    attaque possible apres chaque 5 points gagnes 
    """
    global attack_for_left, attack_for_right, fired_right, fired_left, attempt_left, attempt_right
    attack_font = pygame.font.Font(None, 50)
    attack_msg_left = attack_font.render("Attack! Press A", True, RED, None)
    attack_msg_right = attack_font.render("Pow! Press P", True, RED, None)
    if attack_for_left  and not fired_left and attempt_left == 0:
        GAMESURFACE.blit(attack_msg_left, (WIDTH/4 - attack_msg_left.get_width()/2, 75))
    if attack_for_right  and not fired_right and attempt_right == 0:    
        GAMESURFACE.blit(attack_msg_right, (WIDTH/2 + (WIDTH/4 - attack_msg_right.get_width()/2), 75))

def cut_adversary():
    global bar1_height, bar2_height
    global fired_left, fired_right, attack_for_left, attack_for_right
    global attempt_left, attempt_right
    if attack_for_left and not fired_left and attempt_left == 1:    
        bar2_height -= 10
        attack_for_left = False
        fired_left = True
        attempt_left = 0
    if attack_for_right and not fired_right and attempt_right == 1:
        bar1_height -= 10
        attack_for_right = False
        fired_right = True
        attempt_right = 0
              

# balle : un carre 
cote = 20
xball = WIDTH / 2 
yball= HEIGHT / 2
#ball_rect = pygame.Rect((xball, yball), (cote, cote))
velocity_x = 0.3 # randomiser velocity_x pour faire varier l'angle du tracjectoire 
velocity_y = 0.5
directions = ('downright', 'upright', 'downleft', 'upleft')
direction = directions[random.randint(0, 3)] #randomiser les directions
#barrierx = WIDTH / 2
def accelerate_ball():
    global velocity_y
    velocity_y += 0.25

def randomize_angle():
    global velocity_x
    velocity_x = random.uniform(0.25, 0.8)

def new_ball():
    global xball, yball
    global direction
    direction = directions[random.randint(0, 3)]
    xball = WIDTH / 2 
    yball = HEIGHT / 2
    randomize_angle()
    pygame.draw.rect(GAMESURFACE, WHITE, (xball, yball, cote, cote), 0)



# Score 
bestscore = 0 
score_init_left = 0 
score_init_right = 0 
score_font = pygame.font.Font(None, 60)
score_left = score_font.render(str(score_init_left), True, WHITE, None)
score_right = score_font.render(str(score_init_right), True, WHITE, None)

# Barriere
barrier_width, barrier_height = 20, 500
xbarrier = WIDTH / 2 - barrier_width / 2
ybarrier = 0

# Collions:
goal_left = False
goal_right = False


# Move the bars
bar1_up, bar1_down = False, False
bar2_up, bar2_down = False, False
def slid_right_bar():
    global bar2_y_move, bar2_x, bar2_y, bar_width, bar_height
    if bar2_y_move > 0 and bar2_up:
        bar2_y_move -= 1
    if bar2_y_move + bar_height < HEIGHT and bar2_down:
        bar2_y_move += 1
    pygame.draw.rect(GAMESURFACE, WHITE, (bar2_x, bar2_y_move, bar2_width, bar2_height), 0)

def slid_left_bar():
    global bar1_y_move, bar1_x, bar1_y, bar_height, bar_width
    if bar1_y_move > 0 and bar1_up:
        bar1_y_move -= 1
    if bar1_y_move + bar_height < HEIGHT and bar1_down:
        bar1_y_move += 1
    pygame.draw.rect(GAMESURFACE, WHITE, (bar1_x, bar1_y_move, bar1_width, bar1_height), 0)

# Game over
def gameover():
    GAMESURFACE.fill(BGCOLOR)
    msg_font = pygame.font.Font(None, 50)
    msg_text = msg_font.render("Game Over. Play again ? (Press Y to continue)", True, WHITE, None)
    msg_frame = msg_text.get_rect()
    msg_frame.center = (WIDTH/2, HEIGHT/2)
    
    # Draw the welcome screen
    GAMESURFACE.blit(msg_text, msg_frame)

# Update scores
def update_score():
    global score_init_left, score_init_right
    global score_left, score_right

    if goal_left and not goal_right:
        score_init_right += 1
        
    if goal_right and not goal_left:
        score_init_left += 1
        
        
    score_left = score_font.render(str(score_init_left), True, WHITE, None)
    score_right = score_font.render(str(score_init_right), True, WHITE, None)

    GAMESURFACE.blit(score_left, (WIDTH/4 - score_left.get_width()/2, 30))
    GAMESURFACE.blit(score_right, (WIDTH/2 + (WIDTH/4 - score_right.get_width()/2), 30))
    


# Welcome screen
def welcome():
    GAMESURFACE.fill(BGCOLOR)
    msg_font = pygame.font.Font(None, 100)
    msg_text = msg_font.render("Press SPACE to play", True, WHITE, None)
    msg_frame = msg_text.get_rect()
    msg_frame.center = (WIDTH/2, HEIGHT/2)
    
    # Draw the welcome screen
    GAMESURFACE.blit(msg_text, msg_frame)

playing = False
game_over = False
while True:
    if not playing and not game_over:
        welcome()
    elif playing and game_over:
        gameover()
    elif playing and not game_over:
        pygame.display.update()
        GAMESURFACE.fill(BGCOLOR)
            
        """ La balle au milieu """
        pygame.draw.rect(GAMESURFACE, WHITE, (xball, yball, cote, cote), 0)

        """ 2 barres pour 2 joueurs"""
        pygame.draw.rect(GAMESURFACE, WHITE, (bar1_x, bar1_y_move, bar1_width, bar1_height), 0)
        pygame.draw.rect(GAMESURFACE, WHITE, (bar2_x, bar2_y_move, bar2_width, bar2_height), 0)

        """ Scores des 2 cotes"""
        GAMESURFACE.blit(score_left, (WIDTH/4 - score_left.get_width()/2, 30))
        GAMESURFACE.blit(score_right, (WIDTH/2 + (WIDTH/4 - score_right.get_width()/2), 30))
        
        """ Barriere """
        pygame.draw.rect(GAMESURFACE, GREEN, (xbarrier, ybarrier, barrier_width, barrier_height))

        """ Attack mode """
        attack()

        if direction == 'downright':
            xball += velocity_x
            yball += velocity_y
            if yball + cote >= HEIGHT:
                randomize_angle()
                direction = 'upright'
            elif xball >= WIDTH:
                #direction = 'downleft'
                goal_right = True
                goal_left = False
                update_score()
                accelerate_ball()
                new_ball()
            elif (xball + cote >= bar2_x) and (yball >= bar2_y_move and yball <= bar2_y_move + bar2_height):
                randomize_angle()
                direction = 'downleft'
        elif direction == 'upright':
            xball += velocity_x
            yball -= velocity_y
            if xball >= WIDTH:
                #direction = 'upleft'
                goal_right = True
                goal_left = False
                update_score()
                accelerate_ball()
                new_ball()
            elif yball <= 0:
                randomize_angle()
                direction = 'downright'
            elif (xball + cote >= bar2_x) and (yball >= bar2_y_move and yball <= bar2_y_move + bar2_height):
                randomize_angle()
                direction = 'upleft'
        elif direction == 'upleft':
            xball -= velocity_x
            yball -= velocity_y
            if yball <= 0:
                randomize_angle()
                direction = 'downleft'
            elif xball <= 0:
                #direction = 'upright'
                goal_left = True
                goal_right = False
                update_score()
                accelerate_ball()
                new_ball()
            elif (xball <= bar1_x + bar_width) and (yball >= bar1_y_move and yball <= bar1_y_move + bar1_height):
                randomize_angle()
                direction = 'upright'
            
        elif direction == 'downleft':
            xball -= velocity_x
            yball += velocity_y
            if yball + cote >= HEIGHT :
                randomize_angle()
                direction = 'upleft'
            elif xball <= 0:
                #direction = 'downright'
                goal_left = True
                goal_right = False
                update_score()
                accelerate_ball()
                new_ball()
            elif (xball <= bar1_x + bar_width) and (yball >= bar1_y_move and yball <= bar1_y_move + bar1_height):
                randomize_angle()
                direction = 'downright'
        
        if score_init_left != 0 and score_init_left % 2 == 0:
            attack_for_left = True
            fired_left = False
            
          
        
        if score_init_right != 0 and score_init_right % 2 == 0 :
            attack_for_right = True
            fired_right = False
            

        if score_init_left - score_init_right == 10 or score_init_right - score_init_left  == 10 or bar1_height <= 0 or bar2_height <= 0 :
                game_over, playing = True, True
                bar1_height, bar2_height = bar_height, bar_height
                attempt_left, attempt_right = 0, 0
        
        
              
        
    
    #FPSClock.tick(FPS)
        if pressed[K_UP]:
            bar2_up = True
            bar2_down = False
            slid_right_bar()
        if pressed[K_DOWN]:
            bar2_down = True
            bar2_up = False
            slid_right_bar()
        if pressed[K_w]:
            bar1_up = True
            bar1_down = False
            slid_left_bar()
        if pressed[K_s]:
            bar1_down = True
            bar1_up = False 
            slid_left_bar()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_a and attack_for_left and not fired_left:
                    print(attack_for_left)
                    print(fired_left)
                    print(attempt_left)
                    attempt_left = 1
                    cut_adversary()
                    
                if event.key == K_p and attack_for_right and not fired_right:
                    print("can cut right ")
                    attempt_right = 1 
                    cut_adversary()
                    
              
                    
                
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not playing and event.key == pygame.K_SPACE:
                playing = True
                game_over = False
            if game_over and playing and event.key == pygame.K_y:
                playing = True
                game_over = False
                score_init_left, score_init_right = 0, 0
                goal_left, goal_right = False, False
                update_score()
                attack_for_left, attack_for_right = False, False
                fired_left, fired_right = False, False
                attempt_left, attempt_right = 0, 0

                
    pressed = pygame.key.get_pressed()

    
    pygame.display.update()