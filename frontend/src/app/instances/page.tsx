"use client";

import { useState } from "react";

import StatusChip from "@/components/ui/StatusChip";
import { useToast } from "@/components/ui/Toast";
import { t } from "@/i18n/en";
import { useInstances } from "@/hooks/useInstances";

export default function InstancesPage() {
  const { instances, loading, addInstance, removeInstance } = useInstances();
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [configPath, setConfigPath] = useState("");
  const { toast } = useToast();

  const handleAdd = async () => {
    if (!name.trim() || !configPath.trim()) return;
    try {
      await addInstance(name.trim(), configPath.trim());
      setName("");
      setConfigPath("");
      setShowForm(false);
      toast(t("instances.added"), "success");
    } catch {
      toast(t("instances.add_failed"), "error");
    }
  };

  const handleRemove = async (id: string) => {
    try {
      await removeInstance(id);
      toast(t("instances.removed"), "success");
    } catch {
      toast(t("instances.remove_failed"), "error");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl" style={{ fontWeight: "var(--font-weight-bold)" }}>
          {t("instances.title")}
        </h1>
        <button
          onClick={() => setShowForm((s) => !s)}
          className="rounded-md px-4 py-2 text-sm font-medium"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            color: "#fff",
            borderRadius: "var(--radius-md)",
          }}
        >
          {t("instances.add")}
        </button>
      </div>

      {showForm && (
        <div
          className="flex flex-col gap-3 rounded-lg border p-5"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
            borderRadius: "var(--radius-lg)",
          }}
        >
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={t("instances.name_placeholder")}
            className="rounded-md border px-3 py-2 text-sm"
            style={{
              backgroundColor: "var(--color-bg-primary)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          />
          <input
            type="text"
            value={configPath}
            onChange={(e) => setConfigPath(e.target.value)}
            placeholder={t("instances.path_placeholder")}
            className="rounded-md border px-3 py-2 text-sm font-mono"
            style={{
              backgroundColor: "var(--color-bg-primary)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-sm)",
            }}
          />
          <div className="flex gap-2">
            <button
              onClick={handleAdd}
              className="rounded-md px-4 py-2 text-sm font-medium"
              style={{
                backgroundColor: "var(--color-brand-primary)",
                color: "#fff",
                borderRadius: "var(--radius-sm)",
              }}
            >
              {t("instances.save")}
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="rounded-md px-4 py-2 text-sm"
              style={{ color: "var(--color-text-secondary)" }}
            >
              {t("common.cancel")}
            </button>
          </div>
        </div>
      )}

      {loading && (
        <p className="text-sm" style={{ color: "var(--color-text-muted)" }}>
          {t("common.loading")}
        </p>
      )}

      <div className="flex flex-col gap-3">
        {instances.map((instance) => (
          <div
            key={instance.id}
            className="flex items-center justify-between rounded-lg border p-4"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              borderRadius: "var(--radius-lg)",
            }}
          >
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold">{instance.name}</span>
                {instance.active ? (
                  <StatusChip status="safe" size="sm" />
                ) : (
                  <StatusChip status="attention" size="sm" />
                )}
              </div>
              <span className="font-mono text-xs" style={{ color: "var(--color-text-muted)" }}>
                {instance.config_path}
              </span>
            </div>
            {instance.id !== "default" && (
              <button
                onClick={() => handleRemove(instance.id)}
                className="text-xs transition-opacity hover:opacity-70"
                style={{ color: "var(--color-status-risk)" }}
              >
                {t("instances.remove")}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
