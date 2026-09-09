import { colors, hardShadow, radii } from "@/app/lib/tokens";
import { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: ReactNode;
}

const VARIANT_STYLES: Record<Variant, React.CSSProperties> = {
  primary: {
    background: colors.violet,
    color: colors.base,
    border: `2px solid ${colors.ink}`,
    boxShadow: hardShadow(4),
  },
  secondary: {
    background: colors.base,
    color: colors.ink,
    border: `2px solid ${colors.ink}`,
    boxShadow: hardShadow(4),
  },
  ghost: {
    background: "transparent",
    color: colors.ink,
    border: `2px solid transparent`,
  },
};

export function Button({ variant = "primary", children, className = "", ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`inline-flex items-center justify-center rounded-[${radii.sm}] px-5 py-2.5 text-sm font-semibold transition-transform active:translate-x-0.5 active:translate-y-0.5 active:shadow-none hover:-translate-y-px ${className}`}
      style={{ borderRadius: radii.sm, ...VARIANT_STYLES[variant] }}
    >
      {children}
    </button>
  );
}
