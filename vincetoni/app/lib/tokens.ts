// VINCETONI design tokens
// Neubrutalist-lite: flat color, thick ink borders, hard offset shadows.
// Shared by the website and the team dashboard so both feel like one product.

export const colors = {
  base: "#FAFAF7", // off-white background
  ink: "#14151A", // text + borders
  inkMuted: "#5B5952",
  violet: "#6C4DFF", // primary pop
  coral: "#FF5C5C", // secondary pop
  lime: "#D9F154", // highlight only, never a large fill`r`n  cyan: "#0B99C6", // high-energy illustration backdrop
} as const;

// Per-domain tag colors — used as small badge fills, never full backgrounds
export const domainColors = {
  tech: "#6C4DFF",
  creative: "#FF5C5C",
  learn: "#2FB88E",
} as const;

export type DomainKey = keyof typeof domainColors;

// Hard offset shadow instead of a blurred SaaS drop-shadow
export const hardShadow = (offset = 4) => `${offset}px ${offset}px 0px 0px ${colors.ink}`;

export const radii = {
  sm: "8px",
  md: "14px",
  lg: "20px",
};