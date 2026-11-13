import pandas as pd 
import numpy as np
import sys 


def load_n_clean( file_path , outputPath):


    df  = pd.read_csv(file_path) ; 

    df  = df.dropna() ;
    expenses = df [df['Type'] == 'Debit'].copy() 
    expenses(['Month']) = pd.to_datetime(expenses(['Date'])).dt.to_period('M').astype(str) ;
    expenses.to_csv(outputPath , index = False) ;
    print(f"Raw CSV File is Loaded and cleaned : {len(expenses)} valid debit rows  -> {outputPath} ") ; 


if __name__ == "__main__" :
    load_n_clean(sys.argv[1] , sys.argv[2]) ;

