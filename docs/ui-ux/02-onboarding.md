# Onboarding / Setup Wizard

## Overview

A 4-step wizard that runs on first launch. Guides users through initial setup
with minimal decisions and plain language.

## Flow

```
Welcome → Detect Setup → Usage Questions → Summary & Apply → Done
```

## Step 1: Welcome

- **Mascot:** Friendly guardian claw, waving (Playful mode)
- **Heading:** "Welcome to ClawSafe"
- **Body:** "We'll help keep your OpenClaw safe in a few steps."
- **CTA:** Primary button "Get started"
- **Progress:** Step 1 of 4

## Step 2: Detect Setup

**If OpenClaw found:**
- **Icon:** Green checkmark
- **Body:** "We found an OpenClaw running on this machine."
- **Options:**
  - "Secure existing OpenClaw" (recommended, highlighted)
  - "Set up a new one"

**If OpenClaw not found:**
- **Icon:** Info circle
- **Body:** "We didn't see OpenClaw. We can set it up in a safe way."
- **CTA:** "Set up OpenClaw" (proceeds to install)

## Step 3: Usage Questions

Two questions, each on a card:

**Q1: "Where are you using OpenClaw?"**
- Radio options: Home / Small business / Not sure
- Helper text beneath "Not sure": "That's fine, we'll use safe defaults for both."

**Q2: "Do you want OpenClaw reachable from outside your home/office?"**
- Radio options:
  - "No, keep it private" (recommended badge)
  - "Yes, I know what I'm doing"
  - "I'm not sure"
- Helper text beneath "I'm not sure": "We recommend keeping it private. You can change this later."

## Step 4: Summary & Apply

- **Heading:** "Here's what we'll do"
- **Bullet points** (plain language, checkmark icons):
  - "Keep OpenClaw private to this device."
  - "Turn off some risky abilities unless you need them."
  - "Add a password where needed."
- **CTA:** Primary button "Apply these settings"
- **Secondary:** "Customize first" link (goes to Advanced Settings)

## Completion

- **Mascot:** Thumbs up / shield pose (Playful mode)
- **Heading:** "You're all set!"
- **Body:** "Your AI helper is now much harder to hack."
- **CTA:** "Go to Dashboard"

## Layout Notes

- Centered card layout, max-width 560px
- Progress indicator (dots or steps) at top
- Back button on steps 2-4
- Subtle background pattern/gradient in Playful mode
