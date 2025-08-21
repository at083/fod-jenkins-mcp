---
mode: 'agent'
description: 'Branch-based FoD job submission and monitoring workflow'
---
# Branch Submission Workflow for Fun-on-Demand (FoD)

> **Purpose:**
> This file details how to submit a FoD job using branches (no signed binary required), and how to monitor and track the job through Jenkins and FoD.
> For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).

---

## Submitting a FoD Job by Branch

- **Tool:** `fod_submit_by_branch`
- **Purpose:** Submit a Fun-on-Demand job by specifying only branch and build parameters. This triggers a Jenkins build that produces and launches the FoD job.

### Parameters
- `fod_submit_by_branch` can be called with the following parameters (below is the full list):
  - `RUN_TARGET`: Where to run this job (e.g., "F1D1")
  - `HW_MODEL`: Hardware model to run. The model governs how many clusters exist, which hardware blocks are available (e.g., "F1D1")
  - `RUN_MODE`: Whether to run this job, or just build the install image. The latter is useful for interactive jobs or testing the Palladium build process (by default, leave this as "Batch")
  - `PRIORITY`: Relative priority of job (e.g., "normal_priority", "low_priority", or "high_priority")
  - `DEV_LINE`: Release devline to base the build around (e.g., "master")
  - `MAX_DURATION`: Maximum duration (minutes)
  - `BOOTARGS`: FunOS boot arguments separated by spaces (e.g., "app=load_mods --disable-wu-watchdog", "app=pke_nightly_test", "app=clock_app", "test=timer_test", "test=basic_test", "app=mdt_test,voltest numinstance=1 numios=450 syslog=3 --compress --crypto --serial --hsu_rc --perf", "--csr-replay --dpc-server")
  - `HW_VERSION`: Hardware RTL version to use. Top entry is the most recent supported version. Leave blank by default (e.g., "")
  - `NOTE`: Explanatory note for this job. The note will appear on the Emulation-On-Demand web page and in the email subject. Typically used as reminder for the submitter, or to distinguish ones multiple similar jobs, and for others to know what you are testing (e.g., "Testing NU debug tool")
  - `TAGS`: Tags or keywords identifying this job, comma-separated (e.g. "nightly, test, hbm-bringup, debug, qa-networking-sanity"). Also used for temporary hidden features such as "pci-tdf=s0c0" to turn on PCI logging
  - `EXTRA_EMAIL`: Additional folks to email on job completion, comma-separated
  - `HBM_DUMP`: Dump contents of HBM memory to a file at the completion of the run. Dumping memory takes 15 minutes. Only supported on Palladium for models with HBM--Compute2, Storage2, etc. ("true" or "false")
  - `FAST_EXIT`: Exit FunOS as soon as tests complete. Avoid waiting for idle detection. Turn off for runs that intend to run much longer than their top-level WU. (e.g. "true" or "false")
  - `BLD_TYPE`: Whether use debug binary or release binary, the latter is useful for performance testing (e.g. "debug" or "release")
  - `SKIP_DASM_C`: Option to not generate dasm_c. You may need to rebuild with same parameters to generate this at a later time (e.g. "true" or "false")
  - `REMOTE_SCRIPT`: Path to remote script to run on machine connected to PCI and arguments. Path must start with FunDevelopment, FunOS, or FunSDK, and indicates a single file that will be run standalone on the remote system (e.g. "FunDevelopment/tmp_protium/test_device_exists.sh 1 2 3 4"). Applicable only for hardware models with a separate server attached to the F1 via PCI
  - `NETWORK_SCRIPT`: Script to run on every server connected to test machine via network. Applicable only for hardware models with a server attached to the F1 via network connection
  - `UART_MODE`: How to set up physical UART T-Pod. "none" means do not use physical UART. Not "none" means reserve and use physical UART. In all cases, UARTs are always dumped to text files that you see on job page (e.g. "", "none")
  - `UART_SCRIPT`: Script to run on UART host. For uart-mode=dpcsh, keep the script empty, so that default DPC Shell TCP Proxy script is run (e.g., "dpcsh")
  - `CENTRAL_SCRIPT`: Script to run on lab server. Central scripts know about all the hosts involved in the test, and can ssh in to any of the servers to start complex tests or exercise machines through the management port
  - `POST_SCRIPT`: Script to run when job completes. Post-run scripts can check whether a completed test completed in the expected way. Post-run scripts can examine any of the logs to check if FunOS behaved in an intended way. Post-run scripts can also change the overall return code, returning a PASS if an expected failure occurs in FunOS or vice-versa
  - `DEV_LINE`: Release devline to base the build around (e.g. "rel_1_0a_aa", "rel_2_3", "master")
  - `BRANCH_FunOS`, `BRANCH_FunSDK`, `BRANCH_FunHW`, `BRANCH_FunBlockDev`: Branch names for each component (each are individual parameters). Default (if left blank): master (e.g., "cgray/wiq-route", "bld_5500", "sha1/ecc29af")
  - `BRANCH_FunTest`: Branch of FunTest to use. Leave blank to use tar ball from dockhub
  - `BRANCH_fungible_host_drivers`: Branch to use for getting sources for building host drivers. Leave branch blank to use src tar ball from latest dochub build
  - `BRANCH_FunControlPlane`: Branch to use for building funcontrolplane. Leave branch blank to use FunCP from latest dochub build
  - `BRANCH_frr`: Branch to use for building frr. Leave branch blank to use frr from latest dochub build
  - `BRANCH_FunAgents`: FunAgents version. Default (if left blank): master. Used for building alternate versions of control plane daemons on CC-Linux
  - `BRANCH_FunAPIServer`: Branch of FunAPIServer to use. If not provided, binaries from master build will be used
  - `BRANCH_fungible_rdma_core`: Branch of fungible-rdma-core to use. If not provided, binaries from master build will be used
  - `BRANCH_fungible_perftest`: Branch of fungible-perftest to use. If not provided, binaries from master build will be used
  - `BRANCH_pdclibc`: pdclibc version Default (if left blank): master (e.g. "cgray/wiq-route", "bld_5500", "sha1/ecc29af")
  - `BRANCH_SBPFirmware`: SBPFirmware branch to use to build SBP. ROM will be built from default branch if left blank
  - `BRANCH_u_boot`: U-boot branch to use to optionally build U-boot. Default is to use form SDK cache if left blank
  - `BRANCH_aapl`: Branch to use for building aapl. If blank, uses the version matching your current FunSDK
  - `BRANCH_etcd`: Branch of etcd to use when building control plane. Tar ball from dockhub will be used if no branch is specified
  - `FUNHAL_FROM`: Can be one of three things: (a) build number under dochub/master/funhal_${chip}/, (b) a url to the source tgz file, or (c) a file path accessible from build machine/workspace (e.g., "FUNHAL_FROM": "207", "FUNHAL_FROM": "http://jenkins-hw-01:8080/job/build_com/job/build_funhal2/ws/funhal_s2.src.tar.gz", "FUNHAL_FROM": "/home/userid/funhal_f1d1.src.tar.gz")
  - `SECURE_BOOT`: How the FunOS binary should be cryptographically signed. Signed binaries execute code in the secure boot processor when starting the chip. Sign with the "fungible" development key to test the normal paths. Use "unsigned" for testing or if there's any problems with the signed code path (e.g., "fungible" or "unsigned")
  - `CSR_FILE`: Path to the CSR file to use. File with .cfg extension is for emulation jobs
file with .bjson extesion is for silicon jobs
  - `ENABLE_WULOG`: Log the order and time that WUs run, grouped by transactions. WU logging is selective; you use the macros WU_TRACE_START or WU_TRACE_WITH_PROBABILITY() to start tracing in a specific WU. WU tracing is transitive; if you trace a specific WU, all WUs sent from that WU are also traced (e.g., "true" or "false")
  - `WAVEFORM_CMD`: Explicit TCL commands to script gathering of waveforms. TCL commands must use "run" to start emulation. Only works on Palladium
  - `FUNOS_MAKEFLAGS`: Extra flags to pass to FunOS make command
  - `CCFG`: Name of feature set configuration (ccfg) to use. Must be file installed in FunSDK/feature_sets/ccfg-${CCFG}.bjson (valid choices: "no-come", "10g", "100g", etc.)
  - `BLOBS`: Comma-separated list of signed binary files that should be loaded into FunOS at boot time. Binaries must be present in the Jenkins workspace. Users may be required to add FunOS Makefiles to the build to generate specific binaries
  - `BRANCH_FunTools`: FunTools version. Default (if left blank): master
  - `BRANCH_FunJenkins`: FunJenkins version. Default (if left blank): master. Useful for testing custom versions of stuff in FunJenkins, which includes: Jenkins Build Pipeline scripts for various Jenkins builds
  - `BRANCH_FunDevelopment`: FunDevelopment version. Default (if left blank): master. Useful for testing custom versions of stuff in FunDevelopment, which includes: Run Emulation scripts that submit emulation jobs to LSF, PCI Remote Host scripts, Network Remote Host scripts
  - `RUN_PIPELINE`: Run/Emulation pipeline install environment to use. Useful for testing custom version of run/emulation scripts. The name of an environment installed using ploy command in ~robotpal/install/ e.g. 37ff820.18.11.08 OR 2c8a48e.18.11.08.rlimayemac.18.11.08 OR any absolute path on NFS
  - `BRANCH_libfuncrypto`: Branch of libfuncrypto to use. If not provided, binaries from master build will be used
    "BRANCH_FunHCI": "",
  - `INCLUDE_DRIVER_SRC`: Whether to include Fungible Driver Source Package so that your test script can build drivers (e.g., "false" or "true")
  - `USE_CCLINUX`: Launch CC-Linux on Fungible chips (e.g., "true" or "false")
  - `USE_ACU`: Launch ACU on Fungible chip (e.g., "true" or "false")
  - `INCLUDE_EXTERNAL_ARTIFACTS`: Provide json file path which contains the list of files which needs to be downloaded and provided to Fun-on-demand to run your tests
  - `USE_CLUSTER_SERVICES`: Dump contents of HBM memory to a file at the completion of the run. Dumping memory takes 15 minutes. Only supported on Palladium for models with HBM--Compute2, Storage2, etc. (e.g., "true" or "false")
  - `FUNOS_TYPE`: Choice of funos binary. Current default is "core" (be sure to specify as such for all jobs)
  - `INTERACTIVE`: Whether to send e-mails when job is running and related hosts are accessible (e.g., "true" or "false")
  - `OTP_CHALLENGE`: "i2c" (leave as is unless otherwise specified)
  - `REQUEST_SOURCE`: "jenkins_launch_page_manual" (where request from build is coming from; this is for internal use, please do not change)
  - For any job, you need not specify all of these parameters (unless it specifically says to for any of them or if the user specifies it themselves). The parameters that aren't specified are assumed to be configured as default.
  - Leave binary-related fields blank if you do not want to provide a signed binary.
  - All parameters and definitions must be in string form (e.g. "USE_CCLINUX": "false", "DEV_LINE": "master", "PRIORITY": "normal_priority", "MAX_DURATION": "5", etc.)

#### Example:
```
fod_submit_by_branch(
  RUN_TARGET="F1D1",
  HW_MODEL="F1D1",
  RUN_MODE="Batch",
  PRIORITY="normal_priority",
  DEV_LINE="master",
  BRANCH_FunOS="stable-testdrops1",
  BRANCH_FunSDK="stable",
  MAX_DURATION="5",
  BOOTARGS="--csr-replay --dpc-server",
  NOTE="branch-demo-20250812-unique",
  TAGS="branch-demo-20250812-unique"
)
```

---

## Monitoring and Tracking the Job

After calling `fod_submit_by_branch`, follow this workflow:

1. **Monitor Jenkins Queue:**
   - Use `get_queue_info` with the queue item URL to check the status.
   - If the job is still in the queue, ask the user if they want to check again. Repeat until the job leaves the queue.
   - If the queue info returns empty, proceed to the next step.

2. **Find the Jenkins Build Number:**
   - Use `get_multiple_job_info(job_names=["emulation/fun_on_demand"]) to retrieve a list of recent builds and their corresponding build numbers.
   - Then determine the three most recent builds by calling `get_multiple_build_info(job_build_pairs=[{"job_name": "emulation/fun_on_demand", "build_number": <most recent build's number>}, {"job_name": "emulation/zemulation_nightly", "build_number": <second most recent build's number>}, {"job_name": "emulation/zemulation_nightly", "build_number": <third most recent build's number>}])`.
   - Examine the build parameters or timestamps to identify the correct build (e.g., by matching tags, notes, or submission time).
   - Once the correct build is identified, continue monitoring it with `get_multiple_build_info` until it completes.

3. **Find the FoD Job on Palladium:**
   - Use `fod_get_job_history` to query for the FoD job created by the Jenkins build.
   - Query by `owner`, `hardware_model`, and `tags` (if any were set; use `null` for tags if none were set).
   - Repeat until the FoD lsf ID is found. Note that lsf ID from the user's point of view *is* the job ID of a FoD job.

---

## Important Tips
- Always include a unique tag or note for easier tracking in both Jenkins and FoD.
- This workflow assumes you have permission to trigger Jenkins builds and access the Jenkins and FoD APIs.

---

## References
- For general MCP usage, see [Core MCP Guide](fod_mcp_core.prompt.md).
- For Jenkins build monitoring, see [Jenkins Build Monitoring](fod_jenkins_build_monitoring_workflow.prompt.md).
