import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { STUDIO_NAME, STUDIO_TITLE } from '../src/lib/brand';
import Page from '../src/routes/+page.svelte';

describe('the page', () => {
  it('carries the heading the platform header draws for this site', () => {
    render(Page);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      `biscuit games / ${STUDIO_NAME}`
    );
  });

  it('titles the document after the site', () => {
    render(Page);

    expect(document.title).toBe(STUDIO_TITLE);
  });

  it('has a main landmark to put the site in', () => {
    render(Page);

    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('offers the model and the gallery by name', () => {
    render(Page);

    expect(screen.getByRole('link', { name: 'The model' })).toHaveAttribute('href', '/model/');
    expect(screen.getByRole('link', { name: 'The gallery' })).toHaveAttribute('href', '/gallery/');
  });
});
