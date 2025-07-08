import requests
import json

# This script tests the MCP (Microservice Control Plane) API for Jenkins jobs.
# It sends various intents to the MCP and collects the results.
# Make sure the MCP service is running before executing this script!

MCP_URL = "http://localhost:8000/mcp/intent"  # adjust port if needed

RESULTS_FILE = "integration_test_results.json"

def post_intent(intent, session_id="test-session"):
    resp = requests.post(
        MCP_URL,
        json={"session_id": session_id, "intent": intent},
        timeout=10
    )
    result = {
        "intent": intent,
        "status_code": resp.status_code,
        "response": resp.json()
    }
    return result

def main():
    results = []
    # test single job info
    results.append(post_intent({"operation": "get_job_info", "job_name": "emulation/fun_on_demand"}))

    # test batch job info
    results.append(post_intent({"operation": "get_multiple_job_info", "job_names": ["emulation/fun_on_demand", "nonexistent_job"]}))

    # test single build info
    results.append(post_intent({"operation": "get_build_info", "job_name": "emulation/fun_on_demand", "build_number": 170456}))

    # test batch build info
    results.append(post_intent({
        "operation": "get_multiple_build_info",
        "job_build_pairs": [
            {"job_name": "emulation/fun_on_demand", "build_number": 170456},
            {"job_name": "nonexistent_job", "build_number": 1}
        ]
    }))

    # test build console output (single)
    results.append(post_intent({"operation": "get_build_console_output", "job_name": "emulation/fun_on_demand", "build_number": 170456}))

    # test batch build console output
    results.append(post_intent({
        "operation": "get_multiple_build_console_output",
        "job_build_pairs": [
            {"job_name": "emulation/fun_on_demand", "build_number": 170456},
            {"job_name": "nonexistent_job", "build_number": 1}
        ]
    }))

    # test build test report (single)
    results.append(post_intent({"operation": "get_build_test_report", "job_name": "emulation/fun_on_demand", "build_number": 170456}))

    # test batch build test report
    results.append(post_intent({
        "operation": "get_multiple_build_test_report",
        "job_build_pairs": [
            {"job_name": "emulation/fun_on_demand", "build_number": 170456},
            {"job_name": "nonexistent_job", "build_number": 1}
        ]
    }))

    # write results to file
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()