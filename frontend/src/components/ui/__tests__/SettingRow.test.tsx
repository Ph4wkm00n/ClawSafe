import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import SettingRow from "../SettingRow";

describe("SettingRow", () => {
  it("renders label and description", () => {
    render(
      <SettingRow label="Bind Address" description="Which interfaces to listen on.">
        <select><option>127.0.0.1</option></select>
      </SettingRow>
    );
    expect(screen.getByText("Bind Address")).toBeInTheDocument();
    expect(screen.getByText("Which interfaces to listen on.")).toBeInTheDocument();
  });

  it("shows tooltip when clicked", async () => {
    render(
      <SettingRow
        label="VPN"
        description="Require VPN."
        tooltip="Only connections through a VPN will be accepted."
      >
        <button>Toggle</button>
      </SettingRow>
    );
    await userEvent.click(screen.getByText("What this really means"));
    expect(screen.getByText("Only connections through a VPN will be accepted.")).toBeInTheDocument();
  });
});
