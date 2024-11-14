import game_world
import game_framework
from pannel import Pannel
from pico2d import *
import play_mode

def init():
    global pannel
    pannel =Pannel()
    game_world.add_object(pannel, 3)

def finish():
    game_world.remove_object(pannel)

def update():
    pannel.update()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                 game_framework.pop_mode()
            elif event.key == SDLK_0:
                play_mode.boy.set_item('NONE')
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.set_item('SmallBall')
                game_framework.pop_mode()
            elif event.key== SDLK_2:
                    play_mode.boy.set_item('BigBall')
                    game_framework.pop_mode()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass
def resume():
    pass