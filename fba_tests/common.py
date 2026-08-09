"""Shared helpers for the week-1 validation tests.

Every test script imports from here so the model path and the
prediction gate live in exactly one place.
"""

import os
import cobra

# Adjust if your model sits elsewhere.
MODEL_PATH = os.environ.get("IML1515_PATH", "data/iML1515.xml")

BIOMASS_RXN = "BIOMASS_Ec_iML1515_core_75p37M"


def load_model():
    """Load iML1515 and fail loudly if it is missing."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Could not find {MODEL_PATH}.\n"
            "Download iML1515.xml from http://bigg.ucsd.edu/models/iML1515 "
            "and place it in data/, or set IML1515_PATH."
        )
    model = cobra.io.read_sbml_model(MODEL_PATH)
    model.solver = "glpk" 
    return model


def prediction_gate(test_name, question):
    """Refuse to run until the user confirms a written prediction exists.

    This is the whole point of week 1. Reading output you have not
    predicted teaches nothing, because plausible numbers always look
    plausible.
    """
    print("=" * 70)
    print(f"  {test_name}")
    print("=" * 70)
    print()
    print("BEFORE RUNNING: write your prediction in docs/validation_log.md")
    print()
    print(f"  {question}")
    print()
    answer = input("Type your prediction here (it will be echoed back): ").strip()
    if not answer:
        raise SystemExit("No prediction given. Log one, then re-run.")
    print()
    print(f"Your prediction: {answer}")
    print("-" * 70)
    return answer


def report(label, value):
    print(f"{label:<45} {value}")