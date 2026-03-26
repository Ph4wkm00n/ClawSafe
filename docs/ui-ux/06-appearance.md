# Appearance Settings

## Layout

Simple page with two setting groups and live preview.

```
┌──────────────────────────────────────┐
│  Appearance                          │
│                                      │
│  Visual Style                        │
│  ┌──────────┐  ┌──────────┐        │
│  │ Playful  │  │ Minimal  │        │
│  │ [thumb]  │  │ [thumb]  │        │
│  │  ● ──────│  │  ○ ──────│        │
│  └──────────┘  └──────────┘        │
│                                      │
│  Mode                                │
│  ○ Match system                      │
│  ○ Light                             │
│  ○ Dark                              │
│                                      │
└──────────────────────────────────────┘
```

## Visual Style

Two selectable cards with preview thumbnails:

**Playful (default)**
- Thumbnail shows: mascot, gradient background, rounded cards
- Description: "Friendly look with our guardian mascot, soft colors, and rounded shapes."

**Minimal**
- Thumbnail shows: flat background, clean lines, no mascot
- Description: "Clean and simple. Just the essentials."

Selection is radio-style (one active at a time). Active card has border highlight.

## Mode

Radio group:

- **Match system** (default) - follows OS light/dark preference
- **Light** - always light background
- **Dark** - always dark background

## Behavior

- Changes apply instantly (no save button needed)
- Smooth CSS transition between themes (~200ms)
- Preference persisted in backend settings
- On first visit, defaults to Playful + Match system

## Dark Mode Specifics

Per the design system:
- Background: dark grey/charcoal (`#1A1E2E`), not pure black
- Text: off-white for readability
- Accent colors slightly desaturated to reduce glare
- Focus outlines clearly visible against dark backgrounds
- Cards use subtle elevation (lighter shade) rather than shadows
