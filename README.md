# polybar-pomodoro-timer
A (very) simple pomodoro timer for Polybar.

## Usage:
Once installed, you can see both what type of session (either work or break) you are on and then the time remaning in that session. Right click to skip to next session and left click to pause/unpause the timer.

## Setup:
**Polybar's Config**
```
[module/timer]
type = custom/script
exec = python3 -u /PATH/TO/timer.py
click-left = python3 /PATH/TO/timer.py toggle
click-right = python3 /PATH/TO/timer.py next
interval = 1
```

**Timer Config (timer.json)**
```
{
    "end_time": 100,            # Denotes what epoch the current session will end
    "is_paused": false,         # Is the current timer paused?
    "is_work_time": true,       # Is it work time as opposed to break time? 
    "length_of_break": 5,       # The length (in minutes) of a break session 
    "length_of_work": 25,       # The length (in minutes) of a work session 
    "current_display": "0:0:15" # The time left in the current session
}
```
NOTE: The only two attributes that you should change are `length_of_break` and `length_of_work`.
