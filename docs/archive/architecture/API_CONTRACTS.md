# API_CONTRACTS.md
_Definitive developer schema reference for API request and response contracts. ~700 tokens._

---

## 🛰️ BASE ROUTE
All API routes are served relative to the API gateway root: `http://<server-ip>:8000/api/v1`

---

## 📑 ENDPOINT ROUTING CONTRACTS

### 1. Single Account Prediction
*   **Path:** `/predict/single`
*   **Method:** `POST`
*   **Authentication:** Bearer JWT required
*   **Description:** Performs dynamic tabular ML inference, SHAP evaluation, graph traversal score fusion, and automated compliance routing for a single account.
*   **Request Payload (JSON):**
    ```json
    {
      "account_id": "9082_ACC",
      "features": {
        "F1": 0.0,
        "F2": 245.2,
        "F115": 0.72,
        "F670": 1.0,
        "F886": 0.18,
        "F2082": 0.0,
        "F3889": "G365D",
        "F3891": "student"
      }
    }
    ```
    *(Note: features must supply values corresponding to DataSet.csv features)*

*   **Response Payload (JSON):**
    ```json
    {
      "account_id": "9082_ACC",
      "risk_score": 87.2,
      "tier": "CRITICAL",
      "ml_score": 0.92,
      "graph_score": 0.76,
      "mule_stage": "ACTIVE_MULE",
      "signals": [
        {
          "feature": "F670",
          "value": 1.0,
          "direction": "positive",
          "description": "Prior regulatory watch-list flag active on account"
        },
        {
          "feature": "F886",
          "value": 0.18,
          "direction": "positive",
          "description": "Unusual rapid channel-switching behavior detected"
        }
      ],
      "shap_values": {
        "F670": 0.28,
        "F886": 0.22,
        "F3908": 0.19,
        "F115": 0.11,
        "F2082": 0.08
      },
      "str_recommended": true,
      "str_pre_filled": {
        "report_id": "STR-2026-9082_ACC",
        "pmla_section": "12",
        "transaction_amount": 180000.0,
        "compliance_narrative": "🔁 Automatic goAML Alert: Mule account exhibiting high velocity circular flows detected..."
      }
    }
    ```

---

### 2. Batch Accounts Upload Prediction
*   **Path:** `/predict/batch`
*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`
*   **Description:** Uploads a CSV file matching the structure of `DataSet.csv`. Executes parallel batch prediction using optimized multi-threading.
*   **Request Payload:**
    *   Form field `file`: binary stream of `DataSet.csv`
*   **Response Payload (JSON):**
    ```json
    {
      "summary": {
        "total_analyzed": 9082,
        "critical_count": 16,
        "high_count": 31,
        "medium_count": 89,
        "low_count": 8946,
        "execution_time_ms": 3200
      },
      "accounts": [
        {
          "account_id": "1002_ACC",
          "risk_score": 91.5,
          "tier": "CRITICAL",
          "ml_score": 0.95,
          "graph_score": 0.83,
          "mule_stage": "ACTIVE_MULE",
          "str_recommended": true
        },
        {
          "account_id": "4092_ACC",
          "risk_score": 68.0,
          "tier": "HIGH",
          "ml_score": 0.72,
          "graph_score": 0.58,
          "mule_stage": "NEWLY_RECRUITED",
          "str_recommended": false
        }
      ]
    }
    ```

---

### 3. Government I4C Portal Alert Webhook Ingestion
*   **Path:** `/ingest-i4c`
*   **Method:** `POST`
*   **Authentication:** Webhook token secret required
*   **Request Payload (JSON):**
    ```json
    {
      "complaint_id": "MHA-2026-9908",
      "account_no": "9082_ACC",
      "reported_amount": 180000.0,
      "reported_timestamp": "2026-05-30T10:15:00Z"
    }
    ```
*   **Response Payload (JSON):**
    ```json
    {
      "status": "INGESTED_AND_EVALUATED",
      "complaint_id": "MHA-2026-9908",
      "action_taken": "CASE_OPENED_CRITICAL_LOCK_RECOMMENDED",
      "risk_response": {
        "account_id": "9082_ACC",
        "risk_score": 87.2,
        "tier": "CRITICAL",
        "str_recommended": true
      }
    }
    ```

---

## 🛑 ERROR RESPONSE SCHEMA
All HTTP errors return structured JSON with uniform fields.

*   **HTTP 400 Bad Request (e.g. CSV missing columns):**
    ```json
    {
      "detail": {
        "error_code": "INVALID_SCHEMA_VIOLATION",
        "message": "Missing required data columns: ['from', 'to', 'amount']",
        "timestamp": "2026-05-31T01:00:00Z"
      }
    }
    ```

*   **HTTP 500 Internal Server Error (e.g. Model Fail):**
    ```json
    {
      "detail": {
        "error_code": "ML_INFERENCE_EXCEPTION",
        "message": "Model failed to perform scoring. Standby fallback active.",
        "timestamp": "2026-05-31T01:00:00Z"
      }
    }
    ```
