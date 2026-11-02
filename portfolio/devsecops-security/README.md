# DevSecOps & Container Security — Capstone Evidence Portfolio

**Student:** Ngoc Tien Nguyen (Tommy)  
**University:** Deakin University · Bachelor of Cyber Security  
**Project:** Intelligent IoT Data Management Platform (team capstone, 2026)  
**My workstream:** DevSecOps & Container Security  
**Goal:** Demonstrate practical security testing, remediation, risk documentation and collaborative development for IT/Cyber Security placements.

> This is a portfolio of my documented contribution to a **team project**, not a claim that I built the whole platform. The source system is maintained in the [team project repository](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management). Evidence here records the **September 2026 assessment snapshot**, not a guarantee of the current security state.

## What I worked on

- Reviewed DevSecOps requirements, secure coding expectations and security risks.
- Used **CodeQL** and **Semgrep** for code scanning and **Gitleaks** for secret detection.
- Reviewed Docker configuration and container vulnerability findings.
- Supported targeted security remediation and documented the before/after evidence.
- Prepared security findings, risk assessments, recommendations and verification notes.

## Security workflow evidence

| Tool | Purpose | Project workflow |
| --- | --- | --- |
| CodeQL | Static/code-flow analysis | [codeql.yml](../../.github/workflows/codeql.yml) |
| Semgrep | Rule-based code scanning | [semgrep.yml](../../.github/workflows/semgrep.yml) |
| Gitleaks | Potential secret detection | [gitleaks.yml](../../.github/workflows/gitleaks.yml) |

[Detailed evidence and limitations](evidence/scan-results.md)

### Recorded outcomes — September 21, 2026

The final capstone evidence report recorded:
- Semgrep blocking findings reduced **7 → 0** during the remediation cycle (for the configured rules and snapshot).
- The *overall code scanning view* changed from **32 open alerts** at baseline to **10 open / 24 closed** at the final snapshot. These are UI snapshots, **not** a claim that exactly 22 unique vulnerabilities were eliminated.
- The *CodeQL-only view* was recorded as **10 open / 15 closed** in the final snapshot.
- CodeQL, Semgrep and Gitleaks workflows succeeded for the recorded push at commit [0fa63ae](https://github.com/tien64589-pixel/Intelligent-IoT-Data-Management/commit/0fa63ae).

**Important update (October 12, 2026):** The later scheduled **Gitleaks** run reported **one potential leak** and failed. This requires review and cannot be described as a clean current scan. See [current limitations](evidence/scan-results.md).

## Examples of security improvements

I documented and reviewed changes including API rate limiting, uploaded filename/path validation, Flask debug configuration, Docker Compose credential handling, workflow action pinning and safer Flask bind defaults.

See [remediation cases](evidence/remediation-cases.md), including verified commit links and the limits of each finding.

## Docker and residual risks

Docker Scout/image findings and deployment configuration review were part of the assessment. The final capstone report still recorded residual container-image and CodeQL risks; **passing workflows do not establish that the system is vulnerability-free**.

See [container security review](evidence/docker-review.md).

## Skills demonstrated

**Security:** static analysis, secret scanning, vulnerability triage, risk reporting, remediation verification  
**Tools:** GitHub Actions, CodeQL, Semgrep, Gitleaks, Docker, Kali Linux  
**Collaboration:** review findings, communicate fixes, record residual risks, explain security trade-offs

## Evidence navigation

- [Security scan snapshots](evidence/scan-results.md)
- [Remediation case studies](evidence/remediation-cases.md)
- [Docker and container review](evidence/docker-review.md)
- [Publication checklist / evidence boundaries](evidence/publication-checklist.md)

## Notes on attribution and disclosure

This was a university **team** project. My portfolio describes the security workstream, and links to existing project commits and scan runs. It does not imply sole authorship of every changed line. Screenshots and internal documents will be added only if sharing is authorised and potentially sensitive information has been removed.

*Evidence snapshot: 21 September 2026. Repository checks noted as of 12 October 2026. For current status, examine the live Actions and security findings.*
