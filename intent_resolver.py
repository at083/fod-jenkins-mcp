from fod_jenkins.jenkins_adapter import (
    get_jobs, get_build_console_output, stop_build,
    get_queue_info, cancel_queue, get_plugins, get_version, get_whoami,
    get_multiple_job_info, get_multiple_build_info, get_multiple_build_test_report,
    get_executors,
)

from fod_jenkins.fod_adapter import (
    fod_submit_job, fod_get_job, fod_kill_job, fod_list_jobs, fod_get_raw_file,
    fod_get_human_file, fod_get_job_history, fod_get_nightly_history, fod_get_result_history,
    fod_restart_job, fod_archive_job, fod_delete_job, fod_update_job_metadata,
    fod_update_job_priority, fod_create_reservation, fod_cancel_reservation,
    fod_get_reservation_by_id, fod_get_reservable_resources, fod_get_cluster_status,
    fod_get_machine_status
)

from fod_jenkins.utils import log_debug

# intent resolvers
def resolve_intent(intent: dict, context: dict = None):
    op = intent.get("operation")
    if op == "get_jobs":
        return get_jobs()
    if op == "get_multiple_job_info":
        return get_multiple_job_info(intent.get("job_names"))
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
    if op == "get_multiple_build_test_report":
        return get_multiple_build_test_report(intent.get("job_build_pairs"))
    if op == "stop_build":
        return stop_build(intent.get("job_name"), intent.get("build_number"))
    if op == "get_queue_info":
        return get_queue_info()
    if op == "cancel_queue":
        return cancel_queue(intent.get("queue_id"))
    if op == "get_plugins":
        return get_plugins()
    if op == "get_version":
        return get_version()
    if op == "get_whoami":
        return get_whoami()
    if op == "get_executors":
        return get_executors(intent.get("session_id"))
    if op == "fod_submit_job":
        return fod_submit_job(
            intent.get("funos_binary"),
            intent.get("blobs"),
            intent.get("hardware_model"),
            intent.get("duration"),
            intent.get("tags"),
            intent.get("note"),
            intent.get("params_file"),
            intent.get("extra_args")
        )
    if op == "fod_get_job":
        return fod_get_job(intent.get("job_id"))
    if op == "fod_kill_job":
        return fod_kill_job(intent.get("job_id"))
    if op == "fod_list_jobs":
        return fod_list_jobs(
            intent.get("owner"),
            intent.get("tags"),
            intent.get("state"),
            intent.get("hardware_model"),
            intent.get("page"),
            intent.get("per_page"),
            intent.get("sort"),
            intent.get("session_id")
        )
    if op == "fod_get_raw_file":
        return fod_get_raw_file(intent.get("job_id"), intent.get("file_name"), intent.get("session_id"))
    if op == "fod_get_human_file":
        return fod_get_human_file(intent.get("job_id"), intent.get("file_name"), intent.get("filter_level"), intent.get("session_id"))
    if op == "fod_get_job_history":
        return fod_get_job_history(
            intent.get("days"),
            intent.get("tags"),
            intent.get("owner"),
            intent.get("state"),
            intent.get("sort"),
            intent.get("session_id")
        )
    if op == "fod_get_nightly_history":
        return fod_get_nightly_history(
            intent.get("days"),
            intent.get("tags"),
            intent.get("owner"),
            intent.get("state"),
            intent.get("sort"),
            intent.get("session_id")
        )
    if op == "fod_get_result_history":
        return fod_get_result_history(
            intent.get("days"),
            intent.get("tags"),
            intent.get("owner"),
            intent.get("state"),
            intent.get("sort"),
            intent.get("disable_grouping"),
            intent.get("session_id")
        )
    if op == "fod_restart_job":
        return fod_restart_job(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_archive_job":
        return fod_archive_job(
            intent.get("job_id"),
            intent.get("archive"),
            intent.get("days"),
            intent.get("session_id")
        )
    if op == "fod_delete_job":
        return fod_delete_job(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_update_job_metadata":
        return fod_update_job_metadata(intent.get("job_id"), intent.get("metadata"), intent.get("session_id"))
    if op == "fod_update_job_priority":
        return fod_update_job_priority(intent.get("job_id"), intent.get("priority"), intent.get("session_id"))
    if op == "fod_create_reservation":
        return fod_create_reservation(
            intent.get("owner"),
            intent.get("resource"),
            intent.get("start_time"),
            intent.get("end_time"),
            intent.get("session_id")
        )
    if op == "fod_update_reservation":
        return fod_update_reservation(
            intent.get("reservation_id"),
            intent.get("owner"),
            intent.get("resource"),
            intent.get("start_time"),
            intent.get("end_time"),
            intent.get("session_id")
        )
    if op == "fod_cancel_reservation":
        return fod_cancel_reservation(intent.get("reservation_id"), intent.get("session_id"))
    if op == "fod_get_wu_trace":
        return fod_get_wu_trace(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_get_function_trace":
        return fod_get_function_trace(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_get_telemetry":
        return fod_get_telemetry(intent.get("job_id"), intent.get("vars"), intent.get("session_id"))
    if op == "fod_get_core_dump_outputs":
        return fod_get_core_dump_outputs(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_get_hbm_memory_dumps":
        return fod_get_hbm_memory_dumps(intent.get("job_id"), intent.get("session_id"))
    if op == "fod_get_clusters":
        return fod_get_clusters(intent.get("session_id"))
    if op == "fod_get_machines":
        return fod_get_machines(intent.get("session_id"))
    if op == "fod_get_reservations":
        return fod_get_reservations(intent.get("session_id"))
    if op == "fod_get_reservation_by_id":
        return fod_get_reservation_by_id(intent.get("reservation_id"), intent.get("session_id"))
    if op == "fod_get_reservable_resources":
        return fod_get_reservable_resources(intent.get("session_id"))
    if op == "fod_get_cluster_status":
        return fod_get_cluster_status(intent.get("cluster_id"), intent.get("session_id"))
    if op == "fod_get_machine_status":
        return fod_get_machine_status(intent.get("machine_id"), intent.get("session_id"))
    if op == "fod_enable_cluster":
        return fod_enable_cluster(intent.get("cluster_id"), intent.get("session_id"))
    if op == "fod_disable_cluster":
        return fod_disable_cluster(intent.get("cluster_id"), intent.get("session_id"))
    if op == "fod_fit_cluster":
        return fod_fit_cluster(intent.get("cluster_id"), intent.get("job_requirements"), intent.get("session_id"))
    if op == "fod_enable_machine":
        return fod_enable_machine(intent.get("machine_id"), intent.get("session_id"))
    if op == "fod_disable_machine":
        return fod_disable_machine(intent.get("machine_id"), intent.get("session_id"))
    if op == "fod_fit_machine":
        return fod_fit_machine(intent.get("machine_id"), intent.get("job_requirements"), intent.get("session_id"))
    if op == "fod_get_job_queued_status":
        return fod_get_job_queued_status(intent.get("session_id"))
    if op == "fod_get_order":
        return fod_get_order(intent.get("session_id"))
    if op == "fod_get_robotstate":
        return fod_get_robotstate(intent.get("session_id"))
    if op == "fod_get_distinct_values":
        return fod_get_distinct_values(intent.get("field_name"), intent.get("session_id"))
    if op == "fod_autocomplete":
        return fod_autocomplete(
            intent.get("field_name"),
            intent.get("q"),
            intent.get("limit"),
            intent.get("session_id")
        )
    if op == "fod_submit_job_by_branch":
        return fod_submit_job_by_branch(**{k: v for k, v in intent.items() if k != "operation"})
    return {"error": {"code": "unsupported_intent", "message": f"Operation '{op}' not supported."}, "summary": "Unsupported operation."}
