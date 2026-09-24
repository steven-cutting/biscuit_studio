<script lang="ts">
  import { HeaderBar } from '@steven-cutting/biscuit-games';
  import { resolve } from '$app/paths';

  import { STUDIO_DESCRIPTION, STUDIO_TITLE } from '$lib/brand';
  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The front door: the platform's chrome carrying this site's lockup, one
   * sentence, and the two places to go. `HeaderBar` carries the page's `h1`,
   * so there is no heading here.
   *
   * `home` is the site's root wherever it is served: `/biscuit_studio/` when
   * pages.yml builds the site, `/` locally, and `./` in the prerendered markup,
   * which SvelteKit writes relative so the page works from any address. The two
   * links hang off it. `base` would say the same and is deprecated in this
   * SvelteKit, and `resolve('/model/')` is typed against the routes that exist,
   * which until S03 lands is only `/`. Every selector below names an element,
   * because `svelte-check --fail-on-warnings` turns an unused selector into a
   * failed gate and an element selector cannot go stale.
   */
  const home = resolve('/');
</script>

<svelte:head>
  <title>{STUDIO_TITLE}</title>
  <meta name="description" content={STUDIO_DESCRIPTION} />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <p>
      Where Biscuit is made. The poseable model she is drawn from, the renders taken from it, and
      the illustrations that came before it, kept here so every game draws the same dog.
    </p>

    <ul role="list">
      <li><a href="{home}model/">The model</a></li>
      <li><a href="{home}gallery/">The gallery</a></li>
    </ul>
  </main>
</div>

<style>
  .page {
    max-inline-size: var(--shell-max);
    margin-inline: auto;
    padding-inline: var(--shell-pad);
  }

  main {
    padding-block: var(--s-8) var(--s-11);
    color: var(--text);
    font-family: var(--font-ui);
  }

  p {
    margin-block: 0 var(--s-8);
    color: var(--text-2);
    line-height: 1.5;
  }

  ul {
    display: grid;
    gap: var(--s-5);
    margin-block: var(--s-5) 0;
    padding: 0;
    list-style: none;
  }

  a {
    color: var(--text);
  }
</style>
