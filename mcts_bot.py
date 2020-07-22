import json
import random
import copy

class mcts_bot:
    move_queue = []
    prev_move = None

    def pick_action(self, state):
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
        choice = random.choice(possible_actions)
        mcts_string = self.get_string(state)
        if self.prev_move != None:
            mcts_tree[self.prev_move]['children'][mcts_string] += 1
        if mcts_string not in mcts_tree.keys():
            mcts_tree[mcts_string] = {'children':{}, 'risk':0, 'reward':0}
            for i in possible_actions:
                for j in possible_actions:
                    new_state = copy.deepcopy(state)
                    new_state.act(i, j)
                    new_mcts_string = self.get_string(new_state)
                    mcts_tree[mcts_string]['children'][new_mcts_string] = 0
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        self.prev_move = mcts_string
        return choice

    def get_string(self, state):
        mcts_string = ''
        mcts_string += state.P_Distance
        if state.P1_Action == 'sweep(startup)' or state.P1_Action == 'kick(startup_1)' or state.P1_Action == 'kick(startup_2)' or state.P1_Action == 'recovery':
            mcts_string += str(state.P1_Action)
        else:
            mcts_string += str(None)
        if state.P2_Action == 'sweep(startup)' or state.P2_Action == 'kick(startup_1)' or state.P2_Action == 'kick(startup_2)' or state.P2_Action == 'recovery':
            mcts_string += str(state.P2_Action)
        else:
            mcts_string += str(None)
        return mcts_string
