# Automated Security Scanning — Evidence

## Workflow configurations

- [CodeQL workflow](../../../.github/workflows/codeql.yml)
- [Semgrep workflow](../../../.github/workflows/semgrep.yml)
- [Gitleaks workflow](../../../.github/workflows/gitleaks.yml)

These workflows are configured on the `main` branch; presence or a green job verifies execution, **not** zero vulnerabilities.

## Historical evidence snapshot (21 September 2026)

| Area | Earlier snapshot | Reported final snapshot | Limitations |
| --- | --- | --- | --- |
| Semgrep | 7 blocking findings | 0 findings, 0 blocking | Applies only to configured rules and that specific scan |
| Overall GitHub code-scanning UI | 32 open alerts | 10 open / 24 closed alerts | Counts can vary by date, branch, rule and alert state |
| CodeQL-only UI | Findings including rate-limiting, paths and debug configuration | 10 open / 15 closed | Residual alerts remained |
| Gitleaks | No secrets detected in recorded successful run | Successful on September 21 push | Later scheduled scan failed; do not claim current clean result |

### Links to representative historical runs

- [Semgrep successful run (September 21)](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/35622997202)
- [CodeQL successful run (September 21)](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/35622997035)
- [Gitleaks successful run (September 21)](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/35622997082)

## More recent review (12 October 2026)

- [CodeQL scheduled run: success](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/38236378486)
- [Semgrep scheduled run: success](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/38235405556)
- [Gitleaks scheduled run: failed](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/actions/runs/38237006112)

The October 12 Gitleaks job log reports **"leaks found: 1"**. It has not been assessed here whether the match is a real credential, sample value, or false positive. Do **not** publish the matching value, file content, or raw scan artifact. The authorised project maintainers should review the finding in a restricted setting and rotate/revoke any genuinely exposed credential.

## Before/after screenshots — not yet attached

Only add screenshots you are authorised to publish and have sanitised. Suggested names:

- `screenshots/semgrep-baseline.png`
- `screenshots/semgrep-final-2026-09-21.png`
- `screenshots/code-scanning-final-2026-09-21.png`

Never invent screenshots or attach secret-bearing logs.

**Source of historical figures:** the student's *Final DevSecOps & Container Security Report*, evidence snapshot 21 September 2026.
