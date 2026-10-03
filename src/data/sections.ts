export type SectionId = 'about' | 'experience' | 'projects' | 'skills' | 'publications' | 'contact';

/**
 * Sections on the page, in display order. Drives the nav links and the "01", "02"… labels,
 * so a section shows up in both as soon as it is added here.
 * `about` (the hero) is linked but not numbered; `contact` is the nav call to action.
 */
export const sections: SectionId[] = ['about', 'contact'];

const numbered = sections.filter((id) => id !== 'about');

export function sectionNumber(id: SectionId): string {
  return String(numbered.indexOf(id) + 1).padStart(2, '0');
}
