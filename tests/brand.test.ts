import { describe, expect, it } from 'vitest';

import { STUDIO_DESCRIPTION, STUDIO_NAME, STUDIO_TITLE } from '../src/lib/brand';

describe('the studio brand', () => {
  it('names the lockup in the platform’s own lowercase', () => {
    expect(STUDIO_NAME).toBe(STUDIO_NAME.toLowerCase());
    expect(STUDIO_NAME.trim()).not.toBe('');
  });

  it('titles and describes the document', () => {
    expect(STUDIO_TITLE.trim()).not.toBe('');
    expect(STUDIO_DESCRIPTION.trim()).not.toBe('');
    expect(STUDIO_DESCRIPTION.endsWith('.')).toBe(true);
  });
});
