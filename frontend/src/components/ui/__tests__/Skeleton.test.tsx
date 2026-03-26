import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Skeleton, { SkeletonCard, SkeletonStatus } from "../Skeleton";

describe("Skeleton", () => {
  it("renders with default dimensions", () => {
    const { container } = render(<Skeleton />);
    expect(container.firstChild).toHaveClass("animate-pulse");
  });

  it("renders custom dimensions", () => {
    const { container } = render(<Skeleton width="200px" height="50px" />);
    const el = container.firstChild as HTMLElement;
    expect(el.style.width).toBe("200px");
    expect(el.style.height).toBe("50px");
  });
});

describe("SkeletonCard", () => {
  it("renders without crashing", () => {
    const { container } = render(<SkeletonCard />);
    expect(container.firstChild).toBeTruthy();
  });
});

describe("SkeletonStatus", () => {
  it("renders without crashing", () => {
    const { container } = render(<SkeletonStatus />);
    expect(container.firstChild).toBeTruthy();
  });
});
