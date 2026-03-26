"use client";

interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div
      className="flex flex-col items-center justify-center gap-3 rounded-lg p-8 text-center"
      style={{
        backgroundColor: "var(--color-status-risk-bg)",
        borderRadius: "var(--radius-lg)",
      }}
    >
      <span className="text-3xl">⚠️</span>
      <p className="text-sm" style={{ color: "var(--color-status-risk)" }}>
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="rounded-md px-4 py-2 text-sm font-medium transition-opacity hover:opacity-80"
          style={{
            backgroundColor: "var(--color-brand-primary)",
            color: "#fff",
            borderRadius: "var(--radius-md)",
          }}
        >
          Try again
        </button>
      )}
    </div>
  );
}
