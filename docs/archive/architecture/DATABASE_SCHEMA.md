# DATABASE_SCHEMA.md
_Graph structures (Neo4j Cypher) and relational models (PostgreSQL tables) schema definition. ~600 tokens._

---

## 🌐 GRAPH DATABASE MODEL: NEO4J

The system uses Neo4j to store and evaluate network relationships between financial nodes. High-risk accounts are matched dynamically via graph topologies.

```
       ┌────────────────────────┐
       │        :Account        │ Node
       │ ───────┬────────────── │
       │ account_id (Key)       │
       │ customer_name          │
       │ risk_score             │
       └────────┬───────┬───────┘
                │       ▲
   [:TRANSFERRED│       │[:TRANSFERRED
   {amount,     │       │{amount,
    timestamp}] │       │timestamp}]
                ▼       │
       ┌────────┴───────┴────────┐
       │        :Account        │ Node
       │ ───────┬────────────── │
       │ account_id (Key)       │
       │ customer_name          │
       │ risk_score             │
       └────────────────────────┘
```

### 1. Nodes & Properties
*   **Label:** `:Account`
    *   `account_id`: String (Unique constraint)
    *   `risk_score`: Float
    *   `tier`: String
    *   `mule_stage`: String

### 2. Relationships & Properties
*   **Type:** `[:TRANSFERRED]`
    *   `amount`: Float
    *   `timestamp`: Datetime
    *   `channel`: String (e.g. UPI, RTGS, IMPS, ATM)
    *   `location`: String

---

## ⚡ GRAPH ALGORITHM QUERY TEMPLATES

### 1. Cycle Detection (Circular Flows)
Finds round-tripping of funds where money leaves and returns to an account (length 3 to 5):
```cypher
MATCH path = (a:Account)-[r:TRANSFERRED*3..5]->(a:Account)
WHERE all(i in range(0, size(path)-2) 
          WHERE (path[i]).timestamp < (path[i+1]).timestamp)
RETURN a.account_id AS source, 
       [n in nodes(path) | n.account_id] AS cycle_path,
       [rel in relationships(path) | rel.amount] AS transaction_chain
LIMIT 10
```

### 2. Layering Detection (Multi-Hop Paths)
Detects structural hops intended to obscure money trail (length $\geq 4$ hops):
```cypher
MATCH path = (a:Account)-[:TRANSFERRED*4..6]->(b:Account)
WHERE a <> b AND all(i in range(0, size(path)-2) 
                     WHERE (path[i]).timestamp < (path[i+1]).timestamp)
RETURN a.account_id AS initiator,
       b.account_id AS terminal_sink,
       size(path) AS hop_count,
       [n in nodes(path) | n.account_id] AS trace_route
```

---

## 🐘 RELATIONAL DATABASE SCHEMA: POSTGRESQL

PostgreSQL manages security, access tracking, case tracking, audit trail metrics, and generated XML compliance logs.

```
                  ┌──────────────────────┐
                  │        users         │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ username (UQ)        │
                  │ password_hash        │
                  │ role                 │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ 1..*
                  ┌──────────▼───────────┐
                  │    audit_records     │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ user_id (FK)         │
                  │ action               │
                  │ timestamp            │
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │     cases_table      │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ account_id (UQ)      │
                  │ risk_score           │
                  │ tier                 │
                  │ status               │
                  │ str_xml_id (FK)      │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ 0..1
                  ┌──────────▼───────────┐
                  │      compliance_strs │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ generated_xml        │
                  │ blockchain_hash (UQ) │
                  │ timestamp            │
                  └──────────────────────┘
```

### 1. User Security (`users`)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Audit Trail Logs (`audit_records`)
```sql
CREATE TABLE audit_records (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    target_account VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Incident Case Tracker (`cases_table`)
```sql
CREATE TABLE cases_table (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(100) UNIQUE NOT NULL,
    risk_score NUMERIC(5,2) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'OPEN', -- OPEN, INVESTIGATING, FROZEN, DISMISSED
    assigned_analyst_id INT REFERENCES users(id),
    str_xml_id INT REFERENCES compliance_strs(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Regulatory Suspicious Reports (`compliance_strs`)
```sql
CREATE TABLE compliance_strs (
    id SERIAL PRIMARY KEY,
    generated_xml TEXT NOT NULL,
    blockchain_hash CHAR(64) UNIQUE NOT NULL, -- SHA-256 evidence hash
    anchored_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
