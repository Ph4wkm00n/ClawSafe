import type { Metadata } from "next";

import AppShell from "@/components/layout/AppShell";

import "./globals.css";

export const metadata: Metadata = {
  title: "ClawSafe",
  description: "Keeps your AI helper safe at home, no IT degree needed.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <a href="#main-content" className="skip-to-content">
          Skip to content
        </a>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
