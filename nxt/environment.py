import time
import keyboard
import nxt.locator
import random
from nxt.sensor import *
from nxt.motor import *

# states: 40/20 or 120/70 (rounded)
# 
# actions: UP_UP, UP_DOWN, ...
# move by 10 degrees
# 
# reward: distance moved

class Environment:
    REWARD_BAD = -1000

    SPEED = 50
    WAIT_TIME = 0.2
    ACCURACY = 10

    NUM_ACTIONS = 4

    TOP_MIN = 0
    TOP_MAX = 70

    BOTTOM_MIN = 0
    BOTTOM_MAX = 160

    ORIGINAL_STEP_SIZE = 12

    def __init__(self):
        self.top_current = 0
        self.bottom_current = 0
        self.state = "0/0"
        self.running = True
        
        self.nxt = nxt.locator.find_one_brick()
        print 'nxt: ' + str(self.nxt)
        
        self.ultrasonic1 = Ultrasonic(self.nxt, PORT_1)
        self.ultrasonic2 = Ultrasonic(self.nxt, PORT_2)

        self.motor_top = Motor(self.nxt, PORT_A)
        self.motor_bottom = Motor(self.nxt, PORT_B)
        self.motor_top.reset_position(False)
        self.motor_bottom.reset_position(False)

    def move(self, action):
        step_size = random.randint(ORIGINAL_STEP_SIZE-2,ORIGINAL_STEP_SIZE+2)
        start_distance = self.get_distance()
        print '------'
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

        top_angle = top_fac * step_size
        bottom_angle = bottom_fac * step_size

        top_new = self.top_current + top_angle
        bottom_new = self.bottom_current + bottom_angle

        if self.check_bounds(top_new, bottom_new):
            self.motor_top.turn(top_fac * self.SPEED, step_size)
            self.motor_bottom.turn(bottom_fac * self.SPEED, step_size)
            time.sleep(self.WAIT_TIME)

            self.top_current = self.motor_top.get_tacho().rotation_count
            self.bottom_current = self.motor_bottom.get_tacho().rotation_count
            reward = self.get_distance() - start_distance
            reward *= reward * reward
        else:
            print 'out of bounds'
            reward = self.REWARD_BAD

        self.state = str(round(self.top_current / ACCURACY)) + "/" + str(round(self.bottom_current / ACCURACY))

        print 'top_current: ' + str(self.top_current)
        print 'bottom_current: ' + str(self.bottom_current)
        print 'reward: ' + str(reward)
        if keyboard.is_pressed('q'):
            self.running = False
        return reward

    def check_bounds(self, top_new, bottom_new):
        if top_new < self.TOP_MIN or top_new > self.TOP_MAX: return False
        if bottom_new < self.BOTTOM_MIN or bottom_new > self.BOTTOM_MAX: return False
        return True

    def get_distance(self):
        return (self.ultrasonic1.get_sample() + self.ultrasonic2.get_sample()) / 2

class Action:
    UP_UP = 0
    UP_DOWN = 1
    DOWN_UP = 2
    DOWN_DOWN = 3