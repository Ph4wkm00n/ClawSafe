import type { Metadata } from "next";

import AppShell from "@/components/layout/AppShell";

import "./globals.css";

export const metadata: Metadata = {
  title: "ClawSafe",
  description: "Keeps your AI helper safe at home, no IT degree needed.",
};

// Inline script to prevent theme flash on load
const themeScript = `
(function() {
  try {
    var t = localStorage.getItem('clawsafe-theme');
    var m = localStorage.getItem('clawsafe-mode');
    if (t === 'minimal') document.documentElement.setAttribute('data-theme', 'minimal');
    if (m === 'dark') document.documentElement.setAttribute('data-mode', 'dark');
    else if (!m || m === 'system') {
      if (window.matchMedia('(prefers-color-scheme: dark)').matches)
        document.documentElement.setAttribute('data-mode', 'dark');
    }
  } catch(e) {}
})()
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <a href="#main-content" className="skip-to-content">
          Skip to content
        </a>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
