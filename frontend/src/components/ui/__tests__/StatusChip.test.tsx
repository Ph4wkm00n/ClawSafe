import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import StatusChip from "../StatusChip";

describe("StatusChip", () => {
  it("renders Safe text for safe status", () => {
    render(<StatusChip status="safe" />);
    expect(screen.getByText("Safe")).toBeInTheDocument();
  });

  it("renders Needs Attention text for attention status", () => {
    render(<StatusChip status="attention" />);
    expect(screen.getByText("Needs Attention")).toBeInTheDocument();
  });

  it("renders At Risk text for risk status", () => {
    render(<StatusChip status="risk" />);
    expect(screen.getByText("At Risk")).toBeInTheDocument();
  });

  it("has role=status for accessibility", () => {
    render(<StatusChip status="safe" />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });
});
