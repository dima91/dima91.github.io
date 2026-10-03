import { defineCollection } from 'astro:content';
import { file } from 'astro/loaders';
import { z } from 'astro/zod';

/** Translatable text: a plain string when identical in every language, otherwise { en, it }. */
const text = z.union([z.string(), z.object({ en: z.string(), it: z.string() })]);

const month = z.string().regex(/^\d{4}-(0[1-9]|1[0-2])$/, 'expected YYYY-MM');

const contacts = defineCollection({
  loader: file('src/content/contacts.yaml'),
  schema: z.object({
    order: z.number().int(),
    label: z.string(),
    value: z.string(),
    href: z.url(),
  }),
});

const experience = defineCollection({
  loader: file('src/content/experience.yaml'),
  schema: z.object({
    role: text,
    company: text,
    place: z.string(),
    start: month,
    end: month.optional(),
    bullets: z.array(z.object({ lead: text.optional(), text })),
  }),
});

const education = defineCollection({
  loader: file('src/content/education.yaml'),
  schema: z.object({
    degree: text,
    school: text,
    start: month,
    end: month,
    note: text,
  }),
});

export const collections = { contacts, experience, education };
