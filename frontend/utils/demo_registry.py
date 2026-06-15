"""
MuleShield AI — Demo Mode Registry
Centralized repository for all hackathon demo constants. 
Prevents scattered hardcoded values and enables one-click demo environments.
"""

# The primary account that showcases multiple fraud vectors (Dormant + Layering + ML Anomaly)
DEMO_CRITICAL_ACCOUNT = "BOI4421087653"

# Used for graph visualization and STR generation
DEMO_GRAPH_ACCOUNT = DEMO_CRITICAL_ACCOUNT
DEMO_STR_ACCOUNT = DEMO_CRITICAL_ACCOUNT

# I4C Webhook Integration Constants
DEMO_I4C_ACCOUNT = "ACC0520000000028"
DEMO_I4C_REF = "I4C-2026-8819"

# Default Demo Scenario (Dormant Reactivation Ring)
DEMO_SCENARIO_PATH = "data/scenario_dormant_reactivation.csv"
DEMO_SCENARIO_LABEL = "scenario_dormant_reactivation.csv"
