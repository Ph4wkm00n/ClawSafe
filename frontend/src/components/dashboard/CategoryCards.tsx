"use client";

import CategoryCard from "@/components/ui/CategoryCard";
import type { CategoryStatus } from "@/lib/types";

interface CategoryCardsProps {
  categories: CategoryStatus[];
  onAction: (actionId: string) => void;
}

export default function CategoryCards({
  categories,
  onAction,
}: CategoryCardsProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {categories.map((cat) => (
        <CategoryCard
          key={cat.category}
          category={cat.category}
          title={cat.label}
          status={cat.status}
          summary={cat.summary}
          actionLabel={cat.action_label}
          onAction={() => onAction(cat.action_id)}
        />
      ))}
    </div>
  );
}
