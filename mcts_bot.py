import json
import random
import copy
from collections import deque

class mcts_bot:
    move_queue = deque([])
    prev_state = None

    def pick_action(self, state, player):
        maxdepth = 20
        rollouts = 20
        with open('mcts_tree.json') as f:
            mcts_tree = json.load(f)
        mcts_string = self.get_string(state)

        self.add_to_tree(mcts_tree, mcts_string, state)

        if self.prev_state != None:
            prev_move = self.get_string(self.prev_state)
            try:
                mcts_tree[prev_move]['children'][mcts_string] += 1
            except:
                pass
        self.prev_state = copy.deepcopy(state)

        while len(self.move_queue) <= 5:
            mcts_parent = None
            mcts_node = mcts_string
            curr_state = copy.deepcopy(state)
            for i in range(len(self.move_queue)):
                mcts_parent = mcts_node
                mcts_node = max(mcts_tree[mcts_node]['children'], key=mcts_tree[mcts_node]['children'].get)
                curr_state = self.get_state(mcts_node, state)
                self.add_to_tree(mcts_tree, mcts_node, curr_state)
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
                curr_state = self.get_state(node, state)
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
            best_score = -100
            if check_risk_nodes :
                if player == 'p1':
                    risk = self.rollout(maxdepth, rollouts, 1, False, curr_state)
                    for node in check_risk_nodes:
                        try:
                            score = prob + (1 - risk)
                        except:
                            score = 0
                        if score > best_score:
                            best_node = node
                            best_score = score
                else:
                    risk = self.rollout(maxdepth, rollouts, 2, False, curr_state)
                    for node in check_risk_nodes:
                        try:
                            score = prob + (1 - risk)
                        except:
                            score = 0
                        if score > best_score:
                            best_node = node
                            best_score = score

            if rollout_nodes != []:
                if player == 'p1':
                   
                    for node in rollout_nodes:
                        risk = self.rollout(maxdepth, rollouts, 1, False, self.get_state(node,curr_state))
                        reward = self.rollout(maxdepth, rollouts, 2, True, self.get_state(node,curr_state))
                        try:
                            score = reward + prob + (1 - risk)
                        except:
                            score = 0
                        if score > best_score:
                            best_node = node
                            best_score = score
                else:
                    for node in rollout_nodes:
                        risk = self.rollout(maxdepth, rollouts, 2, False, self.get_state(node,curr_state))
                        reward = self.rollout(maxdepth, rollouts, 1, True, self.get_state(node,curr_state))
                        try:
                            score = reward + prob + (1 - risk)
                        except:
                            score = 0
                        if score > best_score:
                            best_node = node
                            best_score = score

            print(best_node, best_score)
            action = self.move_to_action(best_node, player)
            self.move_queue.append(action)

        print(self.move_queue)
        choice = self.move_queue.popleft()
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

    def get_state(self, stringin, state):
        word_list = stringin.split()
        new_state = copy.deepcopy(state)
        new_state.initialize(int(word_list[0]), word_list[1], word_list[2], 1, 1)
        return new_state

    def move_to_action(self, node, player):
        name_to_action = {'punch(active)':'p', 'sweep(startup)':'s', 'sweep(active)':'s1', 'kick(startup_1)':'k', 'kick(startup_2)':'k1', 'kick(active)':'k2', 'standing_block':'sb', 'crouch_block':'cb', 'move_forward':'f', 'move_backwards':'b', 'parry_high':'ph', 'parry_mid':'pm', 'parry_low':'pl', 'recovery':'r'}
        word_list = node.split()
        if player == 'p1':
            action = word_list[1]
        else:
            action = word_list[2]
        if action == None:
            return None
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

    def rollout(self, maxdepth, rollouts, player, reward, state):
        possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b', 'ph', 'pm', 'pl']
        win = 0
        overall = rollouts
        while overall > 0:
            new_state=copy.deepcopy(state)
            count = maxdepth
            if player == 1:
                playerhealth = new_state.P1_Health
            else:
                playerhealth = new_state.P2_Health
            while count > 0:
                new_state.act(random.choice(possible_actions),random.choice(possible_actions))
                if reward == True:
                    if player == 1:
                        if new_state.P2_Health < playerhealth:
                            break
                        elif new_state.P1_Health<playerhealth:
                            win += 1
                            break
                    else:
                        if new_state.P1_Health < playerhealth:
                            break
                        elif new_state.P2_Health<playerhealth:
                            win += 1
                            break
                if reward == False:
                    if player == 1:
                        if new_state.P1_Health<playerhealth:
                            win += 1
                            break
                    else:
                        if new_state.P2_Health<playerhealth:
                            win += 1
                            break

                count -= 1

            overall =  overall - 1
        return float(win/rollouts)
