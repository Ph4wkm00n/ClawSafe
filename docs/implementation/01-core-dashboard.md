# Phase 1: Core Dashboard (v0.1)

Goal: Deliver a working dashboard with risk detection and manual fix guidance.

Covers: FR-1 through FR-8, FR-11, FR-19 (playful only), FR-22, FR-23.

## Tasks

### 1.1 Risk Detection Engine (Backend)

- [x] **Scanner service** (`services/scanner.py`)
  - Detect OpenClaw presence (Docker container / process)
  - Read OpenClaw config file (bind address, enabled skills, mounts)
  - Check network exposure (localhost vs 0.0.0.0, port accessibility)
  - Check authentication status
  - Detect plaintext secrets in config paths
- [x] **Risk scoring** (`services/scoring.py`)
  - Compute per-category scores: Network, Tools & Skills, Data & Files, Updates
  - Compute overall Safety Status: Safe / Needs Attention / At Risk
  - Internal numeric risk score (0-100) for future tuning
- [x] **API endpoints**
  - `GET /api/v1/status` - overall safety status + category breakdown
  - `GET /api/v1/status/{category}` - detailed category info
  - `GET /api/v1/recommendations` - top recommended actions

### 1.2 Activity Tracking (Backend)

- [x] **Activity logger** (`services/activity.py`)
  - Log security-relevant events to SQLite
  - Track: skill changes, network changes, config edits, policy updates
- [x] **API endpoints**
  - `GET /api/v1/activity` - recent activity list (paginated)
- [x] **SQLite schema** (`db/models.py`)
  - `scans` table (timestamp, results JSON, overall status)
  - `activity` table (timestamp, event type, description, severity)
  - `settings` table (key-value for user preferences)

### 1.3 Onboarding Wizard (Frontend)

- [x] Welcome screen with tagline and "Get started" CTA
- [x] Detect setup screen (found / not found OpenClaw)
- [x] Usage questions (home/business, private/public)
- [x] Summary & apply screen with plain-language bullet points
- [x] Completion confirmation screen
- [x] Store onboarding-complete flag in backend settings

### 1.4 Main Dashboard (Frontend)

- [x] **Global status header** - large status chip (Safe/Attention/At Risk) with subtitle
- [x] **Category cards** (Network, Tools & Skills, Data & Files, Updates)
  - Icon, title, status chip, 1-2 sentence explanation
  - Primary action button ("Fix this" / "Review details")
- [x] **Recent activity** list from API
- [x] Auto-refresh on interval (poll every 30s)

### 1.5 Fix Flow (Frontend)

- [x] Modal/side sheet triggered from category cards
- [x] Short explanation of the issue
- [x] "Show me how" section with steps and copy-pastable commands
- [x] (Auto-fix button disabled in v0.1, enabled in v0.2)

### 1.6 Basic Layout & Navigation

- [x] Sidebar navigation: Dashboard, Activity, Advanced Settings, Appearance, About
- [x] Responsive: sidebar collapses to top tabs on mobile
- [x] Playful theme as default (soft teal/blue, rounded cards, warm accents)
- [x] Basic keyboard navigation and focus states

## Acceptance Criteria

- Dashboard shows live safety status from backend scanner
- Each category card shows relevant risk info with plain-language explanations
- Fix flow shows step-by-step manual instructions
- Activity feed shows recent security events
- Onboarding wizard completes and stores preferences
- Works on desktop and mobile viewports
