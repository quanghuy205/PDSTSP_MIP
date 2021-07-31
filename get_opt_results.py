from gurobi import *
import numpy as np
import pandas as pd
from scipy.spatial import distance
from itertools import chain, combinations
import matplotlib.pyplot as plt
import os, sys


dir_path = os.path.dirname(os.path.realpath(__file__))

# print(dir_path)

path = dir_path + "/Results/20_customers/1"
dirs = os.listdir(path)
problems_list = [file for file in dirs]
print(problems_list)
df = pd.DataFrame()
non_opt = []
df['name'] = []

for prob in problems_list:

    pathh = dir_path + "/Results/20_customers/2/" + prob
    # data.readData("PDSTSP_20_customer_problems/" + prob)
    dt = pd.read_csv(pathh, header=None)
    gap = float(dt[2])
    if gap != 0:
        non_opt.append(prob)


df['name'] = non_opt
df.to_csv(dir_path + '/Results/20_customers/non_opt_2', index = False, header=False)
