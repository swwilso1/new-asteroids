#! /usr/bin/env python3.11

from asteroid import Asteroid
import pgzrun
import random
from ship import Ship
import random
import sys
from vector import Vector
from weapon import Weapon

PLAIN_SHIP = 1
SHIELD_SHIP = 2
THRUST_SHIP = 3
SHIELD_THRUST_SHIP = 4
BIG_ASTEROID1 = 5
BIG_ASTEROID2 = 6
RED_LASER = 7
GREEN_LASER = 8
BLUE_LASER = 9
MISSILE = 10
BASIC_BACKGROUND = 11

STEVE_ASSETS = 1
ELIANNA_ASSETS = 2

assets = {
    STEVE_ASSETS: {
        "ship": {
            PLAIN_SHIP: "starship-no-thrust",
            SHIELD_SHIP: "starship-shield-no-thrust",
            THRUST_SHIP: "starship-thrust",
            SHIELD_THRUST_SHIP: "starship-shield-thrust"
        },
        "asteroids": {
            BIG_ASTEROID1: "big-asteroid1",
            BIG_ASTEROID2: "big-asteroid2"
        },
        "lasers": {
            RED_LASER: "red-laser",
            GREEN_LASER: "green-laser",
            BLUE_LASER: "blue-laser"
        },
        "missiles": {
            MISSILE: "missile"
        },
        "backgrounds": {
            BASIC_BACKGROUND: "starfield-background-640-480"
        }
    },
    ELIANNA_ASSETS: {
        "ship": {
            PLAIN_SHIP: "e-starship-no-thrust",
            SHIELD_SHIP: "e-starship-shield-no-thrust",
            THRUST_SHIP: "e-starship-thrust",
            SHIELD_THRUST_SHIP: "e-starship-shield-thrust"
        },
        "asteroids": {
            BIG_ASTEROID1: "big-asteroid1",
            BIG_ASTEROID2: "big-asteroid2"
        },
        "lasers": {
            RED_LASER: "red-laser",
            GREEN_LASER: "green-laser",
            BLUE_LASER: "blue-laser"
        },
        "missiles": {
            MISSILE: "missile"
        },
        "backgrounds": {
            BASIC_BACKGROUND: "starfield-background-640-480"
        }
    }
}

current_asset = STEVE_ASSETS
current_laser = BLUE_LASER
current_missile = MISSILE
current_background = BASIC_BACKGROUND

# WIDTH = 640
# HEIGHT = 480

WIDTH = 1024
HEIGHT = 768

display_ship_metrics = False

ship = Ship(actor=Actor(assets[current_asset]["ship"][PLAIN_SHIP]),
            rotate_factor=5,
            acceleration=5,
            width=WIDTH,
            height=HEIGHT)

asteroid1 = Asteroid(actor=Actor(assets[current_asset]["asteroids"][BIG_ASTEROID1]),
                     rotate_factor=0.5,
                     speed=Vector(random.uniform(-15, 15), random.uniform(-15, 15)),
                     width=WIDTH,
                     height=HEIGHT)

asteroid1.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

asteroid2 = Asteroid(actor=Actor(assets[current_asset]["asteroids"][BIG_ASTEROID2]),
                     rotate_factor=1,
                     speed=Vector(random.uniform(-20, 20), random.uniform(-20, 20)),
                     width=WIDTH,
                     height=HEIGHT)
asteroid2.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

weapons = []
space_objects = [ship, asteroid1, asteroid2]


def draw():
    global display_ship_metrics

    screen.clear()
    # screen.blit(assets[current_asset]["backgrounds"][current_background], (0,0))

    for space_object in space_objects:
        space_object.draw()

    for weapon in weapons:
        weapon.draw()

    if display_ship_metrics:
        screen.draw.text("position: " + str(ship.position), fontname="courier", fontsize=12, topleft=(10, 10))
        screen.draw.text("heading: " + str(ship.heading), fontname="courier", fontsize=12, topleft=(10, 30))
        screen.draw.text("speed: " + str(ship.speed), fontname="courier", fontsize=12, topleft=(10, 50))


def update():

    for space_object in space_objects:
        space_object.update()

    for weapon in weapons:
        weapon.update()
        if not weapon.onscreen:
            weapons.remove(weapon)

    # Cache the angle so that we can restore it if we change
    # the ship sprite.
    angle = ship.angle

    if ship.shield and ship.thrust:
        ship.image = assets[current_asset]["ship"][SHIELD_THRUST_SHIP]
    elif not ship.shield and ship.thrust:
        ship.image = assets[current_asset]["ship"][THRUST_SHIP]
    elif ship.shield and not ship.thrust:
        ship.image = assets[current_asset]["ship"][SHIELD_SHIP]
    else:  # No shield or thruster
        ship.image = assets[current_asset]["ship"][PLAIN_SHIP]

    # Restore the angle
    ship.angle = angle


def on_key_down(key):
    global display_ship_metrics
    if key == keys.LEFT:
        ship.rotate = True
        ship.rotate_direction = Ship.ROTATE_LEFT
    elif key == keys.RIGHT:
        ship.rotate = True
        ship.rotate_direction = Ship.ROTATE_RIGHT
    elif key == keys.UP:
        ship.thrust = True
    elif key == keys.S:
        ship.shield = True
    elif key == keys.F:
        laser = Weapon(actor=Actor(assets[current_asset]["lasers"][current_laser]),
                       width=WIDTH,
                       height=HEIGHT,
                       acceleration=75)
        laser.angle = ship.angle
        laser.position = ship.laser_position
        weapons.append(laser)
    elif key == keys.M:
        missile = Weapon(actor=Actor(assets[current_asset]["missiles"][current_missile]),
                         width=WIDTH,
                         height=HEIGHT,
                         acceleration=20)
        missile.angle = ship.angle
        missile.position = ship.missile_position
        weapons.append(missile)
    elif key == keys.ESCAPE:
        sys.exit(0)
    elif key == keys.I:
        display_ship_metrics = not display_ship_metrics
    

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        ship.rotate = False
        ship.rotate_direction = Ship.ROTATE_NEUTRAL
    elif key == keys.UP:
        ship.thrust = False
    elif key == keys.S:
        ship.shield = False


pgzrun.go()
