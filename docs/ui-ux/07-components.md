# Shared Components

Reusable UI components used across screens.

## StatusChip

Displays a safety status as a colored pill.

| Prop | Type | Description |
|------|------|-------------|
| `status` | `'safe' \| 'attention' \| 'risk'` | Determines color and label |
| `size` | `'sm' \| 'md' \| 'lg'` | Chip size (default: `md`) |

**Rendering:**
- Safe: green background, "Safe" text
- Attention: amber background, "Needs Attention" text
- Risk: red background, "At Risk" text
- Always includes a text label (not color-only, for accessibility)

## CategoryCard

A card displaying one risk category.

| Prop | Type | Description |
|------|------|-------------|
| `title` | string | "Network", "Tools & Skills", etc. |
| `icon` | ReactNode | Category icon |
| `status` | StatusType | Current risk status |
| `description` | string | Plain-language explanation |
| `action` | object | `{ label, onClick }` for primary button |

## SideSheet

Slide-in panel from right edge. Used for fix flows.

| Prop | Type | Description |
|------|------|-------------|
| `open` | boolean | Visibility state |
| `onClose` | function | Close handler |
| `title` | string | Header text |
| `children` | ReactNode | Sheet content |

- Width: 480px on desktop, full-width on mobile
- Backdrop overlay with click-to-close
- Escape key closes

## CodeBlock

Displays a command or code snippet with copy button.

| Prop | Type | Description |
|------|------|-------------|
| `code` | string | Code content |
| `language` | string | Syntax highlight language |

- Monospace font, dark background
- Copy button in top-right corner
- "Copied!" toast on click

## SettingRow

Standard row for Advanced Settings.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Setting name |
| `description` | string | Short explanation |
| `tooltip` | string | "What this really means" content |
| `children` | ReactNode | Control element (toggle, input, etc.) |

## StepList

Numbered step-by-step instructions for "Show me how" flows.

| Prop | Type | Description |
|------|------|-------------|
| `steps` | Step[] | Array of `{ text, code? }` |
| `result` | string | Expected outcome text |

## MascotIllustration

Displays the guardian claw mascot in different states.

| Prop | Type | Description |
|------|------|-------------|
| `state` | `'safe' \| 'attention' \| 'risk' \| 'welcome' \| 'success'` | Mascot pose |
| `size` | `'sm' \| 'md' \| 'lg'` | Illustration size |

- Hidden when Minimal theme is active
- SVG-based for crisp rendering at all sizes

## ProgressDots

Step indicator for the onboarding wizard.

| Prop | Type | Description |
|------|------|-------------|
| `total` | number | Total steps |
| `current` | number | Active step (0-indexed) |

## Toast

Ephemeral notification for confirmations and errors.

| Prop | Type | Description |
|------|------|-------------|
| `message` | string | Notification text |
| `type` | `'success' \| 'error' \| 'info'` | Visual style |
| `duration` | number | Auto-dismiss time in ms (default: 3000) |
