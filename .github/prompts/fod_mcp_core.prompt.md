---
mode: 'agent'
description: 'Core guide for Fun-on-Demand (FoD) MCP usage'
---
# Fun-on-Demand (FoD) MCP Core Guide

> **Purpose:**
> This file provides a concise overview of the MCP, its main tool categories, and general usage patterns. For detailed workflows, see the referenced workflow prompt files.

---

## What are these tools?
The Model Context Protocol (MCP) exposes Fun-on-Demand (FoD) and Jenkins operations as structured, schema-validated tools for automation agents, LLMs, and Copilot.

---

## Tool Categories
- **Job Submission:** Submit jobs via CLI or by branch (see [Branch Submission Workflow](fod_branch_submission_workflow.prompt.md)).
- **Live Monitoring & Control:** Monitor job/build status, cancel/restart jobs.
- **Log & Artifact Retrieval:** Fetch logs and artifacts for debugging.
- **Job History & Filtering:** Query and filter jobs by owner, tags, hardware model, etc.
- **Reservation & Resource Management:** Reserve lab resources and check status.
- **Field Discovery:** Use distinct values and autocomplete tools to discover valid options.

---

## General Usage Patterns
- Always use MCP tools for all FoD and Jenkins automation.
- For branch-based job submission, see [Branch Submission Workflow](fod_branch_submission_workflow.prompt.md).
- For CLI-based job submission, see [CLI Submission Workflow](fod_cli_submission_workflow.prompt.md).
- For Jenkins build monitoring, see [Jenkins Build Monitoring](fod_jenkins_build_monitoring_workflow.prompt.md).
- For log retrieval, see [Log & Artifact Retrieval](fod_log_artifact_workflow.prompt.md).
- For job history, see [Job History & Filtering](fod_history_filtering_workflow.prompt.md).
- For reservations, see [Reservation & Resource Management](fod_reservation_workflow.prompt.md).

---

## Authentication & Access
- All workflows assume you are authenticated and have access to the required MCP and FoD endpoints.

---

## Not Sure Where to Start?
- If you are unsure which workflow to use, start here and follow the references to the workflow that matches your task.

---

## Best Practices
- Always include a unique tag or note when submitting jobs for easier tracking.
- Use field discovery tools if unsure about valid options.
- Reference workflow-specific prompt files for step-by-step guidance.
