import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { STUDIO_NAME } from '../src/lib/brand';
import Gallery from '../src/routes/gallery/+page.svelte';
import Model from '../src/routes/model/+page.svelte';

const LOCKUP = `biscuit games / ${STUDIO_NAME}`;

describe('the model page', () => {
  it('carries the lockup as its only level-one heading and names its section', () => {
    render(Model);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(LOCKUP);
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('The model');
  });

  it('hands the reader to the pose studio as a whole page', () => {
    render(Model);

    expect(screen.getByRole('link', { name: 'Open the pose studio' })).toHaveAttribute(
      'href',
      '/pose-studio/viewer.html'
    );
  });

  it('offers the GLB for download and the Blender scene on GitHub', () => {
    render(Model);

    expect(screen.getByRole('link', { name: 'Download the GLB' })).toHaveAttribute(
      'href',
      '/pose-studio/model/biscuit-poseable.glb'
    );
    expect(screen.getByRole('link', { name: 'The Blender scene on GitHub' })).toHaveAttribute(
      'href',
      expect.stringContaining('/blob/main/assets/models/biscuit/model/biscuit-poseable.blend')
    );
  });

  it('describes its preview image', () => {
    render(Model);

    expect(screen.getByRole('img').getAttribute('alt')).toMatch(/four preset poses/);
  });

  it('names the toe beans the current model carries', () => {
    render(Model);

    expect(screen.getByText(/charcoal toe beans on all four paws/)).toBeInTheDocument();
  });
});

describe('the gallery page', () => {
  it('carries the lockup and names its section', () => {
    render(Gallery);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(LOCKUP);
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('The gallery');
  });

  it('lists eleven captioned figures, every one with alt text', () => {
    render(Gallery);

    const figures = screen.getAllByRole('figure');

    expect(figures).toHaveLength(11);
    for (const image of screen.getAllByRole('img')) {
      expect(image.getAttribute('alt')?.trim()).not.toBe('');
    }
  });

  it('says the drawings were generated and have not left the studio', () => {
    render(Gallery);

    expect(screen.getByText(/generated with ChatGPT/)).toBeInTheDocument();
    expect(screen.getByText(/has been cleared to leave the studio/)).toBeInTheDocument();
  });
});
