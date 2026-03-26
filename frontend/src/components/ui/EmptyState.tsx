"use client";

interface EmptyStateProps {
  icon: string;
  message: string;
  action?: { label: string; onClick: () => void };
}

export default function EmptyState({ icon, message, action }: EmptyStateProps) {
  return (
    <div
      className="flex flex-col items-center justify-center gap-3 py-12 text-center"
      style={{ color: "var(--color-text-muted)" }}
    >
      <span className="text-4xl">{icon}</span>
      <p className="max-w-sm text-sm">{message}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="rounded-md px-4 py-2 text-sm font-medium transition-opacity hover:opacity-80"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            color: "#fff",
            borderRadius: "var(--radius-md)",
          }}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
