"use client"
// app/style-guide/page.tsx
// A living style guide: renders the real components so the docs never
// drift out of sync with what's actually in the codebase.

import { Button } from "@/app/components/ui/Button";
import { Badge } from "@/app/components/ui/Badge";
import { Card } from "@/app/components/ui/Card";
import { Nav } from "@/app/components/ui/Nav";
import { Chip } from "@/app/components/ui/Chip";
import { Input } from "@/app/components/ui/Input";
import { Textarea } from "@/app/components/ui/Textarea";
import { colors, domainColors } from "@/app/lib/tokens";

function Swatch({ name, hex }: { name: string; hex: string }) {
  return (
    <div className="flex items-center gap-3">
      <div
        className="h-10 w-10 border-2"
        style={{ background: hex, borderColor: colors.ink, borderRadius: 8 }}
      />
      <div className="text-sm">
        <div className="font-semibold" style={{ color: colors.ink }}>
          {name}
        </div>
        <div style={{ color: colors.inkMuted }}>{hex}</div>
      </div>
    </div>
  );
}

export default function StyleGuidePage() {
  return (
    <main style={{ background: colors.base }} className="min-h-screen py-16 sm:px-10">
      <div className="mx-auto max-w-4xl space-y-16">
        <div>
          <h1 className="font-display text-4xl" style={{ color: colors.ink }}>
            VINCETONI style guide
          </h1>
          <p className="mt-2" style={{ color: colors.inkMuted }}>
            Living reference for colors, type, and components. If it's on
            this page, it's a real component you can import.
          </p>
        </div>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Colors
          </h2>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            <Swatch name="Base" hex={colors.base} />
            <Swatch name="Ink" hex={colors.ink} />
            <Swatch name="Violet" hex={colors.violet} />
            <Swatch name="Coral" hex={colors.coral} />
            <Swatch name="Lime" hex={colors.lime} />
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Buttons
          </h2>
          <div className="flex flex-wrap gap-4">
            <Button variant="primary">Primary action</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="ghost">Ghost</Button>
          </div>
          <p className="mt-3 text-sm" style={{ color: colors.inkMuted }}>
            {"<Button variant=\"primary\">Join us</Button>"}
          </p>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Badges (domain tags)
          </h2>
          <div className="flex flex-wrap gap-3">
            <Badge domain="tech">AI & Software</Badge>
            <Badge domain="creative">Music & Games</Badge>
            <Badge domain="learn">Education</Badge>
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Cards
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <Card accent={domainColors.tech}>
              <Badge domain="tech">DevPilot</Badge>
              <p className="mt-3" style={{ color: colors.ink }}>
                An AI-powered developer workspace and agent platform.
              </p>
            </Card>
            <Card accent={domainColors.creative}>
              <Badge domain="creative">Karaoke</Badge>
              <p className="mt-3" style={{ color: colors.ink }}>
                Social music and karaoke, with scoring and challenges.
              </p>
            </Card>
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Nav
          </h2>
          <div style={{ border: `2px solid ${colors.ink}`, borderRadius: 14, overflow: "hidden" }}>
            <Nav
              links={[
                { label: "Products", href: "#" },
                { label: "Community", href: "#" },
                { label: "Products", href: "#" },
                { label: "Community", href: "#" },
              ]}
              ctaLabel="Join us"
              ctaHref="#"
            />
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Chips (filters / selectable tags)
          </h2>
          <div className="flex flex-wrap gap-3">
            <Chip selected>All</Chip>
            <Chip>Games</Chip>
            <Chip>Music</Chip>
            <Chip onRemove={() => {}}>AI (removable)</Chip>
          </div>
          <p className="mt-3 text-sm" style={{ color: colors.inkMuted }}>
            Use Chip for filters/selectable tags — use Badge instead for a
            fixed, color-coded label on a card.
          </p>
        </section>

        <section>
          <h2 className="mb-4 font-display text-xl" style={{ color: colors.ink }}>
            Form inputs
          </h2>
          <div className="grid max-w-md gap-4">
            <Input label="Email" placeholder="you@example.com" />
            <Textarea label="Message" placeholder="What are you building?" />
          </div>
        </section>
      </div>
    </main>
  );
}