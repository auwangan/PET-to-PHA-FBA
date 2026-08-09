"""Test 6 - Degeneracy.

FBA returns ONE optimal solution out of infinitely many. Reporting a
single optimize() flux as 'the' answer is the mistake in your old
riboflavin script.

PASS: you can point to a reaction whose FVA range is wide and explain
that the FBA value was an arbitrary point inside it.
"""

from cobra.flux_analysis import flux_variability_analysis
from common import load_model, prediction_gate, report

pred = prediction_gate(
    "TEST 6 - Solution degeneracy",
    "Pick 3 reactions. Will their FVA ranges be tight or wide? Which and why?",
)

model = load_model()
targets = ["PGI", "PFK", "PYK"]

sol = model.optimize()
print("Single FBA solution:")
for rid in targets:
    report(f"  {rid}", round(sol.fluxes[rid], 5))
print()

print("FVA at 100% of optimal growth:")
fva = flux_variability_analysis(model, reaction_list=targets, fraction_of_optimum=1.0)
print(fva.round(5).to_string())
print()

print("FVA at 90% of optimal growth (the range a real cell might use):")
fva90 = flux_variability_analysis(model, reaction_list=targets, fraction_of_optimum=0.9)
print(fva90.round(5).to_string())
print()

print("QUESTIONS TO ANSWER IN YOUR LOG:")
print("  1. For each reaction: was the FBA value at the min, the max,")
print("     or somewhere in between?")
print("  2. Which widened most when you dropped to 90% optimum?")
print("  3. In your riboflavin script you reported a single riboflavin")
print("     flux. What should you have reported instead?")