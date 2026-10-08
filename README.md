# dima91.github.io

Personal portfolio of Luca Di Mauro, published at <https://dima91.github.io>.
A single static page in English (`/`) and Italian (`/it/`), with light and dark themes.

Built with [Astro](https://astro.build) and [Tailwind CSS](https://tailwindcss.com) only: content collections,
i18n routing, `astro:assets` and the Fonts API on the Astro side, theme tokens and utilities on the Tailwind side.

## Commands

| Command           | Action                                              |
| :---------------- | :-------------------------------------------------- |
| `npm install`     | Install dependencies (Node 22.12+)                  |
| `npm run dev`     | Start the dev server at `localhost:4321`            |
| `npm run build`   | Build the static site to `./dist/`                  |
| `npm run preview` | Serve the build locally                             |
| `npm run check`   | Type-check `.astro` and `.ts` files (`astro check`) |

## Project structure

```text
src/
├── content/              page content (YAML), one file per collection
├── content.config.ts     collection schemas
├── i18n/ui.ts            UI strings (en/it) and translation helpers
├── data/sections.ts      section order → nav links and 01, 02… labels
├── components/           one component per section, plus Card, Chips, Section, PcbBackground
│   └── project-art/      SVG banner illustrations of the project cards
├── layouts/BaseLayout.astro
├── pages/                index.astro (en) and it/index.astro, both render Home.astro
├── styles/global.css     Tailwind theme: palette, breakpoints, type scale
└── assets/               hero image, icons and project photos, optimized at build time
public/                   favicons and the downloadable CV (one PDF per language)
```

## Editing content

Everything shown on the page lives in `src/content/*.yaml` (contacts, experience, education, projects, skills,
publications, hobbies) or, for interface copy such as headings, buttons and the hero bio, in `src/i18n/ui.ts`.
The schemas in `src/content.config.ts` validate every entry at build time, so a typo fails the build with
a message pointing at the field.

- **Translations**: a text field takes a plain string when it reads the same in both languages, otherwise an
  object with both versions:

  ```yaml
  tag:
    en: Web platform
    it: Piattaforma web
  ```

  In `ui.ts`, the Italian dictionary must define every key of the English one (enforced by the type checker).
- **Order**: experience and education are sorted by `start` (`YYYY-MM`) and publications by `year`, newest first.
  Contacts, projects, skills and hobbies are sorted by their `order` field, because Astro stores entries sorted by id
  rather than in file order.
- **Layout adapts by itself**: the projects, skills and hobbies grids widen a lone last card, and the hero counts the
  publications. Adding or removing entries needs no markup change.
- **Project illustrations**: a project's `art` picks one of the components in `src/components/project-art/`.
  To add one, create a component there using the shared paint classes in `paint.ts`, then register it in
  `Projects.astro` and in the `art` enum of the schema.
- **Project photos**: a project can list photos under `images`, with the files kept in `src/assets/projects/`:

  ```yaml
  images:
    - src: ../assets/projects/pi-touch-date/month.png
      alt:
        en: Month view with the on-screen keyboard
        it: Vista mensile con la tastiera su schermo
  ```

  `src` is relative to `projects.yaml`, and `alt` is required and translatable like any other text. The first
  photo replaces the illustration in the card banner, cropped to fit, and links to the full-size photo.
- **CV**: the hero's download button serves `public/CV_EN-Luca_Di_Mauro.pdf` on the English page and
  `public/CV_IT-Luca_Di_Mauro.pdf` on the Italian one. To update a CV, replace its file keeping the name, so the
  link stays the same.

## Theme

Colors are defined once in `src/styles/global.css`: a raw palette per theme (`:root` for dark, the default, and
`:root[data-theme="light"]`) exposed to Tailwind as semantic tokens (`bg-surface`, `text-ink-soft`,
`border-line`, `text-accent`…). Components use only these tokens, so they follow the theme without
`dark:` variants. The chosen theme is stored in `localStorage` and applied before the first paint.

The PCB backdrop (`src/components/PcbBackground.astro`) is inline SVG: trace clusters anchored to the corners
and edges of the viewport, with the center left clear for the content. Each cluster is drawn in units of 1px on
a 1536px-wide screen and scaled by `--pcb-unit`; its colors are the `pcb-*` theme tokens, blended into the
background by `--pcb-strength` (lower is subtler). When editing it, keep
traces at 0°, 90° or 45° and avoid crossings, as on a real board.

## Deployment

Every push to `master` builds the site and deploys it to GitHub Pages
(`.github/workflows/deploy.yml`, using `withastro/action`). In the repository settings,
**Pages → Build and deployment → Source** must be set to **GitHub Actions**.
