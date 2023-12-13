# Zoom Attendence Metrics
Collate information from Zoom attendence reports

## Requirements
python 3.11\
pandas

## Set up
In terminal:
```
pip install pandas
```
or 
```
pip3 install pandas
```

## How to use
In terminal run:
```
python AttendeeMetrics.py Input Output
```
or
```
python3 AttendeeMetrics.py Input Output
``` 
where Input is the path to the folder containing files or folders with Zoom attendence reports and Output is the path to the folder where you want to save the results. These two folders must be different.

## Output
The script should output three .csv files
- Attendees_per_Region.csv: Number of attendees from each country for all sessions
- Sessions_Attended.csv: Total number of sessions attended by each attendee and which sessions they attended (1 if attended, 0 if absent)
- Total_Attendees_per_Session.csv: Total number of attendees for each session
