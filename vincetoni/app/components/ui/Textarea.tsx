import { colors, radii } from "@/app/lib/tokens";
import { TextareaHTMLAttributes, forwardRef } from "react";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(function Textarea(
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
      <textarea
        ref={ref}
        id={id}
        rows={4}
        {...props}
        className={`resize-none px-4 py-2.5 text-sm outline-none ${className}`}
        style={{
          background: colors.base,
          color: colors.ink,
          border: `2px solid ${colors.ink}`,
          borderRadius: radii.sm,
        }}
      />
    </div>
  );
});