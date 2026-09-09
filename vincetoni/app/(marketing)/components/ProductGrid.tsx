// app/(marketing)/components/ProductGrid.tsx

import { Badge } from "@/app/components/ui/Badge";
import { Card } from "@/app/components/ui/Card";
import { ProductMediaPlaceholder } from "./ProductMediaPlaceholder";
import { PRODUCTS, Product } from "./content";
import { colors, domainColors } from "@/app/lib/tokens";

const SPAN_CLASS: Record<Product["size"], string> = {
  // 4-col grid on larger screens, dense-packed. lg tiles take a 2x2 block,
  // md take a 2x1 row, sm take a single cell — grid-flow-dense fills gaps
  // automatically so nothing needs manual row/col placement.
  lg: "sm:col-span-2 sm:row-span-2",
  md: "sm:col-span-2 sm:row-span-1",
  sm: "sm:col-span-1 sm:row-span-1",
};

function ProductTile({ product }: { product: Product }) {
  const accent = domainColors[product.domain];
  const isLarge = product.size === "lg";

  return (
    <Card
      accent={accent}
      className={`flex h-full flex-col ${SPAN_CLASS[product.size]}`}
    >
      <ProductMediaPlaceholder
        label={`${product.name} screenshot`}
        accent={accent}
        className={isLarge ? "mb-4 flex-1" : "mb-3"}
      />
      <Badge domain={product.domain}>{product.name}</Badge>
      <h3
        className={`font-display mt-3 ${isLarge ? "text-2xl" : "text-lg"}`}
        style={{ color: colors.ink }}
      >
        {product.name}
      </h3>
      <p
        className={`mt-2 leading-relaxed ${isLarge ? "text-sm" : "text-xs"}`}
        style={{ color: colors.inkMuted }}
      >
        {product.blurb}
      </p>
    </Card>
  );
}

export function ProductGrid() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-flow-row-dense sm:grid-cols-4 sm:auto-rows-[160px]">
      {PRODUCTS.map((p) => (
        <ProductTile key={p.name} product={p} />
      ))}
    </div>
  );
}