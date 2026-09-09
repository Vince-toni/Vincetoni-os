// app/(marketing)/layout.tsx

import { Nav } from "@/app/components/ui/Nav";
import { Marquee } from "@/app/components/ui/Marquee";
import { NAV_LINKS, PRODUCTS } from "./components/content";
import { colors } from "@/app/lib/tokens";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ background: colors.base }} className="flex min-h-full flex-col">
      <Nav links={NAV_LINKS} ctaLabel="Get in touch" ctaHref="/contact" />
      <Marquee items={PRODUCTS.map((p) => p.name)} />
      <div className="flex-1">{children}</div>
      <footer
        className="px-5 py-8 text-sm sm:px-10"
        style={{ borderTop: `2px solid ${colors.ink}`, color: colors.inkMuted }}
      >
        <div className="mx-auto flex max-w-7xl flex-col items-start gap-2 sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} VINCETONI</span>
          <span>Building the future, one idea at a time.</span>
        </div>
      </footer>
    </div>
  );
}