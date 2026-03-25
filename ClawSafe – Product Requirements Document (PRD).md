# ClawSafe – Product Requirements Document (PRD)

## 1. Product Overview

**Product name:** ClawSafe  
**Tagline:** Keeps your AI helper safe at home, no IT degree needed.

ClawSafe is a self-hosted security sidecar for OpenClaw that makes it easy for home users and small businesses to **secure, monitor, and understand** their OpenClaw instances. It ships as:

- A self-hosted web dashboard + daemon.
- An optional OpenClaw skill for in-chat security checkups.
- An optional (future) SaaS console for cloud-based notifications and multi-device overview.

The primary UX is designed for **non-technical home users**, with an **Advanced Settings** area for “SMB owner with a tech-y friend / part-time DevOps”. Visual style defaults to **playful & cozy** with a mascot, but can be switched to a **minimal, utility-style UI** and supports full dark mode.[web:41][web:43]

---

## 2. Goals & Non-Goals

### 2.1 Goals

1. **Secure-by-default OpenClaw for home & SMB**  
   Provide a one-command install that deploys OpenClaw + ClawSafe with hardened defaults.[web:41][web:32]

2. **Friendly, understandable security for non-tech users**  
   Explain risks in plain language and always offer a clear next step.[web:43][web:54]

3. **Useful knobs for infra/DevOps people**  
   Expose detailed configuration and integrations under Advanced Settings without overwhelming casual users.[web:44][web:60]

4. **Low-friction open source adoption**  
   Make installation and contributions straightforward via GitHub, with templates and examples for common setups.[web:46][web:49]

### 2.2 Non-Goals (v1)

- Full-blown enterprise SIEM or SOC platform.  
- Deep offensive security tooling (active pentesting suite).  
- Managing non-OpenClaw services beyond basic host-level checks.  
- Multi-tenant enterprise tenancy (may be future roadmap).[web:48]

---

## 3. Target Users

### 3.1 Primary Personas

1. **Non-technical home user (“Anna”)**

- Runs OpenClaw for personal automation, home assistant, and media tasks.[web:34][web:47]
- Wants reassurance that “my AI isn’t opening my whole network to hackers”.[web:43]
- Comfortable installing Docker or running a simple script with guidance.[web:46]

2. **Tech-savvy SMB owner / part-time DevOps (“Ben”)**

- Runs OpenClaw for small business workflows (email triage, basic ops automation).[web:28]
- Understands Docker, basic networking, Git, and wants policy-as-code & logs.[web:32][web:41]
- Wants a tool that saves time and provides guardrails while staying lightweight.[web:44]

### 3.2 Secondary Personas

- Home-lab / self-hosting enthusiasts who want a secure, polished companion for OpenClaw.[web:27]
- Security-conscious power users evaluating OpenClaw risk for their small team.[web:43]

---

## 4. Key Use Cases

1. **First-time secure install**

- User just discovered OpenClaw and wants to install it “the safe way” with minimal decisions.[web:41][web:46]
- ClawSafe script/compose sets up OpenClaw bound to localhost, minimal tools, and a basic firewall profile.[web:43]

2. **Existing OpenClaw install checkup**

- User already runs OpenClaw and installs ClawSafe to audit the current setup.[web:32]
- ClawSafe scans config, ports, tools, and filesystem mounts; then provides a simple dashboard with a safety grade and recommended fixes.[web:41]

3. **Ongoing safety monitoring**

- ClawSafe watches for dangerous changes: new public exposure, new privileged skills, or unusual actions.[web:32][web:57]
- Sends occasional notifications or weekly summary that “things look safe” or “something changed”.[web:48]

4. **DevOps / SMB tuning and integration**

- Power user opens Advanced Settings to configure detailed policy, logging, and alerting.[web:41][web:60]
- Exports metrics to Prometheus/Grafana and logs to Loki/ELK or similar.[web:36][web:44]

5. **In-chat security checkup via OpenClaw skill**

- User asks OpenClaw: “Is it safe right now?”[web:1]
- Skill calls ClawSafe API and replies with a plain-language summary plus suggestions.[web:8]

---

## 5. Functional Requirements

### 5.1 Deployment & Installation

- **FR-1:** Provide a one-command installation (e.g., script or make target) that:
  - Installs or updates ClawSafe container(s).
  - Sets up OpenClaw with recommended defaults, or attaches to an existing OpenClaw deployment.[web:46][web:30]

- **FR-2:** Provide Docker Compose files:
  - `docker-compose.yml` with default secure settings.
  - `docker-compose.home.yml` optimized for home setups.
  - `docker-compose.smb.yml` optimized for small business setups.[web:41][web:32]

- **FR-3:** Support self-hosted deployment on Linux (Debian/Ubuntu first), easily adaptable to other hosts.[web:46]

### 5.2 Risk Detection & Scoring

- **FR-4:** Detect whether OpenClaw is:
  - Exposed to the public internet.
  - Bound to localhost vs all interfaces.
  - Protected with authentication / tokens.[web:41][web:43]

- **FR-5:** Inspect OpenClaw configuration for:
  - Enabled skills/tools and their categories (safe/sensitive/privileged).
  - Filesystem mounts and directories accessible.
  - Presence of obvious plaintext secrets in config or known paths.[web:32][web:57]

- **FR-6:** Compute an overall **Safety Status**:
  - `Safe`, `Needs Attention`, `At Risk`.
  - Provide a numeric “risk score” internally for future tuning.[web:48]

- **FR-7:** Provide category-specific card scores: Network, Tools & Skills, Data & Files, Updates.[web:41]

### 5.3 Recommended Actions & Auto-Fix

- **FR-8:** For each major risk, provide:
  - Plain-language explanation.
  - One-click “Fix this for me” (auto-apply safe changes where possible).
  - “Show me how” with command snippets or step-by-step guide.[web:43][web:54]

- **FR-9:** Support auto-fix for:
  - Binding OpenClaw to localhost or private interfaces.
  - Disabling high-risk skills by default.
  - Enabling or tightening authentication.[web:41][web:32]

- **FR-10:** Changes must be logged and reversible where feasible (e.g., backup of previous config).[web:41]

### 5.4 Monitoring & Alerts

- **FR-11:** Track and display recent OpenClaw actions and changes relevant to security, such as:
  - New skills added/enabled.
  - New network bindings or port changes.
  - Elevated file or shell activity.[web:32][web:57]

- **FR-12:** Schedule periodic re-scans (e.g., hourly/daily) and detect configuration drift.[web:49]

- **FR-13:** Offer basic notifications:
  - Email or webhook when risk level escalates (e.g., Safe → At Risk).
  - Weekly safety summary (opt-in).[web:48]

### 5.5 Advanced Settings (SMB / DevOps)

- **FR-14:** Provide an Advanced Settings pane with:
  - Network: bind address, allowed CIDRs, VPN-only toggles.
  - Skills/Tools: per-skill allow/deny, risk tags, interactive confirmation settings.
  - Data: mount paths, backup options, log destinations.[web:41][web:60]

- **FR-15:** Support **policy-as-code**, stored as YAML:
  - Per-instance policy file with clear version and comments.
  - CLI or API to validate and apply policies.[web:41][web:49]

- **FR-16:** Integrations:
  - Metrics endpoint (Prometheus-compatible).
  - Logs to stdout/file in structured format (for Loki/ELK).
  - Webhook configuration (Slack/Discord/others) for important events.[web:36][web:44]

### 5.6 OpenClaw Skill Integration

- **FR-17:** Expose an internal API for:
  - Getting current Safety Status and explanation.
  - Listing top 3 recommended actions.[web:1]

- **FR-18:** Provide a reference OpenClaw skill that:
  - Answers questions like “Is it safe?” and “How do I make it safer?”.
  - Summarizes status in non-technical language.[web:8]

### 5.7 Theming & Modes

- **FR-19:** Support **two visual styles**:
  - Playful (default): mascot, illustrations, rounded cards.
  - Minimal: clean, utility style, no mascot or extra visuals.[web:62][web:61]

- **FR-20:** Support **Light / Dark modes**:
  - Auto (match system).
  - Light.
  - Dark.[web:70][web:72]

- **FR-21:** Provide a unified theme token system so both styles & modes share structure.[web:68]

### 5.8 Localization & Accessibility (v1 Minimum)

- **FR-22:** English-only UI at launch, but store strings in a way that can be localized later.[web:60]
- **FR-23:** Basic accessibility:
  - Keyboard navigable.
  - Sufficient color contrast in both Light and Dark modes.[web:72][web:76]

---

## 6. Non-Functional Requirements

- **NFR-1:** Self-hosted components must run efficiently on modest hardware (e.g., low-end VPS or home server).[web:46]
- **NFR-2:** Backend and UI should be stateless where reasonable; configuration saved to files or a small local DB.[web:60]
- **NFR-3:** No telemetry without explicit opt-in.[web:48]
- **NFR-4:** Clear and easy upgrade path (e.g., via Docker image tags and simple migration steps).[web:46]

---

## 7. UX Design Spec (High-Level)

### 7.1 Key Screens

1. **Onboarding / Setup Wizard**

- Step 1: Welcome + short description (“Protect your OpenClaw in a few clicks”).
- Step 2: Detect existing OpenClaw or set up a new one.
- Step 3: Ask 2–3 simple questions:
  - “Do you want OpenClaw accessible from outside your home?” (Yes/No/Not Sure).
  - “Is this for home or business?” (Home/Small business).
- Step 4: Summary page (“We will: keep it private, remove risky tools, enable a password…”).[web:50][web:41]

2. **Main Dashboard**

- Top section: Big status indicator (Safe / Needs Attention / At Risk).
- Subsections as cards (Network, Tools & Skills, Data & Files, Updates):
  - Each card shows a short summary and a primary action (Fix / Review).
- Recent Activity: list of notable events.[web:54][web:56]

3. **Details / Fix Flow**

- For each risk card, clicking “Fix this” opens a modal or side panel:
  - Short explanation.
  - “Fix automatically” button.
  - “Show me how” with hints/commands.[web:54][web:61]

4. **Advanced Settings**

- Visible link: "Advanced settings (for power users)" from dashboard.
- Tabbed layout: Network, Tools & Skills, Data & Files, Integrations.
- Each setting with label, short description, and optional “What this really means” tooltip.[web:55][web:60]

5. **Theme & Appearance Settings**

- Options:
  - Visual style: Playful / Minimal.
  - Mode: Match system / Light / Dark.
- Preview thumbnails for styles.[web:68][web:71]

### 7.2 Playful vs Minimal Visuals

- **Playful**:
  - Mascot in header or side, reacting to safety state.
  - Soft gradients, warm accent colors, rounded cards.
  - Occasional micro-animations (status changes, hover effects).[web:62][web:83]

- **Minimal**:
  - Flat background, minimal gradients.
  - Subtle borders and hierarchy, more whitespace.
  - Mascot hidden or reduced to a small icon.[web:61][web:75]

### 7.3 Tone & Copy

- Use plain language:
  - “People outside your home can reach your AI. This makes hacking easier.”
  - “We recommend keeping it private unless you know how to protect it with a VPN.”[web:43][web:41]

- Every alert should include a next step:
  - “Fix this now” or “Ask a tech friend to check this page.”[web:54][web:56]

---

## 8. Tech Stack (Proposed)

- **Backend:** Go or Python (FastAPI) – lightweight API server.[web:44]
- **Frontend:** React / Next.js (or similar), built as a single-page app served by backend.[web:61]
- **Packaging:** Docker images + Docker Compose.[web:46]
- **Config:** YAML/JSON files for policies and settings.[web:41][web:49]

(Final choices can be refined based on your preferences.)

---

## 9. Roadmap (High-Level)

- **v0.1:** Core self-hosted dashboard, basic risk detection, manual fixes.
- **v0.2:** Auto-fix paths, theme toggle, light/dark mode, initial Advanced Settings.
- **v0.3:** OpenClaw skill integration, basic email/webhook alerts.
- **v1.0:** Polished UX, documentation, example configs, and first stable release.[web:48]
