import random

class easy_bot:
    def pick_action():
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
        choice = random.choice(possible_actions)
        return choice
