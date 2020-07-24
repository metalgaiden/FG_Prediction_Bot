import pygame
from mcts_bot import mcts_bot
import importlib

class gameState:
    P_Distance = 3
    P1_Action = None
    P2_Action = None
    P1_Health = 15
    P2_Health = 15
    new_distance = P_Distance

    def initialize(self, dist, p1, p2, h1, h2):
        self.P_Distance = dist
        self.P1_Action = p1
        self.P2_Action = p2
        self.P1_Health = h1
        self.P2_Health = h2

    def punch(self, p2, player):
        if self.P_Distance < 2 or (self.P_Distance == 2 and p2 == 'f'):
            if p2 != 'sb' and p2 != 'cb' and p2 != 'ph' and p2 != 's' and p2 != 's1' and not (self.P_Distance == 1 and p2 == 'b'):
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'punch(active)'
        else:
            self.P2_Action = 'punch(active)'

    def sweep(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'sweep(startup)'
        else:
            self.P2_Action = 'sweep(startup)'

    def sweep_1(self, p2, player):
        if self.P_Distance < 3 or (self.P_Distance == 3 and p2 == 'f'):
            if p2 != 'cb' and p2 != 'pl' and not (self.P_Distance == 2 and p2 == 'b'):
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'sweep(active)'
        else:
            self.P2_Action = 'sweep(active)'
    
    def kick(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'kick(startup_1)'
        else:
            self.P2_Action = 'kick(startup_1)'

    def kick_1(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'kick(startup_2)'
        else:
            self.P2_Action = 'kick(startup_2)'

    def kick_2(self, p2, player):
        if self.P_Distance < 4 or (self.P_Distance == 4 and p2 == 'f'):
            if p2 != 'sb' and p2 != 'pm' and not(self.P_Distance == 3 and p2 == 'b'):
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'kick(active)'
        else:
            self.P2_Action = 'kick(active)'

    def sblock(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'standing_block'
        else:
            self.P2_Action = 'standing_block'

    def cblock(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'crouch_block'
        else:
            self.P2_Action = 'crouch_block'

    def parry_high(self, p2, player):
        if p2 == 'p' and self.P_Distance < 2:
            if player == 'P1':
                self.P2_Health -= 1
            else:
                self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'parry_high'
        else:
            self.P2_Action = 'parry_high'
        
    def parry_mid(self, p2, player):
        if p2 == 'k2' and self.P_Distance < 4:
            if player == 'P1':
                self.P2_Health -= 1
            else:
                self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'parry_mid'
        else:
            self.P2_Action = 'parry_mid'

    def parry_low(self, p2, player):
        if p2 == 's1' and self.P_Distance < 3:
            if player == 'P1':
                self.P2_Health -= 1
            else:
                self.P1_Health -= 1
        if player == 'P1':
            self.P1_Action = 'parry_low'
        else:
            self.P2_Action = 'parry_low'

    def recovery(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'recovery'
        else:
            self.P2_Action = 'recovery'

    def forward(self, p2, player):
        if self.P_Distance <= 0:
            if player == 'P1':
                self.P1_Action = 'recovery'
            else:
                self.P2_Action = 'recovery'
        else:
            self.new_distance -= 1
            if player == 'P1':
                self.P1_Action = 'move_forward'
            else:
                self.P2_Action = 'move_forward'

    def backwards(self, p2, player):
        if self.P_Distance >= 4:
            if player == 'P1':
                self.P1_Action = 'recovery'
            else:
                self.P2_Action = 'recovery'
        else:
            self.new_distance += 1
            if player == 'P1':
                self.P1_Action = 'move_backwards'
            else:
                self.P2_Action = 'move_backwards'

    actions = {'p':punch, 's':sweep, 's1':sweep_1, 'k':kick, 'k1':kick_1, 'k2':kick_2, 'sb':sblock, 'cb':cblock, 'f':forward, 'b':backwards, 'ph':parry_high, 'pm':parry_mid, 'pl':parry_low, 'r':recovery}

    def act(self, p1, p2):
        if self.P1_Action == 'sweep(startup)':
            p1 = 's1'
        elif self.P1_Action == 'kick(startup_1)':
            p1 = 'k1'
        elif self.P1_Action == 'kick(startup_2)':
            p1 = 'k2'
        elif self.P1_Action == 'parry_high' or self.P1_Action == 'parry_mid' or self.P1_Action == 'parry_low':
            p1 = 'r'
        if self.P2_Action == 'sweep(startup)':
            p2 = 's1'
        elif self.P2_Action == 'kick(startup_1)':
            p2 = 'k1'
        elif self.P2_Action == 'kick(startup_2)':
            p2 = 'k2'
        elif self.P2_Action == 'parry_high' or self.P2_Action == 'parry_mid' or self.P2_Action == 'parry_low':
            p2 = 'r'
        self.actions[p1](self, p2, 'P1')
        self.actions[p2](self, p1, 'P2')
        self.P_Distance = self.new_distance

def game(state, identity_1, identity_2):
    print('here is a list of all possible actions:')
    print('p:punch, s:sweep, k:kick, sb:stand block, cb:crouch block, f:move forward, b: backwards, ph:parry_high, pm:parry_mid, pl:parry_low')
    if identity_1 == 'mcts_bot':
        bot1 = mcts_bot()
    if identity_2 == 'mcts_bot':
        bot2 = mcts_bot()
    while state.P1_Health > 0 and state.P2_Health > 0:
        print('the distance between players is', state.P_Distance)
        if identity_1 == 'mcts_bot':
            p1 = bot1.pick_action(state, 'p1', identity_2)
        elif state.P1_Action == 'sweep(startup)':
            p1 = 's1'
        elif state.P1_Action == 'kick(startup_1)':
            p1 = 'k1'
        elif state.P1_Action == 'kick(startup_2)':
            p1 = 'k2'
        elif state.P1_Action == 'parry_high' or state.P1_Action == 'parry_mid' or state.P1_Action == 'parry_low':
            p1 = 'r'
        else:
            try:
                bot = importlib.__import__(identity_1)
                p1 = bot.pick_action(state)
            except:
                print('input player 1 action')
                p1 = input()
        if identity_2 == 'mcts_bot':
            p2 = bot2.pick_action(state, 'p2', identity_1)
        elif state.P2_Action == 'sweep(startup)':
            p2 = 's1'
        elif state.P2_Action == 'kick(startup_1)':
            p2 = 'k1'
        elif state.P2_Action == 'kick(startup_2)':
            p2 = 'k2'
        elif state.P2_Action == 'parry_high' or state.P2_Action == 'parry_mid' or state.P2_Action == 'parry_low':
            p2 = 'r'
        else:
            try:
                bot = importlib.__import__(identity_2)
                p2 = bot.pick_action(state)
            except:
                print('input player 2 action')
                p2 = input()
        state.act(p1, p2)
        print('player 1 uses', state.P1_Action, 'with health', state.P1_Health)
        print('player 2 uses', state.P2_Action, 'with health', state.P2_Health)
    if state.P1_Health == state.P2_Health:
        print('draw')
    elif state.P1_Health > state.P2_Health:
        print('player 1 wins')
    elif state.P1_Health < state.P2_Health:
        print('player 2 wins')
    return state.P1_Health
        
def script_input(identity_1, identity_2):
    x = gameState()
    return game(x, identity_1, identity_2)
    
if __name__ == "__main__":
    # print('Who is player 1?')
    # identity_1 = input()
    identity_1 = 'mcts_bot'
    # print('Who is player 2?')
    # identity_2 = input()
    identity_2 = 'sweep_bot'
    x = gameState()
    game(x, identity_1, identity_2)
