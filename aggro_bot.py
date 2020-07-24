import random

def pick_action(state):
    possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
    distance = state.P_Distance

    if distance > 3:
        # Too far for attacks, move forward
        # 1% p, 5% s, 5% k, 8% sb, 5% cb, 75% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 5, 5, 8, 5, 75, 1), k=7)

    elif distance > 2:
        #In range for sweep, favor for Sweep
        # 1% p, 70% s, 2% k, 5% sb, 2% cb, 10% f, 10% b
        choice = random.choices(possible_actions, weights=(1, 70, 2, 5, 2, 15, 5), k=7)
            
    elif distance > 1:
        #In range of Sweep and Kick, favor for Kick
        # 1% p, 13% s, 70% k, 5% sb, 5% cb, 5% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 13, 70, 5, 5, 5, 1), k=7)

    else:
        #In range of Punch, Kick and Sweep, favor for Punch
        # 75% p, 22% s, 1% k, 5% sb, 5% cb, 1% f, 1% b
        choice = random.choices(possible_actions, weights=(75, 12, 1, 5, 5, 1, 1), k=7)
        
    return choice[0] #Returns an array but we just just need the first element as main choice
