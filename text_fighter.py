class gameState:
    P_Distance = 3
    P1_Action = None
    P2_Action = None
    P1_Health = 1
    P2_Health = 1

    def punch(self, p2, player):
        if self.P_Distance < 2 or (self.P_Distance == 2 and p2 == 'f'):
            if p2 == 'sb' or p2 == 'cb' or (self.P_Distance == 1 and p2 == 'b') or p2 == 's':
                if player == 'P1':
                    self.P1_Action = 'punch(active)'
                else:
                    self.P2_Action = 'punch(active)'
            else:
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        else:
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
            if player == 'P1':
                self.P1_Action = 'sweep(active)'
            else:
                self.P2_Action = 'sweep(active)'
            if p2 != 'cb' or not (self.P_Distance == 2 and p2 == 'b'):
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        else:
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
            if p2 == 'sb' or (self.P_Distance == 3 and p2 == 'b'):
                if player == 'P1':
                    self.P1_Action = 'kick(active)'
                else:
                    self.P2_Action = 'kick(active)'
            else:
                if player == 'P1':
                    self.P2_Health -= 1
                else:
                    self.P1_Health -= 1
        else:
            if player == 'P1':
                self.P1_Action = 'kick(active)'
            else:
                self.P2_Action = 'kick(active)'

    def sblock(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'standing block'
        else:
            self.P2_Action = 'standing block'

    def cblock(self, p2, player):
        if player == 'P1':
            self.P1_Action = 'crouch block'
        else:
            self.P2_Action = 'crouch block'

    def forward(self, p2, player):
        self.P_Distance -= 1
        if player == 'P1':
            self.P1_Action = 'move forward'
        else:
            self.P2_Action = 'move forward'

    def backwards(self, p2, player):
        self.P_Distance += 1
        if player == 'P1':
            self.P1_Action = 'move backwards'
        else:
            self.P2_Action = 'move backwards'

    actions = {'p':punch, 's':sweep, 's1':sweep_1, 'k':kick, 'k1':kick_1, 'k2':kick_2, 'sb':sblock, 'cb':cblock, 'f':forward, 'b':backwards}

    def act(self, p1, p2):
        self.actions[p1](self, p2, 'P1')
        self.actions[p2](self, p1, 'P2')

def game(state):
    while state.P1_Health > 0 and state.P2_Health > 0:
        print('the distance between players is', state.P_Distance)
        if state.P1_Action == 'sweep(startup)':
            p1 = 's1'
        elif state.P1_Action == 'kick(startup_1)':
            p1 = 'k1'
        elif state.P1_Action == 'kick(startup_2)':
            p1 = 'k2'
        else:
            print('input player 1 action')
            p1 = input()
        if state.P2_Action == 'sweep(startup)':
            p2 = 's1'
        elif state.P2_Action == 'kick(startup_1)':
            p2 = 'k1'
        elif state.P2_Action == 'kick(startup_2)':
            p2 = 'k2'
        else:
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
    

if __name__ == "__main__":
    x = gameState()
    game(x)
