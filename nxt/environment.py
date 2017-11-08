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

    SPEED = 50
    STEP_SIZE = 10

    NUM_ACTIONS = 4

    def __init__(self):
        self.state = [0,0]
        self.completion = self.RUNNING
        self.nxt = nxt.locator.find_one_brick(name = 'NXT')
        self.ultrasonic = Ultrasonic(nxt, PORT_1)

        self.motor_top = Motor(nxt, PORT_A)
        self.motor_bottom = Motor(nxt, PORT_B)

    def move(self, action):
        start_distance = ultrasonic.get_sample()
        print 'start distance: ' + start_distance
        
        if action == Action.UP_UP:
            motor_top.turn(SPEED, STEP_SIZE)
            motor_bottom.turn(SPEED, STEP_SIZE)
        else if action == Action.UP_DOWN:
            motor_top.turn(SPEED, STEP_SIZE)
            motor_bottom.turn(SPEED, 0 - STEP_SIZE)
        else if action == Action.DOWN_UP:
            motor_top.turn(SPEED, 0 - STEP_SIZE)
            motor_bottom.turn(SPEED, STEP_SIZE)
        else if action == Action.DOWN_DOWN:
            motor_top.turn(SPEED, 0 - STEP_SIZE)
            motor_bottom.turn(SPEED, 0 - STEP_SIZE)

        reward = ultrasonic.get_sample() - start_distance
        self.state = motor_top.

        print 'reward: ' + reward
        return reward

class Action:
    UP_UP = 0x1
    UP_DOWN = 0x2
    DOWN_UP = 0x3
    DOWN_DOWN = 0x4