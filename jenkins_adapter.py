import os
import jenkins
import concurrent.futures
import dotenv
import threading
import time

# load environment vars from
dotenv.load_dotenv(dotenv.find_dotenv())

JENKINS_URL = os.environ["JENKINS_URL"]
JENKINS_USERNAME = os.environ["JENKINS_USERNAME"]
JENKINS_API_TOKEN = os.environ["JENKINS_API_TOKEN"]

# this initializes Jenkins connection (it's a single instance for all operations)
server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_API_TOKEN)

# in-memory cache for logs: {(session_id, job_name, build_number): (timestamp, lines)}
_console_log_cache = {}
_console_log_cache_lock = threading.Lock()
_CONSOLE_LOG_CACHE_TTL = 600  # seconds

def _get_log_handle(session_id, job_name, build_number):
    return (session_id or "default", job_name, build_number)

def _cleanup_console_log_cache():
    now = time.time()
    with _console_log_cache_lock:
        expired = [k for k, (ts, _) in _console_log_cache.items() if now - ts > _CONSOLE_LOG_CACHE_TTL]
        for k in expired:
            del _console_log_cache[k]

# adapter methods
def get_jobs():
    try:
        jobs = server.get_jobs()
        return {"jobs": jobs, "summary": "Fetched all jobs."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch jobs."}

def get_job_info(job_name):
    try:
        info = server.get_job_info(job_name)
        return {"job": info, "summary": f"Fetched info for job '{job_name}'."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to fetch job info for '{job_name}'."}

def get_build_info(job_name, build_number):
    try:
        info = server.get_build_info(job_name, build_number)
        return {"build": info, "summary": f"Fetched build info for job '{job_name}' build #{build_number}."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to fetch build info for '{job_name}' build #{build_number}."}

def get_build_console_output(job_name, build_number, start_line=None, num_lines=None, search=None, handle=None, session_id=None, mode=None):
    from fod_jenkins.utils import log_debug
    _cleanup_console_log_cache()
    cache_key = handle or _get_log_handle(session_id, job_name, build_number)
    lines = None
    with _console_log_cache_lock:
        if cache_key in _console_log_cache:
            _, lines = _console_log_cache[cache_key]
        else:
            try:
                output = server.get_build_console_output(job_name, build_number)
                lines = output.splitlines()
                _console_log_cache[cache_key] = (time.time(), lines)
            except jenkins.JenkinsException as e:
                return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to fetch console output for '{job_name}' build #{build_number}."}
    total_lines = len(lines)
    log_debug(f"Adapter: job_name={job_name}, build_number={build_number}, start_line={start_line}, num_lines={num_lines}, search={search}, handle={handle}, total_lines={total_lines}, mode={mode}")
    start_line = int(start_line) if start_line is not None else 0
    num_lines = int(num_lines) if num_lines is not None else 100
    # mode support
    if mode == "tail":
        start_line = max(total_lines - num_lines, 0)
    elif mode == "head":
        start_line = 0
    # out-of-bounds handling
    if start_line < 0 or start_line > total_lines:
        suggestion = {"start_line": max(total_lines - num_lines, 0), "num_lines": num_lines}
        return {
            "job_name": job_name,
            "build_number": build_number,
            "console": "",
            "total_lines": total_lines,
            "start_line": start_line,
            "end_line": start_line,
            "has_more": False,
            "search": search,
            "handle": cache_key,
            "next_window_suggestion": suggestion,
            "summary": f"start_line {start_line} is out of bounds for log with {total_lines} lines. Try start_line={suggestion['start_line']}, num_lines={num_lines}."
        }
    if search:
        matches = [(i, line) for i, line in enumerate(lines) if search in line]
        result_lines = [f"{i+1}: {line}" for i, line in matches]
        start_line = 0
        end_line = len(result_lines)
        has_more = False
        suggestion = {"start_line": 0, "num_lines": 100}
    else:
        end_line = min(start_line + num_lines, total_lines)
        result_lines = lines[start_line:end_line]
        has_more = end_line < total_lines
        suggestion = {"start_line": end_line, "num_lines": num_lines} if has_more else {"start_line": max(total_lines - num_lines, 0), "num_lines": num_lines}
    return {
        "job_name": job_name,
        "build_number": build_number,
        "console": "\n".join(result_lines),
        "total_lines": total_lines,
        "start_line": start_line,
        "end_line": end_line,
        "has_more": has_more,
        "search": search,
        "handle": cache_key,
        "next_window_suggestion": suggestion,
        "summary": f"Returned lines {start_line+1}-{end_line} of {total_lines} for {job_name} #{build_number}. Use 'handle' for further chunk requests. To fetch the last {num_lines} lines, use mode='tail'."
    }
def stop_build(job_name, build_number):
    try:
        server.stop_build(job_name, build_number)
        return {"stopped": True, "summary": f"Stopped build #{build_number} for job '{job_name}'."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to stop build #{build_number} for '{job_name}'."}

def get_queue_info():
    try:
        queue = server.get_queue_info()
        return {"queue": queue, "summary": "Fetched queue info."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch queue info."}

def cancel_queue(queue_id):
    try:
        server.cancel_queue(queue_id)
        return {"cancelled": True, "summary": f"Cancelled queue item {queue_id}."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to cancel queue item {queue_id}."}

def get_plugins():
    try:
        plugins = server.get_plugins()
        return {"plugins": plugins, "summary": "Fetched all plugins."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch plugins."}

def get_version():
    try:
        version = server.get_version()
        return {"version": version, "summary": "Fetched Jenkins version."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch Jenkins version."}

def get_whoami():
    try:
        whoami = server.get_whoami()
        return {"whoami": whoami, "summary": "Fetched authenticated user info."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch user info."}

def get_multiple_job_info(job_names):
    results = []
    for job_name in job_names:
        try:
            info = server.get_job_info(job_name)
            results.append({"job_name": job_name, "job": info, "error": None})
        except jenkins.JenkinsException as e:
            results.append({"job_name": job_name, "job": None, "error": {"code": "jenkins_error", "message": str(e)}})
    return {"results": results, "summary": f"Fetched info for {len(job_names)} jobs."}

def get_multiple_build_info(job_build_pairs):
    results = []
    errors = []
    def fetch(pair):
        job_name, build_number = pair["job_name"], pair["build_number"]
        try:
            info = server.get_build_info(job_name, build_number)
            return {"job_name": job_name, "build_number": build_number, "build": info, "error": None}
        except jenkins.JenkinsException as e:
            return {"job_name": job_name, "build_number": build_number, "build": None, "error": {"code": "jenkins_error", "message": str(e)}}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch, job_build_pairs))
    partial_failure = any(r["error"] for r in results)
    return {"results": results, "partial_failure": partial_failure, "summary": f"Fetched build info for {len(job_build_pairs)} builds."}

def get_build_test_report(job_name, build_number):
    try:
        report = server.get_build_test_report(job_name, build_number)
        return {"test_report": report, "summary": f"Fetched test report for job '{job_name}' build #{build_number}."}
    except jenkins.JenkinsException as e:
        return {"error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to fetch test report for '{job_name}' build #{build_number}."}

def get_multiple_build_test_report(job_build_pairs):
    results = []
    def fetch(pair):
        job_name, build_number = pair["job_name"], pair["build_number"]
        try:
            report = server.get_build_test_report(job_name, build_number)
            return {"job_name": job_name, "build_number": build_number, "test_report": report, "error": None}
        except jenkins.JenkinsException as e:
            return {"job_name": job_name, "build_number": build_number, "test_report": None, "error": {"code": "jenkins_error", "message": str(e)}}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch, job_build_pairs))
    partial_failure = any(r["error"] for r in results)
    return {"results": results, "partial_failure": partial_failure, "summary": f"Fetched test reports for {len(job_build_pairs)} builds."}

def copy_job(from_name, to_name, session_id=None):
    try:
        server.copy_job(from_name, to_name)
        return {"success": True, "summary": f"Copied job from {from_name} to {to_name}."}
    except jenkins.JenkinsException as e:
        return {"success": False, "error": {"code": "jenkins_error", "message": str(e)}, "summary": f"Failed to copy job from {from_name} to {to_name}."}

def get_executors(session_id=None):
    try:
        executors = server.get_executors()
        return {"executors": executors, "summary": "Fetched Jenkins executors."}
    except jenkins.JenkinsException as e:
        return {"executors": None, "error": {"code": "jenkins_error", "message": str(e)}, "summary": "Failed to fetch Jenkins executors."}
