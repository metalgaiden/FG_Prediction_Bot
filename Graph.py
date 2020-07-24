import text_fighter
import os
from timeit import default_timer as time
import matplotlib.pyplot as plt

time_counts = []
health = []

for i in range(0,7):
    t  = time()
    h = text_fighter.script_input('mcts_bot', 'kick_bot')
    health.append(h)
    time_counts.append(time()-t)

print(time_counts)
li = [1,2,3,4,5,6,7]
plt.plot(li,time_counts,lw = 1)
plt.plot(li,health,lw = 1, color='#ff2d00')
plt.title('Sweep to Kick')

plt.xlabel('Runs')
plt.ylabel('Time/Health')
plt.savefig("test.png")
