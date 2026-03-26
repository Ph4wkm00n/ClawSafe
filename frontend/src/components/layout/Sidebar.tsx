"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { t } from "@/i18n/en";

const NAV_ITEMS = [
  { href: "/", label: t("nav.dashboard"), icon: "🛡️" },
  { href: "/instances", label: t("nav.instances"), icon: "🖥️" },
  { href: "/vulnerabilities", label: t("nav.vulnerabilities"), icon: "🔍" },
  { href: "/activity", label: t("nav.activity"), icon: "📋" },
  { href: "/settings", label: t("nav.settings"), icon: "⚙️" },
  { href: "/appearance", label: t("nav.appearance"), icon: "🎨" },
  { href: "/about", label: t("nav.about"), icon: "❓" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      className="fixed left-0 top-0 hidden h-full flex-col border-r lg:flex"
      style={{
        width: "var(--sidebar-width)",
        backgroundColor: "var(--color-bg-sidebar)",
        borderColor: "var(--color-border)",
      }}
    >
      <div className="flex items-center gap-2 p-5">
        <span className="text-2xl">🦀</span>
        <span
          className="text-lg"
          style={{ fontWeight: "var(--font-weight-bold)" }}
        >
          {t("app.name")}
        </span>
      </div>

      <nav className="flex flex-1 flex-col gap-1 px-3">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors"
              style={{
                backgroundColor: active
                  ? "var(--color-bg-accent)"
                  : "transparent",
                color: active
                  ? "var(--color-brand-primary)"
                  : "var(--color-text-secondary)",
                fontWeight: active ? "var(--font-weight-semibold)" : "var(--font-weight-normal)",
                borderRadius: "var(--radius-md)",
              }}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
