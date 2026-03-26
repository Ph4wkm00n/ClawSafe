"use client";

interface ProgressDotsProps {
  total: number;
  current: number;
}

export default function ProgressDots({ total, current }: ProgressDotsProps) {
  return (
    <div className="flex items-center justify-center gap-2" role="progressbar" aria-valuenow={current + 1} aria-valuemin={1} aria-valuemax={total}>
      {Array.from({ length: total }, (_, i) => (
        <div
          key={i}
          className="h-2 rounded-full transition-all"
          style={{
            width: i === current ? "2rem" : "0.5rem",
            backgroundColor:
              i === current
                ? "var(--color-brand-primary)"
                : i < current
                  ? "var(--color-brand-primary)"
                  : "var(--color-border)",
            opacity: i <= current ? 1 : 0.5,
          }}
        />
      ))}
    </div>
  );
}
