"""Test 8 - Solver check.

Community models (week 4) can reach tens of thousands of variables.
GLPK will struggle. Sort the licence out now, not at 2am in October.
"""

import cobra
from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 8 - Solver",
    "Which solver do you expect cobrapy to be using right now?",
)

print("Solvers cobrapy can see:")
report("  available", list(cobra.util.solver.solvers.keys()))
print()

model = load_model()
report("Solver in use for this model", str(type(model.solver)).split("'")[1])
print()

import time
t0 = time.time()
sol = model.optimize()
report("Time for one FBA (s)", round(time.time() - t0, 4))
report("Growth", round(sol.objective_value, 5))
print()

print("TO DO:")
print("  If only glpk is listed, get a Gurobi academic licence")
print("  (free, gurobi.com/academia) and `pip install gurobipy`.")
print("  Then set: model.solver = 'gurobi'")
print("  Record in your log which solver produced every result.")