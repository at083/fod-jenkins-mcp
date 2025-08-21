---
mode: 'agent'
description: 'Log and artifact retrieval workflow for FoD jobs'
---
# Log & Artifact Retrieval Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to retrieve logs and artifacts from FoD jobs using MCP tools. For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Retrieving Logs and Artifacts

- **Raw File Retrieval:**
  - Use `fod_get_raw_file(lsf_id, file_name)` to fetch raw output or log files.
  - These are the only file names you should ***ever*** query for any of these retrieval tools:
    - `odp/uartout0.0.txt`: FunOS console log
    - `odp/uartout1.0.txt`: SBP console log
    - Other files as listed in the job outputs
  - When the user requests a FunOS log, query for `odp/uartout0.0.txt`. For SBP, query for `odp/uartout1.0.txt`.

- **Human-Readable Logs:**
  - Use `fod_get_human_file(lsf_id, file_name, filter_level)` to fetch filtered, HTML-formatted logs for easier analysis.

- **Workflow:**
  1. Use `fod_get_job(lsf_id)` to list available files for the job.
  2. Fetch the desired log or artifact using `fod_get_raw_file` or `fod_get_human_file`.
  3. For large logs, consider filtering or paging as needed.

---

## Tips
- If you cannot find a log file, check the job’s outputs with `fod_get_job` and confirm the file name.
- Some logs may be large; fetch them in chunks or use filtering as needed.

---

## References
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
- For job history and filtering, see [Job History & Filtering Workflow](fod_history_filtering_workflow.prompt.md).
