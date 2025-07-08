from jenkins_mcp.jenkins_adapter import (
    get_jobs, get_job_info, build_job, get_build_info, get_build_console_output, stop_build,
    get_queue_info, cancel_queue, get_nodes, get_node_info, get_plugins, get_views, get_version, get_whoami,
    get_multiple_job_info, get_multiple_build_info, get_multiple_build_console_output, get_build_test_report, get_multiple_build_test_report
)
from jenkins_mcp.utils import log_debug

# intent resolver (expandable for more intents)
def resolve_intent(intent: dict, context: dict = None):
    op = intent.get("operation")
    if op == "get_jobs":
        return get_jobs()
    if op == "get_job_info":
        return get_job_info(intent.get("job_name"))
    if op == "get_multiple_job_info":
        return get_multiple_job_info(intent.get("job_names"))
    if op == "build_job":
        return build_job(intent.get("job_name"), intent.get("parameters"))
    if op == "get_build_info":
        return get_build_info(intent.get("job_name"), intent.get("build_number"))
    if op == "get_multiple_build_info":
        return get_multiple_build_info(intent.get("job_build_pairs"))
    if op == "get_build_console_output":
        log_debug(f"Intent resolver forwarding: {intent}")
        return get_build_console_output(
            job_name=intent.get("job_name"),
            build_number=intent.get("build_number"),
            start_line=intent.get("start_line"),
            num_lines=intent.get("num_lines"),
            search=intent.get("search"),
            handle=intent.get("handle"),
            session_id=intent.get("session_id"),
            mode=intent.get("mode")
        )
    if op == "get_multiple_build_console_output":
        return get_multiple_build_console_output(intent.get("job_build_pairs"))
    if op == "get_build_test_report":
        return get_build_test_report(intent.get("job_name"), intent.get("build_number"))
    if op == "get_multiple_build_test_report":
        return get_multiple_build_test_report(intent.get("job_build_pairs"))
    if op == "stop_build":
        return stop_build(intent.get("job_name"), intent.get("build_number"))
    if op == "get_queue_info":
        return get_queue_info()
    if op == "cancel_queue":
        return cancel_queue(intent.get("queue_id"))
    if op == "get_nodes":
        return get_nodes()
    if op == "get_node_info":
        return get_node_info(intent.get("node_name"))
    if op == "get_plugins":
        return get_plugins()
    if op == "get_views":
        return get_views()
    if op == "get_version":
        return get_version()
    if op == "get_whoami":
        return get_whoami()
    return {"error": {"code": "unsupported_intent", "message": f"Operation '{op}' not supported."}, "summary": "Unsupported operation."}
