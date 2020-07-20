import json
import random

class mcts_bot:
    move_queue = []

    def pick_action(self, state):
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
        choice = random.choice(possible_actions)
        mcts_tree[state] = None
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        return choice

