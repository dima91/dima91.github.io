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

  'hero.place': 'Siena, Italy',
  'hero.bio1':
    'I build software that lives close to the hardware: firmware for custom embedded boards, and the desktop, web and network tooling around them. Nine years across research, product companies and clinical laboratory instrumentation.',
  'hero.bio2':
    'Today I develop software for diagnostic laboratory instruments at DIESSE and lead the development of a desktop application for ESR exam management, including DAS-28 parameter calculation.',
  'hero.cta.contact': 'Get in touch',
  'hero.cta.experience': 'See experience',
  'hero.alt':
    'Illustration of a laptop showing a system status dashboard, connected to server racks on one side and to an ESP32 board with sensors and LEDs on the other',
  'stats.label': 'Highlights',
  'stats.years': 'years building software',
  'stats.pubs': 'IEEE publications',
  'stats.plugtests': 'ETSI Plugtests',

  'exp.title': 'Experience',
  'exp.present': 'Present',
  'edu.title': 'Education',

  'proj.title': 'Projects',
  'proj.view': 'View on',

  'skills.title': 'Skills',

  'pubs.title': 'Publications',

  'contact.title': 'Let’s talk',
  'contact.lead':
    'Open to interesting projects in embedded, IoT and desktop software. The quickest way to reach me is email.',

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

  'hero.place': 'Siena, Italia',
  'hero.bio1':
    'Costruisco software che vive vicino all’hardware: firmware per schede embedded custom e gli strumenti desktop, web e di rete che le circondano. Nove anni tra ricerca, aziende di prodotto e strumentazione per laboratori clinici.',
  'hero.bio2':
    'Oggi sviluppo il software per gli strumenti diagnostici di laboratorio di DIESSE e guido lo sviluppo di un’applicazione desktop per la gestione degli esami VES, incluso il calcolo del parametro DAS-28.',
  'hero.cta.contact': 'Contattami',
  'hero.cta.experience': 'Vedi esperienza',
  'hero.alt':
    'Illustrazione di un laptop che mostra una dashboard di stato del sistema, collegato da un lato a rack di server e dall’altro a una scheda ESP32 con sensori e LED',
  'stats.label': 'In evidenza',
  'stats.years': 'anni di sviluppo',
  'stats.pubs': 'pubblicazioni IEEE',
  'stats.plugtests': 'ETSI Plugtests',

  'exp.title': 'Esperienza',
  'exp.present': 'Presente',
  'edu.title': 'Formazione',

  'proj.title': 'Progetti',
  'proj.view': 'Vedi su',

  'skills.title': 'Competenze',

  'pubs.title': 'Pubblicazioni',

  'contact.title': 'Parliamone',
  'contact.lead':
    'Aperto a progetti interessanti in ambito embedded, IoT e software desktop. Il modo più rapido per raggiungermi è l’email.',

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

/** Translatable text from a content collection (see `text` in src/content.config.ts). */
export type Localized = string | Record<Lang, string>;

export function l(value: Localized, lang: Lang): string {
  return typeof value === 'string' ? value : value[lang];
}

/** "2021-09", "2024-06" → "09/2021 — 06/2024"; no end means "Present". */
export function formatPeriod(start: string, end: string | undefined, lang: Lang): string {
  const month = (ym: string) => ym.split('-').reverse().join('/');
  return `${month(start)} — ${end ? month(end) : ui[lang]['exp.present']}`;
}
