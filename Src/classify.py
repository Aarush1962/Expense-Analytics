import sys 
import pandas as pd 
import json 


def categorize(desc , rules) :
     desc_lower = str(desc).lower() ;

     for category , keywords in rules.items() :
          if any( k in desc_lower for k in keywords):
               return category ;

     return 'Others' ;


def classify(input_path , rule_path , out_path):
     df = pd.read_csv(input_path) ;
     with open( rule_path , 'r') as f :
          rules = json.load(f) ;

     df['Category'] = df['Description'].apply(lambda x : categorize(x,rules)) ;

     df.to_csv(out_path , index = False) ;
     print(f"File is Categorized according to its Type of Transaction") ;

if (__name__ == "__main__") :
     classify(sys.argv[1] , sys.argv[2] , sys.argv[3]) ;     


     