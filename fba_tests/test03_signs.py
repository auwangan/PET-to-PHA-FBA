"""Test 3 - Sign convention on exchange reactions.

Prevents: setting a bound in the wrong direction and silently starving
or force-feeding the cell.

PASS: you can state that negative flux on an exchange means INTO the
cell, and explain why lower_bound = -10 means "at most 10 units may be
taken up".
"""

from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 3 - Exchange sign convention",
    "Will the flux through EX_glc__D_e at optimum be positive or negative? Why?",
)

model = load_model()
glc = model.reactions.get_by_id("EX_glc__D_e")

report("Reaction", glc.reaction)
report("lower_bound", glc.lower_bound)
report("upper_bound", glc.upper_bound)
print()

sol = model.optimize()
report("Flux at optimum", round(sol.fluxes["EX_glc__D_e"], 5))
report("Growth", round(sol.objective_value, 5))
print()

# Now change it and watch what happens.
print("Halving the allowed glucose uptake:")
with model as m:
    m.reactions.EX_glc__D_e.lower_bound = glc.lower_bound / 2
    s = m.optimize()
    report("  new lower_bound", m.reactions.EX_glc__D_e.lower_bound)
    report("  growth", round(s.objective_value, 5))
print()

print("Setting the UPPER bound to a large negative number instead:")
with model as m:
    try:
        m.reactions.EX_glc__D_e.upper_bound = -5
        s = m.optimize()
        report("  status", s.status)
        report("  growth", round(s.objective_value, 5))
    except Exception as e:
        report("  error", type(e).__name__)
print()

print("QUESTIONS TO ANSWER IN YOUR LOG:")
print("  1. Which bound controls maximum uptake, and why that one?")
print("  2. What did forcing upper_bound = -5 do, and what does it")
print("     mean biologically? (Hint: it forces something.)")