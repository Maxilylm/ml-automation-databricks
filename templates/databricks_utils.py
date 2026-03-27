"""
Databricks utilities for the ml-automation-databricks extension plugin.

Requires ml_utils.py from the ml-automation core plugin to be present
in the same directory (copied via Stage 0 of Databricks commands).
"""

import os
import json
import re
import configparser
from pathlib import Path
from typing import List, Dict, Optional, Any

from ml_utils import save_agent_report, load_agent_report


# --- Relevance Detection ---

DATABRICKS_INDICATORS = {
    "pyspark",
    "databricks",
    "delta",
    "mlflow",
    "databricks.sdk",
    "databricks.connect",
    "databricks.feature_store",
}

DATABRICKS_FILE_PATTERNS = [
    ".databrickscfg",
    "databricks.yml",
    "bundle.yml",
]

DATABRICKS_CODE_PATTERNS = [
    r"dbfs:/",
    r"abfss://",
    r"\.format\([\"']delta[\"']\)",
    r"DeltaTable",
    r"USING DELTA",
    r"spark\.read",
    r"spark\.sql",
    r"dbutils\.",
    r"# Databricks notebook source",
]


def detect_databricks_relevance(project_path="."):
    """Check if project has Databricks indicators for relevance gating.

    Checks: Databricks config files, PySpark/Delta imports, notebook headers,
    DBFS/ABFSS paths, MLflow references, Unity Catalog usage.

    Args:
        project_path: root directory of the project

    Returns:
        dict with 'is_databricks': bool, 'indicators': list of found indicators
    """
    indicators = []
    project = Path(project_path)

    # Check for Databricks config files
    for config_file in DATABRICKS_FILE_PATTERNS:
        config_path = project / config_file
        if config_path.exists():
            indicators.append(f"{config_file} found in project root")

    # Check home directory for .databrickscfg
    home_cfg = Path.home() / ".databrickscfg"
    if home_cfg.exists():
        indicators.append(".databrickscfg found in home directory")

    # Check environment variables
    if os.environ.get("DATABRICKS_HOST"):
        indicators.append("DATABRICKS_HOST environment variable set")
    if os.environ.get("DATABRICKS_TOKEN"):
        indicators.append("DATABRICKS_TOKEN environment variable set")

    # Check requirements for Databricks packages
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]:
        req_path = project / req_file
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                for pkg in DATABRICKS_INDICATORS:
                    if pkg in content:
                        indicators.append(f"{pkg} in {req_file}")
            except (UnicodeDecodeError, PermissionError):
                continue

    # Check Python files for Databricks imports
    py_files = list(project.glob("**/*.py"))[:50]  # limit scan
    for py_file in py_files:
        try:
            content = py_file.read_text()
            # Check notebook header
            if content.startswith("# Databricks notebook source"):
                indicators.append(f"Databricks notebook: {py_file.name}")
                continue
            # Check imports
            for pkg in DATABRICKS_INDICATORS:
                if f"import {pkg}" in content or f"from {pkg}" in content:
                    indicators.append(f"{pkg} import in {py_file.name}")
                    break
            # Check code patterns
            for pattern in DATABRICKS_CODE_PATTERNS:
                if re.search(pattern, content):
                    indicators.append(f"Databricks pattern in {py_file.name}: {pattern}")
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for Delta Lake directories
    for delta_dir in ["delta_tables", "spark-warehouse"]:
        if (project / delta_dir).is_dir():
            indicators.append(f"Delta directory: {delta_dir}/")

    # Check for MLflow artifacts
    if (project / "mlruns").is_dir():
        indicators.append("MLflow runs directory: mlruns/")

    return {
        "is_databricks": len(indicators) > 0,
        "indicators": indicators,
    }


# --- Connection Management ---

def get_databricks_connection(profile="DEFAULT"):
    """Get Databricks connection details from config or environment.

    Priority:
    1. Environment variables (DATABRICKS_HOST, DATABRICKS_TOKEN)
    2. Project-level config (config/databricks_config.json)
    3. ~/.databrickscfg [profile]

    Args:
        profile: config profile name (default: DEFAULT)

    Returns:
        dict with 'host', 'token', 'cluster_id' (any may be None)
    """
    connection = {"host": None, "token": None, "cluster_id": None}

    # 1. Environment variables (highest priority)
    env_host = os.environ.get("DATABRICKS_HOST")
    env_token = os.environ.get("DATABRICKS_TOKEN")
    env_cluster = os.environ.get("DATABRICKS_CLUSTER_ID")
    if env_host:
        connection["host"] = env_host.rstrip("/")
        connection["token"] = env_token
        connection["cluster_id"] = env_cluster
        return connection

    # 2. Project-level config
    project_config = Path("config/databricks_config.json")
    if project_config.exists():
        try:
            config = json.loads(project_config.read_text())
            connection["host"] = config.get("workspace_url", "").rstrip("/")
            connection["cluster_id"] = config.get("default_cluster_id")
            # Token comes from .databrickscfg, not project config
            profile = config.get("profile", profile)
        except (json.JSONDecodeError, PermissionError):
            pass

    # 3. ~/.databrickscfg
    cfg_path = Path.home() / ".databrickscfg"
    if cfg_path.exists():
        try:
            config = configparser.ConfigParser()
            config.read(str(cfg_path))
            if profile in config:
                section = config[profile]
                if not connection["host"]:
                    connection["host"] = section.get("host", "").rstrip("/")
                if not connection["token"]:
                    connection["token"] = section.get("token")
                if not connection["cluster_id"]:
                    connection["cluster_id"] = section.get("cluster_id")
        except (configparser.Error, PermissionError):
            pass

    return connection


def get_spark_session(app_name="ml-automation-databricks", master=None):
    """Get or create a SparkSession.

    Detects Databricks runtime vs. local environment and configures
    accordingly. On Databricks, returns the existing session. Locally,
    creates a new session with Delta Lake support.

    Args:
        app_name: Spark application name
        master: Spark master URL (default: local[*] for local, auto for Databricks)

    Returns:
        SparkSession instance
    """
    try:
        from pyspark.sql import SparkSession
    except ImportError:
        raise ImportError(
            "pyspark required. Install with: pip install pyspark"
        )

    # Check if running on Databricks
    if _is_databricks_runtime():
        # On Databricks, SparkSession is pre-configured
        return SparkSession.builder.getOrCreate()

    # Local environment
    builder = SparkSession.builder.appName(app_name)

    if master:
        builder = builder.master(master)
    else:
        builder = builder.master("local[*]")

    # Enable Delta Lake locally
    builder = builder.config(
        "spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0"
    ).config(
        "spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension"
    ).config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )

    return builder.getOrCreate()


def _is_databricks_runtime():
    """Check if code is running on Databricks runtime."""
    return (
        "DATABRICKS_RUNTIME_VERSION" in os.environ
        or os.path.exists("/databricks/spark")
    )


# --- Spark SQL Execution ---

def execute_spark_sql(query, spark=None):
    """Execute a Spark SQL query and return results.

    Args:
        query: SQL query string
        spark: SparkSession (creates one if not provided)

    Returns:
        dict with 'columns': list, 'rows': list of lists,
        'row_count': int, 'schema': dict
    """
    if spark is None:
        spark = get_spark_session()

    df = spark.sql(query)
    schema = {field.name: str(field.dataType) for field in df.schema.fields}
    rows = [list(row.asDict().values()) for row in df.collect()]

    return {
        "columns": list(schema.keys()),
        "rows": rows,
        "row_count": len(rows),
        "schema": schema,
    }


# --- Delta Lake Operations ---

def load_delta_table(path_or_table, spark=None, version=None, timestamp=None):
    """Load a Delta table into a Spark DataFrame.

    Supports reading by path, table name, version (time travel),
    or timestamp.

    Args:
        path_or_table: Delta table path (dbfs:/...) or name (catalog.schema.table)
        spark: SparkSession (creates one if not provided)
        version: specific version number for time travel
        timestamp: specific timestamp for time travel (string)

    Returns:
        dict with 'dataframe': Spark DataFrame, 'row_count': int,
        'columns': list, 'schema': dict
    """
    if spark is None:
        spark = get_spark_session()

    reader = spark.read.format("delta")

    if version is not None:
        reader = reader.option("versionAsOf", version)
    elif timestamp is not None:
        reader = reader.option("timestampAsOf", timestamp)

    # Determine if path or table name
    if "/" in path_or_table or path_or_table.startswith("dbfs:"):
        df = reader.load(path_or_table)
    else:
        df = reader.table(path_or_table)

    schema = {field.name: str(field.dataType) for field in df.schema.fields}

    return {
        "dataframe": df,
        "row_count": df.count(),
        "columns": list(schema.keys()),
        "schema": schema,
    }


def write_delta_table(df, path_or_table, mode="overwrite", partition_by=None,
                      merge_condition=None, spark=None):
    """Write a Spark DataFrame to a Delta table.

    Supports overwrite, append, and merge (upsert) modes.

    Args:
        df: Spark DataFrame to write
        path_or_table: Delta table path or name
        mode: 'overwrite', 'append', or 'merge'
        partition_by: list of partition columns
        merge_condition: SQL condition for merge mode (e.g., "target.id = source.id")
        spark: SparkSession (needed for merge mode)

    Returns:
        dict with 'status', 'path_or_table', 'mode', 'row_count'
    """
    row_count = df.count()

    if mode == "merge" and merge_condition:
        if spark is None:
            spark = get_spark_session()
        try:
            from delta.tables import DeltaTable
        except ImportError:
            raise ImportError(
                "delta-spark required. Install with: pip install delta-spark"
            )

        if "/" in path_or_table or path_or_table.startswith("dbfs:"):
            delta_table = DeltaTable.forPath(spark, path_or_table)
        else:
            delta_table = DeltaTable.forName(spark, path_or_table)

        delta_table.alias("target").merge(
            df.alias("source"), merge_condition
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    else:
        writer = df.write.format("delta").mode(mode)
        if partition_by:
            writer = writer.partitionBy(*partition_by)

        if "/" in path_or_table or path_or_table.startswith("dbfs:"):
            writer.save(path_or_table)
        else:
            writer.saveAsTable(path_or_table)

    return {
        "status": "completed",
        "path_or_table": path_or_table,
        "mode": mode,
        "row_count": row_count,
    }


# --- MLflow Integration ---

def register_mlflow_model(run_id, model_name, artifact_path="model",
                          tags=None, description=None):
    """Register an MLflow model to the Model Registry.

    Args:
        run_id: MLflow run ID containing the model artifact
        model_name: name for the registered model
        artifact_path: path within the run artifacts (default: "model")
        tags: dict of tags to apply to the model version
        description: model description

    Returns:
        dict with 'name', 'version', 'source', 'status'
    """
    try:
        import mlflow
        from mlflow.tracking import MlflowClient
    except ImportError:
        raise ImportError(
            "mlflow required. Install with: pip install mlflow"
        )

    model_uri = f"runs:/{run_id}/{artifact_path}"

    # Register model
    result = mlflow.register_model(model_uri, model_name)

    client = MlflowClient()

    # Add description
    if description:
        client.update_registered_model(model_name, description=description)

    # Add tags
    if tags:
        for key, value in tags.items():
            client.set_model_version_tag(
                model_name, result.version, key, value
            )

    return {
        "name": result.name,
        "version": result.version,
        "source": result.source,
        "status": result.status,
    }


# --- Cluster Utilities ---

def get_cluster_status(cluster_id=None, connection=None):
    """Get status of a Databricks cluster.

    Args:
        cluster_id: cluster ID (uses default from connection if not provided)
        connection: connection dict from get_databricks_connection()

    Returns:
        dict with cluster details or error
    """
    if connection is None:
        connection = get_databricks_connection()

    if cluster_id is None:
        cluster_id = connection.get("cluster_id")

    if not cluster_id:
        return {"error": "No cluster ID provided or configured"}

    host = connection.get("host")
    token = connection.get("token")

    if not host or not token:
        return {"error": "Databricks host or token not configured"}

    try:
        import urllib.request
        url = f"{host}/api/2.0/clusters/get"
        data = json.dumps({"cluster_id": cluster_id}).encode()
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return {
                "cluster_id": result.get("cluster_id"),
                "cluster_name": result.get("cluster_name"),
                "state": result.get("state"),
                "spark_version": result.get("spark_version"),
                "node_type_id": result.get("node_type_id"),
                "num_workers": result.get("num_workers"),
                "autotermination_minutes": result.get("autotermination_minutes"),
            }
    except Exception as e:
        return {"error": str(e)}


# --- Workspace Utilities ---

def list_workspace_resources(resource_type="all", connection=None):
    """List Databricks workspace resources.

    Args:
        resource_type: 'clusters', 'jobs', 'models', 'endpoints', or 'all'
        connection: connection dict from get_databricks_connection()

    Returns:
        dict with resource listings
    """
    if connection is None:
        connection = get_databricks_connection()

    host = connection.get("host")
    token = connection.get("token")

    if not host or not token:
        return {"error": "Databricks host or token not configured"}

    resources = {}

    def _api_get(path):
        try:
            import urllib.request
            url = f"{host}{path}"
            req = urllib.request.Request(
                url, method="GET",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

    if resource_type in ("clusters", "all"):
        result = _api_get("/api/2.0/clusters/list")
        clusters = result.get("clusters", [])
        resources["clusters"] = [
            {
                "name": c.get("cluster_name"),
                "id": c.get("cluster_id"),
                "state": c.get("state"),
                "runtime": c.get("spark_version"),
                "workers": c.get("num_workers"),
            }
            for c in clusters
        ]

    if resource_type in ("jobs", "all"):
        result = _api_get("/api/2.1/jobs/list")
        jobs = result.get("jobs", [])
        resources["jobs"] = [
            {
                "name": j.get("settings", {}).get("name"),
                "job_id": j.get("job_id"),
                "schedule": j.get("settings", {}).get("schedule", {}).get(
                    "quartz_cron_expression", "manual"
                ),
            }
            for j in jobs[:50]
        ]

    if resource_type in ("models", "all"):
        result = _api_get("/api/2.0/mlflow/registered-models/list")
        models = result.get("registered_models", [])
        resources["models"] = [
            {
                "name": m.get("name"),
                "latest_version": (
                    m.get("latest_versions", [{}])[0].get("version")
                    if m.get("latest_versions") else None
                ),
                "description": m.get("description", ""),
            }
            for m in models
        ]

    if resource_type in ("endpoints", "all"):
        result = _api_get("/api/2.0/serving-endpoints")
        endpoints = result.get("endpoints", [])
        resources["endpoints"] = [
            {
                "name": e.get("name"),
                "state": e.get("state", {}).get("ready"),
                "served_entities": [
                    se.get("entity_name")
                    for se in e.get("config", {}).get("served_entities", [])
                ],
            }
            for e in endpoints
        ]

    return resources
