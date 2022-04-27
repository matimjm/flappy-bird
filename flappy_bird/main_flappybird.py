from random import randrange
from sys import exit
from tkinter import CENTER, RIGHT
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_SPACE,
    USEREVENT
)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 1000
PIPE_SPEED = 15
PIPE_SPAWN = SCREEN_WIDTH+50
PIPE_GAP = 400


pygame.init()

# GRAPHICS



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() ## 100 x 100
        self.surf = pygame.image.load('awatar.png')
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (100, 100)) 
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/4,SCREEN_HEIGHT/2))
        self.weight = 10
        self.velocity = 0
    def update(self,delta_time):
        self.velocity += delta_time*self.weight
        self.rect.move_ip(0,self.velocity*delta_time)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0
    def jump(self):
        self.velocity = -40
        pygame.mixer.Sound.play(jump)


class Pipe():
    def __init__(self):
        self.surfbot = pygame.image.load("pipe_bottom.png").convert_alpha()
        self.surfbot.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.surfbot = pygame.transform.scale(self.surfbot, (100, 1000))
    def update(self,delta_time,score):
        self.rect.move_ip(-PIPE_SPEED*delta_time,0)
        if self.rect.right < 0:
            self.kill()
    

            



class PipeTop(Pipe,pygame.sprite.Sprite):
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        Pipe.__init__(self)
        self.rect = self.surfbot.get_rect(midbottom = (PIPE_SPAWN,height - PIPE_GAP/2))
        self.afterplayer = False
    def update(self,delta_time,score):
        Pipe.update(self,delta_time,score)
        if not self.afterplayer and self.rect.right <= SCREEN_WIDTH/4 - 50:
            self.afterplayer = True
            score.increase()

class PipeBottom(Pipe,pygame.sprite.Sprite):
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        Pipe.__init__(self)
        self.rect = self.surfbot.get_rect(midtop = (PIPE_SPAWN,height + PIPE_GAP/2))
    
class Score():
    def __init__(self):
        self.score = 0
        self.score_msg = game_font.render(f'SCORE: {self.score}',False,(255,255,255))
        self.score_msg_rect = self.score_msg.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
        
    def draw(self):
        self.frame1 = pygame.draw.rect(screen,(0,0,0),(120,190,400,100),0,20)
        self.frame2 = pygame.draw.rect(screen,(102,102,255),(120,190,400,100),10,20)
        screen.blit(self.score_msg,self.score_msg_rect)
    def increase(self):
        self.score += 1
        self.score_msg = game_font.render(f'SCORE: {self.score}',False,(255,255,255))
    def show(self):
        return self.score
    def zero(self):
        self.score = 0
    

    
        
game_font = pygame.font.Font('Pixeltype.ttf',100)



pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('FLAPPY BIRD WINTER SPORTS EDITION')
pygame.display.set_icon(pygame.image.load('awatar.png'))
player = Player()
pipes = pygame.sprite.Group()
score = Score()



x = 0

bg = pygame.image.load('background.png')
player_dead = pygame.image.load('awatar_dead.png')

jump = pygame.mixer.Sound('jump.wav')
hit = pygame.mixer.Sound('hit.wav')


def create_pipe(height):
    return PipeTop(height),PipeBottom(height)

def draw_menu():
    screen.blit(bg,(0,0))
    pygame.draw.rect(screen,(102,102,255),(30,250,575,350))
    screen.blit(welcome1,welcome_rect1)
    screen.blit(welcome2,welcome_rect2)
    screen.blit(welcome3,welcome_rect3)
    screen.blit(instruction1,instruction_rect1)
    screen.blit(instruction2,instruction_rect2)

def draw_game_over():
    screen.blit(bg,(0,0))
    screen.blit(player_dead,(SCREEN_WIDTH/2-100,SCREEN_HEIGHT/2+20))
    screen.blit(game_msg,game_msg_rect)
    score_msg = game_font.render(f'SCORE: {act_score}',False,(255,255,255))
    score_msg_rect = score_msg.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
    pygame.draw.rect(screen,(0,0,0),(120,190,400,100),0,20)
    pygame.draw.rect(screen,(102,102,255),(120,190,400,100),10,20)
    screen.blit(score_msg,score_msg_rect)

def draw_bg():
    rel_x = x % bg.get_rect().width
    screen.blit(bg,(rel_x - bg.get_rect().width, 0))
    if rel_x < SCREEN_WIDTH:                #### <----- do funkcji
        screen.blit(bg,(rel_x,0))
    x -= 1



    


# TEXT MESSAGES



game_msg = game_font.render('GAME OVER',False,(255,255,255))
game_msg_rect = game_msg.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

welcome1 = game_font.render('WELCOME TO',False,(255,255,255))
welcome_rect1 = welcome1.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4+50))
welcome2 = game_font.render('FLAPPY BIRD',False,(255,255,255))
welcome_rect2 = welcome2.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4+125))
welcome3 = game_font.render('WINTER SPORTS',False,(255,255,255))
welcome_rect3 = welcome3.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4+175))

instruction1 = game_font.render('PRESS SPACE',False,(255,255,255))
instruction_rect1 = instruction1.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4+250))
instruction2 = game_font.render('TO START THE GAME',False,(255,255,255))
instruction_rect2 = instruction2.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/4+300))





xtime = randrange(3000,4000)
gap = xtime

ADDPIPE = USEREVENT + 1
pygame.time.set_timer(ADDPIPE,gap)

clock = pygame.time.Clock()
game_active = False
running = True
new_game = True
bgX = 0
bgRelX = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                game_active = True
                player.jump()
                new_game = False
        if game_active:
            if event.type == ADDPIPE:
                pipe_top,pipe_bottom = create_pipe(randrange(100,900))
                pipes.add(pipe_top)
                pipes.add(pipe_bottom)


    if game_active:
        PIPE_SPEED += 0.01

        player.update(delta_time)
        pipes.update(delta_time,score)
        
        # MOVING BACKGROUND
        bgRelX = bgX % bg.get_rect().width
        screen.blit(bg,(bgRelX - bg.get_rect().width,0))
        if bgRelX < SCREEN_WIDTH:
            screen.blit(bg, (bgRelX,0))
        bgX -= 1


        # BLIT PIPES
        for entity in pipes:
            screen.blit(entity.surfbot,entity.rect)
                

        # CHECK COLLISION       
        if pygame.sprite.spritecollideany(player,pipes):
            pygame.mixer.Sound.play(hit)
            player.kill()
            game_active = False
            pipes.empty() 
            act_score = score.show()
            score.__init__()

        # DRAW SCORE AND PLAYER
        score.draw() 
        screen.blit(player.surf,player.rect)

    else:
        if new_game:
            draw_menu()
            
        else:
            draw_game_over()
    


        
    #if pygame.sprite.spritecollideany(player,pipes):
    #    player.kill()
    #    running = False
    delta_time = clock.tick(60)/100
    
    pygame.display.flip()