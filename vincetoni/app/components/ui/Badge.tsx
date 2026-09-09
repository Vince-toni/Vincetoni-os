import { colors, domainColors, DomainKey, radii } from "@/app/lib/tokens";

interface BadgeProps {
  domain: DomainKey;
  children: React.ReactNode;
}

const LABELS: Record<DomainKey, string> = {
  tech: "Tech",
  creative: "Creative",
  learn: "Learning",
};

export function Badge({ domain, children }: BadgeProps) {
  const color = domainColors[domain];
  return (
    <span
      className="inline-flex items-center gap-1.5 border px-2.5 py-1 text-xs font-semibold"
      style={{
        borderRadius: radii.sm,
        borderColor: colors.ink,
        background: color,
        color: colors.ink,
      }}
    >
      <span aria-hidden>{LABELS[domain]}</span>
      <span>{children}</span>
    </span>
  );
}
