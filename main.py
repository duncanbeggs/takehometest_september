import pandas as pd
import os
import datetime
import sys
from check_args import *

# This function takes a file of timestamps and returns a dictionary mapping
# Each timestamp to its count of connections
def conn_counter(df, timestamps_file):
    #create list then populate with lines from the file
    ts_list = []
    with open(timestamps_file) as f:
        for ln in f:
            ln = ln.strip()#trim trailing whitespace and newline
            check_ts(ln)# func to make sure date is in correct format
            ts_list.append(ln)
    
    # iterate through list of time stamps to create dictionary of connection counts
    ts_dict = {}
    for ts in ts_list:
        time_ms = int(ts[-3:])#get millisecond component from arg(last 3 digits)
        e_ts = datetime.datetime.strptime(ts[:-4], '%Y-%m-%d %H:%M:%S')# format argument time
        e_ts = (e_ts.timestamp() * 1000) + time_ms
        
        # count active connections at timestamp time
        conn_count = 0
        for i, row in df.iterrows():
            if row['t_start'] <= e_ts <= row['t_end']:
                conn_count += 1

        ts_dict[ts] = conn_count

    return ts_dict

 
if __name__ == "__main__":
    
    # Check that the user input the correct arguments
    check_args()
    
    # save args to local variables for clarity
    f_path = sys.argv[1]

    u_time = sys.argv[2]#get date from arguments
    time_ms = int(u_time[-3:])#get millisecond component from arg(last 3 digits)
    u_time = datetime.datetime.strptime(u_time[:-4], '%Y-%m-%d %H:%M:%S')# format argument time
    u_time = (u_time.timestamp() * 1000) + time_ms

    # Open file to be read. If this file was larger than a gig we could use a
    # buffer reading of this file, reading 20mb or so per iteration.
    df = pd.read_csv(f_path)
    df['endTs'] = pd.to_datetime(df['endTs'], format='%Y-%m-%d %H:%M:%S.%f')

    #create start times in epoch format because the math is easier/faster
    df['t_start'] = df['endTs'].astype('int64')//1e6
    
    #create end time from adding timeTaken to t_start
    df['t_end'] = df['t_start'] + df['timeTaken']

    pd.options.display.float_format = '{:.4f}'.format

    print("*******************************************************")
    print("Searcing for connections at", sys.argv[2])
    # in below loop for connections that were open during the specified user time
    conn_count = 0
    for i, row in df.iterrows():
        if row['t_start'] <= u_time <= row['t_end']:
            conn_count += 1

    print("*******************************************************")
    print("*** There were", conn_count, "connections open at specified time ***")
    print("*******************************************************")


    # Timestamps file
    ts_file = "timestamps_list.txt"
    print("Program will now read in timestamp list from file:", ts_file)    
    open_conn_dict = conn_counter(df, ts_file)
    for k, v in open_conn_dict.items():
        print(k, "->", v, "open connections.")

    # Calculate the statistics for minimum, maximum and average on the list of values
    conn_max = max(open_conn_dict.keys(), key=(lambda k: open_conn_dict[k]))
    conn_min = min(open_conn_dict.keys(), key=(lambda k: open_conn_dict[k]))
    conn_avg = sum(open_conn_dict.values()) / float(len(open_conn_dict))
    print("*******************************************************")
    print("********************* Stats ***************************")
    print("*** Max:", conn_max, "with", open_conn_dict[conn_max])
    print("*** Min:", conn_min, "with", open_conn_dict[conn_min])
    print("*** Average:", conn_avg)


