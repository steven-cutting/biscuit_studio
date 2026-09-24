/**
 * What this site is called, wherever the platform asks for a name.
 *
 * `STUDIO_NAME` is the words the lockup shows after the platform's own:
 * `Wordmark`'s `product` prop renders "biscuit games / <STUDIO_NAME>", and every
 * page's only `h1` reads exactly that. `STUDIO_TITLE` is the document title and
 * `STUDIO_DESCRIPTION` its description.
 *
 * A file of its own, because this is the one place the name is written: every
 * component, page and test reads it from here.
 */
export const STUDIO_NAME = 'studio';
export const STUDIO_TITLE = 'Biscuit Studio';
export const STUDIO_DESCRIPTION =
  'Where Biscuit is made: the model, the renders and the illustrations behind the games.';
