import subprocess
import requests
import os
from fod_jenkins.utils import log_debug, log_error, normalize_error

FOD_JOB_SERVER = os.environ["FOD_JOB_SERVER"]
FOD_USER_COOKIE = os.environ["FOD_USER_COOKIE"]
FOD_RUN_F1_PATH = os.environ["FOD_RUN_F1_PATH"]

def fod_submit_job(funos_binary, blobs=None, hardware_model=None, duration=None, tags=None, note=None, params_file=None, extra_args=None):
    """Submit a FoD job via run_f1.py CLI."""
    try:
        cmd = FOD_RUN_F1_PATH.split()
        if hardware_model:
            cmd += ["--hardware-model", hardware_model]
        if duration:
            cmd += ["--duration", str(duration)]
        if tags:
            cmd += ["--tags", tags]
        if note:
            cmd += ["--note", note]
        if params_file:
            cmd += ["--params-file", params_file]
        if blobs:
            cmd += ["--blobs", ",".join(blobs)]
        if extra_args:
            cmd += extra_args
        cmd.append(funos_binary)
        log_debug(f"Running FoD CLI: {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            return {"success": True, "output": proc.stdout, "summary": "Job submitted via CLI."}
        else:
            return {"success": False, "error": {"code": "cli_error", "message": proc.stderr}, "summary": "CLI job submission failed."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to submit FoD job via CLI.")

def fod_get_job(job_id):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch job {job_id}.")

def fod_list_jobs(owner=None, tags=None, state=None, hardware_model=None, page=None, per_page=None, sort=None, session_id=None, **filters):
    try:
        url = f"{FOD_JOB_SERVER}/jobs"
        params = {k: v for k, v in {
            "owner": owner,
            "tags": tags,
            "state": state,
            "hardware_model": hardware_model,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            **filters
        }.items() if v is not None}
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            data["summary"] = "Fetched job list."
            return data
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to list jobs."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to list jobs.")

def fod_kill_job(job_id):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/kill"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "summary": f"Killed FoD job {job_id}.",
                "result": data.get("result", True),
                "msg": data.get("msg", "")
            }
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to kill job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to kill job {job_id}.")

def fod_get_raw_file(job_id, file_name, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/raw_file/{file_name}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"content": resp.text, "summary": f"Fetched raw file {file_name} for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch raw file {file_name} for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch raw file {file_name} for job {job_id}.")

def fod_get_human_file(job_id, file_name, filter_level=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/human_file/{file_name}"
        params = {"filter_level": filter_level} if filter_level else None
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"content": resp.text, "summary": f"Fetched human file {file_name} for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch human file {file_name} for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch human file {file_name} for job {job_id}.")

def fod_get_job_history(days=None, tags=None, owner=None, state=None, sort=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/jobs"
        params = {k: v for k, v in {
            "days": days,
            "tags": tags,
            "owner": owner,
            "state": state,
            "sort": sort
        }.items() if v is not None}
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            data["summary"] = "Fetched job history."
            return data
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch job history."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch job history.")

def fod_get_nightly_history(days=None, tags=None, owner=None, state=None, sort=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/nightly"
        params = {k: v for k, v in {
            "days": days,
            "tags": tags,
            "owner": owner,
            "state": state,
            "sort": sort
        }.items() if v is not None}
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            data["summary"] = "Fetched nightly job history."
            return data
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch nightly job history."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch nightly job history.")

def fod_get_result_history(days=None, tags=None, owner=None, state=None, sort=None, disable_grouping=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/result_history"
        params = {k: v for k, v in {
            "days": days,
            "tags": tags,
            "owner": owner,
            "state": state,
            "sort": sort,
            "disable_grouping": disable_grouping
        }.items() if v is not None}
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            data["summary"] = "Fetched result history."
            return data
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch result history."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch result history.")

def fod_restart_job(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/restart"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Restarted job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to restart job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to restart job {job_id}.")

def fod_archive_job(job_id, archive, days=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/state"
        params = {"state": 1 if archive else 0}
        if days is not None:
            params["days"] = days
        log_debug(f"POST {url} with params {params}")
        resp = requests.post(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"{'Archived' if archive else 'Unarchived'} job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to {'archive' if archive else 'unarchive'} job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to {'archive' if archive else 'unarchive'} job {job_id}.")

def fod_delete_job(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/delete"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {
                "summary": f"Killed FoD job {job_id}.",
                "result": data.get("result", True),
                "msg": data.get("msg", "")
            }
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to delete job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to delete job {job_id}.")

def fod_update_job_metadata(job_id, metadata, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}"
        log_debug(f"POST {url} with metadata {metadata}")
        resp = requests.post(url, json=metadata, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Updated metadata for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to update metadata for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update metadata for job {job_id}.")

def fod_update_job_priority(job_id, priority, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/priority"
        params = {"priority": priority}
        log_debug(f"POST {url} with params {params}")
        resp = requests.post(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Updated priority for job {job_id} to {priority}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to update priority for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update priority for job {job_id}.")

def fod_create_reservation(owner, resource, start_time, end_time, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations"
        body = {
            "owner": owner,
            "resource": resource,
            "start_time": start_time,
            "end_time": end_time
        }
        log_debug(f"POST {url} with body {body}")
        resp = requests.post(url, json=body, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": "Created reservation."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to create reservation."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to create reservation.")

def fod_update_reservation(reservation_id, owner, resource, start_time, end_time, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations/{reservation_id}"
        body = {
            "owner": owner,
            "resource": resource,
            "start_time": start_time,
            "end_time": end_time
        }
        log_debug(f"POST {url} with body {body}")
        resp = requests.post(url, json=body, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Updated reservation {reservation_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to update reservation {reservation_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to update reservation {reservation_id}.")

def fod_cancel_reservation(reservation_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations/cancel/{reservation_id}"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Cancelled reservation {reservation_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to cancel reservation {reservation_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to cancel reservation {reservation_id}.")

def fod_get_wu_trace(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/wu_trace"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"trace": resp.json(), "summary": f"Fetched WU trace for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch WU trace for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch WU trace for job {job_id}.")

def fod_get_function_trace(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/function_trace"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"trace": resp.text, "summary": f"Fetched function trace for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch function trace for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch function trace for job {job_id}.")

def fod_get_telemetry(job_id, vars=None, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}/telemetry"
        params = {"vars": vars} if vars else None
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"telemetry": resp.json(), "summary": f"Fetched telemetry for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch telemetry for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch telemetry for job {job_id}.")

def fod_get_core_dump_outputs(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            job = resp.json()
            outputs = job.get("core_dump_outputs")
            return {"outputs": outputs, "summary": f"Fetched core dump outputs for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch core dump outputs for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch core dump outputs for job {job_id}.")

def fod_get_hbm_memory_dumps(job_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job/{job_id}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            job = resp.json()
            outputs = job.get("hbm_memory_dumps")
            return {"outputs": outputs, "summary": f"Fetched HBM memory dumps for job {job_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch HBM memory dumps for job {job_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch HBM memory dumps for job {job_id}.")

def fod_get_clusters(session_id=None):
    try:
        url = os.environ.get("FOD_CLUSTER_MANAGER", "http://palladium-jobs.fungible.local/api/clusters")
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"clusters": data, "summary": "Fetched clusters."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch clusters."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch clusters.")

def fod_get_machines(session_id=None):
    try:
        url = os.environ.get("FOD_MACHINE_MANAGER", "http://palladium-jobs.fungible.local/api/machines")
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"machines": data, "summary": "Fetched machines."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch machines."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch machines.")

def fod_get_reservations(session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"reservations": data.get("reservations", data), "summary": "Fetched reservations."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch reservations."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch reservations.")

def fod_get_reservation_by_id(reservation_id, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations/{reservation_id}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"reservation": data, "summary": f"Fetched reservation {reservation_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch reservation {reservation_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch reservation {reservation_id}.")

def fod_get_reservable_resources(session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/reservations/resources"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"resources": data, "summary": "Fetched reservable resources."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch reservable resources."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch reservable resources.")

def fod_get_cluster_status(cluster_id, session_id=None):
    try:
        url = os.environ.get("FOD_CLUSTER_MANAGER", "http://palladium-jobs.fungible.local/api/clusters") + f"/{cluster_id}/status"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"status": data, "summary": f"Fetched status for cluster {cluster_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch status for cluster {cluster_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch status for cluster {cluster_id}.")

def fod_get_machine_status(machine_id, session_id=None):
    try:
        url = os.environ.get("FOD_MACHINE_MANAGER", "http://palladium-jobs.fungible.local/api/machines") + f"/{machine_id}/status"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"status": data, "summary": f"Fetched status for machine {machine_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch status for machine {machine_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch status for machine {machine_id}.")

def fod_enable_cluster(cluster_id, session_id=None):
    try:
        url = os.environ.get("FOD_CLUSTER_MANAGER", "http://palladium-jobs.fungible.local/api/clusters") + f"/{cluster_id}/enable"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Enabled cluster {cluster_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to enable cluster {cluster_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to enable cluster {cluster_id}.")

def fod_disable_cluster(cluster_id, session_id=None):
    try:
        url = os.environ.get("FOD_CLUSTER_MANAGER", "http://palladium-jobs.fungible.local/api/clusters") + f"/{cluster_id}/disable"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Disabled cluster {cluster_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to disable cluster {cluster_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to disable cluster {cluster_id}.")

def fod_fit_cluster(cluster_id, job_requirements=None, session_id=None):
    try:
        url = os.environ.get("FOD_CLUSTER_MANAGER", "http://palladium-jobs.fungible.local/api/clusters") + f"/{cluster_id}/fit"
        body = job_requirements if job_requirements else {}
        log_debug(f"POST {url} with body {body}")
        resp = requests.post(url, json=body, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"fit_result": data, "summary": f"Fit result for cluster {cluster_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fit cluster {cluster_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fit cluster {cluster_id}.")

def fod_enable_machine(machine_id, session_id=None):
    try:
        url = os.environ.get("FOD_MACHINE_MANAGER", "http://palladium-jobs.fungible.local/api/machines") + f"/{machine_id}/enable"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Enabled machine {machine_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to enable machine {machine_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to enable machine {machine_id}.")

def fod_disable_machine(machine_id, session_id=None):
    try:
        url = os.environ.get("FOD_MACHINE_MANAGER", "http://palladium-jobs.fungible.local/api/machines") + f"/{machine_id}/disable"
        log_debug(f"POST {url}")
        resp = requests.post(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            return {"summary": f"Disabled machine {machine_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to disable machine {machine_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to disable machine {machine_id}.")

def fod_fit_machine(machine_id, job_requirements=None, session_id=None):
    try:
        url = os.environ.get("FOD_MACHINE_MANAGER", "http://palladium-jobs.fungible.local/api/machines") + f"/{machine_id}/fit"
        body = job_requirements if job_requirements else {}
        log_debug(f"POST {url} with body {body}")
        resp = requests.post(url, json=body, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"fit_result": data, "summary": f"Fit result for machine {machine_id}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fit machine {machine_id}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fit machine {machine_id}.")

def fod_get_job_queued_status(session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/job_queued_status"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"queue_status": data, "summary": "Fetched job queue status."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch job queue status."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch job queue status.")

def fod_get_order(session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/order"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"order": data, "summary": "Fetched job order in queue."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch job order in queue."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch job order in queue.")

def fod_get_robotstate(session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/robotstate"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"robotstate": data, "summary": "Fetched robot state."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": "Failed to fetch robot state."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, "Failed to fetch robot state.")

def fod_get_distinct_values(field_name, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/distinct_values/{field_name}"
        log_debug(f"GET {url}")
        resp = requests.get(url, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"values": data, "summary": f"Fetched distinct values for field {field_name}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch distinct values for field {field_name}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch distinct values for field {field_name}.")

def fod_autocomplete(field_name, q=None, limit=10, session_id=None):
    try:
        url = f"{FOD_JOB_SERVER}/autocomplete/{field_name}"
        params = {"q": q, "limit": limit}
        log_debug(f"GET {url} with params {params}")
        resp = requests.get(url, params=params, cookies={"user": FOD_USER_COOKIE} if FOD_USER_COOKIE else None)
        if resp.status_code == 200:
            data = resp.json()
            return {"suggestions": data, "summary": f"Fetched autocomplete suggestions for field {field_name}."}
        else:
            return {"error": {"code": f"http_{resp.status_code}", "message": resp.text}, "summary": f"Failed to fetch autocomplete for field {field_name}."}
    except Exception as e:
        log_error(e)
        return normalize_error(e, f"Failed to fetch autocomplete for field {field_name}.")

def fod_submit_job_by_branch(
    RUN_TARGET, HW_MODEL, HW_VERSION, RUN_MODE, PRIORITY, NOTE, TAGS, EXTRA_EMAIL, BOOTARGS, MAX_DURATION, HBM_DUMP, FAST_EXIT, BLD_TYPE, SKIP_DASM_C, REMOTE_SCRIPT, NETWORK_SCRIPT, UART_MODE, UART_SCRIPT, CENTRAL_SCRIPT, POST_SCRIPT, DEV_LINE, BRANCH_FunOS, BRANCH_FunSDK, BRANCH_FunHW, BRANCH_FunBlockDev, BRANCH_FunTest, BRANCH_fungible_host_drivers, BRANCH_FunControlPlane, BRANCH_frr, BRANCH_FunAgents, BRANCH_FunAPIServer, BRANCH_fungible_rdma_core, BRANCH_fungible_perftest, BRANCH_pdclibc, BRANCH_SBPFirmware, BRANCH_u_boot, BRANCH_aapl, SECURE_BOOT, CSR_FILE, ENABLE_WULOG, WAVEFORM_CMD, FUNOS_MAKEFLAGS, CCFG, BLOBS, BRANCH_FunTools, BRANCH_FunJenkins, BRANCH_FunDevelopment, RUN_PIPELINE, BRANCH_libfuncrypto, BRANCH_FunHCI, INCLUDE_DRIVER_SRC, USE_CCLINUX, USE_ACU, INCLUDE_EXTERNAL_ARTIFACTS, USE_CLUSTER_SERVICES, FUNOS_TYPE, INTERACTIVE, OTP_CHALLENGE, REQUEST_SOURCE, session_id=None
):
    import requests
    JENKINS_URL = os.environ["JENKINS_URL_JOB"]
    USERNAME = os.environ["JENKINS_USERNAME"]
    API_TOKEN = os.environ["JENKINS_API_TOKEN"]
    JOB_PATH = "/ci/job/emulation/job/fun_on_demand/buildWithParameters"
    session = requests.Session()
    session.auth = (USERNAME, API_TOKEN)

    # get Jenkins crumb (CSRF token)
    crumb_url = f"{JENKINS_URL}/ci/crumbIssuer/api/json"
    resp = session.get(crumb_url)
    resp.raise_for_status()
    crumb_data = resp.json()
    crumb = crumb_data["crumb"]
    crumb_field = crumb_data["crumbRequestField"]
    params = {
        "RUN_TARGET": RUN_TARGET,
        "HW_MODEL": HW_MODEL,
        "HW_VERSION": HW_VERSION,
        "RUN_MODE": RUN_MODE,
        "PRIORITY": PRIORITY,
        "NOTE": NOTE,
        "TAGS": TAGS,
        "EXTRA_EMAIL": EXTRA_EMAIL,
        "BOOTARGS": BOOTARGS,
        "MAX_DURATION": MAX_DURATION,
        "HBM_DUMP": HBM_DUMP,
        "FAST_EXIT": FAST_EXIT,
        "BLD_TYPE": BLD_TYPE,
        "SKIP_DASM_C": SKIP_DASM_C,
        "REMOTE_SCRIPT": REMOTE_SCRIPT,
        "NETWORK_SCRIPT": NETWORK_SCRIPT,
        "UART_MODE": UART_MODE,
        "UART_SCRIPT": UART_SCRIPT,
        "CENTRAL_SCRIPT": CENTRAL_SCRIPT,
        "POST_SCRIPT": POST_SCRIPT,
        "DEV_LINE": DEV_LINE,
        "BRANCH_FunOS": BRANCH_FunOS,
        "BRANCH_FunSDK": BRANCH_FunSDK,
        "BRANCH_FunHW": BRANCH_FunHW,
        "BRANCH_FunBlockDev": BRANCH_FunBlockDev,
        "BRANCH_FunTest": BRANCH_FunTest,
        "BRANCH_fungible_host_drivers": BRANCH_fungible_host_drivers,
        "BRANCH_FunControlPlane": BRANCH_FunControlPlane,
        "BRANCH_frr": BRANCH_frr,
        "BRANCH_FunAgents": BRANCH_FunAgents,
        "BRANCH_FunAPIServer": BRANCH_FunAPIServer,
        "BRANCH_fungible_rdma_core": BRANCH_fungible_rdma_core,
        "BRANCH_fungible_perftest": BRANCH_fungible_perftest,
        "BRANCH_pdclibc": BRANCH_pdclibc,
        "BRANCH_SBPFirmware": BRANCH_SBPFirmware,
        "BRANCH_u_boot": BRANCH_u_boot,
        "BRANCH_aapl": BRANCH_aapl,
        "SECURE_BOOT": SECURE_BOOT,
        "CSR_FILE": CSR_FILE,
        "ENABLE_WULOG": ENABLE_WULOG,
        "WAVEFORM_CMD": WAVEFORM_CMD,
        "FUNOS_MAKEFLAGS": FUNOS_MAKEFLAGS,
        "CCFG": CCFG,
        "BLOBS": BLOBS,
        "BRANCH_FunTools": BRANCH_FunTools,
        "BRANCH_FunJenkins": BRANCH_FunJenkins,
        "BRANCH_FunDevelopment": BRANCH_FunDevelopment,
        "RUN_PIPELINE": RUN_PIPELINE,
        "BRANCH_libfuncrypto": BRANCH_libfuncrypto,
        "BRANCH_FunHCI": BRANCH_FunHCI,
        "INCLUDE_DRIVER_SRC": INCLUDE_DRIVER_SRC,
        "USE_CCLINUX": USE_CCLINUX,
        "USE_ACU": USE_ACU,
        "INCLUDE_EXTERNAL_ARTIFACTS": INCLUDE_EXTERNAL_ARTIFACTS,
        "USE_CLUSTER_SERVICES": USE_CLUSTER_SERVICES,
        "FUNOS_TYPE": FUNOS_TYPE,
        "INTERACTIVE": INTERACTIVE,
        "OTP_CHALLENGE": OTP_CHALLENGE,
        "REQUEST_SOURCE": REQUEST_SOURCE
    }
    headers = {crumb_field: crumb}
    submit_url = f"{JENKINS_URL}{JOB_PATH}"
    resp = session.post(submit_url, params=params, headers=headers)
    return {
        "status": resp.status_code,
        "location": resp.headers.get("Location"),
        "response": resp.text,
        "summary": "Submitted branch-only FoD job via Jenkins API."
    }
