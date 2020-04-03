import pgzrun

WIDTH = 800
HEIGHT = 600

cadet = Actor('cadet_1')
cadet.bottomleft = (0,550)

corona = Actor('corona')
corona.pos = 250,250

game_timer = 0
health = 10

def on_key_down(key):
    if keyboard.space:
        pass
        
def draw():
    screen.clear()
    corona.draw()
    cadet.draw()
    screen.draw.text("Game Time: {:.0f}".format(game_timer), (0, 0))
    screen.draw.text("Health Level: {:.0f}".format(health), (650, 0))

def update():
    global game_timer
    game_timer += .017
    if (keyboard.left):
        if (cadet.x > 40):
            cadet.x -= 2
    if (keyboard.right):
        if (cadet.x < 760):
            cadet.x += 2
    corona.left -= 3.5 
    if corona.right < 0:
        corona.left = WIDTH

pgzrun.go()