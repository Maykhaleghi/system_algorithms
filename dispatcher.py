import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

def FCFS (df):
    '''First Come First Service,
    the process that arrives first has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a simple horizantal bar chart,
    *together with the data sorted by arrive time.'''

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
    
    for i,j in enumerate(p["processes"].tolist()):

        # ERROR HANDLING:
        # if the first or other jobs have ended
        # yet new jobs haven't arrived,
        # there should be a gap between the latest job and the next one.
        if var < AT[i]:
            var = AT[i]

        start_point.append(var)
        
        # extracte the cbt of the job being processed.
        element_cbt = p.query("processes == @j")["CBT"].tolist()

        # update 'var' to the finish time of the job.
        var = var + element_cbt[0]
        
        finish_point.append(var)

    print(p)
    print("start time:", start_point)
    print("finish time:", finish_point)

    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    # create a horizantal bar chart, using 'barh'.
    gantt = gnt.barh(p["processes"], p["CBT"], left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    plt.show()

######################
    
def SPN (df):
    '''Shortest Job First,
    The job which has the shortest burst time has the highst priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a simple horizantal bar chart.'''

    sorted_df = df.sort_values("AT")
    #jobs = sorted_df["jobs"].tolist()
    AT = sorted_df["AT"].tolist()
     # initialize value of 'time_counter'
    # to the arrive time of the first job.
    # meaning the earliest arrive time.
    # this value will hold for use the milisecond that we are at.
    time_counter = AT[0]
    start_point = []
    finish_point = []
    process_cbt = []
    process_order = []

    # a loop to iterate over each process.
    while sorted_df["CBT"].tolist() != []:
        print("iffffffffffff")
        # a list to keep track of jobs 
        # which have arrived at one point of time 
        # specified by 'time_counter'
        arrived_list = df.query("AT <= @time_counter")["processes"].tolist()
        arrived_cbt = sorted_df.query("processes == @arrived_list")["CBT"].tolist()
        # ERROR HANDLING:
        # to show the gap from finish time of the last job
        # to arrive time of the next job.
        if arrived_cbt == [] and max(AT) > time_counter: 
            print("time_counter", time_counter)
            time_counter = AT[len(arrived_list)]
            continue
        
        start_point.append(time_counter)
        min_cbt = min(arrived_cbt)
        process_cbt.append(min_cbt)
        time_counter = time_counter + min_cbt

        # add the time to x_range column
        index = sorted_df[sorted_df["CBT"] == min_cbt].index.values
        index = index[0]

        min_process = sorted_df.at[index, "processes"]

        process_order.append(min_process)
        
        sorted_df = sorted_df.drop(index)
        
    print(process_order)
    print(process_cbt)
    print(start_point)
    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    # create a horizantal bar chart, using 'barh'.
    gantt = gnt.barh(process_order, process_cbt, left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    plt.show()

######################
#Testing...
######################
#valid test data with gap:
df1 = pd.DataFrame(
    {
        "processes": ["p1", "p2", "p3"],
        "AT": [0, 6, 2],
        "CBT": [3, 3, 1],
    }
)
######################
######################
#valid test data without gap:
df2 = pd.DataFrame(
    {
        "processes": ["p1", "p2", "p3", "p4", "p5"],
        "AT": [1, 2, 3, 4, 5],
        "CBT": [2, 1, 3, 1, 2],
    }
)
######################
#FCFS (df1)
SPN(df1)