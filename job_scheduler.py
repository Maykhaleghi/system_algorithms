import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

def WT_TT (df, job_order, start, finish):
    df["WT"] = 0
    df["TT"] = 0
    for i, p in enumerate(job_order):
        index = df[df["jobs"] == p].index.values
        index = index[0]
        p_at = df.query("jobs == @p")["AT"].tolist()
        df.at[index, "WT"] = start[i] - p_at[0]
        df.at[index, "TT"] = finish[i] - p_at[0]
    all_wt = df["WT"].tolist()
    all_tt = df["TT"].tolist()
    avg_wt = sum(all_wt)/len(all_wt)
    avg_tt = sum(all_tt)/len(all_tt)
    
    return (avg_wt, avg_tt)

###################### 
    
def preemptive_TT_WT (df, xranges, job_order):
    df["WT"] = 0
    df["TT"] = 0
    for i, j in enumerate(job_order):
        index = df[df["jobs"] == j].index.values
        index = index[0]
        j_at = df.query("jobs == @j")["AT"].tolist()
        WT = xranges[i]
        wt = WT[0][0] - j_at[0]
        for j in range(1, len(WT)):
            wt = wt + (WT[j][0] - (WT[j-1][0] + WT[j-1][1]))
        df.at[index, "WT"] = wt
        df.at[index, "TT"] = (WT[-1][0] + WT[-1][1]) - j_at[0]
    all_wt = df["WT"].tolist()
    all_tt = df["TT"].tolist()
    avg_wt = sum(all_wt)/len(all_wt)
    avg_tt = sum(all_tt)/len(all_tt)

    return (avg_wt, avg_tt)

######################

def FIFO (df):
    '''FIFO or FCFS,
    First Come First Service,
    the job that arrives first has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a simple horizantal bar chart,
    *together with the data sorted by arrive time.'''

    start = time.time()
    p = df.sort_values("AT")
    start_point = []
    finish_point = []
    AT = p["AT"].tolist()
    time_counter = AT[0]
    
    for i,j in enumerate(p["jobs"].tolist()):

        # ERROR HANDLING:
        # if the first or other jobs have ended
        # yet new jobs haven't arrived,
        # there should be a gap between the latest job and the next one.
        if time_counter < AT[i]:
            time_counter = AT[i]

        start_point.append(time_counter)
        element_cbt = p.query("jobs == @j")["CBT"].tolist()
        time_counter = time_counter + element_cbt[0]
        finish_point.append(time_counter)

    # create the chart.
    fig, gnt = plt.subplots(figsize=(10, 6))
    gantt = gnt.barh(p["jobs"], p["CBT"], left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    avg_wt, avg_tt = WT_TT (df, p["jobs"], start_point, finish_point)
    end = time.time()
    elapsed_time = end - start
    return(plt, avg_wt, avg_tt, elapsed_time)

######################

def SJF (df):
    '''SJF,
    Shortest Job First,
    the job whose CBT is smallest has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a broken horizantal bar chart,
    *together with the data sorted by arrive time.'''

    q = int(input("you have called SJF; Enter the time slice!"))
    start = time.time()
    sorted_df = df.sort_values("AT")
    n = len(sorted_df["jobs"].tolist())
    AT = sorted_df["AT"].tolist()
    CBT = df["CBT"].tolist()
    time_counter = AT[0]
    sorted_df["x_range"] = np.empty((len(sorted_df), 0)).tolist()
    
    b = False
    
    while b == False:
        
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
        index = sorted_df[sorted_df["CBT"]== min_cbt].index.values
        index = index[0]
        x_min_cbt = sorted_df.at[index, "x_range"]
        if min_cbt < q:
            x_min_cbt.append((time_counter, min_cbt))
        else:
            x_min_cbt.append((time_counter, q))
        sorted_df.at[index, "x_range"] = x_min_cbt

        if min_cbt < q:
            time_counter = time_counter + min_cbt
            sorted_df.at[index, "CBT"] = 0
        else:
            time_counter = time_counter + q
            sorted_df.at[index, "CBT"] = min_cbt - q

        real_cbt = sorted_df["CBT"].tolist()
        if (time_counter >= sum(CBT)) and (sum(real_cbt) == 0):
            b = True

    # create the chart.
    fig, gnt = plt.subplots(figsize=(10, 6))
    gnt.set_ylim(0, 100)
    gnt.set_xlim(0, time_counter)
    xranges = sorted_df["x_range"].tolist()
    yticks_list = []
    for i in range(0, n):
        yranges = (i * (100 / n), (100 / n))
        yticks_list.append(((i + 1) * (100 / n)) - (0.5 * (100 / n)))
        gnt.broken_barh(xranges[i], yranges)
    job_order = sorted_df["jobs"].tolist()
    gnt.set_yticks(yticks_list)
    gnt.set_yticklabels(job_order)
    avg_wt, avg_tt = preemptive_TT_WT (df, xranges, job_order)
    end = time.time()
    elapsed_time = end - start
    return(plt, avg_wt, avg_tt, elapsed_time)

######################
    
def Random (df):
    '''Random,
    using the random library chooses the jobs to be processed,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a broken horizantal bar chart,
    *together with the data sorted by arrive time.'''

    start = time.time()
    sorted_df = df.sort_values("AT")
    AT = sorted_df["AT"].tolist()
    time_counter = AT[0]
    start_point = []
    finish_point = []
    random_cbt = []
    random_jobs = []

    while sorted_df["CBT"].tolist() != []:

        arrived_jobs = sorted_df.query("AT <= @time_counter")["jobs"].tolist()

        # ERROR HANDLING:
        # to show the gap from finish time of the last job
        # to arrive time of the next job.
        if arrived_jobs == [] and max(AT) > time_counter:
            # 'arrived_jobs_df' is only created for the purpose of error handling.
            arrived_jobs_df = df.query("AT <= @time_counter")["jobs"].tolist()
            print("time_counter", time_counter)
            time_counter = AT[len(arrived_jobs_df)]
            continue

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
        
    # create the chart.
    fig, gnt = plt.subplots(figsize=(10, 6))
    gantt = gnt.barh(random_jobs, random_cbt, left = start_point)
    gnt.bar_label(gantt, finish_point, padding = -17, color = "white")
    avg_wt, avg_tt = WT_TT (df, random_jobs, start_point, finish_point)
    end = time.time()
    elapsed_time = end - start
    return(plt, avg_wt, avg_tt, elapsed_time)

######################

def calculate (alg_name, df):

    print("\n######################")
    print("\n", alg_name.__doc__)
    plt, avg_wt, avg_tt, elapsed_time = alg_name(df)
    print("\n######################")
    print(df)
    print("######################")
    print("Average of Waiting Time: ", avg_wt)
    print("Average of Total Time: ", avg_tt)
    print("######################")
    plt.show()

######################

def the_best (alg_list, df):
    '''the_best,
    It is a function that tells you
    which algorithm is the best for your provided dataframe.
    *accepts two paramete; first a list of the algorithms you want to compare,
    second with the format of a pandas dataframe. 
    '''
    time_list = []
    wt_list = []
    for alg in alg_list:
        plt, avg_wt, avg_tt, elapsed_time = alg(df)
        wt_list.append(avg_wt)
        time_list.append(elapsed_time)
    print(wt_list)
    
    df_to_store = pd.DataFrame(
        {
            "Algorithm": alg_list,
            "Avg_WT": wt_list,
            "Elapsed_time": time_list,
        }
    )
    pd.options.display.float_format = '{: .18f}'.format

    print(df_to_store)
    min_value = min(wt_list)
    list_min = [i for i , j in enumerate(wt_list) if j == min_value]
    best_alg = []
    for index in list_min:
        best_alg.append(wt_list[index])
    
    min_wt = min(wt_list)
    best_wt = df_to_store.query("Avg_WT == @min_wt")["Algorithm"].tolist()
    min_time = min(time_list)
    best_time = df_to_store.query("Elapsed_time == @min_time")["Algorithm"].tolist()

    if best_wt == best_time:
        print("the best algorithm according to **waiting time** and **run_time** is ", best_wt)
    else:
        print("the best algorithm according to **waiting time** is ", best_wt)
        print("the best algorithm according to **Elapsed time** is ", best_time)

######################
#Testing...
######################
#valid test data:
df1 = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3"],
        "AT": [0, 6, 2],
        "CBT": [3, 3, 1],
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
######################
#valid test data without gap:
df3 = pd.DataFrame(
    {
        "jobs": ["job1", "job2", "job3", "job4", "job5"],
        "AT": [1, 2, 3, 4, 5],
        "CBT": [10, 29, 3, 7, 12],
    }
)
######################
#FIFO (df2)
#SJF (df1)
#calculate(FIFO, df1)
#calculate(SJF, df1)
#calculate(Random, df1)
the_best([FIFO, SJF, Random], df3)