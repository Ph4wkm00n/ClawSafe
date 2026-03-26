"use client";

interface SkeletonProps {
  className?: string;
  width?: string;
  height?: string;
}

export default function Skeleton({ className = "", width, height }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse rounded-md ${className}`}
      style={{
        backgroundColor: "var(--color-border)",
        width: width ?? "100%",
        height: height ?? "1rem",
        borderRadius: "var(--radius-sm)",
      }}
    />
  );
}

export function SkeletonCard() {
  return (
    <div
      className="flex flex-col gap-3 border p-5"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: "var(--color-border)",
        borderRadius: "var(--radius-lg)",
      }}
    >
      <div className="flex items-center justify-between">
        <Skeleton width="40%" height="1.25rem" />
        <Skeleton width="4rem" height="1.25rem" />
      </div>
      <Skeleton height="0.875rem" />
      <Skeleton width="60%" height="0.875rem" />
      <Skeleton width="8rem" height="2.25rem" />
    </div>
  );
}

export function SkeletonStatus() {
  return (
    <div
      className="flex flex-col items-center gap-4 p-8"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderRadius: "var(--radius-lg)",
      }}
    >
      <Skeleton width="6rem" height="2rem" />
      <Skeleton width="80%" height="1rem" />
    </div>
  );
}
