import random

class punch_bot:
    def pick_action():
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
        if random.random() < 0.3:
            choice = 'p'
        elif random.random() < 0.4:
            choice = 's'
        elif random.random() < 0.5:
            choice = 'k'
        elif random.random() < 0.6:
            choice = 'sb'
        elif random.random() < 0.7:
            choice = 'cb'
        elif random.random() < 0.8:
            choice = 'f'
        else:
            choice = 'b'
        
        return choice
