"""
MuleShield — BOI Scenario Validation Script
Runs all three realistic BOI scenarios through the detection pipeline
and prints signal + risk score reports for credibility validation.
"""

import sys
sys.path.insert(0, ".")

import pandas as pd
from backend.fraud_detection import (
    detect_cycles, detect_structuring, detect_velocity,
    detect_anomaly, detect_dormant, ml_anomaly, detect_layering,
)
from backend.graph_builder import build_graph
from backend.risk_scoring import (
    calculate_risk,
    calculate_transaction_score,
    calculate_composite_risk,
    assign_tier,
)

SCENARIOS = {
    "Dormant Reactivation Ring":  "data/scenario_dormant_reactivation.csv",
    "Student Mule Recruitment":   "data/scenario_student_recruitment.csv",
    "Agri Subsidy Diversion":     "data/scenario_agri_diversion.csv",
}

for name, path in SCENARIOS.items():
    print()
    print("=" * 65)
    print(f"SCENARIO: {name}")
    print(f"FILE    : {path}")
    print("=" * 65)

    df = pd.read_csv(path)
    n_unique_accts = len(set(df["from_account"].tolist()) | set(df["to_account"].tolist()))
    print(f"Rows: {len(df)} | Unique accounts: {n_unique_accts}")

    G = build_graph(df)
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    cycles      = detect_cycles(G)
    layering    = detect_layering(G)
    structuring = detect_structuring(df)
    velocity    = detect_velocity(df)
    anomaly     = detect_anomaly(df)
    dormant     = detect_dormant(df)
    ml_anom     = ml_anomaly(df)

    signals = {
        "cycle":       set(n for c in cycles for n in c),
        "layering":    set(n for p in layering for n in p),
        "structuring": set(structuring),
        "velocity":    set(velocity),
        "anomaly":     set(anomaly),
        "dormant":     set(dormant),
        "ml_anomaly":  set(ml_anom),
    }

    print()
    print(f"  Cycles detected   : {len(cycles)}")
    print(f"  Layering paths    : {len(layering)}")
    print(f"  Structuring accts : {len(structuring)}")
    print(f"  Velocity accts    : {len(velocity)}")
    print(f"  Anomaly accts     : {len(anomaly)}")
    print(f"  Dormant accts     : {len(dormant)}")
    print(f"  ML anomaly accts  : {len(ml_anom)}")

    print()
    print("  TOP RISK ACCOUNTS:")
    name_lookup = {}
    if "from_name" in df.columns:
        pairs = df[["from_account", "from_name"]].drop_duplicates("from_account")
        name_lookup = dict(zip(pairs["from_account"], pairs["from_name"]))

    scored = []
    for node in G.nodes:
        reasons = [s for s, accts in signals.items() if node in accts]
        score, severity, _ = calculate_risk(node, signals)
        txn_score = calculate_transaction_score(reasons)
        composite = calculate_composite_risk(0.50, None, txn_score)
        tier = assign_tier(composite)
        scored.append((node, name_lookup.get(node, node), reasons, txn_score, composite, tier))

    scored.sort(key=lambda x: x[4], reverse=True)
    for node, acct_name, reasons, txn_score, composite, tier in scored[:8]:
        print(f"    [{tier:8s}] {node} ({acct_name})")
        print(f"             signals={reasons} | txn={txn_score:.0f} | composite={composite:.1f}")

print()
print("=" * 65)
print("VALIDATION COMPLETE")
print("=" * 65)
