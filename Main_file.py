import pygame

from pygame import mixer
from fighter import Fighter


import time
mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dunkin' Punch")

#defining colours 
RED = (255 , 0 ,0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables 
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0 ] #player scores [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN= 2000

#define fighter variables
WARRIOR_SIZE=162
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [50, 40]
WARRIOR_DATA=[WARRIOR_SIZE, WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE=250
WIZARD_SCALE = 2.5
WIZARD_OFFSET = [120,97]
WIZARD_DATA=[WIZARD_SIZE, WIZARD_SCALE,WIZARD_OFFSET]



#load music and sounds 
pygame.mixer.music.load("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\sound effects\\main bg.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0,5000)

sword_fx = pygame.mixer.Sound("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\sound effects\\mixkit-shot-light-energy-flowing-2589_out_2.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\sound effects\\fire sound.wav")
magic_fx.set_volume(0.75)


#load background image
#To use backslashes in file paths, you need to escape them by using double backslashes (\\)
bg_image = pygame.image.load("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\aDVd6aj.gif").convert_alpha()
warrior_sheet = pygame.image.load("C:\\Users\\HP\Desktop\\Java programs\\python_game\\characters\\hero 102.png").convert_alpha()
wizard_sheet = pygame.image.load("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\characters\\villain 102.png").convert_alpha()

#load victory image 
victory_img = pygame.image.load("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\victory img.png").convert_alpha()
print(victory_img)

#define number of steps in each animations 
WARRIOR_ANIMATION_STEPS = [10, 10, 16, 11, 14, 2 , 15]
WIZARD_ANIMATION_STEPS = [8, 8, 8, 8, 8, 2, 13]

#define font 
count_font = pygame.font.Font("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\Turok.ttf" , 100)
score_font = pygame.font.Font("C:\\Users\\HP\\Desktop\\Java programs\\python_game\\Turok.ttf" , 30)

#draw function for drawing text 
def draw_text(text, font , text_col , x , y) :
    img = font.render(text, True , text_col)
    screen.blit(img ,(x ,y))



#function for drawing background
def draw_bg():
   scaled_bg = pygame.transform.scale(bg_image,(SCREEN_WIDTH, SCREEN_HEIGHT))
   screen.blit(scaled_bg, (0,0))

#health bar function for fighters 
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen,WHITE,(x-5,y-5,410,40))
    pygame.draw.rect(screen,RED,(x,y,400,30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400*ratio, 30))
 
 #create two instances of fighters
fighter_1 = Fighter(1,200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,sword_fx)
fighter_2 = Fighter(2,700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,magic_fx)


#game loop to create a loop so that the game stays on until we press quit button
run = True
clock = pygame.time.Clock()
while run:

    #draw bg
    draw_bg()

    #show player health
    draw_health_bar(fighter_1.health,20 ,20)
    draw_health_bar(fighter_2.health,580 ,20)
    draw_text("P1 : " + str(score[0]) , score_font, RED , 20 , 60 )
    draw_text("P2: " +  str(score[1]) , score_font, RED , 580 , 60 )

    #update countdown
    if intro_count == 0 :
         #move fighters
        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen, fighter_2,round_over)
        fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen, fighter_1,round_over)
    else:
        #displayer count timer 
        draw_text(str(intro_count), count_font, YELLOW , SCREEN_WIDTH / 2,SCREEN_HEIGHT/2)
        #update count timer 
        if(pygame.time.get_ticks() - last_count_update ) >= 1000 :
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            

   

    #update fighters
    fighter_1.update()
    fighter_2.update()
 
    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #check for player defeat 
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over=True
            round_over_timer = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over=True
            round_over_timer = pygame.time.get_ticks()    
    else:
        #display victory image 
        screen.blit(victory_img, (10 , 80))
        if pygame.time.get_ticks() - round_over_timer > ROUND_OVER_COOLDOWN:
           round_over = False
           intro_count = 4
           fighter_1 = Fighter(1,200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,sword_fx)
           fighter_2 = Fighter(2,700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,magic_fx)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()