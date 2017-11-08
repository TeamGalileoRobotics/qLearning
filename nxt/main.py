import random
from environment import Environment
from environment import Action

# 0 <= GAMMA < 1
# GAMMA = 0 -> only consider immediate rewards
# GAMMA = 1 -> consider future rewards

GAMMA = 0.8

NUM_EPISODES = 1000
wins = 0.0
losses = 0.0

# initialize "brain"
q = {}


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
def initialize_q_value(value):
    if !value in q:
        q[value] = [0 for _ in range(Environment.NUM_ACTIONS)]


# do episodes
for episode in range(NUM_EPISODES):
    env = Environment()

    output = str(episode) + ": " + str(env.state)

    while env.completion == env.RUNNING:
        old_state = env.state

        # set q value to empty array if not already existing
        initialize_q_value(old_state)

        # pick only best actions (this way of picking might leave actions unexplored)
        # actions = [action for action, q_value in enumerate(q[env.state]) if q_value == max(q[env.state])]
        # more thorough way, also includes all unexplored actions
        actions = [action for action, q_value in enumerate(q[env.state]) if
                   q_value == max(q[env.state]) or q_value == 0]

        action = random.choice(actions)
        reward = env.move(action)

        # q-learning
        q[old_state][action] = reward + GAMMA * max(q[action])

        # normalize values
        q = normalize(q)

        output += ", " + str(env.state)

    # win rate
    output += " (" + str(round(wins / (wins + losses) * 100)) + "%)"

    print(output)
# print learned values
print(q)
