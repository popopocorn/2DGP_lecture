from math import radians
from pico2d import *
from state_machine import *
from ball import *
from game_world import *
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod # @ - decorator, 함수의 기능 변경 멤버함수의 개념 X
    def enter(obj, e):
        obj.dx=0
        if obj.dir >= 0:
            obj.action = 3
        else:
            obj.action = 2
        obj.frame = 0
        obj.start_time = get_time()
    @staticmethod
    def exit(obj,e):
        if space_down(e):
            obj.fire_ball()

    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - obj.start_time > 3:
            obj.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(int(obj.frame) * 100, obj.action * 100, 100, 100, obj.x, obj.y)

class Sleep:
    @staticmethod  # @ - decorator, 함수의 기능 변경 멤버함수의 개념 X
    def enter(obj, e):
        obj.frame = 0

    @staticmethod
    def exit(ob,ej):
        pass

    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(obj):
        if obj.dir >= 0:
            obj.image.clip_composite_draw(int(obj.frame) * 100, 3 * 100, 100, 100, radians(90), '',obj.x - 25, obj.y - 25, 100, 100)
        else:
            obj.image.clip_composite_draw(int(obj.frame) * 100, 2 * 100, 100, 100, radians(-90), '', obj.x + 25,
                                          obj.y - 25, 100, 100)
class Run:
    @staticmethod
    def enter(obj, e):
        if right_down(e) or left_up(e):
            obj.dir = 1
            obj.dx = 1
            obj.action = 1
            obj.frame = 0
        elif left_down(e) or right_up(e):
            obj.dx = -1
            obj.dir = -1
            obj.action = 0
            obj.frame = 0

    @staticmethod
    def exit(obj,e):
        if space_down(e):
            obj.fire_ball()

    @staticmethod
    def do(obj):
        #obj.x += obj.dx * 5
        obj.frame = (obj.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        obj.x += obj.dx * obj.run_speed * game_framework.frame_time

        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(int(obj.frame) * 100, obj.action * 100, 100, 100, obj.x, obj.y)
        pass
class Boy:
    def __init__(self):
        self.font = load_font("ENCR10B.TTF", 16)
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.dx = 0
        self.run_speed = ((20*1000)/3600)*10/0.3
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Run : {space_down : Run, right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle},
                Idle : {space_down : Idle, right_down: Run, left_down : Run, left_up : Run, right_up : Run,time_out : Sleep},
                Sleep : {right_down : Run, left_down: Run, right_up: Run, left_up : Run, space_down : Idle},

            }
        )
        self.set_item('NONE')
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #이건 key, mouse 입력
        #하지만 tuple형식으로 넘겨줘야함
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y, str(get_time()), (255, 255, 0))
    def fire_ball(self):
        if self.item == 'SmallBall':
            ball =Ball(self.x, self.y, self.dir*10)
            add_object(ball, 1)
        elif self.item == 'BigBall':
            ball =BigBall(self.x, self.y, self.dir*10)
            add_object(ball, 1)


    def set_item(self, item):
        self.item = item