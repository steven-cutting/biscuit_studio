<script lang="ts">
  import { STUDIO_DESCRIPTION, STUDIO_TITLE } from '$lib/brand';

  /*
   * A placeholder so `just frontend-build` has a route to prerender. S01
   * replaces this file with the shell: the platform's header carrying the
   * studio's lockup, and a main landmark with the site's front door in it.
   */
</script>

<svelte:head>
  <title>{STUDIO_TITLE}</title>
  <meta name="description" content={STUDIO_DESCRIPTION} />
</svelte:head>

<main>
  <p>{STUDIO_DESCRIPTION}</p>
</main>
