# ClawSafe — Future Roadmap

## Current State (v1.1.0)

ClawSafe is a fully functional self-hosted security sidecar for OpenClaw with:
- Safety dashboard with 4-category risk scoring (policy-aware)
- One-click auto-fix with backup/undo
- Onboarding wizard, playful/minimal themes, light/dark modes
- Background scanning with drift detection
- Webhook notifications, Prometheus metrics
- API key authentication, input validation, SSRF protection
- Docker deployment (home, SMB, production with Caddy HTTPS)
- OpenClaw skill integration
- 65 passing tests, structured logging, comprehensive documentation

**Maturity assessment:** Solid v1 for home users and small businesses. Gaps remain in
multi-instance management, enterprise auth, real-time monitoring, vulnerability scanning,
and integration depth.

---

## v1.2 — Operational Depth ✅ RELEASED

**Theme:** Make the existing features genuinely production-robust.

### Real Health & Version Checking
- [x] Live OpenClaw version detection (Docker image inspection)
- [x] Compare against latest release from upstream registry
- [x] Health check includes OpenClaw process/container reachability
- [x] Alert when running versions with known security advisories

### Notification Channels
- [x] Email notifications via SMTP (SendGrid / Mailgun support)
- [x] Slack app integration (formatted Block Kit messages)
- [x] Microsoft Teams webhook support (Adaptive Cards)
- [x] Webhook HMAC signatures for delivery verification
- [x] Do-not-disturb hours configuration
- [x] Digest mode config (daily/weekly interval)
- [x] Notification templates (Jinja2) — customizable message format

### Observability Improvements
- [x] Request latency histogram (`clawsafe_request_duration_seconds`)
- [x] Scan duration tracking (`clawsafe_scan_duration_seconds`)
- [x] Error rate counter per endpoint (`clawsafe_errors_total`)
- [x] Notification counter per channel (`clawsafe_notifications_total`)
- [x] Ship a Grafana dashboard JSON for one-click import
- [x] OpenTelemetry trace context propagation

### Database & Data
- [x] Optional PostgreSQL backend (for HA and multi-instance)
- [x] Configurable data retention (auto-purge scans/activity older than N days)
- [x] Database backup on schedule (SQLite backup endpoint)
- [x] Export activity/scans to CSV/JSON for auditing

### Developer Experience
- [x] `make migrate` command for schema upgrades
- [x] Pre-commit hooks configuration (`.pre-commit-config.yaml`)
- [x] Development seed data command (`make seed`)
- [x] API client SDK (Python package for programmatic access)

---

## v1.5 — Multi-Instance & RBAC ✅ RELEASED

**Theme:** Support teams and small organizations, not just solo users.

### Multi-Instance Dashboard
- [x] Register multiple OpenClaw instances from one ClawSafe deployment
- [x] Per-instance status endpoint (GET /instances/{id}/status)
- [x] Cross-instance risk aggregation (GET /instances/aggregate)
- [x] Instance groups/tags (tags field in instance model)
- [x] Bulk fix operations (apply policy to all instances)
- [x] Instance health timeline (risk score over time)

### Role-Based Access Control
- [x] User accounts with email/password registration
- [x] Three roles: Admin, Security Officer, Viewer
- [x] JWT authentication (login/register/token)
- [x] Audit trail: who changed what, when (audit_log table + API)
- [x] Login page UI
- [x] Per-instance permissions (User A manages prod, User B manages dev)
- [x] API key management UI (create, revoke, set expiry)

### Policy Management
- [x] Policy version history (GET /policy/history)
- [x] Import/export policies as YAML (GET /policy/export)
- [x] Policy inheritance (base policy + per-instance overrides)
- [x] Policy simulation ("what if I activate this policy?")
- [x] Policy templates library

### Frontend Improvements
- [x] WebSocket connection for real-time status updates
- [x] Keyboard shortcuts (R=refresh, D=dashboard, I=instances, A=activity, S=settings)
- [x] Localization infrastructure + Spanish locale
- [x] Audit trail page with filterable table
- [x] Global state management (Zustand) with cross-tab sync
- [x] Scan history timeline chart
- [x] Comparison view (current config vs. recommended)

---

## v2.0 — Security Intelligence ✅ RELEASED

**Theme:** Go beyond configuration checks into real security detection.

### Vulnerability Scanning
- [x] Container image scanning (Trivy integration)
- [x] Secrets scanning in config files and environment (10 regex patterns)
- [x] Custom rule engine (YAML-based detection rules in /rules/ directory)
- [x] Dependency vulnerability checks (CVE cross-referencing for skill packages)
- [x] SBOM generation (Software Bill of Materials)

### Runtime Monitoring
- [x] OpenClaw process monitoring (CPU, memory, status via ps)
- [x] Network connection tracking (active connections via ss)
- [x] File integrity monitoring (SHA-256 hashing + baseline comparison)
- [x] Resource exhaustion alerts (disk + memory threshold monitoring)
- [x] Skill execution auditing (which skills ran, what they accessed)

### Compliance Mapping
- [x] CIS Benchmark mapping (8 controls across 4 categories)
- [x] SOC 2 control coverage report (6 Trust Services Criteria)
- [x] Compliance score dashboard (% of controls met)
- [x] Gap analysis report (failing controls with remediation)
- [x] Evidence collection (auto-capture proof of compliance state)

### Advanced Scoring
- [x] CVSS 3.1-style vector scoring (exploitability × impact × scope)
- [x] Combined risk analysis (correlated patterns worse than sum of parts)
- [x] Risk trends (score over time from scan history)
- [x] Blast radius estimation (affected systems + remediation recommendations)
- [x] Contextual risk weighting (deployment environment detection)

### Integrations Platform
- [x] Plugin SDK (Python base classes for scanners, fixers, notifiers)
- [x] Plugin loader (auto-discovers .py files from /plugins/ directory)
- [x] Plugin listing API (GET /plugins)
- [x] Plugin registry/marketplace
- [x] Sandboxed plugin execution
- [x] Native integrations: PagerDuty, Jira, GitHub Issues

---

## v2.5 — Enterprise Features

**Theme:** Make ClawSafe adoptable by organizations with compliance requirements.

### Enterprise Authentication
- [ ] OAuth 2.0 / OpenID Connect (Google, Azure AD, Okta)
- [ ] SAML 2.0 for enterprise SSO
- [ ] LDAP/Active Directory integration
- [ ] Multi-factor authentication (TOTP, WebAuthn)
- [ ] SCIM provisioning (auto-sync users from identity provider)

### Governance & Workflows
- [ ] Change approval workflows (require 2 approvals before policy change)
- [ ] Scheduled maintenance windows (suppress alerts during planned changes)
- [ ] Incident response playbooks (auto-create ticket → notify on-call → track resolution)
- [ ] Exception management (mark a risk as "accepted" with reason and expiry)
- [ ] SLA tracking (time from detection to remediation)

### Reporting & Analytics
- [ ] Custom dashboard builder (drag-and-drop widgets)
- [ ] Scheduled report generation (PDF/email weekly security summary)
- [ ] Executive dashboard (high-level risk posture for leadership)
- [ ] Cost of inaction estimation ("this misconfiguration costs $X/day in risk exposure")
- [ ] Benchmark comparisons (your security vs. anonymized community average)

### Deployment & Scale
- [ ] Helm chart for Kubernetes deployment
- [ ] Horizontal scaling (stateless API servers + shared PostgreSQL)
- [ ] High availability (active-active with leader election for scheduler)
- [ ] Agent mode (lightweight ClawSafe agent per instance, central console)
- [ ] Air-gapped deployment support (offline vulnerability database)

---

## v3.0 — AI-Native Security (Long-Term Vision)

**Theme:** Leverage AI capabilities that make ClawSafe uniquely positioned.

### Conversational Security
- [ ] Natural language policy authoring ("block all tools that can access the filesystem")
- [ ] AI-powered security advisor ("explain why this is risky in my specific setup")
- [ ] Contextual remediation ("fix this in a way that doesn't break my email automation")
- [ ] Security Q&A via OpenClaw skill ("what changed since yesterday?" "am I compliant with X?")

### Behavioral Analysis
- [ ] ML-based anomaly detection (unusual skill execution patterns)
- [ ] Baseline establishment (learn normal behavior per instance)
- [ ] Drift detection beyond config (behavioral drift in skill usage)
- [ ] Threat pattern recognition (detect known attack sequences)
- [ ] Automated threat correlation (connect events across instances)

### Trust & Verification
- [ ] Skill capability attestation (verify skills only use declared permissions)
- [ ] Output validation (detect if AI outputs contain sensitive data)
- [ ] Prompt injection detection (alert on suspicious inputs to OpenClaw)
- [ ] Data flow tracking (where does user data go through the AI pipeline?)
- [ ] Model integrity checking (detect if underlying models were tampered)

### Community & Ecosystem
- [ ] Open threat intelligence feed (anonymized, opt-in)
- [ ] Community policy library (curated, rated, versioned)
- [ ] Security research integration (academic partnership API)
- [ ] Bug bounty coordination (report vulnerabilities in monitored instances)

---

## SaaS Edition (Parallel Track)

For users who don't want to self-host:

### Phase 1: Cloud Console
- [ ] Hosted ClawSafe dashboard (multi-tenant SaaS)
- [ ] Agent installer for self-hosted OpenClaw instances
- [ ] Encrypted agent-to-cloud communication (mTLS)
- [ ] Free tier (1 instance), paid tiers (10, 50, unlimited)

### Phase 2: Managed Security
- [ ] Managed scanning (ClawSafe scans your instances from the cloud)
- [ ] Managed alerting (email, SMS, Slack from cloud without self-hosting)
- [ ] Managed compliance reporting (auto-generated SOC 2 evidence)
- [ ] Single pane of glass for all instances across teams

### Phase 3: Enterprise SaaS
- [ ] SOC 2 Type II certification for ClawSafe SaaS itself
- [ ] Data residency options (US, EU, APAC)
- [ ] Enterprise support SLAs (24/7, dedicated CSM)
- [ ] Custom integrations (professional services)
- [ ] On-premises deployment option (air-gapped enterprise)

---

## Prioritization Framework

When deciding what to build next, evaluate each item against:

| Factor | Weight | Question |
|--------|--------|----------|
| **User Impact** | High | Does this help Anna (home user) or Ben (SMB)? |
| **Differentiation** | High | Does this make ClawSafe uniquely valuable vs. generic security tools? |
| **Adoption Blocker** | High | Are users requesting this or unable to adopt without it? |
| **Engineering Cost** | Medium | How much effort relative to impact? |
| **Revenue Potential** | Medium | Does this unlock paid tiers or enterprise deals? |
| **Community Growth** | Medium | Does this attract contributors or users? |

### Highest-Impact Next Steps (Recommended Order)

1. **Email notifications** — most-requested feature for non-technical users
2. **Multi-instance support** — unlocks SMB team adoption
3. **PostgreSQL backend** — enables HA and multi-instance
4. **RBAC with user accounts** — required for any team usage
5. **Real-time WebSocket updates** — biggest UX improvement
6. **Container/CVE scanning** — biggest security depth improvement
7. **Plugin SDK** — opens community contributions
8. **Helm chart** — unlocks Kubernetes-native adoption
