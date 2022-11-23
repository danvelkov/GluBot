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
print("Mean glucose value for the given period is", np.round(gv.mean(),2), ".")
print("You have been in hypoglycemic state for", prop(hypo.size,gv.size),"% of the time.")
print("You have been in hyperglycemic state for", prop(hyper.size,gv.size),"% of the time.")

os.remove(fileName)

