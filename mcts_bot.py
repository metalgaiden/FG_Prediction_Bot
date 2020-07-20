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
        if state.P1_Action == 'sweep(startup)' or state.P1_Action == 'kick(startup_1)' or state.P1_Action == 'kick(startup_2)' or state.P1_Action == 'recovery':
            mcts_string += str(state.P1_Action)
        else:
            mcts_string += str(None)
        if state.P2_Action == 'sweep(startup)' or state.P2_Action == 'kick(startup_1)' or state.P2_Action == 'kick(startup_2)' or state.P2_Action == 'recovery':
            mcts_string += str(state.P2_Action)
        else:
            mcts_string += str(None)
        if mcts_string not in mcts_tree.keys():
            mcts_tree[mcts_string] = {'children':{}, 'risk':0, 'reward':0}
            for i in possible_actions:
                for j in possible_actions:
                    new_state = copy.deepcopy(state)
                    new_state.act(i, j)
                    new_mcts_string = ''
                    new_mcts_string += str(new_state.P_Distance)
                    if new_state.P1_Action == 'sweep(startup)' or new_state.P1_Action == 'kick(startup_1)' or new_state.P1_Action == 'kick(startup_2)' or new_state.P1_Action == 'recovery':
                        new_mcts_string += str(new_state.P1_Action)
                    else:
                        new_mcts_string += str(None)
                    if new_state.P2_Action == 'sweep(startup)' or new_state.P2_Action == 'kick(startup_1)' or new_state.P2_Action == 'kick(startup_2)' or new_state.P2_Action == 'recovery':
                        new_mcts_string += str(new_state.P2_Action)
                    else:
                        new_mcts_string += str(None)
                    mcts_tree[mcts_string]['children'][new_mcts_string] = None
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        return choice

