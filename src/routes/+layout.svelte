<script lang="ts">
  import '@steven-cutting/biscuit-games/app.css';

  import { createMediaPreferences } from '@steven-cutting/biscuit-games';
  import { onMount } from 'svelte';

  import { applyAppearance } from '$lib/appearance';

  /*
   * The design system's stylesheet, imported once and nowhere below it: the
   * token vocabulary, the four palettes, the two faces and the global element
   * rules together. This site's own styles name tokens from it and restate no
   * value.
   *
   * The one place `document` is reached. Everything under src/lib/ takes its
   * element and its port as arguments; this layout is where the real ones are
   * handed over, after hydration, because at prerender there is no document
   * and no device to ask. `createMediaPreferences()` reads `globalThis.matchMedia`
   * and answers "no preference" where it is absent, so the call is safe under
   * jsdom too. The unsubscribe is returned so the listeners go when the layout
   * does.
   */
  let { children }: { children?: import('svelte').Snippet } = $props();

  onMount(() => applyAppearance(document.documentElement, createMediaPreferences()));
</script>

{@render children?.()}
