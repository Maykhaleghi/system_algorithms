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
    
def HRRN (df):
    '''Highest Response Ratio Next,
    The job which has the least RPR at the moment has the highst priority,
    RR is the Reapone Ratio which is calculated as (wating time)/(CBT) in this code,
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
    # create a  new column with initial value of empty list
    # which will hold the (xmin, xwidth) for the chart.
    sorted_df["RPR"] = np.empty((len(sorted_df), 0)).tolist()

    start_point = []
    finish_point = []
    process_cbt = []
    process_order = []

    # a loop to iterate over each process.
    while sorted_df["CBT"].tolist() != []:
        # a list to keep track of jobs 
        # which have arrived at one point of time 
        # specified by 'time_counter'
        arrived_list = sorted_df.query("AT <= @time_counter")["processes"].tolist()
        arrived_cbt = sorted_df.query("processes == @arrived_list")["CBT"].tolist()
        # ERROR HANDLING:
        # to show the gap from finish time of the last job
        # to arrive time of the next job.
        if arrived_cbt == [] and max(AT) > time_counter: 
            # 'arrived_jobs_df' is only created for the purpose of error handling.
            arrived_list_df = df.query("AT <= @time_counter")["processes"].tolist()
            print("time_counter", time_counter)
            time_counter = AT[len(arrived_list_df)]
            continue
        
        start_point.append(time_counter)
        RPR_list = []
        for i, process in enumerate(arrived_list):
            process_at = sorted_df.query("processes == @process")["AT"].tolist()
            RPR = (time_counter - process_at[0]) / arrived_cbt[i]
            print("(process_at[0] - time_counter)", process_at[0] - time_counter)
            print("rpr", RPR)
            index = sorted_df[sorted_df["processes"] == process].index.values
            index = index[0]
            sorted_df.at[index, "RPR"] = RPR
            RPR_list.append(RPR)
            
        RPR_max = max(RPR_list)
        
        same_RR_list = sorted_df.query("RPR == @RPR_max")["processes"].tolist()
        if len(same_RR_list) > 1:
            p_at = sorted_df.query("processes == @same_RR_list")["AT"].tolist()
            # check to see if all the arrive times are the same
            result = all (element == p_at[0] for element in p_at)
            if result == False:
                min_at = min(p_at)
                chosen_row = sorted_df.loc[(sorted_df["RPR"] == RPR_max) & (sorted_df["AT"] == min_at)]
            else:
                p_cbt = sorted_df.query("processes == @same_RR_list")["CBT"].tolist()
                min_cbt = min(p_cbt)
                chosen_row = sorted_df.loc[(sorted_df["RPR"] == RPR_max) & (sorted_df["CBT"] == min_cbt)]

        else:
            chosen_row = sorted_df.loc[(sorted_df["RPR"] == RPR_max)]

            print(sorted_df)
                
        chosen_cbt = chosen_row["CBT"].tolist()
        process_cbt.append(chosen_cbt[0])
        time_counter = time_counter + chosen_cbt[0]

        # add the time to x_range column
        chosen_p = chosen_row["processes"].tolist()
        index = sorted_df[sorted_df["processes"] == chosen_p[0]].index.values
        index = index[0]

        #min_process = sorted_df.at[index, "processes"]
        process_order.append(chosen_p[0])
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
    
def RR (df):
    
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
    n = len(sorted_df["processes"].tolist())
    p_list = sorted_df["processes"].tolist()
    # extracte a list of all the arrive times and CBTs.
    AT = sorted_df["AT"].tolist()
    CBT = df["CBT"].tolist()
    # initialize value of 'time_counter'
    # to the arrive time of the first job.
    # meaning the earliest arrive time.
    # this value will hold for use the milisecond that we are at.
    time_counter = AT[0]
    # create a  new column with initial value of empty list
    # which will hold the (xmin, xwidth) for the chart.
    sorted_df["x_range"] = np.empty((len(sorted_df), 0)).tolist()
    sorted_df["FWT"] = -1
    # a value which only use is to stop 
    # the while loop at the right time.
    b = False

    # to check which job to turn to process next 
    # we need a loop.
    ii = 1
    
    while b == False:
        
        # a list to keep track of jobs 
        # which have arrived at one point of time 
        # specified by 'time_counter'
        arrived_list = sorted_df.query("AT <= @time_counter")["processes"].tolist()
        arrived_cbt = sorted_df.query("processes == @arrived_list")["CBT"].tolist()
        # deleting the finished jobs with 0 CBT.
        arrived_cbt = [i for i in arrived_cbt if i != 0]

        # ERROR HANDLING:
        # to show the gap from finish time of the last job
        # to arrive time of the next job.
        if arrived_cbt == [] and max(AT) > time_counter: 
            # 'arrived_jobs_df' is only created for the purpose of error handling.
            arrived_list_df = df.query("AT <= @time_counter")["processes"].tolist()
            time_counter = AT[len(arrived_list_df)]
            continue

        for p in p_list:
            p_at = sorted_df.query("processes == @p")["AT"].tolist()
            p_cbt = sorted_df.query("processes == @p")["CBT"].tolist()
            if (time_counter >= p_at[0]) and (p_cbt[0] != 0):
                print(p_cbt)
                wt = time_counter - p_at[0]
                index = sorted_df[sorted_df["processes"] == p].index.values
                index = index[0]
                sorted_df.at[index, "FWT"] = wt
        
        p_wt_list = sorted_df["FWT"].tolist()
        print("p_wt_list", p_wt_list)
        max_wt = max(p_wt_list)      
        chosen_p = sorted_df.query("FWT == @max_wt")["processes"].tolist()
        print("chosen_p", chosen_p)
        chosen_p = chosen_p[0]
        print("chosen_p", chosen_p)
                

        print("##############################################", ii)
        ii = ii + 1
        
        chosen_cbt = sorted_df.query("processes == @chosen_p")["CBT"].tolist()

        # add the time to x_range column
        index = sorted_df[sorted_df["processes"] == chosen_p].index.values
        index = index[0]
        x_chosen_cbt = sorted_df.at[index, "x_range"]
        if chosen_cbt[0] < q:
            x_chosen_cbt.append((time_counter, chosen_cbt[0]))
        else:
            x_chosen_cbt.append((time_counter, q))
        sorted_df.at[index, "x_range"] = x_chosen_cbt

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # subtract the run time from CBT of the job and
        # add to the time_counter the amount of run time
        # for this time slice.
        if chosen_cbt[0] < q:
            print("if1")
            time_counter = time_counter + chosen_cbt[0]
            sorted_df.at[index, "CBT"] = 0
            sorted_df.at[index, "FWT"] = -1
        else:
            print("else1")
            time_counter = time_counter + q
            sorted_df.at[index, "CBT"] = chosen_cbt[0] - q
            #p_order.append(chosen_p)
        sorted_df.at[index, "AT"] = time_counter
        # to break from the loop when all jobs have finished.
        real_cbt = sorted_df["CBT"].tolist()
        print("real_cbt", real_cbt)
        #print(time_counter)
        #print(real_cbt)
        if (time_counter >= sum(CBT)) and (sum(real_cbt) == 0):
            b = True

    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    # set limits so later on the placing of each tick can be precise.
    gnt.set_ylim(0, 100)
    gnt.set_xlim(0, time_counter)
    xranges = sorted_df["x_range"].tolist()
    yticks_list = []
    # we need a loop to iterate over each job 
    # so we can create the bar for each job.
    for i in range(0, n):
        # calculate the place of ticks for each job.
        yranges = (i * (100 / n), (100 / n))
        yticks_list.append(((i + 1) * (100 / n)) - (0.5 * (100 / n)))
        gnt.broken_barh(xranges[i], yranges)
    processes = sorted_df["processes"].tolist()
    gnt.set_yticks(yticks_list)
    gnt.set_yticklabels(processes)
    
    plt.show()

######################
    
def SRTF (df):
    '''SRTF,
    Shortest Remaining Time First,
    the process whose CBT is the least has the highest priority,
    *accepts one parameter with the format of a pandas dataframe,
    *this function provides a broken horizantal bar chart,
    *together with the data sorted by arrive time.'''

    q = int(input("Enter the time slice!"))
    # sort the dataframe named 'df' 
    # by 'AT' values.
    sorted_df = df.sort_values("AT")
    # this number will be needed throughout the code.
    n = len(sorted_df["processes"].tolist())
    # extracte a list of all the arrive times and CBTs.
    AT = sorted_df["AT"].tolist()
    CBT = df["CBT"].tolist()
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
        arrived_list = sorted_df.query("AT <= @time_counter")["processes"].tolist()
        arrived_cbt = sorted_df.query("processes == @arrived_list")["CBT"].tolist()
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
        real_cbt = sorted_df["CBT"].tolist()
        print(time_counter)
        print(real_cbt)
        if (time_counter >= sum(CBT)) and (sum(real_cbt) == 0):
            b = True

    # create a figure.
    fig, gnt = plt.subplots(figsize=(10, 6))
    # set limits so later on the placing of each tick can be precise.
    gnt.set_ylim(0, 100)
    gnt.set_xlim(0, time_counter)
    xranges = sorted_df["x_range"].tolist()
    yticks_list = []
    # we need a loop to iterate over each job 
    # so we can create the bar for each job.
    for i in range(0, n):
        # calculate the place of ticks for each job.
        yranges = (i * (100 / n), (100 / n))
        yticks_list.append(((i + 1) * (100 / n)) - (0.5 * (100 / n)))
        gnt.broken_barh(xranges[i], yranges)
    processes = sorted_df["processes"].tolist()
    gnt.set_yticks(yticks_list)
    gnt.set_yticklabels(processes)
    
    plt.show()

######################
#Testing...
######################
#valid test data with gap:
df1 = pd.DataFrame(
    {
        "processes": ["p1", "p2", "p3"],
        "AT": [1, 4, 11],
        "CBT": [5, 5, 1],
    }
)
######################
######################
#valid test data without gap:
df2 = pd.DataFrame(
    {
        "processes": ["p1", "p2", "p3", "p4", "p5"],
        "AT": [1, 2, 3, 4, 5],
        "CBT": [10, 29, 3, 7, 12],
    }
)
######################
#FCFS (df1)
#SPN(df2)
#HRRN(df2)
RR(df2)
#SRTF(df2)
