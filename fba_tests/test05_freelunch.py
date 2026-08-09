"""Test 5 - Free lunch test.

Close every door. If the cell still grows, it is creating biomass from
nothing and every number the model produces is meaningless.

Run this after EVERY pathway you add in week 2. It is the fastest way
to catch a thermodynamically infeasible loop you just introduced.

PASS: growth = 0, OR solver status 'infeasible'. Both are correct -
see the note below about ATPM.
"""

from common import load_model, prediction_gate, report, BIOMASS_RXN

pred = prediction_gate(
    "TEST 5 - Free lunch",
    "With ALL uptake blocked, what growth rate and solver status do you expect?",
)

model = load_model()

report("Baseline growth", round(model.optimize().objective_value, 5))
print()

print("Closing every exchange reaction (no uptake of anything):")
with model as m:
    for rxn in m.exchanges:
        rxn.lower_bound = 0.0
    sol = m.optimize()
    report("  status", sol.status)
    report("  growth", round(sol.objective_value, 5) if sol.objective_value is not None else None)
print()

print("Same, but also relaxing the ATP maintenance requirement:")
with model as m:
    for rxn in m.exchanges:
        rxn.lower_bound = 0.0
    atpm = m.reactions.get_by_id("ATPM")
    report("  ATPM lower_bound was", atpm.lower_bound)
    atpm.lower_bound = 0.0
    sol = m.optimize()
    report("  status", sol.status)
    report("  growth", round(sol.objective_value, 5) if sol.objective_value is not None else None)
print()

print("HOW TO READ THIS:")
print("  ATPM is the non-growth-associated maintenance reaction - the")
print("  ATP the cell burns just staying alive. Its lower bound is")
print("  positive, i.e. the model is FORCED to burn that much ATP.")
print("  With no uptake, that demand cannot be met, so the problem")
print("  becomes infeasible rather than returning growth = 0.")
print()
print("  Both outcomes pass. What FAILS is growth > 0 with ATPM")
print("  relaxed - that means a loop somewhere makes ATP or carbon")
print("  out of nothing.")
print()

print("QUESTIONS TO ANSWER IN YOUR LOG:")
print("  1. Did you predict infeasible, or zero? What did you learn?")
print("  2. Write down the exact snippet you will re-run after every")
print("     reaction you add in week 2.")