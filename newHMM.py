"""

Name:Bria Weisblat
Date: 03/13/24
Assignment:Project #9 (Questions 4-5)
Due Date: 03/24/24
About this project: This project creates a Hidden Markov Model of the recorded PM2.5 Index based
on data from the Changping data set. The evidence for this HMM is the day. The evidence is
true if the day is within the first two weeks of the data set (days 1-14) and the evidence
is false if the day is within the last two weeks of the data set (days 15-28). Prior uses the default
because there is a 50/50 split between true and false for the evidence.I broke the PM2.5 readings
into four ranges: low(0-50), moderate(51-100), high(101-150), and very high(151+). I then calculated
the true and false probabilities for each of the four ranges of the PM2.5 attribute.All together
this makes the HMM.
Assumptions:Assumes proper implementations of everything that is imported.
All work below was performed by Bria Weisblat

"""

import random
import pandas as pd
import numpy as np
from statistics import mean
from probability import *
from utils import rounder

random.seed("aima-python")

#Load the file
file = r"PRSA_Data_Changping_20130301-20170228.csv"
df = pd.read_csv(file)

#Define the four PM2.5 ranges
def label_PM25 (row):
    if row['PM2.5'] < 0:
        return np.nan
    elif 0 <= row['PM2.5'] <= 50:
        return "Low"
    elif 51 <= row['PM2.5'] <= 100:
        return "Moderate"
    elif 101 <= row['PM2.5'] <= 150:
        return "High"
    elif row['PM2.5'] > 150:
        return "Very High"

#Compute sensor evidence
def day_evidence (row):
   # If the day is in the first two weeks of the evidence
   if row['day'] in range(1,15) :
      return True
   return False

df['PM2.5_label'] = df.apply (lambda row: label_PM25(row), axis=1)
df['day_evidence'] = df.apply (lambda row: day_evidence(row), axis=1)

#Create counts for all 16 transitions
CountLowLow = 0
CountLowModerate = 0
CountLowHigh = 0
CountLowVeryHigh = 0
CountModerateLow = 0
CountModerateModerate = 0
CountModerateHigh = 0
CountModerateVeryHigh = 0
CountHighLow = 0
CountHighModerate = 0
CountHighHigh = 0
CountHighVeryHigh = 0
CountVeryHighLow = 0
CountVeryHighModerate = 0
CountVeryHighHigh = 0
CountVeryHighVeryHigh = 0

#Create counts for the evidence (T=true F=false)
CountTLow = 0
CountTModerate = 0
CountTHigh = 0
CountTVeryHigh = 0
CountFLow = 0
CountFModerate = 0
CountFHigh = 0
CountFVeryHigh = 0

#Track the number of each of the 16 types of transitions
#Count the number of evidence variable showings
indxPM25Label = df.columns.get_loc("PM2.5_label")
indxDayEvidLabel = df.columns.get_loc("day_evidence")
for i in range(1,df.shape[0]-1):
    if df.iat[i,indxPM25Label]=='Low':
        if df.iat[i, indxDayEvidLabel]:
            CountTLow+=1
        else:
            CountFLow+=1
        if df.iat[i+1,indxPM25Label]=='Low':
            CountLowLow+=1
        elif df.iat[i+1,indxPM25Label]=='Moderate':
            CountLowModerate+=1
        elif df.iat[i+1,indxPM25Label]=='High':
            CountLowHigh+=1
        elif df.iat[i+1,indxPM25Label]=='Very High':
            CountLowVeryHigh+=1
    elif df.iat[i,indxPM25Label]=='Moderate':
        if df.iat[i, indxDayEvidLabel]:
            CountTModerate+=1
        else:
            CountFModerate+=1
        if df.iat[i+1,indxPM25Label]=='Low':
            CountModerateLow+=1
        elif df.iat[i+1,indxPM25Label]=='Moderate':
            CountModerateModerate+=1
        elif df.iat[i+1,indxPM25Label]=='High':
            CountModerateHigh+=1
        elif df.iat[i+1,indxPM25Label]=='Very High':
            CountModerateVeryHigh+=1
    elif df.iat[i,indxPM25Label]=='High':
        if df.iat[i, indxDayEvidLabel]:
            CountTHigh+=1
        else:
            CountFHigh+=1
        if df.iat[i+1,indxPM25Label]=='Low':
            CountHighLow+=1
        elif df.iat[i+1,indxPM25Label]=='Moderate':
            CountHighModerate+=1
        elif df.iat[i+1,indxPM25Label]=='High':
            CountHighHigh+=1
        elif df.iat[i+1,indxPM25Label]=='Very High':
            CountHighVeryHigh+=1
    elif df.iat[i,indxPM25Label]=='Very High':
        if df.iat[i, indxDayEvidLabel]:
            CountTVeryHigh+=1
        else:
            CountFVeryHigh+=1
        if df.iat[i+1,indxPM25Label]=='Low':
            CountVeryHighLow+=1
        elif df.iat[i+1,indxPM25Label]=='Moderate':
            CountVeryHighModerate+=1
        elif df.iat[i+1,indxPM25Label]=='High':
            CountVeryHighHigh+=1
        elif df.iat[i+1,indxPM25Label]=='Very High':
            CountVeryHighVeryHigh+=1

#Calculate the probabilities for each transition
ProbLowLow = CountLowLow / (CountLowLow + CountLowModerate + CountLowHigh + CountLowVeryHigh)
ProbLowModerate = CountLowModerate / (CountLowLow + CountLowModerate + CountLowHigh + CountLowVeryHigh)
ProbLowHigh = CountLowHigh / (CountLowLow + CountLowModerate + CountLowHigh + CountLowVeryHigh)
ProbLowVeryHigh = CountLowVeryHigh / (CountLowLow + CountLowModerate + CountLowHigh + CountLowVeryHigh)
ProbModerateLow = CountModerateLow / (CountModerateLow + CountModerateModerate + CountModerateHigh + CountModerateVeryHigh)
ProbModerateModerate = CountModerateModerate / (CountModerateLow + CountModerateModerate + CountModerateHigh + CountModerateVeryHigh)
ProbModerateHigh = CountModerateHigh / (CountModerateLow + CountModerateModerate + CountModerateHigh + CountModerateVeryHigh)
ProbModerateVeryHigh = CountModerateVeryHigh / (CountModerateLow + CountModerateModerate + CountModerateHigh + CountModerateVeryHigh)
ProbHighLow = CountHighLow / (CountHighLow + CountHighModerate + CountHighHigh + CountHighVeryHigh)
ProbHighModerate = CountHighModerate / (CountHighLow + CountHighModerate + CountHighHigh + CountHighVeryHigh)
ProbHighHigh = CountHighHigh / (CountHighLow + CountHighModerate + CountHighHigh + CountHighVeryHigh)
ProbHighVeryHigh = CountHighVeryHigh / (CountHighLow + CountHighModerate + CountHighHigh + CountHighVeryHigh)
ProbVeryHighLow = CountVeryHighLow / (CountVeryHighLow + CountVeryHighModerate + CountVeryHighHigh + CountVeryHighVeryHigh)
ProbVeryHighModerate = CountVeryHighModerate / (CountVeryHighLow + CountVeryHighModerate + CountVeryHighHigh + CountVeryHighVeryHigh)
ProbVeryHighHigh = CountVeryHighHigh / (CountVeryHighLow + CountVeryHighModerate + CountVeryHighHigh + CountVeryHighVeryHigh)
ProbVeryHighVeryHigh = CountVeryHighVeryHigh / (CountVeryHighLow + CountVeryHighModerate + CountVeryHighHigh + CountVeryHighVeryHigh)
#############################

#Calculate the probabilities for the evidence
ProbTLow = CountTLow / (CountTLow + CountFLow)
ProbTModerate = CountTModerate / (CountTModerate + CountFModerate)
ProbTHigh = CountTHigh / (CountTHigh + CountFHigh)
ProbTVeryHigh = CountTVeryHigh / (CountTVeryHigh + CountFVeryHigh)
ProbFLow = CountFLow / (CountTLow + CountFLow)
ProbFModerate = CountFModerate / (CountTModerate + CountFModerate)
ProbFHigh = CountFHigh / (CountTHigh + CountFHigh)
ProbFVeryHigh = CountFVeryHigh / (CountTVeryHigh + CountFVeryHigh)

################################

#Transition probabilities
transition = [[ProbLowLow, ProbLowModerate, ProbLowHigh, ProbLowVeryHigh],
              [ProbModerateLow, ProbModerateModerate, ProbModerateHigh, ProbModerateVeryHigh],
              [ProbHighLow, ProbHighModerate, ProbHighHigh, ProbHighVeryHigh],
              [ProbVeryHighLow, ProbVeryHighModerate, ProbVeryHighHigh, ProbVeryHighVeryHigh]]

#Evidence probabilities
sensor = [[ProbTLow, ProbTModerate, ProbTHigh, ProbTVeryHigh],
          [ProbFLow, ProbFModerate, ProbFHigh, ProbFVeryHigh]]



#Assign and print the HMM
pm25HMM = HiddenMarkovModel(transition, sensor)
print('Question #4: HMM')
print(pm25HMM.__dict__)

#Assign five hardcoded values
evidence = [T, T, T, T, F]
print()
print('Question #5: Run forwardOnly with an evidence set of 5 hardcoded values')
print(forwardOnly(pm25HMM, evidence))

