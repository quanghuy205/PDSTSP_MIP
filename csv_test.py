import csv
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)





path = dir_path + "/min-cost VRPD instances/min-cost VRPD-MurrayChu/PDSTSP_10_customer_problems"
dirs = os.listdir(path)
problems_list = [file for file in dirs]
print(problems_list)

header = ['name', 'obj', 'runtime', 'Sol']

with open('results_10_customers.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    # for prob in problems_list:
    # writer.writerow(prob)
f.close()