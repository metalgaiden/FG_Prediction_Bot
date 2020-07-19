class gameState:
    P_Distance = 5
    P1_Action = None
    P2_Action = None
    P1_Health = 1
    P2_Health = 1

    def punch(self, p2, player):
        if self.P_Distance < 2:
            if p2 == 'sblock' or p2 == 'cblock' or (self.P_Distance == 1 and p2 == 'move back') or p2 == 'sweep':
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
        if self.P_Distance < 3:
            if p2 == 'cblock' or (self.P_Distance == 2 and p2 == 'move back'):
                if player == 'P1':
                    self.P1_Action = 'sweep(active)'
                else:
                    self.P2_Action = 'sweep(active)'
            else:
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
        if self.P_Distance < 4:
            if p2 == 'sblock' or (self.P_Distance == 3 and p2 == 'move back'):
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
            self.P1_Action = 'moving forward'
        else:
            self.P2_Action = 'moving forward'

    def backwards(self, p2, player):
        self.P_Distance += 1
        if player == 'P1':
            self.P1_Action = 'moving backwards'
        else:
            self.P2_Action = 'moving backwards'

    actions = {'punch':punch, 'sweep':sweep, 'sweep_1':sweep_1, 'kick':kick, 'kick_1':kick_1, 'kick_2':kick_2, 'sblock':sblock, 'cblock':cblock, 'f':forward, 'b':backwards}

    def act(self, p1, p2):
        self.actions[p1](self, p2, 'P1')
        self.actions[p2](self, p1, 'P2')

def game(state):
    while state.P1_Health > 0 and state.P2_Health > 0:
        print('input player 1 action')
        p1 = input()
        print('input player 2 action')
        p2 = input()
        state.act(p1, p2)
        print(state.P1_Action)
        print(state.P2_Action)
        print(state.P_Distance)
    if state.P1_Health == state.P2_Health:
        print('draw')
    elif state.P1_Health > state.P2_Health:
        print('player 1 wins')
    elif state.P1_Health < state.P2_Health:
        print('player 2 wins')
    

if __name__ == "__main__":
    x = gameState()
    game(x)
