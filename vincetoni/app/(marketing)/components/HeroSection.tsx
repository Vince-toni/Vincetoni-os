// app/(marketing)/components/HeroSection.tsx

import { Button } from "@/app/components/ui/Button";
import { ProductMediaPlaceholder } from "./ProductMediaPlaceholder";
import { HERO_COPY } from "./content";
import { colors } from "@/app/lib/tokens";

export function HeroSection() {
  return (
    <section className="dot-grid relative overflow-hidden px-5 py-10 sm:px-6 sm:py-14 md:px-10 lg:min-h-[82vh]">
      <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-2 lg:items-center lg:gap-16">
        <div>
          <div
            className="mb-5 inline-flex -rotate-3 items-center gap-2 border-2 px-3 py-1.5 text-[0.7rem] font-bold sm:mb-6 sm:px-4 sm:py-2 sm:text-xs"
            style={{
              borderColor: colors.ink,
              background: colors.coral,
              color: colors.ink,
              borderRadius: 999,
              boxShadow: `4px 4px 0px 0px ${colors.ink}`,
            }}
          >
            {HERO_COPY.badge}
          </div>
          <h1
            className="font-display text-[2.6rem] leading-[1.02] sm:text-5xl md:text-6xl lg:text-7xl lg:leading-[0.98]"
            style={{ color: colors.ink }}
          >
            {HERO_COPY.headline}{" "}
            <span style={{ background: colors.lime, padding: "0 0.15em" }}>
              {HERO_COPY.highlight}
            </span>{" "}
            {HERO_COPY.headlineEnd}
          </h1>
          <p
            className="mt-5 max-w-[48ch] text-base leading-relaxed sm:mt-6 sm:text-lg"
            style={{ color: colors.inkMuted }}
          >
            {HERO_COPY.sub}
          </p>
          <div className="mt-7 flex flex-wrap gap-3 sm:mt-8 sm:gap-4">
            <a href="/products">
              <Button variant="primary">See what we&rsquo;re building</Button>
            </a>
            <a href="/community">
              <Button variant="secondary">Join the community</Button>
            </a>
          </div>
        </div>
        <ProductMediaPlaceholder
          label="Hero visual — product screenshot or graphic"
          accent={colors.lime}
          className="w-full"
        />
      </div>
    </section>
  );
}