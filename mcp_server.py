from fastmcp import FastMCP
from jenkins_mcp.intent_resolver import resolve_intent
from jenkins_mcp.context_manager import ContextManager
from jenkins_mcp.utils import log_debug, log_info, log_error, normalize_error
from pydantic import BaseModel, Field
from jenkins_mcp.schemas.get_job_info_output_pydantic import GetJobInfoOutput
from jenkins_mcp.schemas.get_build_console_output_input_pydantic import GetBuildConsoleOutputInput
from jenkins_mcp.schemas.get_build_console_output_output_pydantic import GetBuildConsoleOutputOutput
import argparse
import os

# fail fast if credentials are missing!
for var in ["JENKINS_URL", "JENKINS_USERNAME", "JENKINS_API_TOKEN"]:
    if not os.environ.get(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

mcp = FastMCP("Jenkins MCP")
context_manager = ContextManager()

def _ctx(session_id):
    return context_manager.get_context(session_id or "default")

def _update_ctx(session_id, ctx):
    context_manager.update_context(session_id or "default", ctx)

class JobNameModel(BaseModel):
    job_name: str = Field(..., description="Jenkins job name")
    session_id: str = None

class JobNamesModel(BaseModel):
    job_names: list[str] = Field(..., description="List of Jenkins job names")
    session_id: str = None

class BuildInfoModel(BaseModel):
    job_name: str
    build_number: int
    session_id: str = None

class BuildPairsModel(BaseModel):
    job_build_pairs: list[dict] = Field(..., description="List of {job_name, build_number} pairs")
    session_id: str = None

class NodeNameModel(BaseModel):
    node_name: str
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

@mcp.tool(description="Get info for a single Jenkins job by name.")
def get_job_info(params: JobNameModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_job_info", "job_name": params.job_name}, ctx)
        _update_ctx(params.session_id, ctx)
        # Validate output
        return GetJobInfoOutput(**result).dict()
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get job info for {params.job_name}")

@mcp.tool(description="Get info for multiple Jenkins jobs by name.")
def get_multiple_job_info(params: JobNamesModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_multiple_job_info", "job_names": params.job_names}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get multiple job info")

@mcp.tool(description="Get info for a single Jenkins build.")
def get_build_info(params: BuildInfoModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_build_info", "job_name": params.job_name, "build_number": params.build_number}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get build info for {params.job_name} #{params.build_number}")

@mcp.tool(description="Get info for multiple Jenkins builds.")
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
        # forward parameters exactly as received
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

@mcp.tool(description="Get test report for a single Jenkins build.")
def get_build_test_report(params: BuildInfoModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_build_test_report", "job_name": params.job_name, "build_number": params.build_number}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get test report for {params.job_name} #{params.build_number}")

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

@mcp.tool(description="Get all Jenkins nodes.")
def get_nodes(session_id: str = None):
    try:
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_nodes"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get nodes")

@mcp.tool(description="Get info for a single Jenkins node.")
def get_node_info(params: NodeNameModel):
    try:
        ctx = _ctx(params.session_id)
        result = resolve_intent({"operation": "get_node_info", "node_name": params.node_name}, ctx)
        _update_ctx(params.session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to get node info for {params.node_name}")

@mcp.tool(description="Get Jenkins queue info.")
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
        ctx = _ctx(session_id)
        result = resolve_intent({"operation": "get_whoami"}, ctx)
        _update_ctx(session_id, ctx)
        return result
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to get user info")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", type=str, default="stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.transport == "streamable-http":
        mcp.run(transport=args.transport, port=args.port)
    else:
        mcp.run(transport=args.transport)
