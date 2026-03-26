# Phase 2: Auto-Fix & Themes (v0.2)

Goal: Enable one-click fixes, add theme switching, and build Advanced Settings.

Covers: FR-9, FR-10, FR-14, FR-15, FR-19, FR-20, FR-21.

## Tasks

### 2.1 Auto-Fix Engine (Backend)

- [ ] **Fixer service** (`services/fixer.py`)
  - Bind OpenClaw to localhost (modify config + restart)
  - Disable high-risk skills by default
  - Enable/tighten authentication
- [ ] **Config backup** before every fix (`services/backup.py`)
  - Save timestamped copy of config
  - Store backup metadata in SQLite
- [ ] **Undo support** - restore from backup
- [ ] **API endpoints**
  - `POST /api/v1/fix/{action_id}` - apply a specific fix
  - `POST /api/v1/fix/{action_id}/undo` - undo a fix
  - `GET /api/v1/backups` - list config backups

### 2.2 Policy-as-Code (Backend)

- [ ] **Policy loader** (`services/policy.py`)
  - Parse and validate YAML policy files
  - Apply policy to OpenClaw config
- [ ] **API endpoints**
  - `GET /api/v1/policy` - current active policy
  - `PUT /api/v1/policy` - update policy
  - `POST /api/v1/policy/validate` - validate without applying

### 2.3 Advanced Settings (Frontend)

- [ ] Entry point: "Advanced settings (for power users)" link on dashboard
- [ ] **Network tab** - bind address, allowed CIDRs, VPN-only toggle
- [ ] **Tools & Skills tab** - skill table with risk level + status toggles
- [ ] **Data & Files tab** - mount paths with risk badges, backup options
- [ ] **Integrations tab** - placeholder for v0.3 (metrics, logs, webhooks)
- [ ] "What this really means" tooltips on each setting

### 2.4 Theme System (Frontend)

- [ ] **Design token system** using CSS custom properties
  - Shared token structure for both themes and modes
  - Tokens: colors, spacing, radii, shadows, typography
- [ ] **Playful theme** - soft gradients, warm accents, large radii, mascot visible
- [ ] **Minimal theme** - flat surfaces, muted colors, small radii, no mascot
- [ ] **Light/Dark mode** - auto (system), light, dark
- [ ] **Appearance settings page** with preview thumbnails
- [ ] Persist theme choice in backend settings API

### 2.5 Fix Flow Upgrade (Frontend)

- [ ] Enable "Fix automatically" button (calls auto-fix API)
- [ ] Show progress indicator during fix
- [ ] Success/failure confirmation
- [ ] "Undo last change" button

## Acceptance Criteria

- One-click fixes work for network binding, skill disabling, auth tightening
- Config is backed up before each fix; undo restores previous state
- Advanced Settings allows per-skill policies, network config, data mount review
- Theme toggle switches between Playful and Minimal without layout changes
- Light/Dark mode works in both themes with correct contrast
- Policy YAML can be validated and applied via API
