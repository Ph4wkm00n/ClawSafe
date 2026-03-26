# Main Dashboard

## Layout

```
┌─────────────────────────────────────────┐
│  Sidebar  │  Global Status Header       │
│           │─────────────────────────────│
│  - Dash   │                             │
│  - Activity│  ┌─────────┐ ┌─────────┐  │
│  - Settings│  │ Network │ │ Tools & │  │
│  - Theme  │  │  Card   │ │ Skills  │  │
│  - About  │  └─────────┘ └─────────┘  │
│           │  ┌─────────┐ ┌─────────┐  │
│           │  │ Data &  │ │ Updates │  │
│           │  │  Files  │ │ & Health│  │
│           │  └─────────┘ └─────────┘  │
│           │─────────────────────────────│
│           │  Recent Activity            │
└─────────────────────────────────────────┘
```

## Global Status Header

Large, prominent section at top of content area.

**States:**

| Status | Color | Icon | Subtitle |
|--------|-------|------|----------|
| Safe | Green (`--color-status-safe`) | Shield check | "Your AI helper looks well protected." |
| Needs Attention | Amber (`--color-status-attention`) | Shield alert | "Some things could be safer. We'll show you how." |
| At Risk | Red (`--color-status-risk`) | Shield warning | "Important risks found. Please review these now." |

- Status chip: pill-shaped, large text, bold
- Mascot reacts to state (Playful mode only):
  - Safe: relaxed/smiling
  - Attention: concerned look
  - At Risk: holding shield, alert pose

## Category Cards

2x2 grid (stacks to single column on mobile).

### Card Structure

```
┌──────────────────────────────┐
│  🔒 Network         [Safe]  │
│                              │
│  "Only reachable from this   │
│   machine. Nice and private."│
│                              │
│         [Review details]     │
└──────────────────────────────┘
```

Each card contains:
- **Icon** (left) + **Title** (bold)
- **Status chip** (right) - same colors as global status
- **1-2 sentence explanation** in plain language
- **Primary button:**
  - Safe: "Review details" (secondary style)
  - Needs Attention/At Risk: "Fix this for me" (primary style)

### Card Content by Category

**Network**
- Safe: "Only reachable from this machine. Nice and private."
- Attention: "OpenClaw might be reachable from your local network."
- Risk: "People outside your home can reach OpenClaw. This makes hacking easier."
- Action (risk): "Make it private"

**Tools & Skills**
- Safe: "Only safe abilities are turned on."
- Attention: "Some powerful abilities are enabled. Review if you need them."
- Risk: "High-risk abilities are active (e.g., shell access). This is dangerous unless you know why."
- Action (risk): "Review abilities"

**Data & Files**
- Safe: "OpenClaw can only see the folders it needs."
- Attention: "Some broad folder access detected. Consider limiting it."
- Risk: "OpenClaw can access sensitive areas of your system."
- Action (risk): "Limit access"

**Updates & Health**
- Safe: "Everything is up to date."
- Attention: "An update is available."
- Risk: "You're running an old version with known security issues."
- Action (risk): "See update guide"

## Recent Activity

Below the cards. Simple list, most recent first.

```
│ 🟡 10:32 AM  New skill 'shell_exec' enabled         │
│ 🟢  9:15 AM  Policy updated by user ben             │
│ 🔴  Yesterday Port changed from 127.0.0.1 to 0.0.0.0│
```

- Severity dot (green/amber/red) + timestamp + description
- "View all activity" link at bottom (goes to Activity page)
- Shows last 5 items by default

## Refresh Behavior

- Auto-poll backend every 30 seconds
- Manual refresh button in status header
- Visual indicator when data is stale (>60s)
