# Fix Flow

## Trigger

Opened by clicking "Fix this for me" or a specific action button on a category card.
Renders as a **side sheet** (slides from right) on desktop, **full-screen modal** on mobile.

## Layout

```
┌─────────────────────────────────┐
│  ✕                              │
│                                 │
│  Make OpenClaw Private          │
│                                 │
│  People outside your home can   │
│  reach your AI right now. We    │
│  can change this so only you    │
│  can use it.                    │
│                                 │
│  ┌─────────────────────────┐   │
│  │  Fix automatically      │   │
│  └─────────────────────────┘   │
│  ┌─────────────────────────┐   │
│  │  Show me how            │   │
│  └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

## States

### Initial

- **Heading:** Action title (e.g., "Make OpenClaw Private")
- **Body:** Plain-language explanation of the risk and what the fix does
- **Buttons:**
  - Primary: "Fix automatically" (v0.2+; disabled placeholder in v0.1)
  - Secondary: "Show me how"

### Show Me How (expanded)

Replaces button area with step-by-step instructions:

```
Step 1: Open your terminal
Step 2: Run this command:
┌──────────────────────────────┐
│ sudo nano /etc/openclaw/...  │  [Copy]
└──────────────────────────────┘
Step 3: Change bind_address to "127.0.0.1"
Step 4: Restart OpenClaw:
┌──────────────────────────────┐
│ docker restart openclaw      │  [Copy]
└──────────────────────────────┘

Expected result: OpenClaw will only be reachable from this machine.
```

- Code blocks have a copy button
- Numbered steps in plain language
- "Expected result" at the end

### Fixing (auto-fix in progress)

- Spinner/progress indicator
- "Applying changes..." text
- Buttons disabled

### Success

- Green checkmark icon
- "Done! OpenClaw is now only reachable from this machine."
- "Undo last change" link (if reversible)
- "Close" button

### Error

- Red alert icon
- "Something went wrong. The fix couldn't be applied."
- Error detail in expandable section
- "Try again" button
- "Show me how" fallback

## Interaction Notes

- Clicking outside or pressing Escape closes the sheet
- Backdrop overlay dims the dashboard behind
- Transition: slide in from right (300ms ease)
- Close button (X) always visible in top-right
