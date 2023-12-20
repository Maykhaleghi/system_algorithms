import random
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
    '''SJF,
    Shortest Job First,
    the job whose CBT is smallest has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a broken horizantal bar chart,
    *together with the data sorted by arrive time.'''

    q = int(input("Enter the time slice!"))
    # sort the dataframe named 'df' 
    # by 'AT' values.
    sorted_df = df.sort_values("AT")
    # this number will be needed throughout the code.
    n = len(sorted_df["jobs"].tolist())
    # extracte a list of all the arrive times and CBTs.
    AT = sorted_df["AT"].tolist()
    CBT = sorted_df["CBT"].tolist()
    # initialize value of 'time_counter'
    # to the arrive time of the first job.
    # meaning the earliest arrive time.
    # this value will hold for use the milisecond that we are at.
    time_counter = AT[0]
    # create a  new column with initial value of empty list
    # which will hold the (xmin, xwidth) for the chart.
    sorted_df["x_range"] = np.empty((len(sorted_df), 0)).tolist()
    # a value which only use is to stop 
    # the while loop at the right time.
    b = False

    # to check which job to turn to process next 
    # we need a loop.
    while b == False:
        # a list to keep track of jobs 
        # which have arrived at one point of time 
        # specified by 'time_counter'
        arrived_list = sorted_df.query("AT <= @time_counter")["jobs"].tolist()
        arrived_cbt = sorted_df.query("jobs == @arrived_list")["CBT"].tolist()
        # deleting the finished jobs with 0 CBT.
        arrived_cbt = [i for i in arrived_cbt if i != 0]

        # ERROR HANDLING:
        # to show the gap from finish time of the last job
        # to arrive time of the next job.
        if arrived_cbt == []: 
            time_counter = AT[len(arrived_list)]
            continue

        min_cbt = min(arrived_cbt)

        # add the time to x_range column
        index = sorted_df[sorted_df["CBT"]== min_cbt].index.values
        index = index[0]
        x_min_cbt = sorted_df.at[index, "x_range"]
        if min_cbt < q:
            x_min_cbt.append((time_counter, min_cbt))
        else:
            x_min_cbt.append((time_counter, q))
        sorted_df.at[index, "x_range"] = x_min_cbt

        # subtract the run time from CBT of the job and
        # add to the time_counter the amount of run time
        # for this time slice.
        if min_cbt < q:
            time_counter = time_counter + min_cbt
            sorted_df.at[index, "CBT"] = 0
        else:
            time_counter = time_counter + q
            sorted_df.at[index, "CBT"] = min_cbt - q
        # to break from the loop when all jobs have finished.
        if sum(CBT) <= time_counter:
            b = True

    fig, gnt = plt.subplots(figsize=(10, 6))
    gnt.set_ylim(0, 100)
    gnt.set_xlim(0, sum(CBT))
    xranges = sorted_df["x_range"].tolist()
    yticks_list = []
    for i in range(0, n):
        yranges = (i * (100 / n), (100 / n))
        yticks_list.append(((i + 1) * (100 / n)) - (0.5 * (100 / n)))
        gnt.broken_barh(xranges[i], yranges)
    jobs = sorted_df["jobs"].tolist()
    gnt.set_yticks(yticks_list)
    gnt.set_yticklabels(jobs)
    
    plt.show()

######################
    
def Random (df):

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
    random_cbt = []
    random_jobs = []
    for i in AT:
        # a list to keep track of jobs 
        # which have arrived at one point of time 
        # specified by 'time_counter'
        arrived_jobs = sorted_df.query("AT <= @time_counter")["jobs"].tolist()
        print(arrived_jobs)
        #arrived_cbt = sorted_df.query("jobs == @arrived_list")["CBT"].tolist()
        rand_job = random.choice(arrived_jobs)
        random_jobs.append(rand_job)
        rand_cbt = sorted_df.query("jobs == @rand_job")["CBT"].tolist()
        random_cbt.append(rand_cbt[0])
        start_point.append(time_counter)
        time_counter = time_counter + rand_cbt[0]
        finish_point.append(time_counter)
        index = sorted_df[sorted_df["jobs"]== rand_job].index.values
        index = index[0]
        sorted_df = sorted_df.drop(index)
        print(sorted_df)
        print("ifffffffffffff")




    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    print("random jobs", random_jobs)
    print("random cbt", random_cbt)
    # create a horizantal bar chart, using 'barh'.
    gantt = gnt.barh(random_jobs, random_cbt, left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    plt.show()



######################
#Testing...
######################
#valid test data:
df1 = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3"],
        "AT": [0, 1, 3],
        "CBT": [1, 2, 3],
    }
)
######################
######################
#valid test data:
df2 = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3", "job4", "job5"],
        "AT": [1, 2, 3, 4, 5],
        "CBT": [5, 1, 3, 4, 2],
    }
)
######################
#FIFO (df2)
SJF (df2)
#Random(df2)