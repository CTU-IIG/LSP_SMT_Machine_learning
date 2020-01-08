from z3 import *
import itertools
import time
start_time = time.time()



import os

filename = os.path.dirname(os.path.abspath(__file__)) + "/data/jobshop_j210_m15.data"
with open(filename, "r") as file:
    NB_JOBS, NB_MACHINES = [int(v) for v in file.readline().split()]
    JOBS = [[int(v) for v in file.readline().split()] for i in range(NB_JOBS)]


MACHINES = [[JOBS[j][2 * s] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]

DURATION = [[JOBS[j][2 * s + 1] for s in range(NB_MACHINES)] for j in range(NB_JOBS)]

obj = Int('objectie_function')
c_t = [Int("c_t_%s" % (j)) for j in range(NB_JOBS)]

def must_not_overlap (s, i1 , i2):
    (i1_begin , i1_end)=i1
    (i2_begin , i2_end)=i2
    s.add(Or(i2_begin >=i1_end , i1_begin >= i2_end))

def all_items_in_list_must_not_overlap_each_other (s, lst):

    for pair in itertools.combinations(lst , r=2):
        must_not_overlap(s, (pair [0][1] , pair [0][2]) , (pair [1][1] , pair [1][2]))

s = Optimize ()



tasks_for_machines =[[] for i in range(NB_MACHINES)]


jobs_array =[]
for job in range(NB_JOBS):
    prev_task_end=None
    jobs_array_tmp =[]
    for t in range(NB_MACHINES):
        machine=MACHINES[job][t]
        duration=DURATION[job][t]
        begin=Int('j%d_t%d_begin ' % (job , t))
        end=Int('j%d_t%d_end ' % (job , t))
        if (begin ,end) not in tasks_for_machines[machine ]:
            tasks_for_machines[machine ]. append ((job ,begin ,end))
        if (begin ,end) not in jobs_array_tmp:
            jobs_array_tmp.append ((job ,begin ,end))
        s.add(begin >=0)
        s.add(end== begin+duration) 

        if t==NB_MACHINES-1:
            s.add(end <= c_t[job])

        if prev_task_end !=None:
            s.add(begin >= prev_task_end)
        prev_task_end=end
    jobs_array.append(jobs_array_tmp)


for tasks_for_machine in tasks_for_machines:
    all_items_in_list_must_not_overlap_each_other (s, tasks_for_machine)

for jobs_array_tmp in jobs_array:
    all_items_in_list_must_not_overlap_each_other (s, jobs_array_tmp)

s.add(obj>=sum([c_t[job] for job in range(NB_JOBS)]))
h = s.minimize(obj)
s.set(timeout=3600000)
if s.check ()== unsat:
    print("unsat")
    exit (0)
s.lower(h)
m=s.model ()
objective_function=[m.evaluate(obj)]
makespan = [m.evaluate(c_t[job]) for job in range(NB_JOBS)]
print(objective_function)
print(makespan)
print("--- %s seconds ---" % (time.time() - start_time))
