import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()

tasks = ["task1", "task2", "task3"]
CBT = [3, 2, 5]


def function(tasks, CBT):
    start = []
    end = []
    var = 0
    for i in CBT:
        start.append(var)
        var = var + i
        end.append(var)
    print(start)
    print(end)

    fig, gnt = plt.subplots(figsize=(10, 6))

    gantt = gnt.barh(tasks, CBT, left = start)
    #gantt = gnt.bar(x = tasks , height = CBT)
    gnt.bar_label(gantt, end, padding = -17, color = "white")
    plt.show()

function(tasks, CBT)