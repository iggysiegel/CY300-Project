"""
Name: "Cadet vs. Covid"
File: CY300Project.py
Comments:
"Cadet vs. Covid" is a side-scrolling dungeon game. The player uses the arrow keys to
move an avatar across the level; each level represents one floor of Davis barracks.
While in the hallway, players must jump to avoid the airborne coronavirus particles.
On each floor there are several doors that players can choose to enter; each room
randomly contains one of the following: CGR, TACs, or medical supplies. Medical supplies
increases the player's health, giving them more times they can be hit by coronavirus before
becoming infected and losing. Running into TACs forces players to act fast in order to avoid
losing time to a tasking (time penalty). Running into CGR forces players to act fast to 
avoid mandatory Commadant's PT (health penalty). At the end of each level, players enter a
final door that takes them to the next level, where the enemies are faster.
Currently, the code displays a basic start screen and a rough initial level. The variables
necessary to play are game_status (which tells the loop what to show), the timer (which
corresponds to score), health (which is the amount of lives left), and a few others that
support movement around the screen. Future additions will include the ability to transition
from the hallway (game state 2) to a room (game state 3) to interact with the enemies, a
method of increasing the difficulty to match the level, and a final boss.
 
The project team includes CDTs Siegel and Bolen. We use the modules pygame, pgzrun, and random.
"""


"""
Attribution:
https://pygame-zero.readthedocs.io/en/stable/introduction.html #general pygame tutorial
http://www.penguintutor.com/projects/docs/space-asteroids-pgzero.pdf #code for jump
"""


import pygame, pgzrun, random


#Constants
WIDTH = 800
HEIGHT = 600

#Actors
cadet = Actor('cadet_1')
cadet.bottomleft = (0,550)

corona = Actor('corona')
corona.pos = (WIDTH,random.randint(30,550))

Health = Actor('health')
Health.pos = (60,100)

CGR = Actor('cgr')
CGR.pos = (random.randint(0,WIDTH),random.randint(0,HEIGHT))

#Background
background = ("smallmap.png")

#Variables
game_status = 0 #Status 0 = start screen, 1 = playing game, 2 = end screen, 3 = side room
game_level = 1 #There are six levels. We will adjust difficulty for this later
game_timer = 0
high_scores = [0] #This is actually "low" score right now
health = 2 #Low starting health for testing purposes
corona_hit = False
isJump = False
jumpCount = 10
sideRoom = False
sideRoomChoice = []
old_position = (0,550)
initiate_room = True
CGR_movement = (random.random() * random.choice((-1, 1)),random.random() * random.choice((-1, 1)))
CGR_hit = False
wash_hands = 0

###Top Level Procedures (Draw and Update)

#Procedure: draw
#Pygame zero objects are used to represent items to be displayed to the screen
#None -> None
def draw():
    """
    Draw start screen, play screen, or end screen
    """
    if game_status == 0:
        screen.draw.text("Press ENTER to start", (100, 300),color="white", fontsize=32)
    if game_status == 1:   
        draw_game_status_one()
    if game_status == 3:
        draw_game_status_three()
    if game_status == 2:
        screen.draw.text("Final Time: {:.0f}".format(game_timer), (100, 300),color="white", fontsize=32)
        screen.draw.text("High Score: {:.0f}".format(max(high_scores)), (100, 400),color="white", fontsize=32)
        screen.draw.text("Press ENTER to restart", (100, 500),color="white", fontsize=32)


#Procedure: update
#Pygame zero objects and Python objects represent the state of the game
#None -> None
def update():
    """
    Updates various objects to maintain the current state of the game.    
    """
    global game_status, high_scores, game_timer, sideRoom, old_position, CGR_hit, sideRoom, sideRoomChoice, wash_hands
    if game_status == 0:
        if (keyboard.RETURN):
            game_status = 1
    elif game_status == 2:
        temp_time = round(game_timer,0)
        if not temp_time in high_scores:
            screen.clear()
            high_scores.append(temp_time)
        if (keyboard.RETURN):
            reset()
            game_status = 1
    elif game_status == 1:
        if health < 1:
            screen.clear()
            game_status = 2
        game_timer += .017
        move_cadet()
        move_corona()
        detect_hits()
        if (keyboard.e): #For now, press "e" to enter side room
            old_position = cadet.pos
            sideRoom = True
            game_status = 3
    elif game_status == 3:
        game_timer += .017
        if sideRoom:
            random_choices()
            sideRoom = False
        move_cadet_sideroom()
        if "CGR" in sideRoomChoice:
            random_walk_initiator()
            move_CGR()
            detect_CGR_hit()
        if "Health" in sideRoomChoice:
            detect_health_hit()
        if (keyboard.d): #For now, press "d" to leave side room
            screen.clear()
            cadet.pos = old_position
            corona.pos = (WIDTH,random.randint(30,550))
            game_status = 1
            CGR_hit = False
            wash_hands = 0
            sideRoomChoice = []
            
        
###Other functions

#Procedure: on_key_down
def on_key_down():
    """
    Determines if cadet jumps outside of update loop
    """
    global isJump
    if keyboard.space:
        isJump = True

#Procedure: draw_game_status_one
def draw_game_status_one():
    """
    While playing game, draws screen with time, health, and character
    """
    global health, corona_hit
    screen.clear()
    screen.blit(background, (0,190))
    screen.draw.text("Game Time: {:.0f}".format(game_timer), (0, 0))
    screen.draw.text("Health Level: {:.0f}".format(health), (650, 0))
    if not corona_hit:
        corona.draw()
    else:
        health -= 1
        corona_hit = False
        corona.pos = (WIDTH,random.randint(30,550))
        corona.draw()
    cadet.draw()
    
#Procedure: draw_game_status_three
def draw_game_status_three():
    """
    While playing game, draws side room
    """
    screen.clear()
    if CGR_hit:
        cadet.bottomleft = (0,550)
        screen.draw.text("Game Time: {:.0f}".format(game_timer), (0, 0))
        screen.draw.text("Health Level: {:.0f}".format(health), (650, 0))
        screen.draw.text("CGR! Press 'd' to leave the room!",(WIDTH/2,HEIGHT/2))
        Health.pos = (60, 100)
        CGR.pos = (random.randint(0,WIDTH),random.randint(0,HEIGHT))
    else:        
        screen.draw.text("Game Time: {:.0f}".format(game_timer), (0, 0))
        screen.draw.text("Health Level: {:.0f}".format(health), (650, 0))
        cadet.draw()
        if "Health" in sideRoomChoice and "CGR" not in sideRoomChoice:
            Health.draw()
            CGR.pos = (-200,-200)
        if "CGR" in sideRoomChoice and "Health" not in sideRoomChoice:
            CGR.draw() 
        if "CGR" in sideRoomChoice and "Health" in sideRoomChoice:
            Health.draw()
            CGR.draw()

#Procedure: reset
def reset():
    """
    After the end screen before starting a new game, this procedure resets
    global variables.
    """
    global health, game_timer, isJump, jumpCount, corona_hit
    health = 2
    game_timer = 0
    cadet.bottomleft = (0,550)
    isJump = False
    jumpCount = 10
    corona_hit = False

#Procedure: move_cadet
def move_cadet():
    """
    While playing game, this procedure moves the cadet left/right and jumps
    """
    global jumpCount, isJump
    if isJump == True:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            cadet.y -= (jumpCount ** 2) * .5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    if (keyboard.left):
        if (cadet.x > 40):
            cadet.x -= 4
    if (keyboard.right):
        if (cadet.x < 760):
            cadet.x += 4

#Procedure: move_corona
def move_corona():
    """
    While playing game, this procedure moves the corona across the screen.
    If the corona crosses the left boundary, reset it at a random height.
    """
    if corona.right < 0:
        corona.pos = (WIDTH,random.randint(30,550))
    corona.pos = (corona.x - 3.5, corona.y)

#Procedure: detect_hits
def detect_hits():
    """
    While playing game, this procedure determines if the cadet was hit by Corona
    """
    global corona_hit
    if cadet.colliderect(corona):
        corona_hit = True

#Procedure: game_status_three
def random_choices():
    """
    After entering a side room, this procedure determines what the cadet will
    encounter by random choice (Health Boost or CGR).
    """
    global sideRoomChoice
    if sideRoom:
        random_Health = random.choices(['Health',''], [0.5, 0.5])
        random_CGR = random.choices(['CGR',''], [0.75, 0.25])
        if random_Health == ['Health']:
            sideRoomChoice.append("Health")
        if random_CGR == ['CGR']:
            sideRoomChoice.append("CGR")
        if "Health" not in sideRoomChoice and "CGR" not in sideRoomChoice:
            Health.pos = (-100,-100)
            CGR.pos = (WIDTH + 100,HEIGHT + 100)
        if "Health" in sideRoomChoice and "CGR" not in sideRoomChoice:
            Health.pos = (60,100)
            CGR.pos = (-100,-100)
        if "CGR" in sideRoomChoice and "Health" not in sideRoomChoice:
            Health.pos = (-100,-100)
            CGR.pos = (random.randint(0,WIDTH),random.randint(0,HEIGHT))
        if "CGR" in sideRoomChoice and "Health" in sideRoomChoice:
            Health.pos = (60,100)
            CGR.pos = (random.randint(0,WIDTH),random.randint(0,HEIGHT))
   
#Procedure: move_cadet
def move_cadet_sideroom():
    """
    While playing side room, this procedure moves the cadet left/right and jumps
    """
    if (keyboard.left):
        if (cadet.x > 40):
            cadet.x -= 3
    if (keyboard.right):
        if (cadet.x < 760):
            cadet.x += 3
    if (keyboard.down):
        if (cadet.midbottom[1] < HEIGHT):
            cadet.y += 3
    if (keyboard.up):
        if (cadet.midtop[1] > 0):
            cadet.y -= 3

#Procedure: random_walk_initiator
def random_walk_initiator():
    """
    After entering the side room, initiates random_walk procedure to occur
    at a set schedule
    """
    global initiate_room
    if initiate_room:
        clock.schedule_interval(random_walk,3)
        initiate_room = False

#Procedure: random_walk
def random_walk():
    """
    The procedure creates a random direction (x,y). Then, for a period of time
    determined by random_walk_initiator we save the random direction in the
    global variable CGR_movement
    """
    global CGR_movement
    dx = random.random() * random.choice((-1, 1))
    dy = random.random() * random.choice((-1, 1))
    CGR_movement = (dx,dy)
    return CGR_movement
    
#Procedure: move_CGR
def move_CGR():
    """
    Randomly move CGR around game space
    """
    if (CGR.midtop[1] <= 0):
        CGR.y += 1
    if (CGR.midbottom[1] >= HEIGHT):
        CGR.y -= 1
    if (CGR.midleft[0] <= 0):
        CGR.x += 1
    if (CGR.midright[0] >= WIDTH):
        CGR.x -= 1
    if (CGR.midtop[1] > 0) and (CGR.midbottom[1] < HEIGHT):
        CGR.y += CGR_movement[1]
    if (CGR.midleft[0] > 0) and (CGR.midright[0] < WIDTH):
        CGR.x += CGR_movement[0]

#Procedure: detect_CGR_hit
def detect_CGR_hit():
    """
    While playing side game, this procedure determines if the cadet was hit by CGR
    """
    global CGR_hit
    if cadet.colliderect(CGR):
        CGR_hit = True        

#Procedure: detect_health_hit       
def detect_health_hit():
    """
    While playing side game, this procedure determines if the cadet washes
    its hands. After 10 seconds, the cadet gets a health bonus.
    """
    global wash_hands, health
    if cadet.colliderect(Health):
        wash_hands += .017
    if wash_hands >= 10:
        wash_hands = 0
        Health.pos = (-100,-100)
        health += 1

pgzrun.go() #Run the game with this command. We are using Spyder
