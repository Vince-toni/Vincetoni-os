// app/(marketing)/components/content.ts
// Single source of truth for marketing copy + data. Pages and components
// import from here instead of hardcoding strings, so copy changes happen
// in one place.

import { DomainKey } from "@/app/lib/tokens";

export interface Product {
  name: string;
  blurb: string;
  domain: DomainKey;
  /** Controls bento tile size — see ProductGrid. */
  size: "lg" | "md" | "sm";
}

export const PRODUCTS: Product[] = [
  {
    name: "DevPilot",
    blurb: "An AI command center for developers — projects, agents, repos, all in one place.",
    domain: "tech",
    size: "lg",
  },
  {
    name: "Studyfy",
    blurb: "AI that actually helps you study, not just another app that tracks your homework.",
    domain: "learn",
    size: "md",
  },
  {
    name: "Karaoke",
    blurb: "Sing, get scored, compete with friends. Social music, but make it a game.",
    domain: "creative",
    size: "md",
  },
  {
    name: "Dance",
    blurb: "Learn trending dances, get scored on timing, battle your friends.",
    domain: "creative",
    size: "sm",
  },
  {
    name: "CAP Check",
    blurb: "Spot the fakes. AI that explains why something's misleading, not just that it is.",
    domain: "learn",
    size: "sm",
  },
  {
    name: "3D Portfolio",
    blurb: "An interactive 3D playground built with Three.js — because flat websites are boring.",
    domain: "tech",
    size: "sm",
  },
];

export const DROPS = [
  { date: "This week", text: "DevPilot agent workspace hit its first internal milestone." },
  { date: "Last month", text: "Started prototyping Dance's movement scoring." },
  { date: "2 months ago", text: "CAP Check's first context-explainer model went into testing." },
];

export const NAV_LINKS = [
  { label: "What we make", href: "/products" },
  { label: "Community", href: "/community" },
  { label: "Updates", href: "/updates" },
];

export const HERO_COPY = {
  badge: `⚡ ${PRODUCTS.length} products actively in the lab`,
  headline: "We build stuff.",
  highlight: "AI, games, music",
  headlineEnd: "— whatever the idea needs.",
  sub: "VINCETONI is an independent team turning ideas into real products. No single lane, no corporate mission statement — just stuff we actually want to exist.",
};

export const PHILOSOPHY_COPY =
  "We think good ideas shouldn't have to fit inside one industry.";
export const PHILOSOPHY_HIGHLIGHT = "So we don't make them.";

export const SOCIAL_LINKS = ["Discord", "Instagram", "TikTok", "X"];