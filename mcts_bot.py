import json
import random
import copy

class mcts_bot:
    move_queue = []
    prev_state = None

    def pick_action(self, state):
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b', 'ph', 'pm', 'pl']
        mcts_string = self.get_string(state)

        if self.prev_state != None:
            prev_move = self.get_string(self.prev_state)
            print(prev_move)
            print(mcts_string)
            mcts_tree[prev_move]['children'][mcts_string] += 1
        if mcts_string not in mcts_tree.keys():
            mcts_tree[mcts_string] = {'children':{}, 'p1_damage':{}, 'p2_damage':{}}
            for i in possible_actions:
                for j in possible_actions:
                    new_state = copy.deepcopy(state)
                    new_state.act(i, j)
                    new_mcts_string = self.get_string(new_state)
                    mcts_tree[mcts_string]['p1_damage'][new_mcts_string] = new_state.P1_Health - state.P1_Health
                    mcts_tree[mcts_string]['p2_damage'][new_mcts_string] = new_state.P2_Health - state.P2_Health
                    mcts_tree[mcts_string]['children'][new_mcts_string] = 0

        while len(self.move_queue) <= 1:
            mcts_parent = None
            mcts_node = mcts_string
            for i in range(len(self.move_queue)):
                mcts_parent = mcts_node
                mcts_node = max(mcts_tree[mcts_node]['children'], key=mcts_tree[mcts_node]['children'].get)
            if mcts_parent != None:
                if mcts_tree[mcts_parent]['children'][mcts_node] == 0:
                    prob = 0
                else:
                    prob = mcts_tree[mcts_parent]['children'][mcts_node] / sum(mcts_tree[mcts_parent]['children'].values())
            else:
                prob = 1
            risk = 0
            reward = 0
            self.move_queue.append(random.choice(possible_actions))

        choice = self.move_queue.pop()
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        self.prev_state = copy.deepcopy(state)
        return choice

    def get_string(self, statein):
        new_string = str(statein.P_Distance)
        new_string += ' '
        new_string += str(statein.P1_Action)
        new_string += ' '
        new_string += str(statein.P2_Action)
        return new_string
