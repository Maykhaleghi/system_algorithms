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

def SJF (df):

    q = int(input("Enter the time slice!"))
    sorted_df = df.sort_values("AT")

    print(sorted_df)

    n = len(sorted_df["jobs"].tolist())
    b = "False"
    # extracte a list of all the arrive times.
    AT = sorted_df["AT"].tolist()
    CBT = sorted_df["CBT"].tolist()
    # initialize value of 'var'
    # to the arrive time of the first job.
    # meaning the earliest arrive time.
    time_counter = AT[0]
    # a list for keeping track of jobs 
    # which have arrived at the checking point.
    arrived_list = []
    # create a  new column with initial value of empty list.
    sorted_df["x_range"] = np.empty((len(sorted_df), 0)).tolist()
    print(sorted_df)

    while b == "False":

        arrived_list = sorted_df.query("AT <= @time_counter")["jobs"].tolist()
        print("arrived_list", arrived_list)
        arrived_cbt = sorted_df.query("jobs == @arrived_list")["CBT"].tolist()
        print("arrived_CBT", arrived_cbt)
        arrived_cbt = [i for i in arrived_cbt if i != 0]
        if arrived_cbt == []: 
            time_counter = AT[len(arrived_list)]
            continue

        min_cbt = min(arrived_cbt)
        print("min_cbt", min_cbt)

        # add the run time to x_range column
        index = sorted_df[sorted_df["CBT"]== min_cbt].index.values
        index = index[0]
        print("index", index)
        x_min_cbt = sorted_df.at[index, "x_range"]
        
        if min_cbt < q:
            x_min_cbt.append((time_counter, min_cbt))
        else:
            x_min_cbt.append((time_counter, q))
        
        sorted_df.at[index, "x_range"] = x_min_cbt

        # subtract the run time from 
        # add to the time_counter the amount of run time
        # for this time slice.
        if min_cbt < q:
            time_counter = time_counter + min_cbt
            sorted_df.at[index, "CBT"] = 0
        else:
            time_counter = time_counter + q
            sorted_df.at[index, "CBT"] = min_cbt - q
        print(time_counter)
        if sum(CBT) == time_counter:
            b = "True"
        # if all jobs have finished
        # then break out of the while loop.
        #if arrived_cbt == []:
            #b = "True"

    fig, gnt = plt.subplots(figsize=(10, 6))
    gnt.set_ylim(0, 100)
    gnt.set_xlim(0, sum(CBT))
    xranges = sorted_df["x_range"].tolist()
    #y_range = df["y_range"]
    print(sorted_df)
    print(df)
    yticks_list = []
    for i in range(0, n):
        yranges = (i * (100 / n), (100 / n))
        print("yranges, xranges", yranges, xranges[i])
        yticks_list.append(((i + 1) * (100 / n)) - (0.5 * (100 / n)))
        gnt.broken_barh(xranges[i], yranges)
    jobs = sorted_df["jobs"].tolist()
    print("ytick_list", yticks_list)
    gnt.set_yticks(yticks_list)
    gnt.set_yticklabels(jobs)
    
    plt.show()

######################
#Testing...
######################
#valid test data:
df = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3"],
        "AT": [0, 1, 4],
        "CBT": [1, 2, 3],
    }
)
######################
#FIFO (df)
SJF (df)