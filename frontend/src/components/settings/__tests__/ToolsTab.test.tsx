import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import ToolsTab from "../ToolsTab";

const mockPolicy = {
  version: "1",
  name: "test",
  network: {},
  tools: {
    rules: [
      { name: "web_search", risk: "low", action: "allow" },
      { name: "shell_exec", risk: "high", action: "block" },
    ],
  },
  data: {},
  auth: {},
  monitoring: {},
  integrations: {},
};

describe("ToolsTab", () => {
  it("renders skill table with policy rules", () => {
    render(<ToolsTab policy={mockPolicy} onSave={vi.fn()} />);
    expect(screen.getByText("web_search")).toBeInTheDocument();
    expect(screen.getByText("shell_exec")).toBeInTheDocument();
  });

  it("renders block all high-risk button", () => {
    render(<ToolsTab policy={mockPolicy} onSave={vi.fn()} />);
    expect(screen.getByText("Block all high-risk")).toBeInTheDocument();
  });

  it("renders risk badges", () => {
    render(<ToolsTab policy={mockPolicy} onSave={vi.fn()} />);
    expect(screen.getByText("low")).toBeInTheDocument();
    expect(screen.getByText("high")).toBeInTheDocument();
  });
});
