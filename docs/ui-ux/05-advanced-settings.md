# Advanced Settings

## Entry Point

Link on dashboard: "Advanced settings (for power users)" - styled as a subtle
text link, not a prominent button. Visible but not distracting for casual users.

## Layout

Tabbed interface within the main content area.

```
┌──────────────────────────────────────────┐
│  Advanced Settings                       │
│                                          │
│  [Network] [Tools] [Data] [Integrations] │
│  ─────────────────────────────────────── │
│                                          │
│  Setting rows...                         │
│                                          │
└──────────────────────────────────────────┘
```

## Tab: Network

| Setting | Control | Description |
|---------|---------|-------------|
| Bind address | Dropdown: `127.0.0.1` / `0.0.0.0` / Custom | Which network interfaces OpenClaw listens on |
| Allowed CIDRs | Chip input (multi-value) | IP ranges allowed to connect |
| VPN-only mode | Toggle | Only allow connections through VPN |
| Port | Number input | Port OpenClaw listens on |

## Tab: Tools & Skills

Table layout:

| Skill Name | Risk Level | Status | Actions |
|------------|-----------|--------|---------|
| web_search | Low | Allowed | [Dropdown: Allowed/Ask/Blocked] |
| file_read | Medium | Ask | [Dropdown] |
| shell_exec | High | Blocked | [Dropdown] |

- Risk level shown as colored badge (green/amber/red)
- "Ask" means user confirmation required before skill executes
- Bulk actions: "Block all high-risk" button at top

## Tab: Data & Files

| Setting | Control | Description |
|---------|---------|-------------|
| Mount paths | List with risk badges | Directories OpenClaw can access |
| Backup enabled | Toggle | Auto-backup config on changes |
| Backup frequency | Dropdown: hourly/daily/weekly | How often to back up |
| Backup destination | Text input | Path for backup storage |
| Log destination | Text input | Where to write activity logs |

Each mount path shows:
- Path (e.g., `/home/user/documents`)
- Risk badge (green: safe scope, red: broad/sensitive)
- Remove button

## Tab: Integrations

| Setting | Control | Description |
|---------|---------|-------------|
| Metrics endpoint | Read-only text | Prometheus scrape URL |
| Log format | Dropdown: JSON/text | Structured log output format |
| Webhooks | URL list + Add button | Notification endpoints |
| Email notifications | Toggle + email input | Alert emails |

Webhook row: URL input + event filter dropdown + Test button + Remove button.

## Setting Row Pattern

Every setting follows this structure:

```
┌──────────────────────────────────────┐
│  Setting Label              [Control]│
│  Short description of what it does.  │
│  ⓘ "What this really means"         │
└──────────────────────────────────────┘
```

- **Label:** Bold, left-aligned
- **Control:** Right-aligned (toggle, dropdown, input)
- **Description:** Grey text below label
- **Tooltip:** "What this really means" expandable - explains in non-technical terms

## Save Behavior

- Changes auto-save with debounce (500ms)
- Toast notification: "Settings saved"
- Changes that require restart show warning: "OpenClaw needs to restart for this change. Restart now?"
