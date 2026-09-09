import { colors, radii } from "@/app/lib/tokens";

interface ImagePlaceholderProps {
  label?: string;
  aspect?: "square" | "video" | "wide";
  accent?: string;
  className?: string;
}

const ASPECT_CLASS: Record<NonNullable<ImagePlaceholderProps["aspect"]>, string> = {
  square: "aspect-square",
  video: "aspect-video",
  wide: "aspect-[21/9]",
};

// Drop this in anywhere a real image/screenshot will eventually go.
// Swap for a real <img>/<Image> later — same border/radius so nothing
// needs to be restyled when the real asset lands.
export function ImagePlaceholder({
  label = "Image",
  aspect = "video",
  accent = colors.violet,
  className = "",
}: ImagePlaceholderProps) {
  return (
    <div
      className={`relative flex items-center justify-center overflow-hidden ${ASPECT_CLASS[aspect]} ${className}`}
      style={{
        border: `2px solid ${colors.ink}`,
        borderRadius: radii.md,
        background: `repeating-linear-gradient(45deg, ${colors.base}, ${colors.base} 10px, ${accent}22 10px, ${accent}22 20px)`,
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