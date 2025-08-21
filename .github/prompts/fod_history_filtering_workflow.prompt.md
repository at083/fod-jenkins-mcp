---
mode: 'agent'
description: 'Job history and filtering workflow for FoD jobs'
---
# Job History & Filtering Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to query and filter FoD jobs using MCP tools. For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Querying and Filtering Jobs

- **List Jobs:**
  - Use `fod_list_jobs` to query jobs by owner, tags, hardware model, state, etc.
  - Example queries:
    - "Show all jobs tagged 'nightly' for hardware model F1D1."
    - "List failed jobs for user@fungible.com in the last 7 days."
  - Parameters: `owner`, `tags`, `state`, `hardware_model`, `days`, `sort`, etc.

- **Result History:**
  - Use `fod_get_result_history` to fetch grouped/ungrouped job results for regression tracking.

- **Best Practice:**
  - Always use unique tags or notes when submitting jobs for easier filtering and tracking.
  - Use field discovery tools (`fod_get_distinct_values`, `fod_autocomplete`) if unsure about valid options.

---

## Tips
- For regression tracking, always use consistent tags and hardware model names.
- To filter jobs by reserved resources, see the [Reservation & Resource Management](fod_reservation_workflow.prompt.md) workflow.

---

## References
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
- For log and artifact retrieval, see [Log & Artifact Retrieval Workflow](fod_log_artifact_workflow.prompt.md).
