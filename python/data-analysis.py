import sys
import requests
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
from IPython.display import display

from datetime import datetime
from matplotlib.dates import date2num

MIN = 70
MAX = 180
TIR = 70

response = requests.get(sys.argv[1], allow_redirects=True).content
current_time = datetime.now()
fileName = "buff" + str(datetime.timestamp(current_time)) + ".csv"
open(fileName, "wb").write(response)

df = pd.read_csv(fileName, index_col = 0)
glucose = df[['Timestamp (YYYY-MM-DDThh:mm:ss)', 'Glucose Value (mg/dL)']]
glucose = glucose.drop([1,2,3,4,5,6,7,8,9,10])
glucose.reset_index(drop=True, inplace=True)
glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'] = pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])
glucose = glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)':'Timestamp'})
gv = glucose['Glucose Value (mg/dL)']
gv = gv[gv != 'Low']
gv = gv[gv != 'High']
gv = gv.dropna().to_numpy(int)
hypo = gv[gv < MIN]
hyper = gv[gv > MAX]
def prop(a, b):
	return int((a/b)*100)
hos = prop(hypo.size,gv.size)
hrs = prop(hyper.size,gv.size)
ns = 100-hos-hrs
print ("Statistics:")
print("Mean blood glucose value for the given period is",np.round(gv.mean(),2),"mg/dL.")
print("Low blood glucose (hypoglycemia) is defined by values less than",MIN,"mg/dL.")
print("You have been in hypoglycemic state",hos,"% of the time.")
print("High blood glucose (hyperglycemia) is defined by values more than",MAX,"mg/dL.")
print("You have been in hyperglycemic state",hrs,"% of the time.")
print("Time in range is defined as the percentage of time you spend within the normal range. Your recommended time in range (TIR) is",TIR,"%.")
print("Your measured TIR is",ns,"%.\n")
print("------------------------------")
print("Interpretations:")
if ns >= TIR:
	print("Your results suggest that you have managed to keep your blood glucose levels within the normal range most of the time. Good job, keep it up!")
else:
	print("Your results suggest that you have been struggling to keep your blood glucose levels within the normal range.")
if hos >= (100-TIR)/2:
	print("Try to limit the time you spend in hypoglycemic state. If you want to see some tips about how to prevent blood glucose drops, type /prevent-low.")
if hrs >= (100-TIR)/2:
	print("Try to limit the time you spend in hyperglycemic state. If you want to see some tips about how to prevent blood glucose spikes, type /prevent-high.")
os.remove(fileName)

