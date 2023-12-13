import sys
import pandas as pd
import csv
import os

def getData(filepath):
    ##
    # Input:
    # filepath: string, path to file e.g. 'Data\81035313871 - Attendee Report.csv'
    # Output:
    # topic: title of session
    # df: pandas dataframe
    ##
    # Get row numbers for each section: host, panelist, attendee
    i=1
    with open(filepath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if i==4:
                topic=row[0]
            elif row[0] == 'Host Details':
                host_row = i
            elif row[0]== 'Panelist Details':
                pan_row_start = i
            elif row[0]== 'Attendee Details':
                pan_row_end = i-2
                att_row_start = i
            i=i+1
    # Read data from each section into dataframes. Select columns and remove non-attendees
    hostdf=pd.read_csv(filepath, header=host_row, nrows=1, index_col=False)
    hostdf=hostdf.filter(regex='User Name|Email|Country') 
    pandf=pd.read_csv(filepath, header=pan_row_start, nrows=pan_row_end-pan_row_start, index_col=False)
    pandf=pandf.filter(regex='User Name|Email|Country') 
    attdf=pd.read_csv(filepath, header=att_row_start, index_col=False)
    attdf=attdf[attdf['Attended'].str.contains('No')==False]
    if attdf.filter(regex='User Name|Email|Country').shape[1] == 3:
        attdf=attdf.filter(regex='User Name|Email|Country')
    else:
        attdf=attdf.filter(regex='Name|Email|Country')
        attdf['User Name']=attdf['First Name']+' '+attdf['Last Name']
        attdf=attdf.filter(regex='User Name|Email|Country')
    # Combine dataframes into one and drop duplicates based on email
    df=pd.concat([hostdf, pandf, attdf])
    df=df.drop_duplicates(subset=['Email'])
    # Rename username column
    df=df.rename(columns={ df.columns[0]: 'User Name' })
    return topic,df

def calculateAttendeeMetrics(inputpath, outputpath):
    ##
    # Input:
    # inputpath: string, path to directory containing attendence reports'
    # outputpath: string, path to directory for saving total value csvs.'
    # Must not be the same!
    # Output:
    # 3 .csv files
    ##
    # Create dataframe for all files in folder with columns indicating attendence at each session (1) and total sessions attended.
    # Create dataframes with total values and output to .csv files
    if inputpath != outputpath:
        finaldf=pd.DataFrame(columns=['User Name','Email','Country/Region Name'])
        substring = 'Attendee Report.csv'
        for root, subdirs, files in os.walk(inputpath):
            for filename in files:
                if substring in filename:
                    topic,df=getData(os.path.join(root, filename))
                    df[topic]=[1]*df.shape[0]
                    finaldf=pd.merge(finaldf,df,how='outer',on=['User Name','Email','Country/Region Name'])
        finaldf.iloc[:, 3:] = finaldf.iloc[:, 3:].fillna(value=0)
        # Total sessions attended by attendee
        finaldf.insert(loc=3, column='Total Sessions Attended', value=finaldf[finaldf.columns[3:]].sum(axis=1))
        finaldf.to_csv(os.path.join(outputpath, 'Sessions_Attended.csv'))
        # Total attendees at each session
        totalAtt=pd.DataFrame(finaldf[finaldf.columns[4:]].sum(axis=0),columns=['Total Attendees'])
        totalAtt.to_csv(os.path.join(outputpath, 'Total_Attendees_per_Session.csv'))
        # Number attendees from
        country_counts = finaldf["Country/Region Name"].value_counts()
        country_counts.to_csv(os.path.join(outputpath, 'Attendees_per_Region.csv'))
    else:
        print("Input and output directories must be different")

if __name__ == "__main__":
    calculateAttendeeMetrics(sys.argv[1],sys.argv[2])