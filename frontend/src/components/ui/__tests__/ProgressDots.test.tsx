import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import ProgressDots from "../ProgressDots";

describe("ProgressDots", () => {
  it("renders correct number of dots", () => {
    render(<ProgressDots total={4} current={1} />);
    const progressbar = screen.getByRole("progressbar");
    expect(progressbar.children).toHaveLength(4);
  });

  it("sets correct aria values", () => {
    render(<ProgressDots total={4} current={2} />);
    const progressbar = screen.getByRole("progressbar");
    expect(progressbar).toHaveAttribute("aria-valuenow", "3");
    expect(progressbar).toHaveAttribute("aria-valuemax", "4");
  });
});
