import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import ErrorState from "../ErrorState";

describe("ErrorState", () => {
  it("renders error message", () => {
    render(<ErrorState message="Something went wrong." />);
    expect(screen.getByText("Something went wrong.")).toBeInTheDocument();
  });

  it("renders retry button when onRetry provided", async () => {
    const onRetry = vi.fn();
    render(<ErrorState message="Failed." onRetry={onRetry} />);
    await userEvent.click(screen.getByText("Try again"));
    expect(onRetry).toHaveBeenCalledOnce();
  });
});
