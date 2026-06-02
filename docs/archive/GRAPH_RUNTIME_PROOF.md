# GRAPH_RUNTIME_PROOF.md

**Execution Timestamp:** 2026-06-02T01:50:50.786560  
**Status:** ✅ EXECUTION COMPLETE - EVIDENCE DOCUMENTED

---

## Phase 1: Neo4j State BEFORE Ingestion

| Metric | Value |
|--------|-------|
| Node Count | **0** |
| Relationship Count | **0** |

---

## Phase 2: Baseline Scores (Empty Graph)

**Selected Account:** `ACC05299999999999`

| Component | Value |
|-----------|-------|
| ML Score | 0.6500 |
| Transaction Score | 0.0000 |
| Graph Score | 0.0000 |
| **Composite Score** | **0.2600** |

**Calculation:** (0.65 × 0.40) + (0.0 × 0.40) + (0.0 × 0.20) = 0.26

---

## Phase 3: Batch Prediction Execution

| Metric | Value |
|--------|-------|
| Records Ingested | 50 |
| Status | Completed |
| Transactions Created | 50 (each account → sink node) |

---

## Phase 4: Neo4j State AFTER Ingestion

| Metric | Value |
|--------|-------|
| Node Count | **51** |
| Relationship Count | **50** |
| Nodes Added | **+51** |
| Relationships Added | **+50** |

**Topology Created:**
- 50 source Account nodes (ACC052000000000000 through ACC052000000000049)
- 1 sink Account node (ACC05299999999999)
- 50 TRANSACTED relationships (source → sink)

---

## Phase 5: Final Scores (After Graph Ingestion)

**Selected Account:** `ACC05299999999999` (sink node with all 50 incoming transactions)

| Component | Value |
|-----------|-------|
| ML Score | 0.6500 |
| Transaction Score | 0.0000 |
| Graph Score | **1.0000** |
| **Composite Score** | **0.4600** |

**Calculation:** (0.65 × 0.40) + (0.0 × 0.40) + (1.0 × 0.20) = 0.26 + 0.20 = 0.46

**Centrality Calculation for Account:**
```
Degree (relationships): 50
Total Nodes: 51
Raw Centrality: 50 / (51 - 1) = 50 / 50 = 1.0
Scaled Centrality: min(1.0, 1.0 × 5.0) = 1.0
```

---

## Phase 6: Measured Changes

### Graph Score Change

| Metric | Value |
|--------|-------|
| Before Ingestion | 0.0000 |
| After Ingestion | 1.0000 |
| Delta | **+1.0000** |
| **CHANGED:** | **YES** ✅ |

**Evidence:** Graph score increased from 0.0 to 1.0 after account became central hub in network.

### Composite Score Change

| Metric | Value |
|--------|-------|
| Before Ingestion | 0.2600 |
| After Ingestion | 0.4600 |
| Delta | **+0.2000** |
| **CHANGED:** | **YES** ✅ |

**Evidence:** Composite score increased by exactly 0.20 (graph_score_delta × graph_weight = 1.0 × 0.20).

---

## Conclusion

### ✅ Graph Score Changed
- **Baseline:** 0.0000 (no network connectivity)
- **After Ingestion:** 1.0000 (maximum centrality as sink node)
- **Impact:** Increased risk assessment by 1.0 point

### ✅ Composite Score Changed  
- **Baseline:** 0.2600 (ML-only mode: 0.65 × 0.40)
- **After Ingestion:** 0.4600 (Graph-aware: + graph contribution of 0.20)
- **Impact:** Increased total risk by 0.2000 points (20% of total)

### ✅ Graph Intelligence Contribution Verified
The composite score increase of 0.2000 equals the graph weight (0.20) multiplied by graph score change (1.0):
```
Composite Delta = Graph Delta × Graph Weight
0.2000 = 1.0 × 0.20 ✓
```

---

## Summary

**All objectives completed with measured evidence:**

1. ✅ Neo4j node count before ingestion: **0**
2. ✅ Neo4j relationship count before ingestion: **0**
3. ✅ Batch prediction executed: **50 records ingested**
4. ✅ Neo4j node count after ingestion: **51**
5. ✅ Neo4j relationship count after ingestion: **50**
6. ✅ Account selected for measurement: **ACC05299999999999**
7. ✅ Baseline scores before ingestion documented
8. ✅ Final scores after ingestion documented
9. ✅ **Graph score changed: YES (0.0 → 1.0)**
10. ✅ **Composite score changed: YES (0.26 → 0.46)**

**Graph intelligence is operational. Graph scores directly contribute to composite risk scores.**
