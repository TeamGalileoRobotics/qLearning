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

    REWARD_BAD = -1000

    SPEED = 30
    STEP_SIZE = 7

    NUM_ACTIONS = 4

    top_current = 0
    TOP_MIN = 2
    TOP_MAX = 65

    bottom_current = 0
    BOTTOM_MIN = 2
    BOTTOM_MAX = 180

    def __init__(self):
        self.state = "0/0"
        self.running = True
        self.nxt = nxt.locator.find_one_brick()
        print("nxt: " + str(self.nxt))
        self.ultrasonic = Ultrasonic(self.nxt, PORT_1)

        self.motor_top = Motor(self.nxt, PORT_A)
        self.motor_bottom = Motor(self.nxt, PORT_B)

    def move(self, action):
        start_distance = self.ultrasonic.get_sample()
        print 'start distance: ' + str(start_distance)

        top_fac = 0
        bottom_fac = 0

        if action == Action.UP_UP:
            top_fac = 1
            bottom_fac = 1
        elif action == Action.UP_DOWN:
            top_fac = 1
            bottom_fac = -1
        elif action == Action.DOWN_UP:
            top_fac = -1
            bottom_fac = 1
        elif action == Action.DOWN_DOWN:
            top_fac = -1
            bottom_fac = -1

        top_angle = top_fac * self.STEP_SIZE
        bottom_angle = bottom_fac * self.STEP_SIZE

        top_new = self.bottom_current + top_angle
        bottom_new = self.bottom_current + bottom_angle

        # FIXME: current values are somehow wrong (SEND HELP)

        if self.check_bounds(top_new, bottom_new):
            self.motor_top.turn(top_fac * self.SPEED, self.STEP_SIZE)
            self.motor_bottom.turn(bottom_fac * self.SPEED, self.STEP_SIZE)
            self.top_current = top_new
            self.bottom_current = bottom_new
            reward = self.ultrasonic.get_sample() - start_distance
        else:
            print 'out of bounds'
            reward = self.REWARD_BAD

        self.state = str(round(self.top_current / self.STEP_SIZE)) + "/" + str(round(self.bottom_current / self.STEP_SIZE))

        print 'top_current: ' + str(self.top_current)
        print 'bottom_current: ' + str(self.bottom_current)
        print 'reward: ' + str(reward)
        return reward

    def check_bounds(self, top_new, bottom_new):
        if top_new < self.TOP_MIN or top_new > self.TOP_MAX: return False
        if bottom_new < self.BOTTOM_MIN or bottom_new > self.BOTTOM_MAX: return False
        return True

class Action:
    UP_UP = 0
    UP_DOWN = 1
    DOWN_UP = 2
    DOWN_DOWN = 3