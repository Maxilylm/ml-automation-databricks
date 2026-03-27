# /db-deploy

Deploy models and pipelines to Databricks. Supports model serving endpoints, scheduled jobs, and Delta Live Tables pipelines.

## Usage

```
/db-deploy [--type serving|job|dlt] [--model <model_name>] [--version <version>] [--endpoint <name>]
```

- `--type`: deployment type (default: serving)
- `--model`: registered model name (from MLflow Model Registry or Unity Catalog)
- `--version`: model version (default: latest Staging or Production)
- `--endpoint`: serving endpoint name (default: derived from model name)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Verify Databricks connection and permissions
4. Validate model exists in registry (if `--model` provided)
5. Check existing endpoints/jobs for conflicts
6. Report: environment status, model info, deployment target

### Stage 1: Model Serving Endpoint (--type serving)

1. Resolve model version:
   - Use specified version, or latest in "Staging" stage
   - Verify model has logged signature and input example
2. Create or update serving endpoint:
   ```python
   endpoint_config = {
       "name": endpoint_name,
       "config": {
           "served_entities": [{
               "entity_name": model_name,
               "entity_version": version,
               "workload_size": "Small",
               "scale_to_zero_enabled": True
           }],
           "auto_capture_config": {
               "catalog_name": catalog,
               "schema_name": schema,
               "table_name_prefix": endpoint_name
           }
       }
   }
   ```
3. Wait for endpoint to reach READY state (poll every 30s, timeout 20min)
4. Run smoke test with sample input
5. Configure inference logging (auto-capture to Delta table)
6. Report: endpoint URL, latency, status

### Stage 2: Scheduled Job (--type job)

1. Generate job configuration:
   - Notebook task or Python script task
   - Job cluster with auto-termination
   - Schedule (cron expression from user or default daily)
   - Retry policy (2 retries, 5-min interval)
   - Email notifications on failure
2. Create job via Jobs API
3. Run initial execution to validate
4. Report: job ID, schedule, cluster config

### Stage 3: Delta Live Tables (--type dlt)

1. Validate DLT pipeline notebook exists (or generate from `/db-pipeline --dlt`)
2. Create DLT pipeline:
   ```python
   pipeline_config = {
       "name": pipeline_name,
       "target": f"{catalog}.{schema}",
       "libraries": [{"notebook": {"path": notebook_path}}],
       "continuous": False,
       "development": True,
       "channel": "CURRENT"
   }
   ```
3. Run pipeline update and monitor progress
4. Validate output tables are created
5. Report: pipeline ID, output tables, data quality results

### Stage 4: Post-Deployment

1. Generate deployment documentation:
   - Endpoint/job/pipeline details
   - Rollback instructions
   - Monitoring setup
   - Alerting configuration
2. Generate client code:
   - Python SDK example for endpoint queries
   - cURL command for REST API testing
   - Sample request/response payloads
3. Cost estimation:
   - DBU consumption estimate
   - Scaling cost projections

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-deployer", {
    "status": "completed",
    "command": "db-deploy",
    "deployment_type": deploy_type,
    "model_name": model_name,
    "model_version": version,
    "endpoint_url": endpoint_url,
    "endpoint_status": status,
    "smoke_test": {"success": success, "latency_ms": latency},
    "estimated_dbu_cost": cost_estimate,
    "rollback_instructions": rollback_steps
})
```

Print: deployment summary, endpoint URL, smoke test results, client example, estimated cost.
