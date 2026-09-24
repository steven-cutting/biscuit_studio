import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/**
 * A static site with no server: every route is prerendered and the build is a
 * directory a host serves as-is.
 *
 * `paths.base` reads BASE_PATH, which pages.yml sets to `/biscuit_studio` from
 * the repository name so the app is built to live where Pages serves it; it is
 * empty locally. `just preview` needs the same value the build had. See
 * docs/how-to/deploy-to-github-pages.md.
 */
const base = process.env.BASE_PATH ?? '';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base }
  }
};

export default config;
