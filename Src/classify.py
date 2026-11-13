import sys 
import pandas as pd 
import json 


def categorize(desc , rules) :
     des_lower = str(desc).lower ;

     for category , keywords in rules.item() :
          if any( k in desc_lower for k in keywords):
               return category ;

     return 'Others' ;


def classify(input_path , rule_path , out_path):
     

     