import { defineCollection } from 'astro:content';
import { file } from 'astro/loaders';
import { z } from 'astro/zod';

const contacts = defineCollection({
  loader: file('src/content/contacts.yaml'),
  schema: z.object({
    order: z.number().int(),
    label: z.string(),
    value: z.string(),
    href: z.url(),
  }),
});

export const collections = { contacts };
