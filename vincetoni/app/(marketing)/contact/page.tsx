// app/(marketing)/contact/page.tsx

import { Button } from "@/app/components/ui/Button";
import { Input } from "@/app/components/ui/Input";
import { Textarea } from "@/app/components/ui/Textarea";
import { colors } from "@/app/lib/tokens";

export default function ContactPage() {
  return (
    <section className="mx-auto max-w-lg px-5 py-14 sm:px-10 sm:py-20">
      <h1 className="font-display mb-3 text-3xl sm:text-4xl md:text-5xl" style={{ color: colors.ink }}>
        Got an idea?
      </h1>
      <p className="mb-6" style={{ color: colors.inkMuted }}>
        Tell us about it. We read everything.
      </p>
      <form className="flex flex-col gap-4">
        <Input label="Email" type="email" placeholder="you@example.com" required />
        <Textarea label="Message" placeholder="What are you building?" required />
        <Button variant="primary" type="submit" className="self-start">
          Send it
        </Button>
      </form>
    </section>
  );
}