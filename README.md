## Table of Contents
- [Overview](#overview)
- [Supported Tools](#supported-tools)
- [Installation & Getting Started](#installation--getting-started)
- [Usage](#usage)
- [Prompt Workflows](#prompt-workflows)
- [Tips](#tips)
- [Troubleshooting](#troubleshooting)

## Overview
FoD-Jenkins MCP provides a comprehensive suite of tools to interface AI agents with Fun-on-Demand (FoD) and Jenkins. This includes job submission (CLI and branch-based), live monitoring, log/artifact retrieval, history, resource management, and field discovery.

## Supported Tools

### Fun-on-Demand (FoD) Tools
| Tool Name                        | Description                                         |
|----------------------------------|-----------------------------------------------------|
| `fod_submit_job`                 | Submit a FoD job via CLI with signed binaries and .params file |
| `fod_submit_job_by_branch`       | Submit a FoD job by specifying branches/parameters (no binary required) |
| `fod_get_job`                    | Fetch all details about a FoD job (status, metadata, outputs) |
| `fod_kill_job`                   | Cancel/kill a running FoD job                       |
| `fod_restart_job`                | Restart a FoD job with the same parameters          |
| `fod_archive_job`                | Archive or unarchive a FoD job                      |
| `fod_delete_job`                 | Delete a FoD job                                    |
| `fod_update_job_metadata`        | Update metadata for a FoD job                       |
| `fod_update_job_priority`        | Update priority for a FoD job                       |
| `fod_get_raw_file`               | Fetch raw output/log files for a job                |
| `fod_get_human_file`             | Fetch filtered, human-readable logs for a job       |
| `fod_list_jobs`                  | Query jobs by owner, tags, hardware model, state, etc. |
| `fod_get_job_history`            | Fetch job history with filters                      |
| `fod_get_nightly_history`        | Fetch nightly job history with filters              |
| `fod_get_result_history`         | Fetch grouped/ungrouped job results for regression tracking |
| `fod_create_reservation`         | Reserve lab resources for FoD jobs                  |
| `fod_update_reservation`         | Update a reservation                                |
| `fod_cancel_reservation`         | Cancel a reservation                                |
| `fod_get_reservations`           | List all current reservations                       |
| `fod_get_reservation_by_id`      | Get details for a specific reservation              |
| `fod_get_reservable_resources`   | List reservable resources                           |
| `fod_get_clusters`               | List all clusters                                   |
| `fod_get_machines`               | List all machines                                   |
| `fod_get_cluster_status`         | Get status of a cluster                             |
| `fod_enable_cluster`/`fod_disable_cluster` | Enable/disable a cluster                  |
| `fod_fit_cluster`                | Check if a cluster can fit a job's requirements     |
| `fod_get_machine_status`         | Get status of a machine                             |
| `fod_enable_machine`/`fod_disable_machine` | Enable/disable a machine                  |
| `fod_fit_machine`                | Check if a machine can fit a job's requirements     |
| `fod_get_job_queued_status`      | Get queue state                                     |
| `fod_get_order`                  | Get job order in queue                              |
| `fod_get_robotstate`             | Is FoD accepting jobs?                              |
| `fod_get_wu_trace`               | Fetch WU trace for a job                            |
| `fod_get_function_trace`         | Fetch function trace for a job                      |
| `fod_get_telemetry`              | Fetch telemetry for a job                           |
| `fod_get_core_dump_outputs`      | Fetch core dump outputs for a job                   |
| `fod_get_hbm_memory_dumps`       | Fetch HBM memory dumps for a job                    |
| `fod_get_distinct_values`        | Fetch all unique values for a given job field       |
| `fod_autocomplete`               | Get autocomplete suggestions for a field            |

### Jenkins Tools
| Tool Name                        | Description                                         |
|----------------------------------|-----------------------------------------------------|
| `get_jobs`                       | List all Jenkins jobs                               |
| `get_multiple_job_info`          | Get info for multiple (or a single) Jenkins jobs    |
| `get_multiple_build_info`        | Get info for multiple (or a single) Jenkins builds  |
| `get_build_console_output`       | Windowed/searchable console output for a build      |
| `get_multiple_build_test_report` | Batch test reports for builds                       |
| `get_queue_info`                 | Get Jenkins queue info                              |
| `cancel_queue`                   | Cancel a Jenkins queue item by ID                   |
| `get_plugins`                    | List all Jenkins plugins                            |
| `get_views`                      | List all Jenkins views                              |
| `get_version`                    | Get Jenkins version                                 |
| `get_whoami`                     | Get authenticated Jenkins user info                 |
| `get_executors`                  | Get Jenkins executor status                         |
| `stop_build`                     | Stop a running Jenkins build                        |

## Installation & Getting Started

### Requirements
Create a `requirements.txt` with:
```
fastmcp
python-jenkins
pydantic
python-dotenv
requests
```
Install dependencies:
```
pip install -r requirements.txt
```

### Setup

#### Note: For information on getting GitHub Copilot working with an enterprise account and setting up MCPs, see [Everything AI](https://microsoft.sharepoint.com/:u:/r/teams/FungibleDPU/SitePages/Everything-AI.aspx?csf=1&web=1&e=qnU0iB).

1. Clone the repo and `cd` into it.

3. Set FoD and Jenkins credentials in `.env` or as environment variables:
   ```
   JENKINS_URL=http://jenkins-sw-master.fungible.local/ci
   JENKINS_URL_JOB=http://jenkins-sw-master.fungible.local
   JENKINS_USERNAME=<your-jenkins-user>
   JENKINS_API_TOKEN=<your-api-token>

   FOD_JOB_SERVER=http://palladium-jobs.fungible.local/api
   FOD_USER_COOKIE=<your-email>
   FOD_RUN_F1_PATH=<path-to-the-run_f1.py-script>
   ```

4. Add the MCP. If using VS Code:
   - Open the command palette (with F1 or Ctrl+Shift+P)
   - Type "MCP"
   - You'll be presented with a few options, choose "MCP: Open User Configuration" to open the JSON config file.
   - Add the following snippet under "servers":
  
   ```
   "fod-jenkins": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp/"
   }
     ```

5. Start the server on the command line from your workspace:
   ```
   python3 -m mcp_server --transport streamable-http --port 8000
   ```

6. If on VS Code, click on start just above your MCP configuration or open your extensions pallete (Ctrl+Shift+X) and find `fod-jenkins` under **MCP SERVERS - INSTALLED**. Click on "Start Server":

<img width="700" alt="Screenshot 2025-08-21 033531" src="https://github.com/user-attachments/assets/b7774402-4736-4d19-9849-4aa38c5c8186" />


7. Then, open a new GitHub Copilot window, and click on "Configure Tools." You should see the `fod-jenkins` tool available. Make sure to check it!

<img width="700" alt="image" src="https://github.com/user-attachments/assets/5645b418-7466-46b7-863e-2f7b071d1936" />

## Usage

Enable the MCP and prompt away! Some actions may/will require some hand-holding; be sure to specify exactly what it is you would like your agent to perform so that the appropriate tool is called (e.g. "Submit a FoD job using the binary at `/your-directory` with the following parameters..." or "Find the latest the emulation/zemulation_nightly build on Jenkins that failed and look through the last 1000 lines of the console output for this build to see what went wrong.").

### FoD Workflow Examples (Tools Agents Can Call)

#### Submit a FoD job by branch (no binary required)
```
fod_submit_job_by_branch(RUN_TARGET="F1D1", HW_MODEL="F1D1", BRANCH_FunOS="stable-testdrops1", BOOTARGS="--csr-replay --dpc-server", NOTE="branch-demo", TAGS="nightly")
```

#### Submit a FoD job via CLI
```
fod_submit_job(funos_binary="funos-f1.stripped", params_file="job_8063550.params", hardware_model="F1D1", duration=45, tags="nightly", note="Regression test")
```

#### Monitor a running job
```
fod_get_job(job_id=123456)
```

#### Cancel a running job
```
fod_kill_job(job_id=123456)
```

#### Fetch a log file
```
fod_get_raw_file(job_id=123456, file_name="uartout0.0.txt")
```

#### List jobs by tag and hardware model
```
fod_list_jobs(tags="nightly", hardware_model="F1D1")
```

#### Get distinct hardware models
```
fod_get_distinct_values(field_name="hardware_model")
```

#### Autocomplete tags
```
fod_autocomplete(field_name="tags",query="regress", limit=5)
```

### Jenkins Workflow Examples (Tools Agents Can Call)

#### Get info for multiple Jenkins jobs
```
get_multiple_job_info(job_names=["emulation/fun_on_demand", "emulation/zemulation_nightly"])
```

#### Get info for multiple Jenkins builds
```
get_multiple_build_info(job_build_pairs=[{"job_name": "emulation/fun_on_demand", "build_number": 170456}, {"job_name": "emulation/zemulation_nightly", "build_number": 376258}])
```

#### Get build console output
```
get_build_console_output(job_name="emulation/zemulation_nightly", build_number=376258, mode="tail", num_lines=1000)
```

### Scenarios:

- **Pure FoD Automation:**
  - Prompt agents to use FoD tools for job submission, monitoring, debugging, history, and resource management.
  - Prompt agents to use `fod_get_distinct_values` and `fod_autocomplete` to guide users or agents in selecting valid field values and building queries.
  - Example: Submitting a job, monitoring its status, fetching logs, and analyzing results.

- **Hybrid/Bridged Workflows:**
  - Jenkins tools may be useful if/when you need to correlate FoD jobs with Jenkins builds.
  - Example: Fetching Jenkins build info linked to a FoD job, or tracking test results across both systems.

- **Interactive Guidance:**
  - If unsure about valid options for any FoD field (e.g., hardware_model, tags), prompt the agent to use `fod_get_distinct_values` or `fod_autocomplete` to discover and suggest valid values.

- **Resource Management:**
  - You can use reservation and status tools to avoid contention and optimize resource usage.

## Prompt Workflows

This repository includes a set of prompt workflow files that provide step-by-step guidance for common FoD and Jenkins MCP workflows. These are designed for use with Copilot, LLMs, or any agent that supports prompt-driven automation. Users can to use these prompts as starting points or create their own.

Environments typically allow for prompt file creation. Try documenting your workflow by asking the agent to "save this workflow to a prompt file" after the task is complete and then calling the file for future workflows so the agent knows how to handle it!

### Prompt Files
- `fod_mcp_core.prompt.md`: Core guide for FoD MCP usage and tool categories.
- `fod_branch_submission_workflow.prompt.md`: Branch-based FoD job submission and monitoring.
- `fod_cli_submission_workflow.prompt.md`: CLI-based FoD job submission.
- `fod_jenkins_build_monitoring_workflow.prompt.md`: Jenkins build monitoring for FoD jobs.
- `fod_history_filtering_workflow.prompt.md`: Job history and filtering.
- `fod_log_artifact_workflow.prompt.md`: Log and artifact retrieval.
- `fod_reservation_workflow.prompt.md`: Reservation and resource management.

### How to Use
- Open the prompt file you want to use and tweak the context/steps as necessary.
- Use the prompt as a reference or copy-paste the workflow steps into your Copilot/LLM chat (see [Customize AI responses in VS Code](https://code.visualstudio.com/docs/copilot/copilot-customization) for help with this within GitHub Copilot)
- The agent should follow the step-by-step instructions to perform job submission, monitoring, log retrieval, history filtering, or reservation management.
- Prompts are designed to be modular! Start with the core guide and follow links to workflow-specific prompts as needed.

## Tips
- Use batch tools for efficiency when querying multiple jobs/builds.
- Always use windowed log access for large builds. Additionally, check `total_lines` and `next_window_suggestion` when intending to use the `get_build_console_output` tool to log responses to guide further requests.
- Never echo or log secrets.
- Validate all input/output using the provided schemas.
- Use the `handle` for persistent log chunking and efficient navigation.
- Always use the prompt workflows for complex or multi-step tasks to ensure correct tool usage and maximize automation efficiency.

## Troubleshooting
- **422 Unprocessable Entity:** Ensure your request matches the tool’s schema.
- **Authentication Errors:** Check your `.env` or environment variables for correct Jenkins credentials.
- **Tool Not Found:** Double check that you are calling a registered tool (see [Supported Tools](#supported-tools)).

## Please report any and all issues encountered!
