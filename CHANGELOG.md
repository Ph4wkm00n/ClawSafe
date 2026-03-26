# Changelog

## [2.0.0] - 2026-03-26

### Added
- Secrets scanning (10 regex patterns for AWS, GitHub, JWT, private keys, DB URLs)
- Custom YAML rule engine for organization-specific detection rules
- Runtime monitoring (process, network connections, file integrity, resource alerts)
- CIS Benchmark (8 controls) and SOC 2 (6 criteria) compliance mapping
- Compliance score dashboard and gap analysis with remediation guidance
- CVSS 3.1 base score computation with vector components
- Combined risk analysis (correlated patterns worse than sum of parts)
- Risk trends from scan history and blast radius estimation
- Plugin SDK (ScannerPlugin, FixerPlugin, NotifierPlugin base classes)
- Plugin auto-discovery from /plugins/ directory
- 13 new security intelligence API endpoints
- Slack Block Kit and Microsoft Teams Adaptive Card webhook formatting
- Webhook HMAC-SHA256 signatures for delivery verification
- Do-not-disturb hours and digest mode for notifications
- Request latency histogram and scan duration tracking (Prometheus)
- Grafana dashboard JSON with 9 panels
- Data retention purge, scheduled backup, CSV/JSON export APIs
- Multi-instance aggregation and per-instance status endpoints
- User accounts with JWT authentication and RBAC (3 roles)
- Audit trail with user/action/resource tracking
- Login page with registration support
- Policy version history and YAML export
- Keyboard shortcuts (R/D/I/A/S)
- Spanish locale foundation for i18n
- PostgreSQL support with connection pooling
- Database abstraction layer with migration system
- Helm chart for Kubernetes deployment
- Container/CVE scanning via Trivy integration

### Security Hardening
- PBKDF2-SHA256 password hashing (100k iterations, replaces SHA-256)
- JWT secret no longer falls back to hardcoded value
- Auth bypass prevented (require API key unless debug mode)
- SQL injection prevention via column whitelist in dynamic queries
- Config path validation prevents path traversal in instance management
- Secrets scanner file size limits and symlink-safe directory walking
- Auto-rollback on fix failure (restores backup automatically)
- Security endpoints require authentication
- Audit endpoint requires authentication
- Caddy security headers (HSTS, X-Frame-Options, X-Content-Type-Options)
- Helm security contexts (runAsNonRoot, drop ALL capabilities)
- Production/dev requirements split (requirements.txt + requirements-dev.txt)
- Pre-commit hooks (.pre-commit-config.yaml)

### Changed
- Version bumped to 2.0.0
- App version updated throughout (main.py, schemas.py)

## [1.1.0] - 2026-03-26

### Added
- API key authentication for all write endpoints
- Input validation (action IDs, webhook URLs) preventing path traversal and SSRF
- Structured JSON logging with configurable log level
- Real health check (DB connectivity + scheduler status verification)
- Policy-aware scoring: risk adjustments based on active policy rules
- Prometheus metrics actually populated during scheduled scans
- Scheduler exponential backoff on repeated failures
- Onboarding wizard connected to dashboard (shows on first visit, saves to API)
- Theme flash prevention via localStorage + inline head script
- Settings tabs save to policy API with debounced auto-save and toast feedback
- Focus trap in SideSheet modal for keyboard accessibility
- Toast notification system with role="alert" for screen readers
- Severity text labels on activity dots (not color-only)
- Error boundary (error.tsx) for graceful component crash recovery
- Polling backoff (30s → 300s) on API failures
- Non-root Docker containers with health checks and resource limits
- Production Docker overlay with Caddy reverse proxy (auto HTTPS)
- Makefile for one-command install/dev/test/build/prod
- Security documentation (auth, HTTPS, SSRF protection)
- Operations documentation (backup/restore, upgrades, monitoring, troubleshooting)
- CI: test coverage thresholds, Trivy container scanning
- Scanner and scoring edge case tests

### Changed
- CORS restricted to explicit methods/headers
- Demo data only seeded when CLAWSAFE_DEMO_MODE=true
- Backup retention auto-cleanup at 50 backups
- Settings page loads policy from API instead of using hardcoded data

## [1.0.0] - 2026-03-26

### Added
- UX polish: loading skeletons, empty/error states, mascot illustrations
- Accessibility: skip-to-content link, focus-visible outlines, ARIA labels
- Comprehensive documentation (installation, configuration, API reference, contributing)
- Additional test coverage for all components

## [0.3.0] - 2026-03-26

### Added
- Background scan scheduler with configurable interval
- Webhook notifications for risk escalation events
- Prometheus metrics endpoint (`/metrics`)
- OpenClaw skill integration (plain-language safety queries)
- Scan history tracking and API endpoint
- Integrations tab in Advanced Settings (metrics, webhooks, email)

## [0.2.0] - 2026-03-26

### Added
- One-click auto-fix engine for network, tools, data, and auth
- Config backup and restore with undo support
- Policy-as-code with YAML validation and management
- Advanced Settings page with 4 working tabs (Network, Tools, Data, Integrations)
- SettingRow component with "What this really means" tooltips

## [0.1.0] - 2026-03-26

### Added
- Initial release: FastAPI backend with security scanner and risk scoring
- Next.js frontend with dashboard, category cards, and activity feed
- Onboarding wizard (4-step setup flow)
- Fix flow with step-by-step manual instructions
- Design token system with Playful/Minimal themes and Light/Dark modes
- Docker Compose deployment with home and SMB overlays
- YAML policy files (default, home, SMB examples)
- GitHub Actions CI pipeline
