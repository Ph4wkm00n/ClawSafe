import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ScanTimeline from "../ScanTimeline";

// Mock recharts to avoid SSR/DOM issues in tests
vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  LineChart: ({ children }: { children: React.ReactNode }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
}));

// Mock fetchApi
vi.mock("@/lib/api", () => ({
  fetchApi: vi.fn().mockResolvedValue({ scans: [], total: 0 }),
}));

describe("ScanTimeline", () => {
  it("renders loading state initially", () => {
    render(<ScanTimeline />);
    expect(screen.getByText(/loading scan history/i)).toBeDefined();
  });

  it("renders empty state when no data", async () => {
    render(<ScanTimeline />);
    // After async resolution, should show empty state
    await vi.waitFor(() => {
      expect(screen.getByText(/no scan history/i)).toBeDefined();
    });
  });
});
