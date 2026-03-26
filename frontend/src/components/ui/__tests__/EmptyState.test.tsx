import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import EmptyState from "../EmptyState";

describe("EmptyState", () => {
  it("renders icon and message", () => {
    render(<EmptyState icon="📭" message="Nothing here yet." />);
    expect(screen.getByText("📭")).toBeInTheDocument();
    expect(screen.getByText("Nothing here yet.")).toBeInTheDocument();
  });

  it("renders action button when provided", async () => {
    const onClick = vi.fn();
    render(
      <EmptyState
        icon="📭"
        message="No items."
        action={{ label: "Add one", onClick }}
      />
    );
    await userEvent.click(screen.getByText("Add one"));
    expect(onClick).toHaveBeenCalledOnce();
  });
});
