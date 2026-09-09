import { DomainKey, colors, domainColors } from "@/app/lib/tokens";
import { ReactNode } from "react";

type ProductVisualProps = { name: string; domain: DomainKey; className?: string };

const ICONS: Record<string, ReactNode> = {
  DevPilot: <><rect x="19" y="28" width="82" height="54" rx="9" fill="#14151A" /><rect x="24" y="33" width="72" height="44" rx="5" fill="#FAFAF7" /><path d="m34 48 10 7-10 7M54 65h16" stroke="#6C4DFF" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" /><circle cx="91" cy="32" r="14" fill="#D9F154" stroke="#14151A" strokeWidth="3" /></>,
  Studyfy: <><path d="M25 32c16-7 30-7 46 2v52c-16-9-30-9-46-2V32Z" fill="#FAFAF7" stroke="#14151A" strokeWidth="3" /><path d="M71 34c16-9 30-9 44-2v52c-14-7-28-7-44 2V34Z" fill="#DFF7ED" stroke="#14151A" strokeWidth="3" /><path d="M38 48h19M38 59h19M84 49h17M84 60h12" stroke="#2FB88E" strokeWidth="4" strokeLinecap="round" /></>,
  Karaoke: <><path d="M55 25a17 17 0 0 1 34 0v20a17 17 0 0 1-34 0V25Z" fill="#FF5C5C" stroke="#14151A" strokeWidth="3" /><path d="M48 45a24 24 0 0 0 48 0M72 69v20M57 89h30" fill="none" stroke="#14151A" strokeWidth="4" strokeLinecap="round" /><path d="m29 37 5 5 8-10M103 30l5 5 8-10" fill="none" stroke="#6C4DFF" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" /></>,
  Dance: <><circle cx="69" cy="27" r="11" fill="#FF5C5C" stroke="#14151A" strokeWidth="3" /><path d="M67 39 54 61l18 8 14-15M56 55 39 68M62 68 49 89M72 69l21 18M83 50l16-12" fill="none" stroke="#14151A" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" /></>,
  "CAP Check": <><path d="M39 25h50l13 13v50l-13 13H39L26 88V38l13-13Z" fill="#E1F5ED" stroke="#14151A" strokeWidth="3" /><path d="m46 63 12 12 24-27" fill="none" stroke="#2FB88E" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" /><circle cx="101" cy="30" r="13" fill="#D9F154" stroke="#14151A" strokeWidth="3" /></>,
  "3D Portfolio": <><path d="m64 18 34 19v39L64 96 30 76V37l34-19Z" fill="#E8E3FF" stroke="#14151A" strokeWidth="3" strokeLinejoin="round" /><path d="m30 37 34 20 34-20M64 57v39" fill="none" stroke="#14151A" strokeWidth="3" strokeLinejoin="round" /><circle cx="64" cy="57" r="9" fill="#6C4DFF" stroke="#14151A" strokeWidth="3" /></>,
};

export function ProductVisual({ name, domain, className = "" }: ProductVisualProps) {
  return <div className={`product-visual ${className}`} aria-hidden><svg viewBox="0 0 128 112" role="presentation">{ICONS[name]}</svg><span className="product-visual-glow" style={{ background: domainColors[domain] }} /><span className="product-visual-dot" style={{ background: colors.lime }} /></div>;
}
