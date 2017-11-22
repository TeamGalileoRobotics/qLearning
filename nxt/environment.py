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
    STEP_SIZE = 1

    NUM_ACTIONS = 4

    top_current = 0
    TOP_MIN = 0
    TOP_MAX = 10

    bottom_current = 0
    BOTTOM_MIN = 0
    BOTTOM_MAX = 10

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

        # TODO: add speed (direction) variable to turn motor
        # FIXME: rewrite plox
        
        top_new = self.top_current + self.STEP_SIZE*action[0]
        bottom_new = self.bottom_current + self.STEP_SIZE*action[1]

        if self.check_bounds(top_new, bottom_new):
            self.motor_top.turn(self.SPEED, self.STEP_SIZE)
            self.motor_bottom.turn(self.SPEED, self.STEP_SIZE)
            self.top_current = top_new
            self.bottom_current = bottom_new
            reward = self.ultrasonic.get_sample() - start_distance
        else:
            print 'out of bounds'
            reward = self.REWARD_BAD

        self.state = str(round(self.top_current / 10)) + "/" + str(round(self.bottom_current / 10))

        print 'reward: ' + str(reward)
        print 'bottom_current: ' + str(self.bottom_current)
        print 'top_current: ' + str(self.top_current)
        return reward

    def check_bounds(self, top_new, bottom_new):
        if top_new < self.TOP_MIN or top_new > self.TOP_MAX: return False
        if bottom_new < self.BOTTOM_MIN or bottom_new > self.BOTTOM_MAX: return False
        return True

class Action:
    [1,1] = 0
    [1,-1] = 1
    [-1,1] = 2
    [-1,-1] = 3