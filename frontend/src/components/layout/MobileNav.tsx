"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { t } from "@/i18n/en";

const NAV_ITEMS = [
  { href: "/", label: t("nav.dashboard"), icon: "🛡️" },
  { href: "/activity", label: t("nav.activity"), icon: "📋" },
  { href: "/settings", label: t("nav.settings"), icon: "⚙️" },
  { href: "/appearance", label: t("nav.appearance"), icon: "🎨" },
  { href: "/about", label: t("nav.about"), icon: "❓" },
];

export default function MobileNav() {
  const pathname = usePathname();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 flex border-t lg:hidden"
      style={{
        backgroundColor: "var(--color-bg-sidebar)",
        borderColor: "var(--color-border)",
      }}
    >
      {NAV_ITEMS.map((item) => {
        const active = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className="flex flex-1 flex-col items-center gap-0.5 py-2 text-xs"
            style={{
              color: active
                ? "var(--color-brand-primary)"
                : "var(--color-text-muted)",
            }}
          >
            <span className="text-lg">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
