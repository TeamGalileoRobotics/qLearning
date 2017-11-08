import random
import nxt.locator
from nxt.sensor import *
from nxt.motor import *

# states: 40/20 or 120/70 (rounded)
# 
# actions: UP_UP, UP_DOWN, ...
# move by 10 degrees
# 
# reward: distance moved

class Environment:
    running = True

    REWARD_BAD = -100

    SPEED = 50
    STEP_SIZE = 10

    NUM_ACTIONS = 4

    top_current = 0
    TOP_MIN = 0
    TOP_MAX = 84

    bottom_current = 0
    BOTTOM_MIN = 0
    BOTTOM_MAX = 270

    def __init__(self):
        self.state = [0, 0]
        self.running = True
        self.nxt = nxt.locator.find_one_brick()
        self.ultrasonic = Ultrasonic(nxt, PORT_1)

        self.motor_top = Motor(nxt, PORT_A)
        self.motor_bottom = Motor(nxt, PORT_B)

    def move(self, action):
        start_distance = ultrasonic.get_sample()
        print 'start distance: ' + start_distance
        
        if action == Action.UP_UP:
            top_new = top_current + STEP_SIZE
            bottom_new = bottom_current + STEP_SIZE
        else if action == Action.UP_DOWN:
            top_new = top_current + STEP_SIZE
            bottom_new = bottom_current - STEP_SIZE
        else if action == Action.DOWN_UP:
            top_new = top_current - STEP_SIZE
            bottom_new = bottom_current + STEP_SIZE
        else if action == Action.DOWN_DOWN:
            top_new = top_current - STEP_SIZE
            bottom_new = bottom_current - STEP_SIZE

        if check_bounds(top_new, bottom_new):
            motor_top.turn(SPEED, top_new)
            motor_bottom.turn(SPEED, bottom_new)
            reward = ultrasonic.get_sample() - start_distance
        else:
            print 'out of bounds'
            reward = REWARD_BAD

        self.state = round(top_current / 10) + "/" + round(bottom_current / 10)

        print 'reward: ' + reward
        return reward

    def check_bounds(self, top_new, bottom_new):
        if top_new < TOP_MIN or top_new > TOP_MAX: return False
        if bottom_new < BOTTOM_MIN or bottom_new > BOTTOM_MAX: return False
        return True

class Action:
    UP_UP = 0x1
    UP_DOWN = 0x2
    DOWN_UP = 0x3
    DOWN_DOWN = 0x4