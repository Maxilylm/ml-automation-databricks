# /db-spark

Generate PySpark code from natural language descriptions. Produces optimized Spark DataFrame or Spark SQL code.

## Usage

```
/db-spark "<description>" [--output notebook|script] [--sql] [--optimize]
```

- `description`: natural language description of the desired Spark operation
- `--output`: output format — Databricks notebook or Python script (default: script)
- `--sql`: prefer Spark SQL over DataFrame API where possible
- `--optimize`: include performance optimization hints in generated code

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin
2. Check if `databricks_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/databricks_utils.py`
3. Scan project for existing Spark code patterns:
   - SparkSession variable name conventions
   - Existing import patterns
   - Delta table naming conventions
   - Catalog/schema in use
4. Report: detected conventions, available tables

### Stage 1: Parse Intent

1. Analyze natural language description to determine:
   - Data sources (tables, files, streams)
   - Operations (filter, join, aggregate, window, pivot)
   - Output requirements (table, file, display)
   - Performance constraints (if any)
2. If ambiguous, ask clarifying questions

### Stage 2: Generate Code

1. Generate PySpark code with:
   - Proper imports and SparkSession setup
   - DataFrame API operations (preferred for complex logic)
   - Spark SQL queries (preferred if `--sql` or for simple queries)
   - Inline comments explaining each transformation
   - Type hints and docstrings
2. If `--optimize`:
   - Add broadcast hints for small tables
   - Use persist/cache for reused DataFrames
   - Apply predicate pushdown
   - Repartition recommendations
3. If `--output notebook`:
   - Add `# Databricks notebook source` header
   - Split into cells with `# COMMAND ----------`
   - Add markdown cells for documentation

### Stage 3: Validation

1. Static analysis of generated code:
   - Import completeness
   - Variable name consistency
   - No hardcoded paths (use config)
   - Proper null handling
2. If Databricks connection available:
   - Validate table names exist
   - Check column name references
   - Dry-run explain plan

### Stage 4: Report

```python
from ml_utils import save_agent_report
save_agent_report("databricks-engineer", {
    "status": "completed",
    "command": "db-spark",
    "description": description,
    "output_file": output_path,
    "operations": detected_operations,
    "tables_referenced": tables,
    "optimization_hints": hints
})
```

Print: generated file path, operations summary, optimization notes.
