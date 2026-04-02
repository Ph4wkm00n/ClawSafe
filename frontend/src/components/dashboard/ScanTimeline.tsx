"use client";

import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchApi } from "@/lib/api";

interface ScanPoint {
  id: number;
  timestamp: string;
  overall_status: string;
  score: number;
}

export default function ScanTimeline() {
  const [data, setData] = useState<ScanPoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApi<{ scans: ScanPoint[]; total: number }>("/scans?limit=50")
      .then((res) => {
        setData(res.scans.reverse()); // oldest first for timeline
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
        <p style={{ color: "var(--text-secondary)" }}>Loading scan history...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
        <p style={{ color: "var(--text-secondary)" }}>No scan history yet.</p>
      </div>
    );
  }

  const chartData = data.map((s) => ({
    time: new Date(s.timestamp).toLocaleDateString(),
    score: s.score,
    status: s.overall_status,
  }));

  return (
    <div className="rounded-xl border p-4" style={{ borderColor: "var(--border)" }}>
      <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--text-primary)" }}>
        Risk Score Over Time
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis dataKey="time" tick={{ fontSize: 11 }} stroke="var(--text-secondary)" />
          <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} stroke="var(--text-secondary)" />
          <Tooltip
            contentStyle={{
              background: "var(--surface)",
              border: "1px solid var(--border)",
              borderRadius: 8,
            }}
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke="var(--accent)"
            strokeWidth={2}
            dot={{ fill: "var(--accent)", r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
