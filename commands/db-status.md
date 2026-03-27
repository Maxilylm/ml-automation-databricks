# /db-status

Check Databricks workspace resource status. Lists clusters, jobs, models, serving endpoints, and Delta tables.

## Usage

```
/db-status [--resource clusters|jobs|models|endpoints|tables|all] [--verbose]
```

- `--resource`: specific resource type to check (default: all)
- `--verbose`: show detailed information per resource

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Verify Databricks connection
4. Report: connection status, workspace URL

### Stage 1: Clusters

1. List all clusters: `GET /api/2.0/clusters/list`
2. For each cluster:
   - Name, ID, state (RUNNING, TERMINATED, PENDING, ERROR)
   - Runtime version (e.g., 14.3.x-scala2.12)
   - Node type and worker count
   - Auto-termination setting
   - Uptime (if running)
3. Flag: running clusters with no recent activity (cost waste)

### Stage 2: Jobs

1. List recent jobs: `GET /api/2.1/jobs/list`
2. For each job:
   - Name, ID, schedule (cron or manual)
   - Last run status (SUCCESS, FAILED, RUNNING, SKIPPED)
   - Last run duration and timestamp
   - Next scheduled run
3. Flag: failed jobs in last 24h, jobs with no recent runs

### Stage 3: Models (MLflow Registry)

1. List registered models: `GET /api/2.0/mlflow/registered-models/list`
2. For each model:
   - Name, latest version, current stage
   - Last updated timestamp
   - Description (if set)
3. If Unity Catalog: list models from `system.ml.models`
4. Flag: models in "Staging" for more than 7 days (stale)

### Stage 4: Serving Endpoints

1. List endpoints: `GET /api/2.0/serving-endpoints`
2. For each endpoint:
   - Name, state (READY, NOT_READY, UPDATING)
   - Served model and version
   - Scale configuration (min/max instances)
   - Recent traffic (requests/min, p50/p99 latency)
3. Flag: NOT_READY endpoints, endpoints with zero traffic

### Stage 5: Delta Tables (if --resource tables or all)

1. List tables in configured catalog/schema:
   ```sql
   SHOW TABLES IN catalog.schema
   ```
2. For each table:
   - Name, type (MANAGED, EXTERNAL), format
   - Row count estimate, size on disk
   - Last modified timestamp
   - Partitioning columns
3. Flag: tables not updated in 30+ days, tables needing OPTIMIZE

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-engineer", {
    "status": "completed",
    "command": "db-status",
    "clusters": cluster_summary,
    "jobs": job_summary,
    "models": model_summary,
    "endpoints": endpoint_summary,
    "tables": table_summary,
    "alerts": alerts,
    "cost_warnings": cost_warnings
})
```

Print formatted status dashboard:
```
=== Databricks Workspace Status ===
Workspace: https://adb-xxx.azuredatabricks.net

Clusters (3):
  [RUNNING]    ml-cluster-01    14.3 LTS    4 workers    uptime: 2h 15m
  [TERMINATED] etl-cluster-02   14.3 LTS    8 workers    idle: 3d
  [RUNNING]    dev-cluster-03   15.1 LTS    2 workers    uptime: 45m

Jobs (5):
  [OK]      daily-etl           last: SUCCESS  2h ago     next: tomorrow 06:00
  [FAILED]  weekly-retrain      last: FAILED   1d ago     next: Sunday 00:00
  [OK]      hourly-ingest       last: SUCCESS  15m ago    next: :00

Models (2):
  fraud_detector     v3 (Production)    updated: 5d ago
  churn_predictor    v7 (Staging)       updated: 12d ago  [STALE]

Endpoints (1):
  [READY]  fraud-detector-ep    v3    1-4 instances    p50: 45ms

Alerts:
  - weekly-retrain job FAILED 1d ago
  - churn_predictor model in Staging for 12 days
```
