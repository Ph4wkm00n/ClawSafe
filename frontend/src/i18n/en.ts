const strings: Record<string, string> = {
  // App
  "app.name": "ClawSafe",
  "app.tagline": "Keeps your AI helper safe at home, no IT degree needed.",

  // Navigation
  "nav.dashboard": "Dashboard",
  "nav.instances": "Instances",
  "nav.vulnerabilities": "Vulnerabilities",
  "nav.activity": "Activity",
  "nav.audit": "Audit Trail",
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
  "fix.applying": "Applying fix...",

  // Settings
  "settings.title": "Advanced Settings",
  "settings.link": "Advanced settings (for power users)",
  "settings.tab.network": "Network",
  "settings.tab.tools": "Tools & Skills",
  "settings.tab.data": "Data & Files",
  "settings.tab.integrations": "Integrations",

  // Settings - Network
  "settings.network.bind": "Bind Address",
  "settings.network.bind_desc": "Which network interfaces OpenClaw listens on.",
  "settings.network.bind_tooltip": "127.0.0.1 means only this machine can reach OpenClaw. 0.0.0.0 means any device on your network (or the internet) could connect.",
  "settings.network.cidrs": "Allowed CIDRs",
  "settings.network.cidrs_desc": "IP ranges allowed to connect.",
  "settings.network.cidrs_tooltip": "CIDR notation like 192.168.1.0/24 means all devices on your local network. Fewer ranges = more secure.",
  "settings.network.vpn": "VPN-Only Mode",
  "settings.network.vpn_desc": "Only allow connections through a VPN.",
  "settings.network.vpn_tooltip": "When enabled, OpenClaw will only accept connections that come through a VPN tunnel, adding an extra layer of security.",
  "settings.network.port": "Port",
  "settings.network.port_desc": "Port OpenClaw listens on.",

  // Settings - Tools
  "settings.tools.block_high_risk": "Block all high-risk",
  "settings.tools.name": "Skill",
  "settings.tools.risk": "Risk Level",
  "settings.tools.status": "Status",

  // Settings - Data
  "settings.data.mounts": "Mount Paths",
  "settings.data.backup": "Auto-Backup",
  "settings.data.backup_desc": "Automatically back up config before changes.",
  "settings.data.frequency": "Backup Frequency",
  "settings.data.frequency_desc": "How often to create backups.",

  // Settings - Integrations
  "settings.integrations.metrics": "Metrics Endpoint",
  "settings.integrations.metrics_desc": "Prometheus-compatible scrape URL (read-only).",
  "settings.integrations.log_format": "Log Output Format",
  "settings.integrations.log_format_desc": "Format for structured log output.",
  "settings.integrations.webhooks": "Webhooks",
  "settings.integrations.webhooks_desc": "Notification endpoints for Slack, Discord, etc.",
  "settings.integrations.email": "Email Notifications",
  "settings.integrations.email_desc": "Send alerts via email when risk level changes.",
  "settings.integrations.email_address": "Email address",
  "settings.integrations.test_email": "Send test",
  "settings.integrations.sending": "Sending...",
  "settings.integrations.email_test_sent": "Test email sent successfully.",
  "settings.integrations.email_test_failed": "Failed to send test email. Check SMTP configuration.",
  "settings.integrations.test_success": "Test notification sent successfully.",
  "settings.integrations.test_failed": "Failed to send test notification.",
  "settings.saved": "Settings saved",
  "settings.save_failed": "Failed to save settings",

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

  // Instances
  "instances.title": "Instances",
  "instances.add": "Add Instance",
  "instances.remove": "Remove",
  "instances.added": "Instance added successfully.",
  "instances.add_failed": "Failed to add instance.",
  "instances.removed": "Instance removed.",
  "instances.remove_failed": "Cannot remove this instance.",
  "instances.name_placeholder": "Instance name (e.g., Production)",
  "instances.path_placeholder": "/etc/openclaw/config.yaml",
  "instances.save": "Save",

  // Activity
  "activity.title": "Activity",
  "activity.view_all": "View all activity",
  "activity.empty": "No recent activity.",

  // About
  "about.title": "About & Help",
  "about.version": "Version",
  "about.docs": "Documentation",
  "about.github": "GitHub",

  // Vulnerabilities
  "vulns.title": "Vulnerabilities",
  "vulns.containers": "Containers",
  "vulns.total_vulns": "Vulnerabilities",
  "vulns.critical": "Critical",
  "vulns.no_containers": "No Docker containers detected. Is Docker running?",
  "vulns.no_vulns": "No vulnerabilities found in this image.",

  // Auth
  "auth.login": "Sign in",
  "auth.register": "Create account",
  "auth.login_subtitle": "Sign in to your ClawSafe dashboard.",
  "auth.register_subtitle": "Create a new account.",
  "auth.email": "Email address",
  "auth.password": "Password",
  "auth.have_account": "Already have an account? Sign in",
  "auth.no_account": "Don't have an account? Register",

  // Audit
  "audit.title": "Audit Trail",
  "audit.time": "Time",
  "audit.user": "User",
  "audit.action": "Action",
  "audit.resource": "Resource",
  "audit.details": "Details",
  "audit.empty": "No audit entries yet.",

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
