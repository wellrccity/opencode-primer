# Mobile Web and PWA

Use when: building or reviewing a touch-first site or installable web app that must hold up on phones, slow networks, and offline moments.

## Layout and hierarchy

- Design the smallest supported view first: 320 CSS px wide with no horizontal scroll.
- One primary action per screen region. On phones, anchor it in the bottom third where thumbs rest; secondary actions move up or into an overflow menu.
- Keep top-of-screen areas for content and status, not for frequent taps. Reaching the top edge requires a grip change.
- Interactive targets: 24x24 CSS px minimum (WCAG 2.2 AA, 2.5.8), 44x44 CSS px recommended (2.5.5 is AAA at 44x44). Space targets at least 8 CSS px apart.
- Reserve room for safe areas and the on-screen keyboard before placing fixed bars.

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
.action-bar { padding-bottom: max(12px, env(safe-area-inset-bottom)); }
```

- Never set `maximum-scale=1` or `user-scalable=no`; it blocks pinch zoom and fails 1.4.4.
- Use `100dvh` or `min-height: 100svh` rather than `100vh` for full-height screens; static viewport units get hidden behind browser chrome.
- Sticky headers cost vertical space on a small screen. Make them compact, hide-on-scroll-down only if a visible path back exists, and never cover focused inputs.

## Required states

| State | What the user sees |
| --- | --- |
| First load | Content skeleton matching final layout, no spinner-only screen |
| Cached load | Data plus a subtle "updated <time>" or stale marker |
| Offline | Persistent, dismissible banner plus a clear list of unavailable actions |
| Queued write | Item marked "pending sync", not silently dropped |
| Sync failure | Retry control, preserved input, no data loss |
| Empty | Cause plus the next action |
| Error | Message, retry, and a support path |
| Install | Discoverable entry after value is shown, dismissible |
| Update ready | Non-blocking prompt with "reload" and "later" |
| Permission denied | Explanation and a manual fallback |

## Interaction rules

- Every gesture needs a visible alternative: swipe to archive pairs with a menu action; pull-to-refresh pairs with a refresh button.
- Never bind a destructive action to swipe alone. Require confirmation or offer undo.
- Keep system gestures working: no full-edge swipe traps that break back navigation or the home indicator.
- Long press is optional sugar, never the only route to a function.
- Scroll containers need `-webkit-overflow-scrolling` behavior left to the platform and a visible affordance that more content exists.
- Inputs: correct `type`, `inputmode`, `autocomplete`, and `enterkeyhint` so the right keyboard appears. Label every field; placeholder-only labels fail once typing starts.
- When the keyboard opens, scroll the focused field into view and keep the submit control reachable. Avoid `position: fixed` footers that jump above the keyboard without layout checks.

## Data and edge cases

- Cache per resource intent: app shell cache-first, API reads network-first with cache fallback, writes queued and replayed with an idempotency key.
- Cap cache size and prune old entries; storage is shared and can be evicted without notice.
- Handle a cache version bump: activate the new service worker only when no critical flow is mid-write, or warn the user first.
- On logout, delete cached private responses and queued writes for that account.
- Detect offline with `navigator.onLine` plus a real request; the flag alone lies behind captive portals.
- Retry with backoff and a visible counter. Stop after a bounded number of attempts and surface manual retry.
- Validate on the server; treat client validation as UX only.

## Accessibility

- Use landmarks, headings in order, and native controls; a styled `div` button loses keyboard and screen-reader behavior.
- Move focus into an opened sheet, trap it there, and return it to the trigger on close. Announce offline, sync, and update changes with a polite live region.
- Support reflow at 320 CSS px and 200 percent zoom (1.4.10) and 1.4.4 resize text. Long translations must not clip fixed-width controls.
- Respect `prefers-reduced-motion`: replace slide and parallax with short fades or no transition. Page transitions must not be the only signal of navigation.
- Dark mode is a token swap, not an inversion: keep 4.5:1 text contrast (1.4.3), 3:1 for large text and UI boundaries (1.4.11), and recheck images, shadows, and status colors. Never encode state in color alone.
- Test with a screen reader using one-hand reach, and verify orientation change keeps content and state.

## Performance

- Core Web Vitals targets at the 75th percentile: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less. Measure field data before optimizing.
- Set budgets in the build and fail on regression. Example starting points, labeled as recommendations: 170 KB compressed initial JS, 100 KB critical CSS, total page weight under 1 MB on the mobile profile.
- Serve responsive images with `srcset` and `sizes`, modern formats with fallback, explicit `width` and `height`, and `loading="lazy"` only below the fold. Preload or `fetchpriority="high"` the LCP image.
- Subset fonts, self-host or preconnect, use `font-display: swap`, and preload only the critical face.
- Keep the service worker small and versioned; precache the shell, not the whole app. Do not cache opaque cross-origin responses blindly.
- Verify on a throttled mobile profile and a mid-range device, not only on desktop DevTools.

## Anti-patterns

- Gesture-only navigation, hidden menus, or swipe-only deletion.
- Fixed footers that overlap content, safe areas, or the keyboard.
- Blocking install interstitials on first paint, or repeated prompts after dismissal.
- Claiming "works offline" while showing a browser error page.
- Silent update that discards a form or a queued write.
- Hover-only affordances and tooltips carrying required information.
- Full-page spinners, layout-shifting banners, and animation on every transition.
- Real-data-looking placeholders left in production.

## Checklist

- [ ] No horizontal overflow at 320, 375, and 768 CSS px; layout checked in portrait and landscape.
- [ ] Every tap target measures at least 24x24 CSS px with 8 px spacing; primary actions sit in the thumb zone.
- [ ] Safe-area insets applied to fixed top and bottom bars; `viewport-fit=cover` set and no zoom blocking.
- [ ] Each gesture has a visible button or menu equivalent; no destructive swipe without confirm or undo.
- [ ] Offline reload renders cached shell and data, and every failed write shows a retry path.
- [ ] Cache version bump tested: the old worker is replaced and no queued write is lost.
- [ ] Install prompt appears only after demonstrated value and stays dismissed across reloads.
- [ ] Update prompt is non-blocking; "later" keeps the session usable.
- [ ] Keyboard opens on the correct layout, focused field stays visible, submit remains reachable.
- [ ] Dark mode and reduced motion verified; contrast ratios measured in both themes.
- [ ] Lighthouse or field data recorded for LCP, INP, CLS on a throttled profile, compared to budget.
- [ ] Images declare dimensions and `srcset`; only the LCP image is prioritized.
