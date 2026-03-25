# ClawSafe

> Keeps your AI helper safe at home, no IT degree needed.

ClawSafe is a self-hosted security sidecar for [OpenClaw](https://openclaw.ai) that helps home users and small businesses **secure, monitor, and understand** their OpenClaw instances.[web:41][web:43] It gives you friendly, plain-language guidance by default, plus powerful **Advanced Settings** for tech-savvy users.

- ✅ Secure-by-default install for OpenClaw  
- ✅ Simple dashboard for non-technical users  
- ✅ Advanced policy & integrations for “SMB owner with a tech-y friend / part-time DevOps”[web:41][web:32]

---

## Features

- **Secure install wizard**  
  One-command setup that deploys OpenClaw + ClawSafe with hardened defaults (localhost binding, minimal risky tools, recommended auth).[web:41][web:46]

- **Friendly safety dashboard**  
  Clear status (“Safe / Needs Attention / At Risk”) and category cards for Network, Tools & Skills, Data & Files, Updates.[web:54][web:56]

- **One-click fixes & guides**  
  For each risk, ClawSafe can auto-fix common issues or show you easy step-by-step instructions with copy-pastable commands.[web:43]

- **Advanced Settings for power users**  
  Configure network rules, per-skill policies, data mounts, logging, and webhooks using a clean UI and YAML-based policy-as-code.[web:41][web:49]

- **OpenClaw skill integration**  
  Ask your agent “Is it safe?” and get a plain-language security summary powered by ClawSafe’s internal API.[web:1][web:8]

- **Playful & minimal themes, light & dark**  
  Choose a cozy, mascot-driven look or a minimal utility style, both with light/dark mode and good contrast.[web:68][web:70]

---

## Who Is It For?

ClawSafe is primarily designed for:

- 🏠 **Home users** running OpenClaw for personal automation, home assistant, or media tasks.  
- 🧑‍💼 **Small businesses** using OpenClaw for email, docs, or simple ops automation.[web:28][web:34]

If you know enough to install Docker but don’t want to become a security engineer, ClawSafe is built for you.[web:46][web:43]

---

## Quick Start

> **Note:** v0.1 is pre-release; details may change.

### 1. Requirements

- Linux host (Debian/Ubuntu recommended)  
- Docker + Docker Compose installed  
- An existing OpenClaw instance **or** willingness to install a new one[web:41][web:46]

### 2. Install via Docker Compose

Clone the repo:

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
