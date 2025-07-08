## Table of Contents
- [Overview](#overview)
- [Supported Tools](#supported-tools)
- [Installation & Getting Started](#installation--getting-started)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview
Jenkins MCP exposes Jenkins operations as schema-validated tools for AI agents and automation. It supports batch, windowed, and context-aware operations, and is designed for tight integration with Jenkins with Fungible DPU workflows in mind.

## Supported Tools
| Tool Name                        | Description                                         |
|----------------------------------|-----------------------------------------------------|
| `get_job_info`                   | Get info for a single Jenkins job by name           |
| `get_multiple_job_info`          | Get info for multiple Jenkins jobs                  |
| `get_build_info`                 | Get info for a single Jenkins build                 |
| `get_multiple_build_info`        | Get info for multiple Jenkins builds                |
| `get_build_console_output`       | Windowed/searchable console output for a build      |
| `get_multiple_build_console_output` | Batch console output for builds                  |
| `get_build_test_report`          | Get test report for a single build                  |
| `get_multiple_build_test_report` | Batch test reports for builds                       |
| `get_jobs`                       | List all Jenkins jobs                               |
| `get_nodes`                      | List all Jenkins nodes                              |
| `get_node_info`                  | Get info for a single Jenkins node                  |
| `get_queue_info`                 | Get Jenkins queue info                              |
| `cancel_queue`                   | Cancel a Jenkins queue item by ID                   |
| `get_plugins`                    | List all Jenkins plugins                            |
| `get_views`                      | List all Jenkins views                              |
| `get_version`                    | Get Jenkins version                                 |
| `get_whoami`                     | Get authenticated Jenkins user info                 |

## Installation & Getting Started

### Requirements
Create a `requirements.txt` with:
```
fastmcp
python-jenkins
pydantic
python-dotenv
```
Install dependencies:
```
pip install -r requirements.txt
```

### Setup
1. Clone the repo and `cd` into it.
2. Set Jenkins credentials in `.env` or as environment variables:
   ```
   JENKINS_URL=http://jenkins-sw-master.fungible.local/ci/
   JENKINS_USERNAME=your-username
   JENKINS_API_TOKEN=your-password
   ```
3. Start the server:
   ```
   python3 mcp_server.py --transport streamable-http --port 8000
   ```

## Usage

Enable the MCP and prompt away! Some actions may/will require some hand-holding; be sure to specify exactly what it is you would like your agent to perform so that the appropriate tool is called (e.g. "Find the latest the emulation/zemulation_nightly build on Jenkins that failed and look through the last 1000 lines of the console output for this build to see what went wrong."). Some environments/agents allow for prompt file creation—try documenting your workflow by asking the agent to "save this workflow to a prompt file" after the task is complete and then calling the file for future workflows so the agent knows how to handle it!

### The following tools are supported (and still experimental):

#### Get info for a single job
```
get_job_info(job_name="emulation/XXX")
```

#### Get info for multiple jobs
```
get_multiple_job_info(job_names=["emulation/XXX", "emulation/XXX"])
```

#### Get info for a single build
```
get_build_info(job_name="emulation/XXX", build_number=XXX)
```

#### Get info for multiple builds
```
get_multiple_build_info(job_build_pairs=[{"job_name": "emulation/XXX", "build_number": XXXXXX}, {"job_name": "emulation/XXX", "build_number": XXXXXX}])
```

#### Get last X lines of console output for a build
```
get_build_console_output(job_name="emulation/XXX", build_number=XXXXXX, mode="tail", num_lines=XXX)
```

#### Search for "Exception" in console output
```
get_build_console_output(job_name="emulation/XXX", build_number=XXXXXX, search="Exception")
```

#### Get test report for a build
```
get_build_test_report(job_name="emulation/XXX", build_number=XXXXXX)
```

#### Get all jobs
```
get_jobs()
```

#### Get all nodes
```
get_nodes()
```

#### Get info for a node
```
get_node_info(node_name="sw-bld-13")
```

#### Get Jenkins queue info
```
get_queue_info()
```

#### Cancel a queue item
```
cancel_queue(queue_id=XXXXX)
```

#### Get all plugins
```
get_plugins()
```

#### Get all views
```
get_views()
```

#### Get Jenkins version
```
get_version()
```

#### Get authenticated user info
```
get_whoami()
```

### 

## Troubleshooting
- **422 Unprocessable Entity:** Ensure your request matches the tool’s schema.
- **Authentication Errors:** Check your `.env` or environment variables for correct Jenkins credentials.
- **Large Log Handling:** Always use windowed access (`start_line`, `num_lines`, `mode`) for large logs. Do not fetch the entire log at once.
- **Tool Not Found:** Ensure you are calling a registered tool (see Supported Tools).
- **Debugging:** Set `JENKINS_MCP_DEBUG=1` in your environment to enable debug logging.

## Best Practices
- Always use windowed log access for large builds.
- Use batch tools for efficiency when querying multiple jobs/builds.
- Check `total_lines` and `next_window_suggestion` in log responses to guide further requests.
- Never echo or log secrets.
- Validate all input/output using the provided schemas.
- Use the `handle` for persistent log chunking and efficient navigation.

## Security
- Credentials are never returned or echoed.
- All input is validated and sanitized.
- Batch operations are parallelized for efficiency but never leak sensitive data.

## Note: Testing for this MCP is still underway. Please report any and all issues encountered!
