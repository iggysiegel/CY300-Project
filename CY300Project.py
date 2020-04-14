"""
Documentation:
https://pygame-zero.readthedocs.io/en/stable/introduction.html
http://www.penguintutor.com/projects/docs/space-asteroids-pgzero.pdf

Description:
"Cadet vs. Covid" is a side-scrolling dungeon game. The player uses the arrow keys to
move an avatar across the level; each level represents one floor of Davis barracks.
While in the hallway, players must jump to avoid the airborne coronavirus particles.
One each floor there are several doors that players can choose to enter; each room
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
import pygame, pgzrun, random #I'm running this in Spyder

WIDTH = 800
HEIGHT = 600

cadet = Actor('cadet_1')
cadet.bottomleft = (0,550)

corona = Actor('corona')
corona.pos = (WIDTH,random.randint(30,550))

background = ("smallmap.png")

game_status = 0 #Status 0 = start screen, 1 = playing game, 2 = end screen
game_timer = 0
high_scores = [0]
health = 2
corona_hit = False
isJump = False
jumpCount = 10  #gravity simuator 2020

def on_key_down():
    global isJump
    if keyboard.space:
        isJump = True

def draw_game_status_one():
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

def reset():
    global health, game_timer, isJump, jumpCount, corona_hit
    health = 2
    game_timer = 0
    cadet.bottomleft = (0,550)
    isJump = False
    jumpCount = 10
    corona_hit = False

def move_cadet():
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

def move_corona():
    if corona.right < 0:
        corona.pos = (WIDTH,random.randint(30,550))
    corona.pos = (corona.x - 3.5, corona.y)

def detect_hits():
    global corona_hit
    if cadet.colliderect(corona):
        corona_hit = True

def draw():
    if game_status == 0:
        screen.draw.text("Press ENTER to start", (100, 300),color="white", fontsize=32)
    if game_status == 1:
        draw_game_status_one()
    if game_status == 2:
        screen.draw.text("Final Time: {:.0f}".format(game_timer), (100, 300),color="white", fontsize=32)
        screen.draw.text("High Score: {:.0f}".format(max(high_scores)), (100, 400),color="white", fontsize=32)
        screen.draw.text("Press ENTER to restart", (100, 500),color="white", fontsize=32)

def update():
    global game_status, high_scores, game_timer
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

pgzrun.go()
