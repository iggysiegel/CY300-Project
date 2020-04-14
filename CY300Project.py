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


pgzrun.go() #Run the game with this command. We are using Spyder


import pygame, pgzrun, random

#Constants
WIDTH = 800
HEIGHT = 600

#Actors
cadet = Actor('cadet_1')
cadet.bottomleft = (0,550)

corona = Actor('corona')
corona.pos = (WIDTH,random.randint(30,550))

#Background
background = ("smallmap.png")

#Variables
game_status = 0 #Status 0 = start screen, 1 = playing game, 2 = end screen, 3 = side room
game_level = 1 #There are six levels. We will adjust difficulty for this later
game_timer = 0
high_scores = [0]
health = 2 #Low starting health for testing purposes
corona_hit = False
isJump = False
jumpCount = 10
sideRoom = False

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
    global game_status, high_scores, game_timer, sideRoom
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
        if (keyboard.a): #For now, press "a" to enter side room
            sideRoom = True
            game_status = 3
    elif game_status == 3:
        screen.clear()
        game_status_three()
        if (keyboard.RETURN):
            screen.clear()
            corona.pos = (WIDTH,random.randint(30,550))
            game_status = 1

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
    While playing game, this function determines if the cadet was hit
    """
    global corona_hit
    if cadet.colliderect(corona):
        corona_hit = True

#Procedure: game_status_three
def game_status_three():
    """
    After entering a side room, this procedure determines what the cadet will
    encounter by random choice (Health Boost, TACs, CGR) then takes appropriate
    actions. For now, we are just drawing a message on the screen.
    """
    global sideRoom, room_choice
    if sideRoom:
        room_choice = random.choices(['Health','TAC','CGR'], [0.5, 0.25, 0.25]) #Change probability based off game_level
        sideRoom = False
    if room_choice == ["CGR"]:
        screen.draw.text("CGR! Press Enter to return", (100, 300),color="white", fontsize=32)
    if room_choice == ["TAC"]:
        screen.draw.text("TAC! Press Enter to return", (100, 300),color="white", fontsize=32)
    if room_choice == ["Health"]:
        screen.draw.text("Health Boost! Press Enter to return", (100, 300),color="white", fontsize=32)
