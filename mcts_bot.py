import json
import random
import copy
from collections import deque

class mcts_bot:
    move_queue = deque([])
    prev_state = None

    def pick_action(self, state, player):
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        mcts_string = self.get_string(state)

        self.add_to_tree(mcts_tree, mcts_string, state)

        if self.prev_state != None:
            prev_move = self.get_string(self.prev_state)
            print(prev_move)
            print(mcts_string)
            mcts_tree[prev_move]['children'][mcts_string] += 1
        self.prev_state = copy.deepcopy(state)

        while len(self.move_queue) <= 1:
            mcts_parent = None
            mcts_node = mcts_string
            this_state = copy.deepcopy(state)
            for i in range(len(self.move_queue)):
                mcts_parent = mcts_node
                possible_nodes = []
                for child in mcts_tree[mcts_node]['children']:
                    if self.move_to_action(child, player) == self.move_queue[-i-1]:
                        possible_nodes.append(child)
                mcts_node = max(possible_nodes)
                this_state.act(self.move_to_action(mcts_node, 'p1'), self.move_to_action(mcts_node, 'p2'))
                self.add_to_tree(mcts_tree, mcts_node, state)
            if mcts_parent != None:
                if mcts_tree[mcts_parent]['children'][mcts_node] == 0:
                    prob = 0
                else:
                    prob = mcts_tree[mcts_parent]['children'][mcts_node] / sum(mcts_tree[mcts_parent]['children'].values())
            else:
                prob = 1
            check_risk_nodes = []
            dead_nodes = []
            rollout_nodes = []
            for node in mcts_tree[mcts_node]['children'].keys():
                curr_state = copy.deepcopy(this_state)
                curr_state.act(self.move_to_action(node, 'p1'), self.move_to_action(node, 'p2'))
                self.add_to_tree(mcts_tree, node, curr_state)
                if player == 'p1':
                    if mcts_tree[mcts_node]['p1_damage'][node] > 0:
                        dead_nodes.append(node)
                    elif mcts_tree[mcts_node]['p2_damage'][node] > 0:
                        check_risk_nodes.append(node)
                    else:
                        rollout_nodes.append(node)
                else:
                    if mcts_tree[mcts_node]['p2_damage'][node] > 0:
                        dead_nodes.append(node)
                    elif mcts_tree[mcts_node]['p1_damage'][node] > 0:
                        check_risk_nodes.append(node)
                    else:
                        rollout_nodes.append(node)
            if dead_nodes != []:
                best_node = random.choice(dead_nodes)
            else:
                best_node = node
            best_score = 0
            if check_risk_nodes != []:
                if player == 'p1':
                    risk = sum(mcts_tree[mcts_parent]['p1_damage'].values()) #replace with rollout function
                    for node in check_risk_nodes:
                        score = 1*(sum(mcts_tree[node]['p2_damage'].values()) * prob / (risk))
                        if score > best_score:
                            best_node = node
                            best_score = score
                else:
                    risk = sum(mcts_tree[mcts_parent]['p2_damage'].values())
                    for node in check_risk_nodes:
                        score = 1*(sum(mcts_tree[node]['p1_damage'].values()) * prob / (risk))
                        if score > best_score:
                            best_node = node
                            best_score = score
            if rollout_nodes != []:
                if player == 'p1':
                    risk = sum(mcts_tree[node]['p1_damage'].values())
                    for node in check_risk_nodes:
                        score = 1*((sum(mcts_tree[node]['p2_damage'].values())/len(mcts_tree[node]['p2_damage'])) * prob / (risk))
                        if score > best_score:
                            best_node = node
                            best_score = score
                else:
                    risk = sum(mcts_tree[node]['p2_damage'].values())
                    for node in check_risk_nodes:
                        score = 1*((sum(mcts_tree[node]['p1_damage'].values())/len(mcts_tree[node]['p1_damage'])) * prob / (risk))
                        if score > best_score:
                            best_node = node
                            best_score = score

            action = self.move_to_action(best_node, player)
            self.move_queue.append(action)

        print(self.move_queue)
        choice = self.move_queue.popleft()
        print(choice)
        with open('mcts_tree.json', 'w') as f:
            json.dump(mcts_tree, f, indent=2)
        return choice

    def get_string(self, statein):
        new_string = str(statein.P_Distance)
        new_string += ' '
        new_string += str(statein.P1_Action)
        new_string += ' '
        new_string += str(statein.P2_Action)
        return new_string

    def move_to_action(self, node, player):
        name_to_action = {'punch(active)':'p', 'sweep(startup)':'s', 'sweep(active)':'s1', 'kick(startup_1)':'k', 'kick(startup_2)':'k1', 'kick(active)':'k2', 'standing_block':'sb', 'crouch_block':'cb', 'move_forward':'f', 'move_backwards':'b', 'parry_high':'ph', 'parry_mid':'pm', 'parry_low':'pl', 'recovery':'r'}
        word_list = node.split()
        if player == 'p1':
            action = word_list[1]
        else:
            action = word_list[2]
        return name_to_action[action]

    def add_to_tree(self, mcts_tree, mcts_string, state):
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b', 'ph', 'pm', 'pl']
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
