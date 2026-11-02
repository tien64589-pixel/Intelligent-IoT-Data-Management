# Docker & Container Security Review

## Scope

During the 2026 IoT capstone, the security workstream reviewed Docker build/runtime configuration, Compose settings and selected Docker Scout image vulnerability results.

Relevant repository resources:
- [Docker directory](../../../Docker)
- [docker-compose.yaml](../../../Docker/docker-compose.yaml)
- [Docker frontend build](../../../Docker/Frontend-Dockerfile)
- [Docker backend build](../../../Docker/Backend-Dockerfile)

## Main points documented

1. Earlier Compose configuration embedded literal PostgreSQL credentials; later changes used environment-provided configuration.
2. Docker Scout evidence showed Critical/High findings in several images (including frontend, archived analytics, correlation-alert and backend images).
3. The final capstone report explicitly retained residual container-image risks rather than describing the environment as fully secure.

## Evidence to add (after authorisation)

- Redacted Docker Scout summary by image and scan date.
- Docker Compose before/after excerpts without real secrets.
- Notes on remediation proposals, including image updates, minimal base images, least privilege and re-scanning, **clearly labelled as recommendations unless implemented**.
- Screenshots with identifying information, host paths, credentials and internal infrastructure hidden.

**Do not claim that Docker vulnerabilities were fixed solely because a CodeQL/Semgrep/Gitleaks GitHub Action passed.** These scanners do not replace verified container-image assessment.

*Historical evidence: September 2026 Capstone Final DevSecOps & Container Security Report.*
