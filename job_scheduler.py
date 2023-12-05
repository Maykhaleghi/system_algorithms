import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

df = pd.DataFrame(
    {
        "tasks": ["task1", "task2", "task3"],
        "AT": [3, 0, 2],
        "CBT": [3, 2, 1],
    }
)

def function(df):
    p = df.sort_values("AT")
    start = []
    end = []
    var = 0
    for i in p["tasks"]:
        start.append(var)
        print("var", var)
        
        x = p.query("tasks == @i")["CBT"].astype('int')
        print("varrrr", type(x))
        var = var + x
        #if var >= (p.query("tasks == @i")["AT"]):
            #var = p.query("tasks == @i")["AT"]
        #print("i", i)
        end.append(var)
    #print(start)
    #print(end)


    fig, gnt = plt.subplots(figsize=(10, 6))

    gantt = gnt.barh(p["tasks"], p["CBT"], left = start)
    #gantt = gnt.bar(x = tasks , height = CBT)
    gnt.bar_label(gantt, end, padding = -17, color = "white")
    plt.show()

function(df)