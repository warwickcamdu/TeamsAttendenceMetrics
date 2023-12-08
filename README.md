# Teams Attendence Metrics
Collate information from Teams attendence reports

## Requirements
python 3.11\
pandas

## How to use
In terminal run:
```
python AttendeeMetrics.py Input Output
```
Where Input is the path to the folder containing the Teams attendence reports and Output is the path to the folder where you want to save the results. These two folders must be different.

## Output
The script should output three .csv files
- Attendees_per_Region.csv: Number of attendees from each country for all sessions
- Sessions_Attended.csv: Total number of sessions attended by each attendee and which sessions they attended (1 if attended, 0 if absent)
- Total_Attendees_per_Session.csv: Total number of attendees for each session
