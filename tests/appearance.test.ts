import { createFakePreferences } from '@steven-cutting/biscuit-games';
import { describe, expect, it } from 'vitest';

import { applyAppearance, documentAttributes } from '../src/lib/appearance';

/*
 * appearance.allium — the `Appearance` surface, as this site honours it with
 * its settings fixed at the platform default: theme dark, high contrast off,
 * animations on. Only the device can move the two attributes below.
 */
describe('documentAttributes', () => {
  // ReducedMotionOverridesTheAnimationSetting: the device wins.
  it('keeps animations on while the device asks for no less motion', () => {
    expect(documentAttributes(createFakePreferences()).animations).toBe('on');
  });

  it('turns animations off when the device asks for less motion', () => {
    const port = createFakePreferences({ prefersReducedMotion: true });

    expect(documentAttributes(port).animations).toBeNull();
  });

  // MoreContrastFromTheDeviceTurnsHighContrastOn.
  it('leaves high contrast off while the device is silent', () => {
    expect(documentAttributes(createFakePreferences()).highContrast).toBeNull();
  });

  it('turns high contrast on when the device asks for more', () => {
    const port = createFakePreferences({ prefersMoreContrast: true });

    expect(documentAttributes(port).highContrast).toBe('true');
  });
});

describe('applyAppearance', () => {
  // SystemFollowsTheDeviceAsItChanges: written now, and again on every change.
  it('writes both attributes on the element it is given, and follows the device', () => {
    const root = document.createElement('div');
    const port = createFakePreferences();

    applyAppearance(root, port);

    expect(root).toHaveAttribute('data-animations', 'on');
    expect(root).not.toHaveAttribute('data-high-contrast');

    port.set({ prefersReducedMotion: true, prefersMoreContrast: true });

    expect(root).not.toHaveAttribute('data-animations');
    expect(root).toHaveAttribute('data-high-contrast', 'true');
  });

  it('stops following the device once unsubscribed', () => {
    const root = document.createElement('div');
    const port = createFakePreferences();
    const stop = applyAppearance(root, port);

    stop();
    port.set({ prefersReducedMotion: true });

    expect(root).toHaveAttribute('data-animations', 'on');
  });
});
