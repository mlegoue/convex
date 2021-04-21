import csv
import matplotlib.pyplot as plt
import math


times_find = {}
times_subset = {}
total= {}

with open('time_find_convex.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_find[nb_nodes] = mapped_row
        nb_nodes += 1

with open('time_convex_subset.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_subset[nb_nodes] = mapped_row
        nb_nodes += 1

with open('time_total.csv', 'r') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:
        mapped_row = list(map(float, row))
        total[i] = mapped_row
        i += 1

def trace_pts_find(x, times):
    plt.plot([x]*500, times[x], '+', color='b')

def trace_pts_subset(x, times):
    plt.plot([x]*500, times[x], '+', color='g')

plt.figure()

for i in range(2, 21):
    trace_pts_find(i, times_find)
    trace_pts_subset(i, times_subset)

plt.plot([*range(2, 21)], total[0], 'r', label="new find convex")
plt.plot([*range(2, 21)], total[1], 'orange', label="old find convex")

plt.legend()
plt.show()

plt.figure()



