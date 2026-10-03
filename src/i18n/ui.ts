/** Locales configured in astro.config.mjs, with the label shown in the language toggle. */
export const languages = { en: 'EN', it: 'IT' } as const;

export type Lang = keyof typeof languages;

export const defaultLang: Lang = 'en';

const en = {
  'meta.title': 'Luca Di Mauro — Software Engineer',
  'meta.description':
    'Luca Di Mauro is a software engineer from Siena, Italy, working on embedded systems, IoT and desktop applications for laboratory instrumentation.',

  'nav.label': 'Main',
  'nav.about': 'About',
  'nav.experience': 'Experience',
  'nav.projects': 'Projects',
  'nav.skills': 'Skills',
  'nav.publications': 'Publications',
  'nav.contact': 'Contact',

  'toggle.theme': 'Toggle light/dark theme',
  // label for switching *to* this language (see LangToggle)
  'toggle.lang': 'Read in English',

  'footer.top': 'Back to top ↑',
} as const;

export type UiKey = keyof typeof en;

/** Every key is required, so a missing translation is a type error rather than a silent fallback. */
const it: Record<UiKey, string> = {
  'meta.title': 'Luca Di Mauro — Software Engineer',
  'meta.description':
    'Luca Di Mauro è un software engineer di Siena, specializzato in sistemi embedded, IoT e applicazioni desktop per la strumentazione di laboratorio.',

  'nav.label': 'Principale',
  'nav.about': 'Chi sono',
  'nav.experience': 'Esperienza',
  'nav.projects': 'Progetti',
  'nav.skills': 'Competenze',
  'nav.publications': 'Pubblicazioni',
  'nav.contact': 'Contatti',

  'toggle.theme': 'Cambia tema chiaro/scuro',
  'toggle.lang': 'Leggi in italiano',

  'footer.top': 'Torna su ↑',
};

const ui: Record<Lang, Record<UiKey, string>> = { en, it };

/** Maps `Astro.currentLocale` to a supported language. */
export function getLang(locale: string | undefined): Lang {
  return locale && locale in languages ? (locale as Lang) : defaultLang;
}

export function useTranslations(lang: Lang) {
  return (key: UiKey) => ui[lang][key];
}
