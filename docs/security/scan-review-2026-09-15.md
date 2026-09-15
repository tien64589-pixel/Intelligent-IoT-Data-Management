# Security Scan Review and Remediation Recommendations

Prepared for Tommy Nguyen and the project team | 15 September 2026

Repository: tien64589-pixel/Intelligent-IoT-Data-Management  
Reviewed main commit: `2dd2dcd117d6eecbf82193dd8d9fe2dbe3beee93`.

## Summary

The scans are providing different levels of assurance. CodeQL completed and uploaded results. Gitleaks detected two historical items again. Semgrep reported a successful job even though its log showed a configuration error. A green workflow must not be presented as evidence that all vulnerabilities are fixed.

No credential rotation, application deployment or successful remediation rescan is claimed in this review. The Semgrep correction is prepared on a review branch. Application fixes below remain recommendations.

## Verified workflow evidence

| Tool | Latest run inspected | Evidence | Correct reporting |
| --- | --- | --- | --- |
| CodeQL | [14 September, run 34795635433](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/34795635433) | JavaScript/TypeScript and Python analysis jobs completed; logs confirm results uploaded. | Scan execution confirmed. Current open-alert count is unverified because the available connector does not expose the alerts endpoint. |
| Gitleaks | [14 September, run 34821995828](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/34821995828) | Scheduled scan failed: 287 commits scanned, two findings. | Historical findings remain detected. The 9 September seven-commit pass does not clear them. |
| Semgrep | [9 September, run 34340846699](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/34340846699) | Unsupported publishDeployment input; log requests login or explicit configuration. Job and upload nevertheless passed. | Coverage and finding count are unverified. Do not describe this as a clean scan. |

## Priorities, impact and recommendations

Priority is a review judgement, not a new CVSS score. Confirm exposure before assigning final system risk.

### 1. Historical secret candidates — urgent validation

**Locations:** `backend/.env.example:15` at commit `0d4989ac1d7d8041b82f1d96b18c163240f63eeb` (generic-api-key); `newBackend/BackendCode/mock_data/users.json:37` at commit `cc2d0d3f83f7040daf33c81683e2b293d6ec504a` (JWT). These are historical line numbers, not current-main locations.

**Impact:** If valid, the values could enable unauthorised API access or use of an exposed session. A JWT does not, by itself, prove that its signing key is compromised. Validity and privileges have not been tested.

**Fix:** The credential owner should identify the issuer and check whether each value was ever usable. Revoke or rotate a real API credential; invalidate the exposed JWT/session using the issuer's supported mechanism. Replace usable credentials in examples or fixtures with unmistakably inert placeholders. Deleting a file or adding it to .gitignore does not remove Git history or revoke credentials. Coordinate any history rewrite with repository maintainers. For a proven dummy value, document the evidence before a narrowly scoped exception; do not suppress the whole directory.

**Verification:** Record revocation or dummy-value evidence and rerun a history scan. Retain the scheduled Gitleaks scan: its failure is evidence of detection, not a broken scanner. See GitHub (n.d.-b) and Gitleaks (n.d.).

### 2. Semgrep configuration — high assurance priority

**Location:** `.github/workflows/semgrep.yml:38–48` on the reviewed main commit.

**Impact:** The team may rely on an ineffective scan and merge vulnerable code believing it was checked.

**Prepared fix:** Replace the legacy action with Semgrep CLI 1.177.0 and explicit `p/ci` rules. Use `--error` to fail on findings and `--strict` for scan warnings/errors, write SARIF, and preserve the failing scan status. Upload SARIF only when it exists and the PR context supports write permissions. Add manual execution. This is Community Edition scanning; it does not reproduce any account-specific Pro rules or policies.

**Verification:** YAML parsing and failure-propagation configuration were checked locally. A successful GitHub run is still required. Confirm rule loading, scanned/skipped files and expected detection using an intentionally vulnerable test fixture before calling the gate validated. Registry rules can change independently of the pinned CLI; retain rule metadata with evidence. See Semgrep (n.d.-a, n.d.-b).

### 3. Python upload path — high if the endpoint is reachable

**Current source:** `data_science/archive/development/server.py:40–41` joins an uploaded filename directly to the storage directory and saves it.

**Impact:** A crafted absolute or traversal filename may write outside the intended directory, subject to service permissions. The file is archived; production use is not confirmed.

**Fix:** Since this handler immediately reads CSV data, prefer parsing the uploaded stream directly with `pd.read_csv(uploaded_file, parse_dates=['created_at'])` and remove the filename-based disk write. If persistent storage is required, generate the filename on the server, enforce containment within a dedicated directory and use exclusive creation. Validate CSV structure and enforce an agreed request-size limit.

**Verification:** Test normal CSV upload, malformed CSV, oversized requests and traversal filenames. Confirm no file is created outside storage. See GitHub (n.d.-c).

### 4. Debug mode and detailed errors — high if exposed

**Current source:** `correlation_alert/server.py:108` and `data_science/archive/development/server.py:76` enable debug mode. Detailed exception text is returned at correlation lines 100–104 and archive lines 50–51 and 56–58.

**Impact:** Debug features and detailed errors may expose internal paths or implementation details. An exposed interactive debugger can have severe consequences; deployment exposure has not been established.

**Fix:** Set debug to false, use a production WSGI server, and return generic errors with appropriate HTTP status codes. Log diagnostic information internally with access controls and secret redaction. Disabling debug alone does not make Flask's development server production-ready.

**Verification:** Trigger invalid input and internal failures in a controlled environment; confirm no traceback, internal exception details or interactive debugger reaches the client. See Pallets (n.d.).

### 5. Historical CodeQL rate-limiting findings — remap before changing code

The uploaded CodeQL evidence report refers to `backend/routes/auth.js:9,15` and `backend/routes/thingspeak.js:11`. Both paths returned 404 on current main. Its “13 open findings” is historical evidence, not a verified current count. Its v3/autobuild description also differs from current v4, build-mode none configuration.

**Fix recommendation:** Review current CodeQL alerts and map them to the replacement routes. Where confirmed, place suitable rate limits before expensive authentication, database or outbound API work; configure trusted proxies and shared counters appropriately for deployment. Verify normal traffic works and excess requests receive 429 responses. Do not recreate obsolete files just to match old line numbers. See GitHub (n.d.-a, n.d.-d).

## Completion evidence required

Keep the finding ID, commit, file/line, owner, remediation commit, scan run and verification result together. Distinguish “recommended,” “implemented on branch,” “merged,” and “verified.” Current CodeQL alert exports or screenshots are still needed for complete alert-by-alert remediation.

## References (APA 7)

GitHub. (n.d.-a). *Assessing code scanning alerts for your repository*. https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/assess-alerts

GitHub. (n.d.-b). *Resolving alerts from secret scanning*. https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-secret-scanning-alerts/resolving-alerts

GitHub. (n.d.-c). *Uncontrolled data used in path expression*. CodeQL query help. https://codeql.github.com/codeql-query-help/python/py-path-injection/

GitHub. (n.d.-d). *Missing rate limiting*. CodeQL query help. https://codeql.github.com/codeql-query-help/javascript/js-missing-rate-limiting/

Gitleaks. (n.d.). *Gitleaks* [Computer software]. GitHub. https://github.com/gitleaks/gitleaks

Pallets. (n.d.). *Deploying to production*. Flask documentation. https://flask.palletsprojects.com/en/stable/deploying/

Semgrep. (n.d.-a). *CLI reference*. https://docs.semgrep.dev/cli-reference

Semgrep. (n.d.-b). *Sample continuous integration (CI) configurations*. https://docs.semgrep.dev/semgrep-ci/sample-ci-configs
