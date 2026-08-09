"""Test 1 - Know what you are holding.

Prevents: the riboflavin `break` bug. You grabbed a compartment at
random because you did not know compartments existed.

PASS: you can state how many compartments iML1515 has and explain why
one chemical species appears more than once in the metabolite list.
"""

from collections import Counter
from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 1 - Model structure",
    "How many compartments does iML1515 have, and what are they?",
)

model = load_model()

report("Reactions", len(model.reactions))
report("Metabolites", len(model.metabolites))
report("Genes", len(model.genes))
print()

report("Compartments", model.compartments)
print()

# How many metabolites live in each compartment?
counts = Counter(m.compartment for m in model.metabolites)
for comp, n in sorted(counts.items()):
    report(f"  metabolites in '{comp}'", n)
print()

# The riboflavin case specifically - every match, not just the first.
print("Every metabolite whose name mentions riboflavin:")
hits = [m for m in model.metabolites if "riboflavin" in m.name.lower()]
if not hits:
    print("  (none - try searching the id 'ribflv' instead)")
for m in hits:
    print(f"  id={m.id:<12} compartment={m.compartment:<4} formula={m.formula}")
print()

print("Same search by id fragment 'ribflv':")
for m in model.metabolites:
    if "ribflv" in m.id:
        print(f"  id={m.id:<12} compartment={m.compartment:<4} name={m.name}")
print()

print("QUESTION TO ANSWER IN YOUR LOG:")
print("  Your old script used `break` on the first name match.")
print("  Which id above would it have grabbed, and what would")
print("  `EX_<that id>` have physically represented?")