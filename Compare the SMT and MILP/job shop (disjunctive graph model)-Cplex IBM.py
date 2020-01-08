from docplex.mp.model import Model
from docplex.util.environment import get_environment
import os

# ----------------------------------------------------------------------------
# Initialize the problem data
# ----------------------------------------------------------------------------
filename = os.path.dirname(os.path.abspath(__file__)) + "/data/jobshop_j100_m10-D.data"
with open(filename, "r") as file:
    NB_JOBS, NB_MACHINES = [int(v) for v in file.readline().split()]
    JOBS = [[int(v) for v in file.readline().split()] for i in range(NB_JOBS)]

#-----------------------------------------------------------------------------
# Prepare the data for modeling
#-----------------------------------------------------------------------------


MACHINES = [[JOBS[j][2 * s] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]


DURATION = [[JOBS[j][2 * s + 1] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]


A=[(j,o) for j in range(NB_JOBS) for o in range(NB_MACHINES) if MACHINES[j][o]<=NB_MACHINES]
B=[(j,o,jj,oo) for j,o in A for jj,oo in A if (j,o)!=(jj,oo) and (MACHINES[j][o]==MACHINES[jj][oo] or MACHINES[j][o]==NB_MACHINES or MACHINES[jj][oo]==NB_MACHINES) and MACHINES[j][o]<=NB_MACHINES and MACHINES[jj][oo]<=NB_MACHINES]

G=10000
# ----------------------------------------------------------------------------
# Build the model
# ----------------------------------------------------------------------------
mdl = Model('disjunctive_graph')
s= mdl.continuous_var_dict(A,name='s')
y=mdl.binary_var_dict(B,name='y')
c_t=mdl.continuous_var_dict([(j) for j in range(NB_JOBS) if j<NB_JOBS-1],name='c_t')

z=mdl.minimize(mdl.sum(c_t[j] for j in range(NB_JOBS) if j<NB_JOBS-1))

mdl.add_constraints((y[j,o,jj,oo]+y[jj,oo,j,o]==1) for j,o,jj,oo in B)
mdl.add_constraint(mdl.sum(y[j,o,NB_JOBS-1,0] for j,o in A if (j,o)!=(NB_JOBS-1,0))<=0)
mdl.add_constraint(mdl.sum(y[NB_JOBS-1,1,j,o] for j,o in A if (j,o)!=(NB_JOBS-1,1))<=0)
mdl.add_constraints((s[j,o]-s[j,o-1]-DURATION[j][o-1]>=0) for j,o in A if o>0 and j<NB_JOBS-1)
mdl.add_constraints((s[j,o]-s[jj,oo]-DURATION[jj][oo]+(1-y[jj,oo,j,o])*G>=0) for j,o,jj,oo in B)
mdl.add_constraints((c_t[j]-s[j,NB_MACHINES-1]-DURATION[j][NB_MACHINES-1]>=0) for j in range(NB_JOBS) if j<NB_JOBS-1)

solution= mdl.solve(log_output=True)
print(solution)
