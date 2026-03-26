"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { t } from "@/i18n/en";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const endpoint = isRegister ? "/api/v1/auth/register" : "/api/v1/auth/login";

    try {
      const resp = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await resp.json();

      if (!resp.ok) {
        setError(data.detail || "Authentication failed.");
        return;
      }

      if (!isRegister && data.access_token) {
        localStorage.setItem("clawsafe-token", data.access_token);
        localStorage.setItem("clawsafe-user", JSON.stringify(data.user));
        router.push("/");
      } else if (isRegister) {
        setIsRegister(false);
        setError("");
        setEmail(data.email || email);
        setPassword("");
      }
    } catch {
      setError("Connection failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4" style={{ backgroundColor: "var(--color-bg-primary)" }}>
      <div
        className="flex w-full max-w-sm flex-col gap-6 rounded-xl border p-8"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
          borderRadius: "var(--radius-lg)",
          boxShadow: "var(--shadow-lg)",
        }}
      >
        <div className="flex flex-col items-center gap-2">
          <span className="text-4xl">🦀</span>
          <h1 className="text-xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
            {t("app.name")}
          </h1>
          <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
            {isRegister ? t("auth.register_subtitle") : t("auth.login_subtitle")}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={t("auth.email")}
            required
            className="rounded-lg border px-4 py-2.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-primary)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-md)",
            }}
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={t("auth.password")}
            required
            minLength={6}
            className="rounded-lg border px-4 py-2.5 text-sm"
            style={{
              backgroundColor: "var(--color-bg-primary)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-md)",
            }}
          />

          {error && (
            <p className="text-sm" style={{ color: "var(--color-status-risk)" }}>
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="rounded-lg px-4 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            style={{
              backgroundColor: "var(--color-brand-primary)",
              borderRadius: "var(--radius-md)",
            }}
          >
            {loading
              ? t("common.loading")
              : isRegister
                ? t("auth.register")
                : t("auth.login")}
          </button>
        </form>

        <button
          onClick={() => {
            setIsRegister((v) => !v);
            setError("");
          }}
          className="text-sm transition-opacity hover:opacity-70"
          style={{ color: "var(--color-brand-primary)" }}
        >
          {isRegister ? t("auth.have_account") : t("auth.no_account")}
        </button>
      </div>
    </div>
  );
}
