import { colors, hardShadow, radii } from "@/app/lib/tokens";
import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  accent?: string; // optional top accent bar color
  className?: string;
}

export function Card({ children, accent, className = "" }: CardProps) {
  const isFlex = className.includes("flex");
  return (
    <div
      className={`overflow-hidden ${className}`}
      style={{
        background: colors.base,
        border: `2px solid ${colors.ink}`,
        borderRadius: radii.md,
        boxShadow: hardShadow(5),
      }}
    >
      {accent && <div style={{ height: 6, background: accent }} />}
      <div className={isFlex ? "flex flex-1 flex-col p-6" : "p-6"}>{children}</div>
    </div>
  );
}