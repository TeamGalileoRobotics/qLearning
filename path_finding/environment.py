import random


class Environment:
    #           +---+
    #           | 1 +-----+
    #           +-+-+     |
    #             |       |
    #   +---+   +-+-+   +-+-+
    #   | 2 +---+ 3 |   | 5 | <- goal
    #   +---+   +-+-+   +-+-+
    #             |       |
    #   +---+   +-+-+     |
    #   | 0 +---+ 4 +-----+
    #   +---+   +---+

    GOAL_STATE = 5

    GOAL = 10  # goal / exit
    BAD = -100  # no way
    NONE = 0  # neutral way

    REWARDS = [
        [BAD, BAD, BAD, BAD, NONE, BAD],
        [BAD, BAD, BAD, NONE, BAD, GOAL],
        [BAD, BAD, BAD, NONE, BAD, BAD],
        [BAD, NONE, NONE, BAD, NONE, BAD],
        [NONE, BAD, BAD, NONE, BAD, GOAL],
        [BAD, NONE, BAD, BAD, NONE, GOAL]
    ]

    RUNNING = 0
    WON = 1
    LOST = 2

    def __init__(self):
        self.state = random.randint(0, 5)
        self.completion = self.RUNNING

    def move(self, action):
        reward = self.REWARDS[self.state][action]
        self.state = action

        # agent won
        if self.state == self.GOAL_STATE:
            self.completion = self.WON

        # agent lost
        if reward == self.BAD:
            self.completion = self.LOST

        return reward
