import random

def pick_action(state):
    possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
    distance = state.P_Distance
 
    if distance > 1:
        # Too far for attacks, move forward
        # 1% p, 5% s, 5% k, 8% sb, 5% cb, 75% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 0, 5, 8, 5, 80, 1), k=7)

    else:
        #In range of Punch, Kick and Sweep, favor for Punch
        # 75% p, 7% s, 1% k, 5% sb, 5% cb, 1% f, 1% b
        choice = random.choices(possible_actions, weights=(80, 7, 1, 5, 5, 1, 1), k=7)
        
    return choice[0] #Returns an array but we just just need the first element as main choice
