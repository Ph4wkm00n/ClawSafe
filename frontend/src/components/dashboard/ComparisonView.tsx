"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";

interface ComparisonItem {
  field: string;
  current_value: string;
  recommended_value: string;
  status: "match" | "mismatch" | "missing";
}

interface ComparisonData {
  items: ComparisonItem[];
  match_percentage: number;
}

const STATUS_COLORS: Record<string, string> = {
  match: "var(--safe)",
  mismatch: "var(--risk)",
  missing: "var(--attention)",
};

const STATUS_LABELS: Record<string, string> = {
  match: "OK",
  mismatch: "Needs Fix",
  missing: "Missing",
};

export default function ComparisonView() {
  const [data, setData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApi<ComparisonData>("/comparison")
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
        <p style={{ color: "var(--text-secondary)" }}>Loading comparison...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
        <p style={{ color: "var(--text-secondary)" }}>Comparison unavailable.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
          Config vs. Recommended
        </h3>
        <span
          className="text-xs font-medium px-2 py-1 rounded-full"
          style={{
            background: data.match_percentage >= 80 ? "var(--safe)" : "var(--attention)",
            color: "white",
          }}
        >
          {data.match_percentage}% Match
        </span>
      </div>
      <table className="w-full text-xs">
        <thead>
          <tr style={{ color: "var(--text-secondary)" }}>
            <th className="text-left py-1">Setting</th>
            <th className="text-left py-1">Current</th>
            <th className="text-left py-1">Recommended</th>
            <th className="text-right py-1">Status</th>
          </tr>
        </thead>
        <tbody>
          {data.items.map((item) => (
            <tr key={item.field} className="border-t" style={{ borderColor: "var(--border)" }}>
              <td className="py-2" style={{ color: "var(--text-primary)" }}>{item.field}</td>
              <td className="py-2 font-mono" style={{ color: "var(--text-secondary)" }}>
                {item.current_value}
              </td>
              <td className="py-2 font-mono" style={{ color: "var(--text-secondary)" }}>
                {item.recommended_value}
              </td>
              <td className="py-2 text-right">
                <span
                  className="px-2 py-0.5 rounded text-white text-xs"
                  style={{ background: STATUS_COLORS[item.status] }}
                >
                  {STATUS_LABELS[item.status]}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
