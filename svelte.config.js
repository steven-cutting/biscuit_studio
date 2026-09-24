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

/*
 * Until S03 lands, the two pages the home page links to do not exist. The
 * prerender crawler follows every link it renders and fails the build on a
 * 404, so a 404 on exactly those two paths is let through and every other
 * error still fails the build. S03 deletes this set and the `prerender` block
 * below in the same change that adds the routes.
 */
const NOT_YET_BUILT = new Set([`${base}/model/`, `${base}/gallery/`]);

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base },
    prerender: {
      handleHttpError: ({ status, path, message }) => {
        if (status === 404 && NOT_YET_BUILT.has(path)) return;
        throw new Error(message);
      }
    }
  }
};

export default config;
