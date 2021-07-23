import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)



path = dir_path + "/min-cost VRPD instances/min-cost VRPD-MurrayChu/PDSTSP_10_customer_problems"
dirs = os.listdir(path)
problems_list = [file for file in dirs]
print(problems_list)
obj = [1 for file in dirs]

df = pd.DataFrame()
df['name'] = problems_list
df['obj'] = obj

print(df)
df.to_csv(dir_path + '/testcsv.csv',header=True)