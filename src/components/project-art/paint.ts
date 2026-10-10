/**
 * Paint vocabulary for the project banner illustrations (inline SVG shapes).
 * Colours are theme tokens.
 * Line caps and joins are rounded on the parent <svg> (Projects.astro): that is also what turns
 * the zero-length `h.01` segments of `dots` into round dots.
 */
export const pa = {
  panel: 'fill-surface stroke-ink-soft stroke-[1.5]',
  frame: 'fill-bg stroke-line stroke-[1.5]',
  fillA: 'fill-accent-bright',
  fillM: 'fill-magenta',
  fillInk: 'fill-ink',
  dim: 'fill-ink-soft opacity-30',
  stroke: 'fill-none stroke-ink-soft stroke-[1.5]',
  strokeA: 'fill-none stroke-accent-bright stroke-2',
  strokeM: 'fill-none stroke-magenta stroke-[1.5]',
  rule: 'fill-none stroke-ink-soft stroke-[1.5] opacity-40',
  trace: 'fill-none stroke-accent-bright stroke-[1.5] opacity-45',
  ringA: 'fill-none stroke-accent-bright stroke-3',
  ringM: 'fill-none stroke-magenta stroke-3',
  dots: 'fill-none stroke-accent-bright stroke-5 opacity-60',
  dotsM: 'fill-none stroke-magenta stroke-5',
  // square dashes: the calendar's day cells
  week: 'fill-none stroke-ink-soft stroke-2 opacity-50 [stroke-dasharray:14_4] [stroke-linecap:butt]',
  cells: 'fill-none stroke-ink-soft stroke-10 opacity-30 [stroke-dasharray:14_4] [stroke-linecap:butt]',
  // modifiers
  dash: '[stroke-dasharray:4_3]',
  soft: 'opacity-60',
  faint: 'opacity-40',
};
