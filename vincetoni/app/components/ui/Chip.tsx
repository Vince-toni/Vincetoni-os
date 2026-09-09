import { colors, radii } from "@/app/lib/tokens";
import { ButtonHTMLAttributes } from "react";

interface ChipProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  selected?: boolean;
  onRemove?: () => void;
}

// Chip is for filters/selectable tags (e.g. "Filter by: Games").
// Use Badge instead when you need a fixed, color-coded domain label on a card.
export function Chip({ selected = false, onRemove, children, className = "", ...props }: ChipProps) {
  return (
    <button
      {...props}
      className={`inline-flex items-center gap-1.5 border px-3 py-1.5 text-xs font-semibold transition-colors ${className}`}
      style={{
        borderRadius: radii.sm,
        borderColor: colors.ink,
        background: selected ? colors.ink : colors.base,
        color: selected ? colors.base : colors.ink,
      }}
    >
      {children}
      {onRemove && (
        <span
          role="button"
          aria-label="Remove"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-0.5 opacity-70 hover:opacity-100"
        >
          ×
        </span>
      )}
    </button>
  );
}