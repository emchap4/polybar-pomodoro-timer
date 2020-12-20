#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import datetime
import os

'''
Change the following directory with where this file and `timer.json` are located
'''
os.chdir("/home/emchap4/scripts/polybar/pomodoro")

'''
# JSON Setup (in timer.json):
{
    "end_time": 100,            # Denotes what epoch the current session will end
    "is_paused": false,         # Is the current timer paused?
    "is_work_time": true,       # Is it work time as opposed to break time? 
    "length_of_break": 5,       # The length (in minutes) of a break session 
    "length_of_work": 25,       # The length (in minutes) of a work session 
    "current_display": "0:0:15" # The time left in the current session
}
'''
# display : None -> String
# Returns the human-readable current display
def display():
    with open("timer.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        
        if data["is_work_time"]:
            session_type = "Work"
        else:
            session_type = "Break"

        # Next session?
        if data["current_display"] == "00:00":
            if data["is_work_time"]:
                data["end_time"] = time.time() + data["length_of_break"]*60
            else:
                data["end_time"] = time.time() + data["length_of_work"]*60

            data["is_work_time"] = not data["is_work_time"]

        if not data["is_paused"]:
            data["current_display"] = time_diff(data["end_time"])

        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()
        return(session_type + ": " + data["current_display"])

# toggle : None -> None
# Toggles the `is_paused` parameter in the json file
def toggle():
    with open("timer.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        if data["is_paused"]:
            new_date_time = datetime.datetime.strptime(data["current_display"], "%M:%S").replace(year = 1970)

            # still don't know why it's off by 5 hours, but this works
            new_seconds = time.mktime(new_date_time.timetuple()) - 5*60*60 

            data["end_time"] = time.time() + new_seconds

            
        data["is_paused"] = not data["is_paused"]

        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()

# next_session : None -> None
# Proceeds to the next session artificially
def next_session():
    with open("timer.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        if data["is_work_time"]:
            data["end_time"] = time.time() + data["length_of_break"]*60
        else:
            data["end_time"] = time.time() + data["length_of_work"]*60

        data["is_work_time"] = not data["is_work_time"]

        data["current_display"] = time_diff(data["end_time"])

        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()

# time_diff : Number -> String
# Returns the time until _end_ (epoch).
def time_diff(end):
    diff = round(end - time.time())
    value = datetime.datetime.fromtimestamp(diff + 5*60*60) # Adds 5 hours
    return value.strftime("%M:%S") 

def main():
    if (len(sys.argv) == 1):
        print(display())
    elif (sys.argv[1] == "toggle"):
        toggle()
    elif (sys.argv[1] == "next"):
        next_session()

if __name__ == "__main__":
    main()
