---
name: db-connect
description: "Setup Databricks workspace connection. Configures authentication (PAT, OAuth, Service Principal), validates cluster access, and stores connection profile."
aliases: [databricks connect, databricks auth, databricks login, databricks setup]
extends: ml-automation
user_invocable: true
---

# Databricks Connect

Configure and validate a Databricks workspace connection. Supports Personal Access Token, OAuth, Service Principal, and Azure CLI authentication methods. Validates cluster access, checks Unity Catalog availability, and generates project configuration files.

## Full Specification

See `commands/db-connect.md` for the complete workflow.
