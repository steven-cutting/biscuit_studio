import eslint from '@eslint/js';
import globals from 'globals';
import svelte from 'eslint-plugin-svelte';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {
    // `eslint .` walks the filesystem and does not read .gitignore, so the
    // generated build outputs have to be named here as well as there.
    ignores: ['.svelte-kit/', 'build/', 'coverage/', 'dist/', 'node_modules/', 'assets/', 'static/']
  },
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...svelte.configs.recommended,
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { projectService: true }
    }
  },
  {
    // `.svelte.ts` is a rune module rather than a component, and
    // eslint-plugin-svelte hands both to svelte-eslint-parser. That parser only
    // reads TypeScript when it is given one, so the glob has to name the rune
    // modules as well as the components, or the first rune module added here
    // fails to parse at its first `import type`.
    files: ['**/*.svelte', '**/*.svelte.ts', '**/*.svelte.js'],
    languageOptions: {
      parserOptions: {
        extraFileExtensions: ['.svelte'],
        parser: tseslint.parser,
        projectService: true
      }
    }
  },
  {
    ...tseslint.configs.disableTypeChecked,
    files: ['**/*.js', '*.config.ts']
  }
);
