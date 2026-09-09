// app/(marketing)/components/ProductMediaPlaceholder.tsx

import { colors, radii } from "@/app/lib/tokens";

interface ProductMediaPlaceholderProps {
  label: string;
  accent?: string;
  className?: string;
}

// Route-specific placeholder for product screenshots/media.
// Swap the inner content for a real <Image> once assets exist — border,
// radius, and aspect are already set so nothing else needs restyling.
export function ProductMediaPlaceholder({
  label,
  accent = colors.violet,
  className = "",
}: ProductMediaPlaceholderProps) {
  return (
    <div
      className={`relative flex aspect-video items-center justify-center overflow-hidden sm:aspect-auto sm:h-full ${className}`}
      style={{
        border: `2px solid ${colors.ink}`,
        borderRadius: radii.md,
        background: `repeating-linear-gradient(45deg, ${colors.base}, ${colors.base} 10px, ${accent}22 10px, ${accent}22 20px)`,
        minHeight: 120,
      }}
    >
      <span
        className="border-2 px-3 py-1 text-xs font-semibold"
        style={{
          borderColor: colors.ink,
          background: colors.base,
          color: colors.ink,
          borderRadius: radii.sm,
        }}
      >
        {label}
      </span>
    </div>
  );
}