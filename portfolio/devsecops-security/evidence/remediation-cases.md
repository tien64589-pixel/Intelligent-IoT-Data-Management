# Security Remediation Case Studies

These are **documented team-capstone changes**. The linked commits exist in the project repository; contribution/ownership should be described accurately in interviews rather than assuming sole authorship.

| Finding | Change documented | Commit |
| --- | --- | --- |
| Missing API rate limiting | Added API limiter plus stricter auth limiter | [f8e89f2](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/f8e89f2) |
| User-controlled upload path | Sanitised CSV filenames and validated upload directory containment | [8d4a628](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/8d4a628) |
| Flask debug mode | Disabled `debug=True` for archived services | [9924a96](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/9924a96) |
| Literal database credentials in Compose | Moved password configuration to environment variables, provided example env file | [74ccd2d](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/74ccd2d) |
| Mutable GitHub Actions references | Pinned selected action dependencies to full SHAs | [64fa8fe](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/64fa8fe) |
| Broad Flask network binding | Safer default `127.0.0.1` binding, with explicit override where required | [0fa63ae](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/0fa63ae) |

## Case study 1 — API rate limiting

**Issue:** Some routes lacked controls against rapid or repeated requests.  
**Risk:** Automated abuse, high request volume or attempts against authentication endpoints.  
**Change:** API-wide and stronger authentication-specific rate limits were introduced.  
**Verification:** The capstone report notes successful subsequent CodeQL execution and that related alerts no longer appeared on the final open list.  
**Remaining limitation:** Rate limiting reduces exposure, but it does not independently prove resistance to denial-of-service or credential attacks.

## Case study 2 — CSV upload path validation

**Issue:** User-controlled filenames were used in filesystem paths.  
**Risk:** Invalid file paths and potentially unsafe path traversal.  
**Change:** Filename sanitisation, CSV restriction and upload-directory containment validation.  
**Verification:** Follow-up CodeQL scans completed; related alerts were no longer listed in the reported final snapshot.  
**Remaining limitation:** File validation, file size limits and end-to-end abuse cases still need testing.

## Case study 3 — Docker credentials

**Issue:** Database passwords appeared literally in an earlier Compose configuration.  
**Risk:** Exposure of credentials in configuration and version control.  
**Change:** Environment-supplied password configuration plus `.env.example`.  
**Verification:** The report indicates the original literals were removed from the current Compose configuration.  
**Remaining limitation:** Environment variables are not a substitute for credential rotation, secrets management or Git history review.

## What I learned

Security scanning is only the first step: verify a finding, assess context, make a focused change, rerun checks and document any residual risks. A passing CI workflow is an execution result, not proof of comprehensive security.
