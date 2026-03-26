import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import StatusHeader from "../StatusHeader";

describe("StatusHeader", () => {
  it("renders status and subtitle", () => {
    render(
      <StatusHeader
        status="safe"
        subtitle="Your AI helper looks well protected."
        onRefresh={vi.fn()}
      />
    );
    expect(screen.getByText("Safe")).toBeInTheDocument();
    expect(
      screen.getByText("Your AI helper looks well protected.")
    ).toBeInTheDocument();
  });

  it("renders refresh button", () => {
    render(
      <StatusHeader
        status="risk"
        subtitle="Issues found."
        onRefresh={vi.fn()}
      />
    );
    expect(screen.getByText("Refresh")).toBeInTheDocument();
  });
});
