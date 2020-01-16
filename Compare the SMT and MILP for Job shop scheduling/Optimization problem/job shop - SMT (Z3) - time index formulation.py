from z3 import *
import itertools
import time
start_time = time.time()



import os

filename = os.path.dirname(os.path.abspath(__file__)) + "/data/jobshop_j300_m15.data"
with open(filename, "r") as file:
    NB_JOBS, NB_MACHINES = [int(v) for v in file.readline().split()]
    JOBS = [[int(v) for v in file.readline().split()] for i in range(NB_JOBS)]


MACHINES = [[JOBS[j][2 * s] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]

DURATION = [[JOBS[j][2 * s + 1] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]

HORIZON=215

# create variables
obj = Real('total completion time')
c_t = [Real("c_t_%s" % (j)) for j in range(NB_JOBS)]
s = [[[Bool("s%d_%d_%d" % (j,o,t)) for t in range(HORIZON)] for o in range(NB_MACHINES)]
      for j in range(NB_JOBS)]

# solver
sol = Optimize ()
# formulate constraints

sol.add(obj>=sum([c_t[j] for j in range(NB_JOBS)]))

for j in range(NB_JOBS):
    for o in range(NB_MACHINES):
        sol.add(Or([s[j][o][t] for t in range(HORIZON)]))

for j in range(NB_JOBS):
    for o in range(NB_MACHINES):
        for t in range(HORIZON):
            if o<NB_MACHINES-1:
                sol.add(Or(Not(s[j][o][t]), And(s[j][o][t], And([Not(s[j][o+1][tt]) for tt in range(HORIZON) if tt<t+DURATION[j][o]]))))

for t in range(HORIZON):
    for j in range(NB_JOBS):
        for o in range(NB_MACHINES):
            for jj in range(NB_JOBS):
                for oo in range(NB_MACHINES):
                    if (j,o)!=(jj,oo) and MACHINES[j][o]==MACHINES[jj][oo]:
                        sol.add(Or(Not(s[j][o][t]), And(s[j][o][t], And([Not(s[jj][oo][tt]) for tt in range(HORIZON) if tt<t+DURATION[j][o] and tt>=t]))))

for j in range(NB_JOBS):
    for t in range(HORIZON):
        sol.add(Or(Not(s[j][NB_MACHINES-1][t]), And(s[j][NB_MACHINES-1][t],c_t[j]>= t+DURATION[j][NB_MACHINES-1])))


h = sol.minimize(obj)
sol.set(timeout=3600)
if sol.check ()== unsat:
    print("unsat")
    exit (0)
sol.lower(h)
m=sol.model ()
objective_function=[m.evaluate(obj)]
print(objective_function)
start_times = [[[m.evaluate(s[j][o][t]) for t in range(HORIZON)] for o in range(NB_MACHINES)] for j in range(NB_JOBS)]

for j in range(NB_JOBS):
    for o in range(NB_MACHINES):
        for t in range(HORIZON):
            if start_times[j][o][t]==True:
                print("s_",j,"_",o,"_",t)      

print("--- %s seconds ---" % (time.time() - start_time))

"o36 ---> H=70  obj=265   time= 175 s"
"o80 ---> H=70 obj=534   time= 118 s"
"o100 ---> H=110 obj=898   time= >3600  s"
"o150 ---> H=150  obj=1391   time= >3600  s"
"o210 ---> H=180  obj= unsat   time= >3600  s"
"o210 ---> H=200  obj=2762    time= >3600  s"
"o300 ---> H=215  obj=unsat    time= >3600  s"