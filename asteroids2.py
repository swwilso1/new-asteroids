import math
import space_object
import sys
import vector

PLAIN_SHIP = 1
SHIELD_SHIP = 2
THRUST_SHIP = 3
SHIELD_THRUST_SHIP = 4

INITIAL_SPEED = 0
TOP_SPEED = 30
DRAG = 0.07

STEVE_ASSETS = 1
ELIANNA_ASSETS = 2

assets = {
    STEVE_ASSETS : {
        "ship" : {
            PLAIN_SHIP : "starship-no-thrust",
            SHIELD_SHIP : "starship-shield-no-thrust",
            THRUST_SHIP : "starship-thrust",
            SHIELD_THRUST_SHIP : "starship-shield-thrust"
        }
    }
}

current_asset = STEVE_ASSETS

WIDTH = 640
HEIGHT = 480

class GameState(object):

    def __init__(self):
        self.rotate_factor = 0
        self.rotate_direction = False
        self.shield_active = False
        self.ship_thrust = False
        self.ship_speed = INITIAL_SPEED
        self.ship_acceleration = 1.001

game_state = GameState()

# ship = space_object.SpaceObject(assets[current_asset]["ship"][PLAIN_SHIP])
# ship = Actor(assets[current_asset]["ship"][PLAIN_SHIP])
ship = space_object.SpaceObject(Actor(assets[current_asset]["ship"][PLAIN_SHIP]))
ship.center = WIDTH / 2, HEIGHT / 2

last_heading = ship.heading

def draw():
    screen.clear()
    ship.draw()

def update():

    if game_state.rotate_direction:
        ship.angle += game_state.rotate_factor
        if ship.angle > 360:
            ship.angle -= 360
        if ship.angle < 0:
            ship.angle += 360

    if game_state.ship_thrust:

        if game_state.ship_speed <= TOP_SPEED:
            game_state.ship_speed += game_state.ship_acceleration

        ship.direction += ship.heading
 
    else:
        game_state.ship_speed -= DRAG

        if game_state.ship_speed < 0:
            game_state.ship_speed = 0
            ship.direction = 0

    distance = game_state.ship_speed * (1 / 60) # update fires 60/second

    ship.position += ship.direction * distance

    if ship.x > WIDTH:
        ship.x = 0
    elif ship.x < 0:
        ship.x = WIDTH
    
    if ship.y > HEIGHT:
        ship.y = 0
    elif ship.y < 0:
        ship.y = HEIGHT

    # Cache the angle so that we can restore it if we change
    # the ship sprite.
    angle = ship.angle

    if game_state.shield_active and game_state.ship_thrust:
        ship.image = assets[current_asset]["ship"][SHIELD_THRUST_SHIP]
    elif not game_state.shield_active and game_state.ship_thrust:
        ship.image = assets[current_asset]["ship"][THRUST_SHIP]
    elif game_state.shield_active and not game_state.ship_thrust:
        ship.image = assets[current_asset]["ship"][SHIELD_SHIP]
    else: # No shield or thruster
        ship.image = assets[current_asset]["ship"][PLAIN_SHIP]

    # Restore the angle
    ship.angle = angle

def on_key_down(key):
    if key == keys.LEFT:
        game_state.rotate_direction = True
        game_state.rotate_factor = 5
    elif key == keys.RIGHT:
        game_state.rotate_direction = True
        game_state.rotate_factor = -5
    elif key == keys.UP:
        game_state.ship_thrust = True
    elif key == keys.S:
        game_state.shield_active = True

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        game_state.rotate_direction = False
        game_state.rotate_factor = 0
    elif key == keys.UP:
        game_state.ship_thrust = False
    elif key == keys.S:
        game_state.shield_active = False
