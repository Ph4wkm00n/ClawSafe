"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div
      className="flex min-h-[50vh] flex-col items-center justify-center gap-4 p-8 text-center"
      style={{ color: "var(--color-text-primary)" }}
    >
      <span className="text-4xl">⚠️</span>
      <h2
        className="text-xl"
        style={{ fontWeight: "var(--font-weight-bold)" }}
      >
        Something went wrong
      </h2>
      <p
        className="max-w-md text-sm"
        style={{ color: "var(--color-text-secondary)" }}
      >
        {error.message || "An unexpected error occurred. Please try again."}
      </p>
      <button
        onClick={reset}
        className="rounded-lg px-5 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90"
        style={{
          backgroundColor: "var(--color-brand-primary)",
          borderRadius: "var(--radius-md)",
        }}
      >
        Try again
      </button>
    </div>
  );
}
