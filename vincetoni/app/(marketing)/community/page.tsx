// app/(marketing)/community/page.tsx

import { Chip } from "@/app/components/ui/Chip";
import { SOCIAL_LINKS } from "../components/content";
import { colors } from "@/app/lib/tokens";

export default function CommunityPage() {
  return (
    <section className="mx-auto max-w-3xl px-5 py-14 sm:px-10 sm:py-20">
      <h1 className="font-display mb-3 text-3xl sm:text-4xl md:text-5xl" style={{ color: colors.ink }}>
        Come build with us
      </h1>
      <p className="mb-8 max-w-[48ch]" style={{ color: colors.inkMuted }}>
        Follow along, drop feedback, or just hang out while we build.
      </p>
      <div className="flex flex-wrap gap-3">
        {SOCIAL_LINKS.map((s) => (
          <Chip key={s}>{s}</Chip>
        ))}
      </div>
    </section>
  );
}