from gurobi import *
import numpy as np
import pandas as pd
from scipy.spatial import distance
from itertools import chain, combinations
import matplotlib.pyplot as plt
import os, sys


class Data:
    def __init__(self):
        self.customerNum = 0
        self.nodeNum = 0
        self.droneNum = 1
        self.cities = []
        self.cor_X = []
        self.cor_Y = []
        self.serviceTime = []
        self.disMatrix = [[]]
        self.dt = None
        self.i_pot = None
        self.cus_can_served_by_drone = None
        self.drone_distances = None
        self.truck_distances = None
        self.model = None

    def readData(self, path):
        self.dt = pd.read_csv(path, header=None).to_numpy()[:-1]
        self.customerNum = len(self.dt)
        self.i_pot = self.dt[0, 1:3]
        self.nodeNum = self.customerNum + 2
        self.cor_X = [self.dt[i, 1:3][0] for i in range(len(self.dt))]
        self.cor_Y = [self.dt[i, 1:3][1] for i in range(len(self.dt))]
        self.cities = [self.dt[i, 0] for i in range(len(self.dt))]

        self.cus_can_served_by_drone = [i for i in range(len(self.dt)) if self.dt[i, 3] == 0]

        self.drone_distances = [round(distance.euclidean((self.dt[i, 1:3]), self.i_pot), 2)
                                if self.dt[i, 3] == 0 else float('inf')
                                for i in range(len(self.dt))]
        self.truck_distances = [[round(distance.cityblock(self.dt[i, 1:3], self.dt[j, 1:3]), 1)
                                 for i in range(len(self.dt))] for j in range(len(self.dt))]

        # Decision variables

        # x_ij if (i->j) in vehicle tour
        # # y_im = 1 if cus i assigned to drone m ()

        self.x = None
        self.y = None

    def addConstrs(self):

        # SET
        V = [i for i in range(self.customerNum)]
        C = [i for i in range(1, self.customerNum)]
        U = [k for k in range(self.droneNum)]

        C_U = data.cus_can_served_by_drone

        C_truck = {(i, j): self.truck_distances[i][j] for i in V for j in V}
        C_drone = self.drone_distances

        self.x = [[[] for i in V] for j in V]
        self.y = [[[] for i in V] for k in U]

        # 1
        # completion time
        alpha = self.model.addVar(0, GRB.INFINITY, 1.0, GRB.CONTINUOUS, "traveltime")
        self.model.update()
        expr = LinExpr(0)
        expr.addTerms(1.0, alpha)

        self.model.setObjective(expr, GRB.MINIMIZE)
        expr.clear()

        # 2
        expr = LinExpr(0)
        for i in V:
            for j in V:
                if i != j:
                    self.x[i][j] = self.model.addVar(0, 1, vtype=GRB.BINARY, name="x%d,%d" % (i, j))

                    self.model.update()
                    expr.addTerms(self.truck_distances[i][j], self.x[i][j])
                else:
                    self.x[i][i] = self.model.addVar(0.0, 1.0, 0.0, GRB.BINARY, "x%d,%d" % (i, j))

        #         print(expr)

        self.model.addConstr(alpha >= expr, "truckTime")
        expr.clear()
        self.model.update()

        # 3
        for k in U:
            expr = LinExpr(0)
            for i in C:

                if i in C_U:
                    self.y[k][i] = self.model.addVar(0, 1, vtype=GRB.BINARY, name="y%d,%d" % (k, i))
                    #                     print(i)

                    expr.addTerms(self.drone_distances[i], self.y[k][i])
                else:
                    self.y[k][i] = self.model.addVar(0, 0, vtype=GRB.BINARY, name="y%d,%d" % (k, i))
            self.model.update()
            #             print(expr)
            self.model.addConstr(alpha >= expr, "dronetime")
            expr.clear()
        expr.clear()

        # 4
        for j in C:

            expr1 = LinExpr(0)
            expr2 = LinExpr(0)

            for i in V:
                expr1.addTerms(1.0, self.x[i][j])
            #                 print(expr1)

            if j in C_U:
                for k in U:
                    expr2.addTerms(1.0, self.y[k][j])

            #             print(expr2)
            #             print("------------------")

            self.model.addConstr(expr1 + expr2 == 1, "served customer once")
            expr1.clear()
            expr2.clear()
        expr1.clear()
        expr2.clear()

        # 5
        for i in C:

            expr1 = LinExpr(0)
            expr2 = LinExpr(0)

            for j in V:
                expr1.addTerms(1.0, self.x[i][j])
            #             print(expr1)
            if i in C_U:
                for k in U:
                    expr2.addTerms(1.0, self.y[k][i])

            #             print(expr2)
            #             print("------------------")
            self.model.addConstr(expr1 + expr2 == 1, "served customer once")
            expr1.clear()
            expr2.clear()
        expr1.clear()
        expr2.clear()

        # 6
        for i in C:
            expr1 = LinExpr(0)
            expr2 = LinExpr(0)

            for j in V:
                expr1.addTerms(1.0, self.x[j][i])

            for h in V:
                expr2.addTerms(1.0, self.x[i][h])
            self.model.addConstr(expr1 == expr2, "flow conservation")
            expr1.clear()
            expr2.clear()
        expr1.clear()
        expr2.clear()

        # get all subtours
        def powerset(iterable):
            "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

        S = list(powerset(range(1, len(data.cities))))
        # The first element of the list is the empty set and the last element is the full set, hence we remove them.
        S = S[1:(len(S))]
        S = [list(s) for s in S]

        #         print(len(S))
        #         import sysdata.model = Model("test")
# data.readData("20140813T125053.csv")
# data.addConstrs()
# data.model.optimize()
        #         print(sys.getsizeof(S)/1024/1024," GB")
        #         print(type(S))

        # for s in S:

        #         s.insert(0,0)
        S.insert(0, [0])
        S = S[0:len(S) - 1]
        # print(S)
        # S = [[0,1,2,3,4]]

        # 7
        for s in S:
            expr1 = LinExpr(0)
            expr2 = LinExpr(0)

            for i in s:
                for j in V:
                    if j not in s:
                        expr1.addTerms(1.0, self.x[i][j])

                for k in U:
                    if i in C_U:
                        expr2.addTerms(1.0, self.y[k][i])
            # self.model.update()
            #     print(expr1)
            #     print(expr2)
            self.model.addConstr(expr1 + expr2 >= 1)
            expr1.clear()
            expr2.clear()

dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)

path = dir_path + "/PDSTSP_20_customer_problems"
dirs = os.listdir(path)
problems_list = [file for file in dirs]
print(problems_list)

obj = [1 for file in dirs]

df = pd.DataFrame()
df['name'] = problems_list
df['obj'] = obj

data = Data()

data.model = Model("test")
data.readData("PDSTSP_20_customer_problems/20140813T124847.csv")
data.addConstrs()
data.model.setParam(GRB.TIME_LIMIT, 600)

data.model.optimize()

# %%
print(data.model.ObjVal, data.model.Runtime)



# results = []/home/fatpc/huyvq/Git/PDSTSP_MIP/min-cost VRPD instances/min-cost VRPD-MurrayChu/PDSTSP_10_customer_problems
# for prob in problems_list:
#     data = Data()
#     data.model = Model("PDSTSP")
#     data.readData(
#         "/home/quanghuy205/PDSTSP_model/min-cost VRPD instances/min-cost VRPD-MurrayChu/PDSTSP_10_customer_problems/" + prob)
#     data.addConstrs()
#
#     data.model.optimize()
#     results.append(data.model.ObjVal)
#
#
