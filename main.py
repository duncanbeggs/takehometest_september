import pandas as pd
import os
import datetime
import sys


def print_usage():
    print("****************************************************************************")
    print("Please run script with correct parameters.")
    print("Argument 1: Location of input file.")
    print("Argument 2: Unix timestamp to check.Requires yyyy-MM-dd hh:mm:ss.sss format.")
    print("EXAMPLE:: python main.py docs/log.csv \"2017-10-23 12:00:00\"") 
    print("****************************************************************************")

# Double check that the date the user has entered is in the correct format
def check_ts(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        raise ValueError("Incorrect date format. Should be yyyy-MM-dd hh:mm:ss")
        return False

# Check that the correct number of arguments have been entered and that they are in the correct format
def check_args():
    if len(sys.argv) == 1:
        print("No arguments provided!")
        print_usage()
        sys.exit()
    elif len(sys.argv) == 2:
        print("One argument provided. Two required.")
        print_usage()
        sys.exit()
    elif len(sys.argv) > 3:
        print("Too many arguments provided!")
        print_usage()
        sys.exit()

    f_path = sys.argv[1]
    u_time = sys.argv[2]
    
    if not os.path.isfile(f_path):
        print("Argument ", f_path, " is not a valid file.")
        print_usage()
        sys.exit()

    # check if argument for datetime is in correct format
    if not check_ts(u_time): 
        print_usage()
        sys.exit()
        

if __name__ == "__main__":
    
    # Check that the user input the correct arguments
    check_args()
    
    # save args to local variables for clarity
    f_path = sys.argv[1]
    u_time = sys.argv[2]

    # Open file to be read. If this file was larger than a gig we could use a
    # buffer reading of this file, reading 20mb or so per iteration.
    df = pd.read_csv(f_path)
    print(df.head())

    
