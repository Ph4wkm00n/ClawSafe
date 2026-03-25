# ClawSafe – UI / UX Design Spec

## 1. Design Principles

- **Friendly first, powerful second:** Default framing for non-technical home users, with Advanced Settings for SMB/DevOps users.[web:54][web:56]
- **Explain, don’t scare:** Clear, calm language about risks and concrete actions.[web:43]
- **Same structure, different skins:** Playful vs Minimal and Light vs Dark change look, not information architecture.[web:68][web:75]

---

## 2. Visual Identity

### 2.1 Name & Tagline

- Product name: **ClawSafe**
- Tagline: “Keeps your AI helper safe at home, no IT degree needed.”[web:83][web:86]

### 2.2 Logo & Icon

- Shape: Rounded shield with a stylized claw or “C” inside.
- Light theme: Soft teal/blue shield, white inner claw.
- Dark theme: Deep navy shield, soft teal claw.[web:82][web:85][web:72]

### 2.3 Mascot

- Character: Friendly “guardian claw” character, more abstract than a full lobster.
- States:
  - Relaxed/smiling when Safe.
  - Concerned when At Risk.
  - Helpful pose (e.g., holding wrench/shield) when suggesting fixes.[web:63][web:86]

Usage:

- Prominent in Playful mode onboarding and empty states.
- Reduced or hidden entirely in Minimal mode.[web:62][web:61]

---

## 3. Layout & Navigation

### 3.1 Global Layout

- Left navigation (or top tabs on mobile):
  - Dashboard
  - Activity
  - Advanced Settings
  - Appearance
  - About / Help[web:61]

- Main content area:
  - Top: Global safety status.
  - Middle: Category cards.
  - Bottom: Recent activity.

### 3.2 Primary Navigation Items

- **Dashboard:** Overview status and key actions.
- **Activity:** Timeline of notable security events (new skills, exposure changes).
- **Advanced Settings:** Detailed controls for power users.
- **Appearance:** Theme style and mode toggles.
- **About / Help:** Quick guides and links to docs/GitHub.

---

## 4. Key Screens & Flows

### 4.1 Onboarding / Setup Wizard

**Flow:**

1. **Welcome**

- Text: “Welcome to ClawSafe. We’ll help keep your OpenClaw safe in a few steps.”
- CTA: “Get started”

2. **Detect Setup**

- If OpenClaw detected:
  - “We found an OpenClaw running on this machine.”
  - Choices: “Secure existing OpenClaw” / “Set up a new one”
- If not detected:
  - “We didn’t see OpenClaw. We can set it up in a safe way.”[web:46]

3. **Usage Questions**

- Q1: “Where are you using OpenClaw?”
  - Home / Small business / Not sure
- Q2: “Do you want OpenClaw reachable from outside your home/office?”
  - No, keep it private (recommended)
  - Yes, I know what I’m doing
  - I’m not sure[web:41][web:43]

4. **Summary & Apply**

- Summary bullet points (plain language):
  - “We’ll keep it private to this device.”
  - “We’ll turn off some risky abilities unless you need them.”
  - “We’ll add a password where needed.”
- CTA: “Apply these settings”

Feedback:

- Show progress and a completion message: “You’re all set. Your AI helper is now much harder to hack.”[web:54][web:56]

---

### 4.2 Main Dashboard

Sections:

1. **Global Status Header**

- Large status chip:
  - Safe (green)
  - Needs Attention (amber)
  - At Risk (red)[web:52][web:56]
- Short line beneath:
  - “Your AI helper looks well protected.”
  - “Some things could be safer. We’ll show you how.”
  - “Important risks found. Please review these now.”

2. **Category Cards**

Four cards:

- Network
- Tools & Skills
- Data & Files
- Updates & Health

Each card includes:

- Icon and title.
- Status chip (Safe / Needs Attention / At Risk).
- 1–2 sentence explanation in plain language.
- Primary button:
  - “Fix this for me”
  - “Review details”[web:54][web:61]

Example (Network card):

> “People outside your home can reach OpenClaw. This makes hacking easier.”  
> Button: “Make it private”

3. **Recent Activity**

- Simple list:
  - “New skill ‘shell_exec’ enabled.”
  - “Port changed from 127.0.0.1 to 0.0.0.0.”
  - “Policy updated by user ben.”[web:32][web:57]

---

### 4.3 Fix Flow (Modal / Side Sheet)

When user clicks “Fix this”:

- Header: “Make OpenClaw private”
- Paragraph: short explanation and impact.
- Buttons:
  - Primary: “Fix automatically”
  - Secondary: “Show me how”

“Show me how” shows:

- Steps in plain language.
- Commands snippet (copy button).
- Expected result.

After success:

- Confirmation state: “Done! OpenClaw is now only reachable from this machine.”
- Option: “Undo last change” where possible.[web:43][web:41]

---

### 4.4 Advanced Settings

Entry: link from Dashboard — “Advanced settings (for power users)”.

Tabs:

1. **Network**

- Bind address (dropdown or free text).
- Allowed CIDRs (multi-line text or chip input).
- “VPN-only mode” toggle with explanation.[web:41][web:60]

2. **Tools & Skills**

- Table: Skill name, risk level, status (Allowed / Ask / Blocked).
- Toggles and dropdown per skill.[web:57]

3. **Data & Files**

- List of mount paths with risk badges.
- Backup options (enable, frequency, destination).[web:41]

4. **Integrations**

- Metrics endpoint URL (read-only).
- Log output format/type.
- Webhook URLs (Slack, Discord, etc.).[web:36][web:44]

Helper elements:

- Each setting has:
  - Label
  - Description
  - Optional “What this really means” tooltip that explains for non-experts.[web:56][web:61]

---

### 4.5 Appearance Settings

Controls:

- **Visual style**
  - Playful (default)
  - Minimal

- **Mode**
  - Match system
  - Light
  - Dark[web:68][web:71][web:70]

Show preview thumbnails for each style:

- Playful: mascot visible, gradients, rounded cards.
- Minimal: flat surfaces, no mascot, more neutral palette.[web:62][web:61]

---

## 5. Playful vs Minimal Design Details

### 5.1 Playful Theme

- Colors: soft teal/blue primary, warm secondary accent.
- Shapes: rounded cards, slightly larger radius.
- Mascot: appears in Dashboard header, onboarding, and key alerts.
- Motion: small bounce on status changes, subtle hover transitions.[web:62][web:83]

### 5.2 Minimal Theme

- Colors: muted blues/greys, fewer gradients.
- Shapes: smaller radius, clear section separation.
- Mascot: hidden or reduced to small icon.
- Motion: minimal animations for focus and clarity.[web:61][web:75]

### 5.3 Dark Mode Guidelines

- Background: dark grey/charcoal, not pure black.
- Text: off-white, high contrast for body text.
- Accent: slightly desaturated primary colors to reduce glare.
- Ensure focus states and keyboard outlines are clearly visible.[web:70][web:72][web:74]

---

## 6. Tone & Microcopy

### 6.1 Principles

- Avoid jargon where possible.
- When jargon is needed, provide a short explanation.
- Every alert includes a clear suggested action.[web:54][web:56]

### 6.2 Example Phrases

- “Good news: your AI helper is only visible inside your home network.”
- “We noticed a change that could make hacking easier.”
- “If you’re not sure, choose this safe option.”[web:43]

---

## 7. Accessibility

- Keyboard navigable across all controls.
- Minimum contrast ratios respected in all modes.
- Avoid relying solely on color to indicate state; include text labels and icons.[web:72][web:76]
