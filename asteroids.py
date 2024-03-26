import math
import sys

PLAIN_SHIP = 1
SHIELD_SHIP = 2
THRUST_SHIP = 3
SHIELD_THRUST_SHIP = 4

INITIAL_SPEED = 0
TOP_SPEED = 300

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

ship = Actor(assets[current_asset]["ship"][PLAIN_SHIP])
ship.center = WIDTH / 2, HEIGHT / 2
ship.angle = 0


def screen_angle_value(angle: int) -> int:
    new_angle = angle + 90
    if new_angle >= 360:
        new_angle -= 360
    return new_angle

def calculate_slope_and_y_intercept(angle, point: tuple) -> tuple:
    slope = math.tan(math.radians(angle))
    b = point[1] - slope * point[0]
    return (slope, b)

class GameState(object):

    def __init__(self):
        self.rotate_factor = 0
        self.rotate_direction = False
        self.shield_active = False
        self.ship_thrust = False
        self.ship_speed = INITIAL_SPEED
        self.ship_acceleration = 1.001
        self.ship_route = calculate_slope_and_y_intercept(
            screen_angle_value(ship.angle),
            (ship.x, ship.y)
        )

game_state = GameState()

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

        if game_state.rotate_direction:
            game_state.ship_route = calculate_slope_and_y_intercept(
                screen_angle_value(ship.angle),
                (ship.x, -1 * ship.y)
            )
            print("ship_route: {}".format(game_state.ship_route))

        if game_state.ship_speed <= TOP_SPEED:
            game_state.ship_speed += game_state.ship_acceleration
        
        print("speed: {}".format(game_state.ship_speed))

    visible_angle = screen_angle_value(ship.angle)

    distance = game_state.ship_speed * (1 / 60) # update fires 60/second

    update_ship_location(ship, visible_angle, distance, game_state.ship_route)



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

def calculate_new_y_value(x: int, parameters: tuple):
    y_value = parameters[0] * x + parameters[1]
    return y_value

def update_ship_location(craft, visible_angle, distance, route):
    calc_new_y_value = False

    if visible_angle == 0:
        craft.x += distance
    elif visible_angle > 0 and visible_angle < 90:
        craft.x += distance
        calc_new_y_value = True
    elif visible_angle == 90:
        craft.y -= distance
    elif visible_angle > 90 and visible_angle < 180:
        craft.x -= distance
        calc_new_y_value = True
    elif visible_angle == 180:
        craft.x -= distance
    elif visible_angle > 180 and visible_angle < 270:
        craft.x -= distance
        calc_new_y_value = True
    elif visible_angle == 270:
        craft.y += distance
    else: # visible_angle > 270
        craft.x += distance
        calc_new_y_value = True

    if calc_new_y_value:
        new_y = calculate_new_y_value(craft.x, route)
        print("x: {}, new_y: {}, route: {}".format(craft.x, new_y, route))
        craft.y = -1 * new_y
    
    print("position: ({}, {})".format(craft.x, craft.y))
