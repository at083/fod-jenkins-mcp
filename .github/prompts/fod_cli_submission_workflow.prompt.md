---
mode: 'agent'
description: 'CLI-based FoD job submission workflow'
---
# CLI Job Submission Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to submit a FoD job using the CLI (with signed binaries and a .params file). For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Submitting a FoD Job via CLI

- **Tool:** `fod_submit_job`
- **Purpose:** Launch a parameterized FoD job using a signed binary and a `.params` file.

### How to Use
- Ensure all required artifacts (signed FunOS binary, blobs, etc.) are available and referenced in the `.params` file.
- The `.params` file defines job parameters (see below for structure).
- Call `fod_submit_job` with:
  - `funos_binary`: Path to the signed FunOS binary.
  - `blobs`: List of blob files (if any).
  - `hardware_model`, `duration`, `tags`, `note`, `params_file`, `extra_args`: As needed.
- After submitting a job, retrieve the job's ***lsf_id*** (this is the user-end job id) and status (see the job history & filtering workflow for details).

### Creating/Editing .params Files
- Each line is `KEY: VALUE`.
- Common keys:
  - `EXTRA_EMAIL`: Notification email (must be @fungible.com or @microsoft.com)
  - `HW_MODEL`: Hardware model (e.g., F1D1)
  - `RUN_TARGET`: Target platform (e.g., F1, S1, F1D1)
  - `BOOTARGS`: Boot arguments for FunOS
  - `USE_CCLINUX`, `USE_ACU`, `USE_CLUSTER_SERVICES`: true/false
  - `MAX_DURATION`: Job duration (minutes)
  - `PRIORITY`: low_priority, normal_priority, high_priority
  - `TAGS`, `NOTE`, etc.
- Example:
  ```
  EXTRA_EMAIL: user@microsoft.com
  HW_MODEL: F1D1
  RUN_TARGET: F1D1
  BOOTARGS: --dpc-server --skip_abort
  USE_CCLINUX: true
  MAX_DURATION: 45
  PRIORITY: normal_priority
  ```
- To create or modify a `.params` file, write or update the relevant keys as above.

---

## Determining the Job (lsf) ID After CLI Submission

After submitting a job via CLI, you can determine the job's lsf_id (job ID) as follows:

- Use the `fod_get_job_history` tool to search for recent jobs.
- Filter by unique tags, note, owner, or other parameters you provided during submission (e.g., hardware model, duration, etc.).
- Example: To find your job, query for jobs with the same tag and note you used, and within a recent time window (e.g., last 7 days).
- The returned job object will include the `lsf_id` field, which is the unique job identifier for monitoring, log retrieval, and further actions.

**Best Practice:**
- Always include a unique tag or note in your CLI submission for easy identification.
- Refer to the [Job History & Filtering Workflow](fod_history_filtering_workflow.prompt.md) for more details on querying and filtering jobs.

---

## Tips
- If you need to correlate a CLI-submitted job with a Jenkins build, always include a unique tag or note.
- For post-submission analysis, see the [Log & Artifact Retrieval](fod_log_artifact_workflow.prompt.md) and [Job History & Filtering](fod_history_filtering_workflow.prompt.md) workflows.

---

## References
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
- For branch-based job submission, see [Branch Submission Workflow](fod_branch_submission_workflow.prompt.md).
