<script lang="ts">
  import { CardLabel, HeaderBar } from '@steven-cutting/biscuit-games';

  import Lockup from '$lib/components/Lockup.svelte';

  import coolBody from '../../../assets/illustrations/good/cool-body.png';
  import coolHead from '../../../assets/illustrations/good/cool-head.png';
  import warmBody from '../../../assets/illustrations/good/warm-body.png';
  import warmHead from '../../../assets/illustrations/good/warm-head.png';
  import warmHeadBashful from '../../../assets/illustrations/good/warm-head-bashful.png';
  import warmHeadBashfulBlush from '../../../assets/illustrations/good/warm-head-bashful-blush-exaggerated.png';
  import warmHeadChinLifted from '../../../assets/illustrations/good/warm-head-chin-lifted.png';
  import warmHeadEyeSlant from '../../../assets/illustrations/good/warm-head-eye-slant.png';
  import warmHeadLookingUp from '../../../assets/illustrations/good/warm-head-looking-up.png';
  import warmHeadSad from '../../../assets/illustrations/good/warm-head-sad.png';
  import warmHeadSideEye from '../../../assets/illustrations/good/warm-head-side-eye.png';

  /*
   * The cel set: two bodies and nine heads, two colour grades, made to be mixed
   * and matched. Imported rather than read from static/ so the build fingerprints
   * each file and a stale cache cannot show an old drawing under a new name.
   *
   * Every figure carries its own caption and its own alt text, because the
   * caption says what the drawing is for and the alt says what is in it, and a
   * reader who hears only one of them should not lose the other.
   */
  const FIGURES = [
    {
      src: warmHead,
      caption: 'Warm head, resting',
      alt: 'Biscuit’s head in the warm grade, in three-quarter view: a cream topknot, long russet ears and brown eyes with a soft, open gaze.'
    },
    {
      src: warmBody,
      caption: 'Warm body',
      alt: 'Biscuit’s body in the warm grade, sitting in the cream turtleneck sweater with her tail curled beside her, drawn without a head so a head can be placed on it.'
    },
    {
      src: coolHead,
      caption: 'Cool head, resting',
      alt: 'The same resting head in the cool grade, the cream fur turned grey.'
    },
    {
      src: coolBody,
      caption: 'Cool body',
      alt: 'The same sitting body in the cool grade, the sweater and fur turned grey, drawn without a head.'
    },
    {
      src: warmHeadBashful,
      caption: 'Warm head, bashful',
      alt: 'Biscuit’s head with the eyes closed in a contented squint.'
    },
    {
      src: warmHeadBashfulBlush,
      caption: 'Warm head, bashful with blush',
      alt: 'Biscuit’s head with the eyes closed in a squint and a pink blush, hatched with short strokes, on both cheeks.'
    },
    {
      src: warmHeadChinLifted,
      caption: 'Warm head, chin lifted',
      alt: 'Biscuit’s head with the chin raised, looking down her nose through heavy lids.'
    },
    {
      src: warmHeadEyeSlant,
      caption: 'Warm head, eye slant',
      alt: 'Biscuit’s head with the eyes half closed under lowered lids, unimpressed.'
    },
    {
      src: warmHeadLookingUp,
      caption: 'Warm head, looking up',
      alt: 'Biscuit’s head tilted, the eyes raised to something above and to one side.'
    },
    {
      src: warmHeadSad,
      caption: 'Warm head, sad',
      alt: 'Biscuit’s head with the brows drawn together and the eyes cast down and away.'
    },
    {
      src: warmHeadSideEye,
      caption: 'Warm head, side eye',
      alt: 'Biscuit’s head facing forward with the eyes slid up and to one side.'
    }
  ] as const;
</script>

<svelte:head>
  <title>Biscuit Studio: the gallery</title>
  <meta
    name="description"
    content="The cel illustrations of Biscuit: two bodies and nine heads in two colour grades."
  />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <CardLabel>The gallery</CardLabel>

    <p>
      Eleven cel drawings made before the model: two bodies and nine heads, in a warm and a cool
      grade, cut to be mixed and matched. They were generated with ChatGPT from photographs of the
      real dog and picked by hand. They are studio material: nothing here has been cleared to leave
      the studio, and the platform's design direction decides whether any of it can.
    </p>

    <ul role="list">
      {#each FIGURES as figure, index (figure.caption)}
        <li>
          <figure>
            <img
              src={figure.src}
              alt={figure.alt}
              loading={index === 0 ? 'eager' : 'lazy'}
              decoding="async"
            />
            <figcaption>{figure.caption}</figcaption>
          </figure>
        </li>
      {/each}
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
    margin-block: var(--s-5) var(--s-8);
    color: var(--text-2);
    line-height: 1.5;
  }

  ul {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
    gap: var(--s-5);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  figure {
    margin: 0;
  }

  img {
    display: block;
    inline-size: 100%;
    block-size: auto;
    background: var(--surface);
    border: var(--rule-w) solid var(--rule);
    border-radius: var(--radius-card);
  }

  figcaption {
    margin-block-start: var(--s-2);
    color: var(--text-3);
    font-size: var(--fs-small);
  }
</style>
