import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import CategoryCard from "../CategoryCard";

describe("CategoryCard", () => {
  const defaultProps = {
    category: "network",
    title: "Network",
    status: "safe" as const,
    summary: "All good here.",
    actionLabel: "Review details",
    onAction: vi.fn(),
  };

  it("renders title and summary", () => {
    render(<CategoryCard {...defaultProps} />);
    expect(screen.getByText("Network")).toBeInTheDocument();
    expect(screen.getByText("All good here.")).toBeInTheDocument();
  });

  it("renders action button", () => {
    render(<CategoryCard {...defaultProps} />);
    expect(screen.getByText("Review details")).toBeInTheDocument();
  });

  it("calls onAction when button clicked", async () => {
    const onAction = vi.fn();
    render(<CategoryCard {...defaultProps} onAction={onAction} />);
    await userEvent.click(screen.getByText("Review details"));
    expect(onAction).toHaveBeenCalledOnce();
  });
});
