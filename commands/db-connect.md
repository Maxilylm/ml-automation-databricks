# /db-connect

Setup Databricks workspace connection. Configures authentication, validates access, and stores connection profile.

## Usage

```
/db-connect [--workspace <url>] [--token <pat>] [--cluster <cluster_id>] [--profile <name>]
```

- `--workspace`: Databricks workspace URL (e.g., `https://adb-1234567890.12.azuredatabricks.net`)
- `--token`: Personal Access Token (if not using OAuth or CLI auth)
- `--cluster`: Default cluster ID for interactive sessions
- `--profile`: Connection profile name (default: `DEFAULT`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Check for existing Databricks configuration:
   - `~/.databrickscfg` file
   - `DATABRICKS_HOST` and `DATABRICKS_TOKEN` environment variables
   - Databricks CLI installation (`databricks --version`)
4. Report: existing configuration found or fresh setup needed

### Stage 1: Authentication Setup

1. Determine authentication method:
   - **PAT (Personal Access Token)** — simplest, provided via `--token`
   - **OAuth (U2M)** — `databricks auth login` (requires CLI)
   - **Service Principal** — for CI/CD (client_id + client_secret)
   - **Azure CLI** — if Azure Databricks (`az login` token)
2. Write or update `~/.databrickscfg`:
   ```ini
   [<profile>]
   host = <workspace_url>
   token = <pat>
   cluster_id = <cluster_id>
   ```
3. Validate token has not expired

### Stage 2: Connection Validation

1. Test workspace connectivity: `GET /api/2.0/clusters/list`
2. Verify cluster exists and get status (RUNNING, TERMINATED, PENDING)
3. Check user permissions: workspace access level
4. List available catalogs (Unity Catalog): `GET /api/2.1/unity-catalog/catalogs`
5. Report: connection status, cluster state, available catalogs

### Stage 3: Project Configuration

1. Generate `config/databricks_config.json`:
   ```json
   {
     "workspace_url": "<url>",
     "profile": "<profile>",
     "default_cluster_id": "<cluster_id>",
     "default_catalog": "main",
     "default_schema": "default",
     "dbfs_prefix": "dbfs:/FileStore/project"
   }
   ```
2. Add `.databrickscfg` to `.gitignore` if not present
3. Generate `src/db_connection.py` helper module

### Stage 4: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-engineer", {
    "status": "completed",
    "command": "db-connect",
    "workspace_url": workspace_url,
    "profile": profile,
    "cluster_id": cluster_id,
    "cluster_state": cluster_state,
    "catalogs_available": catalogs,
    "auth_method": auth_method
})
```

Print: workspace URL, auth method, cluster state, available catalogs.
