"""Test 4 - Mass and charge balance.

THE MOST IMPORTANT TEST IN THIS SUITE.

An unbalanced reaction is a matter generator. It does not error. It
just inflates every yield downstream. Run this on every reaction you
add in week 2.

PASS: you have seen check_mass_balance() return a non-empty dict, and
you know how to read the output.
"""

from cobra import Reaction, Metabolite
from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 4 - Mass and charge balance",
    "Will iML1515's own EXCHANGE reactions pass a mass balance check? Why or why not?",
)

model = load_model()

# --- 4a: five normal internal reactions -------------------------------
print("4a. Five internal reactions from iML1515:")
internal = [r for r in model.reactions if not r.boundary][:5]
for r in internal:
    imbalance = r.check_mass_balance()
    status = "BALANCED" if not imbalance else f"IMBALANCED {imbalance}"
    print(f"  {r.id:<14} {status}")
print()

# --- 4b: an exchange reaction -----------------------------------------
print("4b. An exchange reaction:")
ex = model.reactions.get_by_id("EX_glc__D_e")
print(f"  {ex.id:<14} {ex.reaction}")
print(f"  check_mass_balance() -> {ex.check_mass_balance()}")
print("  ^ This is EXPECTED. Exchange reactions are deliberately")
print("    unbalanced - they represent matter crossing the system")
print("    boundary. This is why you EXCLUDE boundary reactions when")
print("    checking, and why `if not r.boundary` appears above.")
print()

# --- 4c: a deliberately broken reaction -------------------------------
print("4c. A subtly broken reaction (missing a cofactor):")
# Real chemistry: pyruvate + NADH + H+ -> D-lactate + NAD+
# Broken version: pyruvate -> D-lactate, cofactors omitted.
with model as m:
    broken = Reaction("BROKEN_LDH")
    broken.add_metabolites({
        m.metabolites.get_by_id("pyr_c"): -1.0,
        m.metabolites.get_by_id("lac__D_c"): 1.0,
    })
    m.add_reactions([broken])
    report("  reaction", broken.reaction)
    report("  check_mass_balance()", broken.check_mass_balance())
    print()
    print("  Read that dict: each key is an element (or 'charge') and")
    print("  each value is how many atoms the reaction creates (+) or")
    print("  destroys (-). Anything non-zero is a bug.")
print()

# --- 4d: sweep the whole model ----------------------------------------
print("4d. How many non-boundary reactions in iML1515 are imbalanced?")
bad = []
for r in model.reactions:
    if r.boundary:
        continue
    try:
        imb = r.check_mass_balance()
    except ValueError:
        continue  # metabolite with no formula
    if imb:
        bad.append((r.id, imb))
report("  imbalanced non-boundary reactions", len(bad))
for rid, imb in bad[:10]:
    print(f"    {rid:<14} {imb}")
print()

print("QUESTIONS TO ANSWER IN YOUR LOG:")
print("  1. Why do exchange reactions 'fail' this check by design?")
print("  2. Some iML1515 reactions are imbalanced. Pick one and work")
print("     out why the curators allowed it. (Biomass is a good one.)")
print("  3. Write the one-line check you will run after EVERY reaction")
print("     you add in week 2.")