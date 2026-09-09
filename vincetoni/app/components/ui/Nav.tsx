"use client";

import { colors, radii } from "@/app/lib/tokens";
import { ReactNode, useState } from "react";
import { Button } from "./Button";

interface NavLink {
  label: string;
  href: string;
}

interface NavProps {
  logo?: ReactNode;
  links: NavLink[];
  ctaLabel?: string;
  ctaHref?: string;
}

export function Nav({ logo, links, ctaLabel, ctaHref }: NavProps) {
  const [open, setOpen] = useState(false);

  return (
    <header style={{ background: colors.base, borderBottom: `2px solid ${colors.ink}` }}>
      <div className="flex items-center justify-between px-5 py-4 sm:px-10">
        <div className="font-display text-lg" style={{ color: colors.ink }}>
          {logo ?? "VINCETONI"}
        </div>
        <nav className="hidden items-center gap-8 sm:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm font-medium transition-opacity hover:opacity-60"
              style={{ color: colors.ink }}
            >
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          {ctaLabel && ctaHref && (
            <a href={ctaHref} className="hidden sm:block">
              <Button variant="primary" className="!py-2 !px-4 text-xs">
                {ctaLabel}
              </Button>
            </a>
          )}
          <button
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((v) => !v)}
            className="flex h-9 w-9 items-center justify-center border-2 sm:hidden"
            style={{ borderColor: colors.ink, borderRadius: radii.sm, color: colors.ink }}
          >
            {open ? "✕" : "☰"}
          </button>
        </div>
      </div>
      {open && (
        <nav
          className="flex flex-col gap-1 px-5 pb-4 sm:hidden"
          style={{ borderTop: `2px solid ${colors.ink}` }}
        >
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setOpen(false)}
              className="py-3 text-sm font-semibold"
              style={{ color: colors.ink }}
            >
              {link.label}
            </a>
          ))}
          {ctaLabel && ctaHref && (
            <a href={ctaHref} onClick={() => setOpen(false)} className="pt-2">
              <Button variant="primary" className="w-full">
                {ctaLabel}
              </Button>
            </a>
          )}
        </nav>
      )}
    </header>
  );
}