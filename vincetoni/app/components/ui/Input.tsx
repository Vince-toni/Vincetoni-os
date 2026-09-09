import { colors, radii } from "@/app/lib/tokens";
import { InputHTMLAttributes, forwardRef } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, id, className = "", ...props },
  ref
) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-sm font-semibold" style={{ color: colors.ink }}>
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={id}
        {...props}
        className={`px-4 py-2.5 text-sm outline-none transition-shadow focus:shadow-[3px_3px_0px_0px_var(--tw-shadow-color)] ${className}`}
        style={{
          background: colors.base,
          color: colors.ink,
          border: `2px solid ${colors.ink}`,
          borderRadius: radii.sm,
          // @ts-ignore -- custom property for the focus shadow color above
          "--tw-shadow-color": colors.violet,
        }}
      />
    </div>
  );
});