<script lang="ts">
  import { CardLabel, HeaderBar } from '@steven-cutting/biscuit-games';
  import { asset } from '$app/paths';

  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The model, and the three ways to have it. The viewer is a whole page of its
   * own rather than a frame here: it is 26 MB with its textures inlined, and it
   * carries its own light palette, which would sit inside the platform's dark
   * ground as a second break. The .blend is not served — it is an LFS object,
   * and Pages would serve its pointer as text — so that link goes to GitHub.
   *
   * `asset()` puts a file under static/ wherever the site is served:
   * /biscuit_studio/ on Pages, / locally, and a relative path in the
   * prerendered markup. `base` would say the same and is deprecated in this
   * SvelteKit. The two links into static/ carry `rel="external"` and
   * `data-sveltekit-reload` so the client router hands them to the browser
   * rather than looking for a route, which would be a 404 inside the shell.
   */
  const BLEND_URL =
    'https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend';
</script>

<svelte:head>
  <title>Biscuit Studio: the model</title>
  <meta
    name="description"
    content="The approved poseable model of Biscuit: the pose studio, the portable GLB and the Blender scene."
  />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <CardLabel>The model</CardLabel>

    <img
      src={asset('/pose-studio/previews/pose-overview.jpg')}
      alt="Biscuit in the four preset poses, each in the cream sweater: standing, sitting, lying down and with a paw raised."
      width="1920"
      height="2070"
    />

    <p>
      The approved model: the Soft Charm face, the Full Soft ears, the Longer Drape tail and the
      fitted cream sweater, on a rig of thirty-three deform bones with four preset poses. It is a
      rig for still posing. There is no facial rig, no cloth simulation and no animation.
    </p>

    <ul role="list">
      <li>
        <a href={asset('/pose-studio/viewer.html')} rel="external" data-sveltekit-reload>
          Open the pose studio
        </a>
        — poses, views and a PNG or pose file to save, in a page of its own. It needs WebGL 2 and works
        offline.
      </li>
      <li>
        <a
          href={asset('/pose-studio/model/biscuit-poseable.glb')}
          rel="external"
          data-sveltekit-reload
          download>Download the GLB</a
        >
        — the skinned standing rig with its textures and the sweater's corrective shapes. It carries standard
        PBR materials rather than the approved cel shading, so it looks different from the studio in another
        viewer.
      </li>
      <li>
        <a href={BLEND_URL}>The Blender scene on GitHub</a> — the editable native source, with the pose
        panel embedded.
      </li>
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

  img {
    display: block;
    inline-size: 100%;
    block-size: auto;
    margin-block: var(--s-5) var(--s-8);
    border: var(--rule-w) solid var(--rule);
    border-radius: var(--radius-card);
  }

  p {
    margin-block: 0 var(--s-8);
    color: var(--text-2);
    line-height: 1.5;
  }

  ul {
    display: grid;
    gap: var(--s-5);
    margin: 0;
    padding: 0;
    list-style: none;
    color: var(--text-2);
    line-height: 1.5;
  }

  a {
    color: var(--text);
  }
</style>
