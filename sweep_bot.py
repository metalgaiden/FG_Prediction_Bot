import random

def pick_action(state):
    possible_actions = ['p', 's', 'k', 'sb', 'cb', 'f', 'b']
    distance = state.P_Distance

    if distance > 3:
        # Too far for attacks, move forward
        # 1% p, 5% s, 5% k, 8% sb, 5% cb, 75% f, 1% b
        choice = random.choices(possible_actions, weights=(1, 5, 5, 8, 5, 75, 1), k=7)

    else:
        #In range for sweep, favor for Sweep
        # 1% p, 80% s, 2% k, 5% sb, 2% cb, 10% f, 10% b
        choice = random.choices(possible_actions, weights=(1, 80, 2, 5, 2, 5, 5), k=7)

        return choice[0]
            