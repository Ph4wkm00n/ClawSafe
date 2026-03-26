const strings: Record<string, string> = {
  // App
  "app.name": "ClawSafe",
  "app.tagline": "Keeps your AI helper safe at home, no IT degree needed.",

  // Navigation
  "nav.dashboard": "Dashboard",
  "nav.activity": "Activity",
  "nav.settings": "Advanced Settings",
  "nav.appearance": "Appearance",
  "nav.about": "About & Help",

  // Status
  "status.safe": "Safe",
  "status.attention": "Needs Attention",
  "status.risk": "At Risk",
  "status.subtitle.safe": "Your AI helper looks well protected.",
  "status.subtitle.attention": "Some things could be safer. We'll show you how.",
  "status.subtitle.risk": "Important risks found. Please review these now.",

  // Categories
  "category.network": "Network",
  "category.tools": "Tools & Skills",
  "category.data": "Data & Files",
  "category.updates": "Updates & Health",

  // Onboarding
  "onboarding.welcome.title": "Welcome to ClawSafe",
  "onboarding.welcome.body": "We'll help keep your OpenClaw safe in a few steps.",
  "onboarding.welcome.cta": "Get started",
  "onboarding.detect.found": "We found an OpenClaw running on this machine.",
  "onboarding.detect.not_found": "We didn't see OpenClaw. We can set it up in a safe way.",
  "onboarding.detect.secure_existing": "Secure existing OpenClaw",
  "onboarding.detect.setup_new": "Set up a new one",
  "onboarding.q1.title": "Where are you using OpenClaw?",
  "onboarding.q1.home": "Home",
  "onboarding.q1.business": "Small business",
  "onboarding.q1.not_sure": "Not sure",
  "onboarding.q1.not_sure_help": "That's fine, we'll use safe defaults for both.",
  "onboarding.q2.title": "Do you want OpenClaw reachable from outside your home/office?",
  "onboarding.q2.no": "No, keep it private",
  "onboarding.q2.no_badge": "recommended",
  "onboarding.q2.yes": "Yes, I know what I'm doing",
  "onboarding.q2.not_sure": "I'm not sure",
  "onboarding.q2.not_sure_help": "We recommend keeping it private. You can change this later.",
  "onboarding.summary.title": "Here's what we'll do",
  "onboarding.summary.private": "Keep OpenClaw private to this device.",
  "onboarding.summary.tools": "Turn off some risky abilities unless you need them.",
  "onboarding.summary.auth": "Add a password where needed.",
  "onboarding.summary.cta": "Apply these settings",
  "onboarding.summary.customize": "Customize first",
  "onboarding.done.title": "You're all set!",
  "onboarding.done.body": "Your AI helper is now much harder to hack.",
  "onboarding.done.cta": "Go to Dashboard",

  // Fix flow
  "fix.auto": "Fix automatically",
  "fix.show_how": "Show me how",
  "fix.undo": "Undo last change",
  "fix.success": "Done!",
  "fix.error": "Something went wrong. The fix couldn't be applied.",
  "fix.try_again": "Try again",

  // Settings
  "settings.title": "Advanced Settings",
  "settings.link": "Advanced settings (for power users)",
  "settings.tab.network": "Network",
  "settings.tab.tools": "Tools & Skills",
  "settings.tab.data": "Data & Files",
  "settings.tab.integrations": "Integrations",

  // Appearance
  "appearance.title": "Appearance",
  "appearance.style": "Visual Style",
  "appearance.style.playful": "Playful",
  "appearance.style.playful_desc": "Friendly look with our guardian mascot, soft colors, and rounded shapes.",
  "appearance.style.minimal": "Minimal",
  "appearance.style.minimal_desc": "Clean and simple. Just the essentials.",
  "appearance.mode": "Mode",
  "appearance.mode.system": "Match system",
  "appearance.mode.light": "Light",
  "appearance.mode.dark": "Dark",

  // Activity
  "activity.title": "Activity",
  "activity.view_all": "View all activity",
  "activity.empty": "No recent activity.",

  // About
  "about.title": "About & Help",
  "about.version": "Version",
  "about.docs": "Documentation",
  "about.github": "GitHub",

  // Common
  "common.back": "Back",
  "common.next": "Next",
  "common.close": "Close",
  "common.save": "Save",
  "common.cancel": "Cancel",
  "common.loading": "Loading...",
  "common.refresh": "Refresh",
};

export default strings;

export function t(key: string): string {
  return strings[key] ?? key;
}
