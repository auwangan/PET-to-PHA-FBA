"""Test 2 - Reproduce a known number.

If you cannot reproduce the simplest documented result, nothing
downstream is trustworthy.

PASS: growth rate within ~5% of the published iML1515 value on glucose
minimal medium. Look that value up yourself in Monk et al. 2017
(Nat Biotechnol 35:904) or on the BiGG model page - do NOT take a
number from me or from this docstring.
"""

from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 2 - Reproduce published growth rate",
    "What growth rate (1/h) do you expect on glucose minimal medium?",
)

model = load_model()

# What medium is the model shipped with? Do not assume - look.
print("Default open uptake bounds (non-zero lower bound on exchanges):")
for rxn in model.exchanges:
    if rxn.lower_bound < 0:
        report(f"  {rxn.id}", f"lb={rxn.lower_bound}  ({rxn.name})")
print()

sol = model.optimize()
report("Solver status", sol.status)
report("Growth rate (1/h)", round(sol.objective_value, 5))
report("Objective reaction", str(model.objective.expression)[:60])
print()

print("QUESTIONS TO ANSWER IN YOUR LOG:")
print("  1. What is the published value? Cite where you found it.")
print("  2. Is yours within 5%? If not, which exchange bound differs?")
print("  3. What glucose uptake rate is the default, and in what units?")