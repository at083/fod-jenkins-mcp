---
mode: 'agent'
description: 'Jenkins build monitoring workflow for FoD jobs'
---
# Jenkins Build Monitoring Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to monitor Jenkins builds for FoD jobs, especially when the build number is unknown. For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Monitoring Jenkins Builds When Build Number is Unknown

- After submitting a job (e.g., with `fod_submit_by_branch`), you may not know the Jenkins build number.
- To monitor the build:
  1. Use `get_multiple_job_info(job_names=["emulation/fun_on_demand"]) to retrieve a list of recent builds and their corresponding build numbers.
  2. Then determine the three most recent builds by calling `get_multiple_build_info(job_build_pairs=[{"job_name": "emulation/fun_on_demand", "build_number": <most recent build's number>}, {"job_name": "emulation/zemulation_nightly", "build_number": <second most recent build's number>}, {"job_name": "emulation/zemulation_nightly", "build_number": <third most recent build's number>}])`.
  3. Examine the build parameters or timestamps to identify the correct build (e.g., by matching tags, notes, or submission time).
  4. Once the correct build is identified, continue monitoring it with `get_multiple_build_info` until it completes.
  5. After the build is finished, proceed to find the corresponding FoD job using `fod_list_jobs` as described in the branch submission workflow.

**Best Practice:**
- Always include a unique tag or note in your submission to make it easier to identify your build among recent jobs.
- If you are unsure which build is yours, check all three most recent builds for matching parameters.

---

## Notes
- Build parameters may not be visible in all Jenkins setups; if so, use tags/notes and timestamps for correlation.
- Advanced: You may also poll the Jenkins queue item API for parameter details if available.

---

## References
- For branch-based job submission, see [Branch Submission Workflow](fod_branch_submission_workflow.prompt.md).
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
