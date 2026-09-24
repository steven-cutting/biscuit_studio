import {
  animationsActive,
  highContrastActive,
  type PreferencesPort
} from '@steven-cutting/biscuit-games';

/** The two attributes the device decides, given the studio's fixed settings. */
export function documentAttributes(port: PreferencesPort): {
  animations: 'on' | null;
  highContrast: 'true' | null;
} {
  return {
    animations: animationsActive(true, port.prefersReducedMotion()) ? 'on' : null,
    highContrast: highContrastActive(false, port.prefersMoreContrast()) ? 'true' : null
  };
}

/**
 * Writes them on `root` now and on every change the port reports. Returns the
 * unsubscribe. `root` is passed in rather than read from `document`, so nothing
 * here touches a global and a test hands it a jsdom element.
 */
export function applyAppearance(root: Element, port: PreferencesPort): () => void {
  const write = () => {
    const { animations, highContrast } = documentAttributes(port);
    if (animations === null) root.removeAttribute('data-animations');
    else root.setAttribute('data-animations', animations);
    if (highContrast === null) root.removeAttribute('data-high-contrast');
    else root.setAttribute('data-high-contrast', highContrast);
  };
  write();
  return port.subscribe(write);
}
