"use client";

import type { ReactNode } from "react";

import { ToastProvider } from "@/components/ui/Toast";

import MobileNav from "./MobileNav";
import Sidebar from "./Sidebar";

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <ToastProvider>
      <div className="min-h-screen">
        <Sidebar />
        <main
          className="min-h-screen pb-20 lg:pb-0"
          style={{ marginLeft: "var(--sidebar-width)" }}
        >
          <div className="mx-auto max-w-5xl p-5 lg:p-8">{children}</div>
        </main>
        <MobileNav />

        {/* CSS to hide sidebar margin on mobile */}
        <style>{`
          @media (max-width: 1023px) {
            main { margin-left: 0 !important; }
          }
        `}</style>
      </div>
    </ToastProvider>
  );
}
