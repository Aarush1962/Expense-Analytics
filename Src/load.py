import pandas as pd 
import numpy as np
import sys 


file_path = sys.argv[1] 
df  = pd.read_csv(file_path) 

df  = df.dropna() ;
expenses = df [df['Type'] == 'Debit'].copy() 
expenses(['Month']) = pd.to_datetime(expenses(['Date'])).dt.to_period('M').astype(str) ;

