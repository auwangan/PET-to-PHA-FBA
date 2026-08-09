"""Test 7 - Autopsy of the riboflavin script.

You already have the wrong answer. Now find out HOW wrong. This is the
highest-value hour in week 1 because it calibrates you against a
mistake you actually made.

Five claims to check. Fill in the verdict column in your log.
"""

from cobra.flux_analysis import flux_variability_analysis
from common import load_model, prediction_gate, report, BIOMASS_RXN

pred = prediction_gate(
    "TEST 7 - Riboflavin script autopsy",
    "Of the 5 suspected bugs, how many do you predict were real?",
)

model = load_model()

# --- Q1: which metabolite did `break` grab? ---------------------------
print("Q1. Which riboflavin metabolite would the first-match loop grab?")
first = None
for met in model.metabolites:
    if "riboflavin" in met.name.lower():
        first = met
        break
if first is None:
    print("   No name match. Your original script would have exited here.")
else:
    report("   first match id", first.id)
    report("   its compartment", first.compartment)
    print(f"   -> your script would have created EX_{first.id}")
    print(f"   -> does an exchange for {first.id} already exist?")
    existing = [r.id for r in model.reactions
                if r.boundary and first in r.metabolites]
    report("      existing boundary reactions", existing or "NONE")
print()

# --- Q2: was the 'overexpression' a no-op? ----------------------------
print("Q2. Upper bounds of the b3846 reactions BEFORE 'overexpression':")
try:
    gene = model.genes.get_by_id("b3846")
    report("   gene name", gene.name)
    for rxn in gene.reactions:
        report(f"   {rxn.id}", f"ub={rxn.upper_bound}  lb={rxn.lower_bound}")
    print("   -> if ub is already 1000, setting it to 1000 changed nothing.")
except KeyError:
    print("   b3846 not found in this model. That is itself a finding.")
print()

# --- Q3/Q4: are the locus tags what you thought? ----------------------
print("Q3/Q4. Locus tag identity check:")
for locus, assumed in [("b3846", "ribA"), ("b4025", "pgi")]:
    try:
        g = model.genes.get_by_id(locus)
        match = "MATCHES" if g.name.lower() == assumed.lower() else "DOES NOT MATCH"
        report(f"   {locus}", f"model says '{g.name}' - assumed '{assumed}' - {match}")
    except KeyError:
        report(f"   {locus}", "NOT IN MODEL")
print("   -> Now verify independently on EcoCyc. The model is not")
print("      an authority on gene naming; cross-check it.")
print()

# --- Q5: how degenerate was the reported flux? ------------------------
print("Q5. FVA on the riboflavin exchange under the KO condition:")
ribflv_ex = [r.id for r in model.reactions
             if r.boundary and any("ribflv" in m.id for m in r.metabolites)]
report("   riboflavin exchange(s) found", ribflv_ex or "NONE")
if ribflv_ex:
    ex_id = ribflv_ex[0]
    wt_growth = model.optimize().objective_value
    with model as m:
        m.reactions.get_by_id(BIOMASS_RXN).lower_bound = wt_growth * 0.9
        m.objective = ex_id
        s = m.optimize()
        report("   single optimize() value", round(s.objective_value, 5))
        fva = flux_variability_analysis(m, reaction_list=[ex_id],
                                        fraction_of_optimum=0.9)
        print(fva.round(5).to_string())
print()

print("WRITE IN YOUR LOG:")
print("  A short paragraph: which of the 5 were real bugs, which were")
print("  not, and what the corrected numbers are. Be specific. This is")
print("  the paragraph that proves you can tell correct from incorrect.")