import text_fighter
import os
from timeit import default_timer as time
import matplotlib.pyplot as plt

time_counts = []

for i in range(0,5):
    t  = time()
    os.system('python3 text_fighter.py')
    time_counts.append(time()-t)

print(time_counts)
li = [1,2,3,4,5,6]
plt.plot(time_counts,li,lw = 1)
plt.title('Time taken')

plt.xlabel('Time')
plt.ylabel('Runs')
plt.savefig("test.png")