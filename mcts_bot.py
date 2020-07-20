import json
import random
import copy

class mcts_bot:
    move_queue = []

    def pick_action(self, state):
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
        choice = random.choice(possible_actions)
        mcts_string = ''
        mcts_string += str(state.P_Distance)
        mcts_string += str(state.P1_Action)
        mcts_string += str(state.P2_Action)
        if mcts_string not in mcts_tree.keys():
            mcts_tree[mcts_string] = {'children':{}, 'risk':0, 'reward':0}
            for i in possible_actions:
                for j in possible_actions:
                    new_state = copy.deepcopy(state)
                    new_state.act(i, j)
                    new_mcts_string = ''
                    new_mcts_string += str(new_state.P_Distance)
                    new_mcts_string += str(new_state.P1_Action)
                    new_mcts_string += str(new_state.P2_Action)
                    mcts_tree[mcts_string]['children'][new_mcts_string] = None
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        return choice

