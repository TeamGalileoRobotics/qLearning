import random


class Environment:
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
