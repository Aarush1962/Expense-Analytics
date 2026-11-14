import pandas as pd 
import numpy as np
import sys 


def load_n_clean( file_path , outputPath):


    df  = pd.read_csv(file_path) ;
    
    transactions = df.dropna().copy() ;
    transactions['Month'] = pd.to_datetime(transactions['Date']).dt.to_period('M').astype(str) ;
    transactions.to_csv(outputPath , index = False) ;
    print(f"Raw CSV File is Loaded and cleaned : {len(transactions)} valid transactions rows  -> {outputPath} ") ; 


if __name__ == "__main__" :
    load_n_clean(sys.argv[1] , sys.argv[2]) ;