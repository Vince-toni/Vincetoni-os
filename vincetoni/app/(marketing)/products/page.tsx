// app/(marketing)/products/page.tsx

import { ProductGrid } from "../components/ProductGrid";
import { colors } from "@/app/lib/tokens";

export default function ProductsPage() {
  return (
    <section className="mx-auto max-w-7xl px-5 py-14 sm:px-10 sm:py-20">
      <h1 className="font-display mb-3 text-3xl sm:text-4xl md:text-5xl" style={{ color: colors.ink }}>
        What we make
      </h1>
      <p className="mb-8 max-w-[52ch] sm:mb-10" style={{ color: colors.inkMuted }}>
        Six products, six different lanes. No corporate roadmap — just
        things we actually wanted to build.
      </p>
      <ProductGrid />
    </section>
  );
}