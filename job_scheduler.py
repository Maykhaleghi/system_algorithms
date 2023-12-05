import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

def FIFO (df):
    '''FIFO or FCFS,
    First Come First Service,
    the job that arrives first has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a simple horizantal bar chart,
    *together with the sorted data by arrive time.'''

    # sort the dataframe named 'df' 
    # by 'AT' values.
    p = df.sort_values("AT")
    # create lists of response time and
    # finish time for each job.
    start_point = []
    finish_point = []
    # extracte a list of all the arrive times.
    AT = p["AT"].tolist()
    # initialize value of 'var'
    # to the arrive time of the first job.
    # meaning the earliest arrive time.
    var = AT[0]
    
    for i,j in enumerate(p["jobs"].tolist()):

        # ERROR HANDLING:
        # if the first or other jobs have ended
        # yet new jobs haven't arrived,
        # there should be a gap between the latest job and the next one.
        if var < AT[i]:
            var = AT[i]

        start_point.append(var)
        
        # extracte the cbt of the job being processed.
        element_cbt = p.query("jobs == @j")["CBT"].tolist()

        # update 'var' to the finish time of the job.
        var = var + element_cbt[0]
        
        finish_point.append(var)

    print(p)
    print("start time:", start_point)
    print("finish time:", finish_point)

    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    # create a horizantal bar chart, using 'barh'.
    gantt = gnt.barh(p["jobs"], p["CBT"], left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    plt.show()


######################
#Testing...
######################
#valid test data:
df = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3"],
        "AT": [3, 0, 3],
        "CBT": [1, 2, 3],
    }
)
######################
FIFO (df)