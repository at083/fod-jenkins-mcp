---
mode: 'agent'
description: 'Reservation and resource management workflow for FoD jobs'
---
# Reservation & Resource Management Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to manage reservations and resources for FoD jobs using MCP tools. For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Managing Reservations

- **Create Reservation:**
  - Use `fod_create_reservation(owner, resource, start_time, end_time)` to reserve lab resources for a specific time window.
  - Parameters:
    - `owner`: Reservation owner (email)
    - `resource`: Resource to reserve (e.g., machine or cluster name)
    - `start_time`, `end_time`: Reservation window (ISO8601 format)

- **Update Reservation:**
  - Use `fod_update_reservation(reservation_id, owner, resource, start_time, end_time)` to modify an existing reservation.

- **Cancel Reservation:**
  - Use `fod_cancel_reservation(reservation_id)` to cancel an existing reservation.

- **List Reservations:**
  - Use `fod_get_reservations()` to view all current reservations.
  - Use `fod_get_reservation_by_id(reservation_id)` to get details for a specific reservation.

- **List Reservable Resources:**
  - Use `fod_get_reservable_resources()` to see which resources can be reserved.

---

## Resource Status

- **Cluster Status:**
  - Use `fod_get_cluster_status(cluster_id)` to check the status of a cluster.
  - Use `fod_enable_cluster(cluster_id)` or `fod_disable_cluster(cluster_id)` to enable/disable a cluster.

- **Machine Status:**
  - Use `fod_get_machine_status(machine_id)` to check the status of a machine.
  - Use `fod_enable_machine(machine_id)` or `fod_disable_machine(machine_id)` to enable/disable a machine.

- **Fit/Capacity Checks:**
  - Use `fod_fit_cluster(cluster_id, job_requirements)` or `fod_fit_machine(machine_id, job_requirements)` to check if a job can fit on a resource.

---

## Best Practices
- Always check and manage reservations before submitting jobs to ensure resource access and avoid contention.
- Use resource status tools to optimize lab usage and troubleshoot resource issues.

---

## Tips
- If a job fails to start due to resource contention, check current reservations and resource status.
- For how to specify a reservation when submitting a job, see the job submission workflows ([Branch Submission Workflow](fod_branch_submission_workflow.prompt.md), [CLI Submission Workflow](fod_cli_submission_workflow.prompt.md)).

---

## References
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
- For job submission workflows, see [Branch Submission Workflow](fod_branch_submission_workflow.prompt.md) and [CLI Submission Workflow](fod_cli_submission_workflow.prompt.md).
