import { colors } from "@/app/lib/tokens";

interface MarqueeProps {
  items: string[];
}

// Infinite scrolling ticker strip. Respects prefers-reduced-motion via the
// CSS in globals.css (animation-play-state paused + no transform fallback).
export function Marquee({ items }: MarqueeProps) {
  const track = [...items, ...items]; // duplicate for seamless loop

  return (
    <div
      className="overflow-hidden py-3"
      style={{ background: colors.ink, borderBottom: `2px solid ${colors.ink}` }}
    >
      <div className="marquee-track flex w-max gap-8 whitespace-nowrap">
        {track.map((item, i) => (
          <span
            key={i}
            className="font-display text-sm font-semibold tracking-wide"
            style={{ color: colors.base }}
          >
            {item} <span style={{ color: colors.lime }}>•</span>
          </span>
        ))}
      </div>
    </div>
  );
}