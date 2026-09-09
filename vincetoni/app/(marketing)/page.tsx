// app/(marketing)/page.tsx

import { HeroSection } from "./components/HeroSection";
import { ProductGrid } from "./components/ProductGrid";
import { PHILOSOPHY_COPY, PHILOSOPHY_HIGHLIGHT } from "./components/content";
import { colors } from "@/app/lib/tokens";
import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <HeroSection />

      <section className="mx-auto max-w-7xl px-5 py-16 sm:px-10 sm:py-20">
        <div className="mb-6 flex items-baseline justify-between sm:mb-8">
          <h2 className="font-display text-2xl sm:text-3xl md:text-4xl" style={{ color: colors.ink }}>
            What we make
          </h2>
          <Link href="/products" className="text-sm font-semibold underline" style={{ color: colors.violet }}>
            See all →
          </Link>
        </div>
        <ProductGrid />
      </section>

      <section className="px-5 py-16 sm:px-10 sm:py-24" style={{ background: colors.ink }}>
        <p
          className="mx-auto max-w-2xl font-display text-2xl leading-snug sm:text-4xl md:text-5xl"
          style={{ color: colors.base }}
        >
          {PHILOSOPHY_COPY}{" "}
          <span style={{ color: colors.lime }}>{PHILOSOPHY_HIGHLIGHT}</span>
        </p>
      </section>
    </>
  );
}