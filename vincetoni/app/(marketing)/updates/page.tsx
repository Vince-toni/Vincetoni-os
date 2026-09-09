// app/(marketing)/updates/page.tsx

import { DROPS } from "../components/content";
import { colors } from "@/app/lib/tokens";

export default function UpdatesPage() {
  return (
    <section className="mx-auto max-w-3xl px-5 py-14 sm:px-10 sm:py-20">
      <h1 className="font-display mb-8 text-3xl sm:text-4xl md:text-5xl" style={{ color: colors.ink }}>
        Recent drops
      </h1>
      <div className="space-y-6">
        {DROPS.map((d, i) => (
          <div key={i} className="flex flex-col gap-1 sm:flex-row sm:gap-4">
            <span className="w-28 shrink-0 text-sm font-semibold" style={{ color: colors.violet }}>
              {d.date}
            </span>
            <p style={{ color: colors.ink }}>{d.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}