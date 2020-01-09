from gurobipy import *
import os
import time
start_time = time.time()

filename = os.path.dirname(os.path.abspath(__file__)) + "/data/jobshop_j100_m10-D.data"
with open(filename, "r") as file:
    NB_JOBS, NB_MACHINES = [int(v) for v in file.readline().split()]
    JOBS = [[int(v) for v in file.readline().split()] for i in range(NB_JOBS)]

#-----------------------------------------------------------------------------
# Prepare the data for modeling
#-----------------------------------------------------------------------------

# Build list of machines. MACHINES[j][s] = id of the machine for the operation s of the job j
MACHINES = [[JOBS[j][2 * s] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]

# Build list of durations. DURATION[j][s] = duration of the operation s of the job j
DURATION = [[JOBS[j][2 * s + 1] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]


A=[(j,o) for j in range(NB_JOBS) for o in range(NB_MACHINES) if MACHINES[j][o]<=NB_MACHINES]
B=[(j,o,jj,oo) for j,o in A for jj,oo in A if (j,o)!=(jj,oo) and (MACHINES[j][o]==MACHINES[jj][oo] or MACHINES[j][o]==NB_MACHINES or MACHINES[jj][oo]==NB_MACHINES) and MACHINES[j][o]<=NB_MACHINES and MACHINES[jj][oo]<=NB_MACHINES]
G=10000

model = Model('disjunctive graph')


s = model.addVars(A,name='s')
y = model.addVars(B,vtype=GRB.BINARY,name='y')
c_t = model.addVars([(j) for j in range(NB_JOBS) if j<NB_JOBS-1],name='completaion time') 



model.addConstrs((y[j,o,jj,oo]+y[jj,oo,j,o]==1) for j,o,jj,oo in B)
model.addConstr(quicksum(y[j,o,NB_JOBS-1,0] for j,o in A if (j,o)!=(NB_JOBS-1,0))<=0)
model.addConstr(quicksum(y[NB_JOBS-1,1,j,o] for j,o in A if (j,o)!=(NB_JOBS-1,1))<=0)
model.addConstrs((s[j,o]-s[j,o-1]-DURATION[j][o-1]>=0) for j,o in A if o>0 and j<NB_JOBS-1)
model.addConstrs((s[j,o]-s[jj,oo]-DURATION[jj][oo]+(1-y[jj,oo,j,o])*G>=0) for j,o,jj,oo in B)
model.addConstrs((c_t[j]-s[j,NB_MACHINES-1]-DURATION[j][NB_MACHINES-1]>=0) for j in range(NB_JOBS) if j<NB_JOBS-1)

obj= quicksum(c_t[j] for j in range(NB_JOBS) if j<NB_JOBS-1)

model.setObjective(obj, GRB.MINIMIZE)  
model.optimize()
print("--- %s seconds ---" % (time.time() - start_time))

