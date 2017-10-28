import random
import nxt.locator
from nxt.sensor import *
from nxt.motor import *

class Environment:
    running = True
    
    UP_UP = 0
    UP_DOWN = 1
    DOWN_UP = 2
    DOWN_DOWN = 3

    def __init__(self):
        self.state = [0,0]
        self.completion = self.RUNNING
        self.nxt = nxt.locator.find_one_brick(name = 'NXT')
        self.ultrasonic = Ultrasonic(nxt, PORT_1)

    def move(self, action):
        start_distance = ultrasonic.get_sample()
        print start_distance
        #TODO: move motor 
        reward = ultrasonic.get_sample() - start_distance
        self.state = action

        return reward
