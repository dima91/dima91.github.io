/**
 * A photo as the full-page preview shows it (src/components/Lightbox.astro).
 * An element opens the preview by listing its photos, as JSON, in a `data-lightbox` attribute.
 */
export type LightboxPhoto = {
  src: string;
  srcset: string;
  /** size of `src` in pixels: the preview never shows the photo larger than this */
  width: number;
  height: number;
  alt: string;
};
