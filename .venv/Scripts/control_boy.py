from pico2d import *
import random

from grass import Grass
from boy import Boy
from game_world import *
# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in(SDL_KEYDOWN, SDL_KEYUP):
                boy.handle_event(event) #boy에게 event 전달


def reset_world():
    global running
    global grass
    global team
    global boy

    running = True


    grass = Grass()
    add_object(grass, 0)
    boy = Boy()
    add_object(boy, 1)


def update_world():
    update()
    pass


def render_world():
    clear_canvas()
    render()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.016)

# finalization code
close_canvas()

