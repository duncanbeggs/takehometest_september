import pandas as pd
import os
import datetime
import sys
from check_args import *

# This function takes a file of timestamps and returns a dictionary mapping
# Each timestamp to its count of connections
def conn_counter(df, timestamps_f):
    

if __name__ == "__main__":
    # Check that the user input the correct arguments
    check_args()
    
    # save args to local variables for clarity
    f_path = sys.argv[1]

    u_time = sys.argv[2]#get date from arguments
    time_ms = int(u_time[-3:])#get millisecond component from arg(last 3 digits)
    print(time_ms)
    u_time = datetime.datetime.strptime(u_time[:-4], '%Y-%m-%d %H:%M:%S')# format argument time
    u_time = (u_time.timestamp() * 1000) + time_ms
    print(u_time)

    # Open file to be read. If this file was larger than a gig we could use a
    # buffer reading of this file, reading 20mb or so per iteration.
    df = pd.read_csv(f_path)
    df['endTs'] = pd.to_datetime(df['endTs'], format='%Y-%m-%d %H:%M:%S.%f')

    #create start times in epoch format because the math is easier/faster
    df['t_start'] = df['endTs'].astype('int64')//1e6
    
    #create end time from adding timeTaken to t_start
    df['t_end'] = df['t_start'] + df['timeTaken']

    pd.options.display.float_format = '{:.4f}'.format

    # in below loop for connections that were open during the specified user time
    conn_count = 0
    for i, row in df.iterrows():
        print(row['endTs'], row['t_start'], row['t_end'])
        if row['t_start'] <= u_time <= row['t_end']:
            print("Found one!")
            conn_count += 1


    print("*******************************************************")
    print("*** There were", conn_count, "connections open at specified time ***")
    print("*******************************************************")
    



