from z3 import *
import os
import time
start_time = time.time()

filename = os.path.dirname(os.path.abspath(__file__)) + "/data/o300.smt2"

obj = Real('objectie_function')
sol = z3.Optimize()
b = z3.parse_smt2_file(filename, sorts={}, decls={})
sol.add(b)
sol.minimize(obj)

sol.set(timeout=3600000)
if sol.check ()== unsat:
    print("unsat")
    exit (0)

m=sol.model()
objective_function=[m.evaluate(obj)]
print(objective_function)
print("--- %s seconds ---" % (time.time() - start_time))

"o36 ---> obj:265   time: 0.5 s "
"o80 ---> obj:534   time: 720 s "
"o100 ---> obj:819   time: >3600 s "
"o150 ---> obj:1112   time: >3600 s "
"o210 ---> obj: 3152   time: >3600 s "
