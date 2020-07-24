import random

def pick_action(state):
    possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
    distance = state.P_Distance

    if distance > 2:
        # Too far for kick, move forward
        # 1% p, 5% s, 5% k, 8% sb, 5% cb, 75% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 1, 4, 8, 5, 80, 1), k=7)
    
    else:
        #In range of Sweep and Kick, favor for Kick
        # 1% p, 13% s, 70% k, 5% sb, 5% cb, 5% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 3, 80, 5, 5, 5, 1), k=7)

    return choice[0] #Returns an array but we just just need the first element as main choice


        
