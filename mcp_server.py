from fastmcp import FastMCP
from pydantic import BaseModel, Field

from fod_jenkins.intent_resolver import resolve_intent
from fod_jenkins.context_manager import ContextManager
from fod_jenkins.utils import log_debug, log_info, log_error, normalize_error
from fod_jenkins.schemas.get_build_console_output_input_pydantic import GetBuildConsoleOutputInput
from fod_jenkins.schemas.get_build_console_output_output_pydantic import GetBuildConsoleOutputOutput
from fod_jenkins.schemas.copy_job_input_pydantic import CopyJobInput
from fod_jenkins.schemas.copy_job_output_pydantic import CopyJobOutput
from fod_jenkins.schemas.get_executors_output_pydantic import GetExecutorsOutput
from fod_jenkins.schemas.fod_submit_job_input_pydantic import FoDSubmitJobInput
from fod_jenkins.schemas.fod_submit_job_output_pydantic import FoDSubmitJobOutput
from fod_jenkins.schemas.fod_get_job_input_pydantic import FoDGetJobInput
from fod_jenkins.schemas.fod_get_job_output_pydantic import FoDGetJobOutput
from fod_jenkins.schemas.fod_kill_job_input_pydantic import FoDKillJobInput
from fod_jenkins.schemas.fod_kill_job_output_pydantic import FoDKillJobOutput
from fod_jenkins.schemas.fod_list_jobs_input_pydantic import FoDListJobsInput
from fod_jenkins.schemas.fod_list_jobs_output_pydantic import FoDListJobsOutput
from fod_jenkins.schemas.fod_get_raw_file_input_pydantic import FoDGetRawFileInput
from fod_jenkins.schemas.fod_get_raw_file_output_pydantic import FoDGetRawFileOutput
from fod_jenkins.schemas.fod_get_human_file_input_pydantic import FoDGetHumanFileInput
from fod_jenkins.schemas.fod_get_human_file_output_pydantic import FoDGetHumanFileOutput
from fod_jenkins.schemas.fod_get_job_history_input_pydantic import FoDGetJobHistoryInput
from fod_jenkins.schemas.fod_get_job_history_output_pydantic import FoDGetJobHistoryOutput
from fod_jenkins.schemas.fod_get_nightly_history_input_pydantic import FoDGetNightlyHistoryInput
from fod_jenkins.schemas.fod_get_nightly_history_output_pydantic import FoDGetNightlyHistoryOutput
from fod_jenkins.schemas.fod_get_result_history_input_pydantic import FoDGetResultHistoryInput
from fod_jenkins.schemas.fod_get_result_history_output_pydantic import FoDGetResultHistoryOutput
from fod_jenkins.schemas.fod_restart_job_input_pydantic import FoDRestartJobInput
from fod_jenkins.schemas.fod_restart_job_output_pydantic import FoDRestartJobOutput
from fod_jenkins.schemas.fod_archive_job_input_pydantic import FoDArchiveJobInput
from fod_jenkins.schemas.fod_archive_job_output_pydantic import FoDArchiveJobOutput
from fod_jenkins.schemas.fod_delete_job_input_pydantic import FoDDeleteJobInput
from fod_jenkins.schemas.fod_delete_job_output_pydantic import FoDDeleteJobOutput
from fod_jenkins.schemas.fod_update_job_metadata_input_pydantic import FoDUpdateJobMetadataInput
from fod_jenkins.schemas.fod_update_job_metadata_output_pydantic import FoDUpdateJobMetadataOutput
from fod_jenkins.schemas.fod_update_job_priority_input_pydantic import FoDUpdateJobPriorityInput
from fod_jenkins.schemas.fod_update_job_priority_output_pydantic import FoDUpdateJobPriorityOutput
from fod_jenkins.schemas.fod_create_reservation_input_pydantic import FoDCreateReservationInput
from fod_jenkins.schemas.fod_create_reservation_output_pydantic import FoDCreateReservationOutput
from fod_jenkins.schemas.fod_get_wu_trace_input_pydantic import FoDGetWuTraceInput
from fod_jenkins.schemas.fod_get_wu_trace_output_pydantic import FoDGetWuTraceOutput
from fod_jenkins.schemas.fod_get_function_trace_input_pydantic import FoDGetFunctionTraceInput
from fod_jenkins.schemas.fod_get_function_trace_output_pydantic import FoDGetFunctionTraceOutput
from fod_jenkins.schemas.fod_get_telemetry_input_pydantic import FoDGetTelemetryInput
from fod_jenkins.schemas.fod_get_telemetry_output_pydantic import FoDGetTelemetryOutput
from fod_jenkins.schemas.fod_get_core_dump_outputs_input_pydantic import FoDGetCoreDumpOutputsInput
from fod_jenkins.schemas.fod_get_core_dump_outputs_output_pydantic import FoDGetCoreDumpOutputsOutput
from fod_jenkins.schemas.fod_get_hbm_memory_dumps_input_pydantic import FoDGetHbmMemoryDumpsInput
from fod_jenkins.schemas.fod_get_hbm_memory_dumps_output_pydantic import FoDGetHbmMemoryDumpsOutput
from fod_jenkins.schemas.fod_get_clusters_output_pydantic import FoDGetClustersOutput
from fod_jenkins.schemas.fod_get_machines_output_pydantic import FoDGetMachinesOutput
from fod_jenkins.schemas.fod_get_reservations_output_pydantic import FoDGetReservationsOutput
from fod_jenkins.schemas.fod_update_reservation_input_pydantic import FoDUpdateReservationInput
from fod_jenkins.schemas.fod_update_reservation_output_pydantic import FoDUpdateReservationOutput
from fod_jenkins.schemas.fod_cancel_reservation_input_pydantic import FoDCancelReservationInput
from fod_jenkins.schemas.fod_cancel_reservation_output_pydantic import FoDCancelReservationOutput
from fod_jenkins.schemas.fod_get_reservation_by_id_input_pydantic import FoDGetReservationByIdInput
from fod_jenkins.schemas.fod_get_reservation_by_id_output_pydantic import FoDGetReservationByIdOutput
from fod_jenkins.schemas.fod_get_reservable_resources_output_pydantic import FoDGetReservableResourcesOutput
from fod_jenkins.schemas.fod_get_cluster_status_input_pydantic import FoDGetClusterStatusInput
from fod_jenkins.schemas.fod_get_cluster_status_output_pydantic import FoDGetClusterStatusOutput
from fod_jenkins.schemas.fod_get_machine_status_input_pydantic import FoDGetMachineStatusInput
from fod_jenkins.schemas.fod_get_machine_status_output_pydantic import FoDGetMachineStatusOutput
from fod_jenkins.schemas.fod_enable_cluster_input_pydantic import FoDEnableClusterInput
from fod_jenkins.schemas.fod_enable_cluster_output_pydantic import FoDEnableClusterOutput
from fod_jenkins.schemas.fod_disable_cluster_input_pydantic import FoDDisableClusterInput
from fod_jenkins.schemas.fod_disable_cluster_output_pydantic import FoDDisableClusterOutput
from fod_jenkins.schemas.fod_fit_cluster_input_pydantic import FoDFitClusterInput
from fod_jenkins.schemas.fod_fit_cluster_output_pydantic import FoDFitClusterOutput
from fod_jenkins.schemas.fod_fit_machine_input_pydantic import FoDFitMachineInput
from fod_jenkins.schemas.fod_fit_machine_output_pydantic import FoDFitMachineOutput
from fod_jenkins.schemas.fod_enable_machine_input_pydantic import FoDEnableMachineInput
from fod_jenkins.schemas.fod_enable_machine_output_pydantic import FoDEnableMachineOutput
from fod_jenkins.schemas.fod_disable_machine_input_pydantic import FoDDisableMachineInput
from fod_jenkins.schemas.fod_disable_machine_output_pydantic import FoDDisableMachineOutput
from fod_jenkins.schemas.fod_get_job_queued_status_output_pydantic import FoDGetJobQueuedStatusOutput
from fod_jenkins.schemas.fod_get_order_output_pydantic import FoDGetOrderOutput
from fod_jenkins.schemas.fod_get_robotstate_output_pydantic import FoDGetRobotStateOutput
from fod_jenkins.schemas.fod_get_distinct_values_input_pydantic import FoDGetDistinctValuesInput
from fod_jenkins.schemas.fod_get_distinct_values_output_pydantic import FoDGetDistinctValuesOutput
from fod_jenkins.schemas.fod_autocomplete_input_pydantic import FoDAutocompleteInput
from fod_jenkins.schemas.fod_autocomplete_output_pydantic import FoDAutocompleteOutput
from fod_jenkins.schemas.fod_submit_job_by_branch_input_pydantic import FoDSubmitJobByBranchInput
from fod_jenkins.schemas.fod_submit_job_by_branch_output_pydantic import FoDSubmitJobByBranchOutput
from fod_jenkins.schemas.stop_build_input_pydantic import StopBuildInput
from fod_jenkins.schemas.stop_build_output_pydantic import StopBuildOutput
from fod_jenkins import fod_adapter

import argparse
import re
import os
import sys
import json

# fail fast if credentials are missing
for var in ["JENKINS_URL", "JENKINS_USERNAME", "JENKINS_API_TOKEN", "FOD_JOB_SERVER", "FOD_USER_COOKIE"]:
    if not os.environ.get(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

mcp = FastMCP("Jenkins MCP")
context_manager = ContextManager()

def _ctx(session_id):
    return context_manager.get_context(session_id or "default")

def _update_ctx(session_id, ctx):
    context_manager.update_context(session_id or "default", ctx)

class JobNamesModel(BaseModel):
    job_names: list[str] = Field(..., description="List of Jenkins job names")
    session_id: str = None

class BuildPairsModel(BaseModel):
    job_build_pairs: list[dict] = Field(..., description="List of {job_name, build_number} pairs")
    session_id: str = None

class QueueIdModel(BaseModel):
    queue_id: int
    session_id: str = None

class BuildConsoleInputModel(BaseModel):
    job_name: str
    build_number: int
    start_line: int = 0
    num_lines: int = 500
    search: str = None
    handle: str = None
    session_id: str = None
    mode: str = None

@mcp.tool(description="Get info for multiple (or a single) Jenkins jobs by name.")
def get_multiple_job_info(params: JobNamesModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_multiple_job_info", "job_names": params.job_names}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get multiple job info")

@mcp.tool(description="Get info for multiple (or a single) Jenkins builds. Use with Jenkins build number(s) (after builds leaves the queue).")
def get_multiple_build_info(params: BuildPairsModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_multiple_build_info", "job_build_pairs": params.job_build_pairs}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get multiple build info")

@mcp.tool(description="Get a window or search results from the console output for a Jenkins build. Use start_line/num_lines for paging, or search for pattern matching. Use 'handle' for persistent chunking. Use mode='tail' for last N lines.")
def get_build_console_output(params: BuildConsoleInputModel):
    try:
        log_debug(f"get_build_console_output called with: job_name={params.job_name}, build_number={params.build_number}, start_line={params.start_line}, num_lines={params.num_lines}, search={params.search}, handle={params.handle}, session_id={params.session_id}, mode={params.mode}")
        ctx = _ctx(params.session_id)
        # forward all parameters exactly as received
        result = resolve_intent({
            "operation": "get_build_console_output",
            "job_name": params.job_name,
            "build_number": params.build_number,
            "start_line": params.start_line,
            "num_lines": params.num_lines,
            "search": params.search,
            "handle": params.handle,
            "session_id": params.session_id,
            "mode": params.mode
        }, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get console output for {params.job_name} #{params.build_number}")

@mcp.tool(description="Get test reports for multiple Jenkins builds.")
def get_multiple_build_test_report(params: BuildPairsModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_multiple_build_test_report", "job_build_pairs": params.job_build_pairs}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get multiple build test reports")

@mcp.tool(description="Get all Jenkins jobs.")
def get_jobs(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_jobs"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get jobs")

@mcp.tool(description="Get Jenkins queue info. Use when you want to check the Jenkins queue and/or find the queue number.")
def get_queue_info(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_queue_info"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get queue info")

@mcp.tool(description="Cancel a Jenkins queue item by ID.")
def cancel_queue(params: QueueIdModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "cancel_queue", "queue_id": params.queue_id}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to cancel queue item {params.queue_id}")

@mcp.tool(description="Get all Jenkins plugins.")
def get_plugins(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_plugins"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get plugins")

@mcp.tool(description="Get all Jenkins views.")
def get_views(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_views"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get views")

@mcp.tool(description="Get Jenkins version.")
def get_version(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_version"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get version")

@mcp.tool(description="Get authenticated Jenkins user info.")
def get_whoami(session_id: str = None):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_whoami"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get user info")

@mcp.tool(description="Get Jenkins executor status.")
def get_executors(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_executors", "session_id": session_id}, ctx)
        _update_ctx(session_id, ctx)
        return GetExecutorsOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get Jenkins executors")

@mcp.tool(description="Submit a Fun-on-Demand job via CLI (run_f1.py).")
def fod_submit_job(params: FoDSubmitJobInput):
    try:
        result = fod_adapter.fod_submit_job(
            funos_binary=params.funos_binary,
            blobs=params.blobs,
            hardware_model=params.hardware_model,
            duration=params.duration,
            tags=params.tags,
            note=params.note,
            params_file=params.params_file,
            extra_args=params.extra_args
        )
        return FoDSubmitJobOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to submit FoD job via CLI.")

@mcp.tool(description="Get details for a Fun-on-Demand job by lsf_id (actual job ID). This should be used with Fun-on-Demand lsf_id (after job is running on Fun-on-Demand).")
def fod_get_job(params: FoDGetJobInput):
    try:
        result = fod_adapter.fod_get_job(params.job_id)
        return FoDGetJobOutput(job=result, summary="Fetched job details.")
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get FoD job {params.job_id}.")

@mcp.tool(description="Kill/cancel a running Fun-on-Demand job by lsf_id.")
def fod_kill_job(params: FoDKillJobInput):
    try:
        result = fod_adapter.fod_kill_job(params.job_id)
        return FoDKillJobOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to kill FoD job {params.job_id}.")

@mcp.tool(description="List Fun-on-Demand jobs with filtering and pagination.")
def fod_list_jobs(params: FoDListJobsInput):
    try:
        result = fod_adapter.fod_list_jobs(
            owner=params.owner,
            tags=params.tags,
            state=params.state,
            hardware_model=params.hardware_model,
            page=params.page,
            per_page=params.per_page,
            sort=params.sort,
            session_id=params.session_id
        )
        return FoDListJobsOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to list FoD jobs.")

@mcp.tool(description="Fetch a raw output/log file for a Fun-on-Demand job.")
def fod_get_raw_file(params: FoDGetRawFileInput):
    try:
        result = fod_adapter.fod_get_raw_file(params.job_id, params.file_name, params.session_id)
        return FoDGetRawFileOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch raw file {params.file_name} for job {params.job_id}.")

@mcp.tool(description="Fetch a human-readable (HTML) log file for a Fun-on-Demand job.")
def fod_get_human_file(params: FoDGetHumanFileInput):
    try:
        result = fod_adapter.fod_get_human_file(params.job_id, params.file_name, params.filter_level, params.session_id)
        return FoDGetHumanFileOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch human file {params.file_name} for job {params.job_id}.")

@mcp.tool(description="Fetch Fun-on-Demand job history with filters.")
def fod_get_job_history(params: FoDGetJobHistoryInput):
    try:
        result = fod_adapter.fod_get_job_history(
            days=params.days,
            tags=params.tags,
            owner=params.owner,
            state=params.state,
            sort=params.sort,
            session_id=params.session_id
        )
        return FoDGetJobHistoryOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch FoD job history.")

@mcp.tool(description="Fetch Fun-on-Demand nightly job history with filters.")
def fod_get_nightly_history(params: FoDGetNightlyHistoryInput):
    try:
        result = fod_adapter.fod_get_nightly_history(
            days=params.days,
            tags=params.tags,
            owner=params.owner,
            state=params.state,
            sort=params.sort,
            session_id=params.session_id
        )
        return FoDGetNightlyHistoryOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch FoD nightly job history.")

@mcp.tool(description="Fetch Fun-on-Demand result history with filters.")
def fod_get_result_history(params: FoDGetResultHistoryInput):
    try:
        result = fod_adapter.fod_get_result_history(
            days=params.days,
            tags=params.tags,
            owner=params.owner,
            state=params.state,
            sort=params.sort,
            disable_grouping=params.disable_grouping,
            session_id=params.session_id
        )
        return FoDGetResultHistoryOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch FoD result history.")

@mcp.tool(description="Restart a Fun-on-Demand job by lsf_id.")
def fod_restart_job(params: FoDRestartJobInput):
    try:
        result = fod_adapter.fod_restart_job(params.job_id, params.session_id)
        return FoDRestartJobOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to restart FoD job {params.job_id}.")

@mcp.tool(description="Archive or unarchive a Fun-on-Demand job by lsf_id.")
def fod_archive_job(params: FoDArchiveJobInput):
    try:
        result = fod_adapter.fod_archive_job(params.job_id, params.archive, params.days, params.session_id)
        return FoDArchiveJobOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to {'archive' if params.archive else 'unarchive'} FoD job {params.job_id}.")

@mcp.tool(description="Delete a Fun-on-Demand job by lsf_id.")
def fod_delete_job(params: FoDDeleteJobInput):
    try:
        result = fod_adapter.fod_delete_job(params.job_id, params.session_id)
        return FoDDeleteJobOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to delete FoD job {params.job_id}.")

@mcp.tool(description="Update metadata for a Fun-on-Demand job by lsf_id.")
def fod_update_job_metadata(params: FoDUpdateJobMetadataInput):
    try:
        result = fod_adapter.fod_update_job_metadata(params.job_id, params.metadata, params.session_id)
        return FoDUpdateJobMetadataOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update metadata for FoD job {params.job_id}.")

@mcp.tool(description="Update priority for a Fun-on-Demand job by lsf_id.")
def fod_update_job_priority(params: FoDUpdateJobPriorityInput):
    try:
        result = fod_adapter.fod_update_job_priority(params.job_id, params.priority, params.session_id)
        return FoDUpdateJobPriorityOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update priority for FoD job {params.job_id}.")

@mcp.tool(description="Create a Fun-on-Demand resource reservation.")
def fod_create_reservation(params: FoDCreateReservationInput):
    try:
        result = fod_adapter.fod_create_reservation(params.owner, params.resource, params.start_time, params.end_time, params.session_id)
        return FoDCreateReservationOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to create FoD reservation.")

@mcp.tool(description="Fetch WU trace for a Fun-on-Demand job by lsf_id.")
def fod_get_wu_trace(params: FoDGetWuTraceInput):
    try:
        result = fod_adapter.fod_get_wu_trace(params.job_id, params.session_id)
        return FoDGetWuTraceOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch WU trace for FoD job {params.job_id}.")

@mcp.tool(description="Fetch function trace for a Fun-on-Demand job by lsf_id.")
def fod_get_function_trace(params: FoDGetFunctionTraceInput):
    try:
        result = fod_adapter.fod_get_function_trace(params.job_id, params.session_id)
        return FoDGetFunctionTraceOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch function trace for FoD job {params.job_id}.")

@mcp.tool(description="Fetch telemetry data for a Fun-on-Demand job by lsf_id.")
def fod_get_telemetry(params: FoDGetTelemetryInput):
    try:
        result = fod_adapter.fod_get_telemetry(params.job_id, params.vars, params.session_id)
        return FoDGetTelemetryOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch telemetry for FoD job {params.job_id}.")

@mcp.tool(description="Fetch core dump outputs for a Fun-on-Demand job by lsf_id.")
def fod_get_core_dump_outputs(params: FoDGetCoreDumpOutputsInput):
    try:
        result = fod_adapter.fod_get_core_dump_outputs(params.job_id, params.session_id)
        return FoDGetCoreDumpOutputsOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch core dump outputs for FoD job {params.job_id}.")

@mcp.tool(description="Fetch HBM memory dumps for a Fun-on-Demand job by lsf_id.")
def fod_get_hbm_memory_dumps(params: FoDGetHbmMemoryDumpsInput):
    try:
        result = fod_adapter.fod_get_hbm_memory_dumps(params.job_id, params.session_id)
        return FoDGetHbmMemoryDumpsOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch HBM memory dumps for FoD job {params.job_id}.")

@mcp.tool(description="Fetch list of clusters from Fun-on-Demand cluster manager.")
def fod_get_clusters(session_id: str = None):
    try:
        result = fod_adapter.fod_get_clusters(session_id)
        return FoDGetClustersOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch clusters.")

@mcp.tool(description="Fetch list of machines from Fun-on-Demand machine manager.")
def fod_get_machines(session_id: str = None):
    try:
        result = fod_adapter.fod_get_machines(session_id)
        return FoDGetMachinesOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch machines.")

@mcp.tool(description="Fetch list of reservations from Fun-on-Demand.")
def fod_get_reservations(session_id: str = None):
    try:
        result = fod_adapter.fod_get_reservations(session_id)
        return FoDGetReservationsOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch reservations.")

@mcp.tool(description="Update a Fun-on-Demand reservation by reservation_id.")
def fod_update_reservation(params: FoDUpdateReservationInput):
    try:
        result = fod_adapter.fod_update_reservation(params.reservation_id, params.owner, params.resource, params.start_time, params.end_time, params.session_id)
        return FoDUpdateReservationOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update FoD reservation {params.reservation_id}.")

@mcp.tool(description="Cancel a Fun-on-Demand reservation by reservation_id.")
def fod_cancel_reservation(params: FoDCancelReservationInput):
    try:
        result = fod_adapter.fod_cancel_reservation(params.reservation_id, params.session_id)
        return FoDCancelReservationOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to cancel FoD reservation {params.reservation_id}.")

@mcp.tool(description="Fetch a Fun-on-Demand reservation by reservation_id.")
def fod_get_reservation_by_id(params: FoDGetReservationByIdInput):
    try:
        result = fod_adapter.fod_get_reservation_by_id(params.reservation_id, params.session_id)
        return FoDGetReservationByIdOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch FoD reservation {params.reservation_id}.")

@mcp.tool(description="Fetch list of reservable resources from Fun-on-Demand.")
def fod_get_reservable_resources(session_id: str = None):
    try:
        result = fod_adapter.fod_get_reservable_resources(session_id)
        return FoDGetReservableResourcesOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch reservable resources.")

@mcp.tool(description="Fetch status for a Fun-on-Demand cluster by cluster_id.")
def fod_get_cluster_status(params: FoDGetClusterStatusInput):
    try:
        result = fod_adapter.fod_get_cluster_status(params.cluster_id, params.session_id)
        return FoDGetClusterStatusOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch status for cluster {params.cluster_id}.")

@mcp.tool(description="Fetch status for a Fun-on-Demand machine by machine_id.")
def fod_get_machine_status(params: FoDGetMachineStatusInput):
    try:
        result = fod_adapter.fod_get_machine_status(params.machine_id, params.session_id)
        return FoDGetMachineStatusOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch status for machine {params.machine_id}.")

@mcp.tool(description="Enable a Fun-on-Demand cluster by cluster_id.")
def fod_enable_cluster(params: FoDEnableClusterInput):
    try:
        result = fod_adapter.fod_enable_cluster(params.cluster_id, params.session_id)
        return FoDEnableClusterOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to enable cluster {params.cluster_id}.")

@mcp.tool(description="Disable a Fun-on-Demand cluster by cluster_id.")
def fod_disable_cluster(params: FoDDisableClusterInput):
    try:
        result = fod_adapter.fod_disable_cluster(params.cluster_id, params.session_id)
        return FoDDisableClusterOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to disable cluster {params.cluster_id}.")

@mcp.tool(description="Fit a Fun-on-Demand cluster for job requirements.")
def fod_fit_cluster(params: FoDFitClusterInput):
    try:
        result = fod_adapter.fod_fit_cluster(params.cluster_id, params.job_requirements, params.session_id)
        return FoDFitClusterOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fit cluster {params.cluster_id}.")

@mcp.tool(description="Fit a Fun-on-Demand machine for job requirements.")
def fod_fit_machine(params: FoDFitMachineInput):
    try:
        result = fod_adapter.fod_fit_machine(params.machine_id, params.job_requirements, params.session_id)
        return FoDFitMachineOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fit machine {params.machine_id}.")

@mcp.tool(description="Enable a Fun-on-Demand machine by machine_id.")
def fod_enable_machine(params: FoDEnableMachineInput):
    try:
        result = fod_adapter.fod_enable_machine(params.machine_id, params.session_id)
        return FoDEnableMachineOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to enable machine {params.machine_id}.")


@mcp.tool(description="Disable a Fun-on-Demand machine by machine_id.")
def fod_disable_machine(params: FoDDisableMachineInput):
    try:
        result = fod_adapter.fod_disable_machine(params.machine_id, params.session_id)
        return FoDDisableMachineOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to disable machine {params.machine_id}.")

@mcp.tool(description="Fetch Fun-on-Demand job queue state.")
def fod_get_job_queued_status(session_id: str = None):
    try:
        result = fod_adapter.fod_get_job_queued_status(session_id)
        return FoDGetJobQueuedStatusOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch job queue status.")

@mcp.tool(description="Fetch Fun-on-Demand job order in queue.")
def fod_get_order(session_id: str = None):
    try:
        result = fod_adapter.fod_get_order(session_id)
        return FoDGetOrderOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch job order in queue.")

@mcp.tool(description="Fetch Fun-on-Demand robot state (is FoD accepting jobs).")
def fod_get_robotstate(session_id: str = None):
    try:
        result = fod_adapter.fod_get_robotstate(session_id)
        return FoDGetRobotStateOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch robot state.")

@mcp.tool(description="Fetch distinct values for a field from Fun-on-Demand jobs.")
def fod_get_distinct_values(params: FoDGetDistinctValuesInput):
    try:
        result = fod_adapter.fod_get_distinct_values(params.field_name, params.session_id)
        return FoDGetDistinctValuesOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch distinct values for field {params.field_name}.")

@mcp.tool(description="Fetch autocomplete suggestions for a field from Fun-on-Demand jobs.")
def fod_autocomplete(params: FoDAutocompleteInput):
    try:
        result = fod_adapter.fod_autocomplete(params.field_name, params.q, params.limit, params.session_id)
        return FoDAutocompleteOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch autocomplete for field {params.field_name}.")

@mcp.tool(description="Submit a Fun-on-Demand job by specifying branches and parameters (no binary required). Mimics the Jenkins launch web UI.")
def fod_submit_job_by_branch(params: FoDSubmitJobByBranchInput):
    try:
        result = fod_adapter.fod_submit_job_by_branch(**params.dict(exclude_none=True))
        return FoDSubmitJobByBranchOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to submit branch-only FoD job.")

@mcp.tool(description="Stop a running Jenkins build.")
def stop_build(params: StopBuildInput) -> StopBuildOutput:
    ctx = _ctx(params.session_id)
    result = resolve_intent({
        "operation": "stop_build",
        "job_name": params.job_name,
        "build_number": params.build_number
    }, ctx)
    if result.get("error"):
        return StopBuildOutput(success=False, summary=result.get("summary", "Failed to stop build."), error=result["error"])
    return StopBuildOutput(success=True, summary=result.get("summary", "Build stopped successfully."))

def run_stdio_server():
    """
    Production-ready stdio server loop for MCP (JSON-RPC 2.0, Content-Length headers).
    """
    content_length_re = re.compile(r"Content-Length: (\d+)")
    while True:
        # Read headers
        headers = ""
        while True:
            line = sys.stdin.readline()
            if not line or line in ("\r\n", "\n"):
                break
            headers += line
        match = content_length_re.search(headers)
        if not match:
            continue
        content_length = int(match.group(1))
        # Read the JSON body
        body = sys.stdin.read(content_length)
        try:
            request = json.loads(body)
            method = request.get("method")
            params = request.get("params", {})
            id_ = request.get("id")
            if not hasattr(mcp, method):
                response = {
                    "jsonrpc": "2.0",
                    "id": id_,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}
                }
            else:
                tool = getattr(mcp, method)
                result = tool(params)
                response = {"jsonrpc": "2.0", "id": id_, "result": result}
        except Exception as e:
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
        response_bytes = json.dumps(response).encode("utf-8")
        sys.stdout.write(f"Content-Length: {len(response_bytes)}\r\n\r\n")
        sys.stdout.write(response_bytes.decode("utf-8"))
        sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", type=str, default="stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.transport == "streamable-http":
        mcp.run(transport=args.transport, port=args.port)
    elif args.transport == "stdio":
        run_stdio_server()
    else:
        raise RuntimeError(f"Unsupported transport: {args.transport}")
