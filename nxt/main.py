import random
import os
import json
from environment import Environment
from environment import Action

# 0 <= GAMMA < 1
# GAMMA = 0 -> only consider immediate rewards
# GAMMA = 1 -> consider future rewards

GAMMA = 0.8

# initialize "brain"
brain = open("brainFile", "r")

if(os.stat("./brainFile").st_size == 0):
    q = {}
else:
    q = json.load(brain)
brain.close()


# normalize so highest/lowest value is 100/-100
def normalize(matrix):
    flat = []
    for li in matrix:
        for i in li:
            flat.append(abs(i))

    max_val = max(flat)
    if max_val == 0:
        return matrix

    for x, li in enumerate(matrix):
        for y, val in enumerate(li):
            matrix[x][y] = (val / max_val) * 100

    return matrix

# initialize a q value array
def initialize_q_value(key):
    if not key in q:
        q[key] = [0 for _ in range(Environment.NUM_ACTIONS)]


env = Environment()

while env.running:
    old_state = env.state

    # set q value to empty array if not already existing
    initialize_q_value(old_state)
    #print(q)
    # pick only best actions (this way of picking might leave actions unexplored)
    # actions = [action for action, q_value in enumerate(q[env.state]) if q_value == max(q[env.state])]
    # more thorough way, also includes all unexplored actions
    actions = [action for action, q_value in enumerate(q[env.state]) if
               q_value == max(q[env.state]) or q_value == 0]

    action = random.choice(actions)
    reward = env.move(action)

    initialize_q_value(env.state)

    # q-learning
    q[old_state][action] = reward + GAMMA * max(q[env.state])

    # normalize values
    #q = normalize(q)

# write brain to file
brain = open("brainFile", "w")
json.dump(q,brain)
brain.close()