import random

def pick_action(state):
    possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
    choice = random.choice(possible_actions)
    return choice
