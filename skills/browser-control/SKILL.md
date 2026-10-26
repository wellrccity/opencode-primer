---
name: browser-control
description: Use when the user asks to open or navigate sites, inspect the DOM, click, type, fill forms, test a web app, take screenshots, read console or network, manage cookies, emulate a device, or automate any browser flow with real Chrome via the OpenCode Browser Bridge and the tools.chrome.* tools.
---

# Browser control

This skill is the usage manual for the **OpenCode Browser Bridge** integration: a local MCP server (`chrome`) plus an MV3 extension that controls real Google Chrome, with trusted input through CDP when available.

OpenCode already starts the MCP server and injects its instructions into the session. This skill complements that with the workflow, recipes, and cautions that do not fit in the short tool descriptions. In this project the server runs in **Code Mode**: the tools live under `tools.chrome.*` inside `execute` (see below). This skill does not replace the connection.

## Code Mode

This project configures the `chrome` server with `"codemode": true`. The tools do not appear directly in the native list; call them inside the `execute` tool:

```js
const status = await tools.chrome.status({});
const snap = await tools.chrome.snapshot({ tabId: 123 });
return { status, snap };
```

Rules:

- Use `tools.chrome.<name>({...})` with the same arguments as the reference (`chrome_click` becomes `tools.chrome.click`).
- Batch independent calls: `const [a, b] = await Promise.all([...])`.
- Add an explicit `return` at the end of `execute`; the returned value is what the model sees.
- `await` every call whose result matters. Pending calls are interrupted when `execute` ends.
- To go back to the direct `chrome_*` tools, set `"codemode": false` in `opencode.json` and run `opencode reload`.

## Before any action

1. Call `tools.chrome.status({})` (or `chrome_status` in direct mode). It shows the bridge state, the extension version, the open tabs, and the active tab.
2. If you see `Bridge: disconnected`, do not invent commands. Ask the user to open the extension popup and click **Connect**, check the port (`ws://127.0.0.1:8787`), and reload the extension at `chrome://extensions` if needed.
3. If more than one window or tab is open, **pass `tabId` explicitly** on every call. The active tab may be the OpenCode UI itself or one of the user's personal tabs; do not control it by mistake.
4. The MCP server must be named `chrome` in `opencode.json`. **Do not use `browser`**: OpenCode V2 has a native `browser` namespace that is denied by default and shadows MCP tools with the same names (`navigate`, `snapshot`, `click`, `screenshot`, and so on). If you just renamed it, run `opencode reload` and open a **new session**. If tools are still missing, open another session; the MCP catalog can be frozen per session in affected versions.

## Golden rules

- **Prefer refs over selectors.** Take a `chrome_snapshot` and use refs such as `f0_e12`. Refs belong to a frame (`f123_e4` is frame 123) and can go stale after DOM changes; take a new snapshot in that case.
- **Actually wait.** After clicking, typing, or navigating, use `chrome_wait_for` with a selector, text, URL, `js`, or `loadState`. Avoid guessed `sleep`.
- **Read before acting.** Use `chrome_dom` for HTML, text, attributes, styles, rects, and counts. Use `chrome_evaluate` for structured extraction or actions no tool covers.
- **CDP is the default.** `chrome_click` and `chrome_type` use trusted input (`isTrusted=true`) by default. Use `trusted:false` when the iframe needs synthetic events or when the Chrome debug banner gets in the way.
- **Do not mix `ref` and `selector`** in the same call when the tool expects a single target.
- **Confirm irreversible actions.** Before buying, deleting, sending a message, publishing, or changing settings, ask the user to confirm.
- **Protect secrets.** Cookies, tokens, sessions, and personal data should only be inspected when the task requires it. Do not copy sensitive values into the answer without need; redact when possible.
- **Do not start another server on port 8787.** The bridge belongs to OpenCode. If you get `PORT_IN_USE`, identify the process before stopping anything.
- **Restricted pages.** Chrome blocks automation on `chrome://`, the Chrome Web Store, and some internal pages. Use `http(s)`; for `file://`, enable "Allow access to file URLs" in the extension.
- **Dialogs.** Interception of `alert`/`confirm`/`prompt` is on by default. Use `chrome_dialog` to inspect the log or change the policy. If a native dialog is already blocking the tab, `chrome_dialog` may not respond; close the tab or ask the user to dismiss the dialog.

## Performance (fast defaults)

The defaults favor speed. Adjust only when the site requires it:

- `chrome_click`: `human=false` by default (no humanized mouse path). Use `human=true` only when the site reacts to abrupt movement.
- `chrome_click`: watches for navigation for about 700 ms (`detectNavigationMs`). Increase it if a click is slow to navigate.
- Navigation and post-action waits use `waitUntil="domcontentloaded"`. Ask for `load` or `networkidle` when content depends on late resources, or `none` to skip waiting.
- Prefer `chrome_snapshot` over `chrome_screenshot`; snapshots use far less context.
- Avoid guessed `sleep`: use `chrome_wait_for` with a selector, text, URL, `js`, or `loadState`.

## Standard flow

1. `tools.chrome.status({})` - connection, tabs, and active tab.
2. `chrome_tabs` (`list`/`get`) - pick the tab and keep the `tabId`.
3. `chrome_navigate` (`goto`) or `chrome_tabs` (`new`) - open the page.
4. `chrome_snapshot` - accessibility tree with refs.
5. Action: `chrome_click`, `chrome_type`, `chrome_select`, `chrome_press`, `chrome_hover`, `chrome_scroll`, `chrome_drag`, or `chrome_fill_form`.
6. `chrome_wait_for` - wait for the asynchronous effect.
7. Verification: a new `chrome_snapshot`, `chrome_dom`, or `chrome_evaluate`.
8. `chrome_screenshot` - only when the visual result truly matters.

## Quick reference

| Tool | What it is for |
| --- | --- |
| `chrome_status` | Bridge state, extension version, tabs, and active tab. |
| `chrome_tabs` | List, create, activate, close, reload, duplicate, pin, or mute tabs. |
| `chrome_navigate` | `goto`, `back`, `forward`, `reload`, `stop`; waits for the requested load state. |
| `chrome_snapshot` | Accessibility tree with refs; iframes and shadow DOM. |
| `chrome_screenshot` | Viewport, full page, or element; optional `annotate` and `grid`. |
| `chrome_click` | Click by ref, selector, text, or coordinates; CDP by default. |
| `chrome_type` | Type into input/textarea/contenteditable; clear and submit with Enter. |
| `chrome_press` | Keys and combinations: Enter, Tab, Escape, Control+A, Shift+Enter, F5. |
| `chrome_hover` | Move the mouse to open menus, tooltips, and trigger `:hover`. |
| `chrome_select` | Choose `<select>` options by value, label, or index. |
| `chrome_scroll` | Scroll page/container, go to top/bottom, or bring an element into view. |
| `chrome_wait_for` | Wait for a selector, text, URL, JS predicate, or load state. |
| `chrome_evaluate` | Run JavaScript in the main world and return JSON. |
| `chrome_dom` | Query HTML, text, attributes, styles, rects, and counts; `>>>` for shadow DOM. |
| `chrome_fill_form` | Fill several fields at once and optionally submit. |
| `chrome_upload_file` | Attach files to `<input type="file">` through CDP. |
| `chrome_console` | Read logs, warnings, errors, and unhandled rejections. |
| `chrome_network` | Read captured `fetch`/XHR requests with status and duration. |
| `chrome_cookies` | Read, create, delete, or clear cookies for the site. |
| `chrome_dialog` | Inspect `alert`/`confirm`/`prompt` and change the answering policy. |
| `chrome_highlight` | Draw temporary outlines on elements. |
| `chrome_drag` | Drag from one element/point to another. |
| `chrome_emulate` | Emulate viewport, mobile, user agent, geolocation, theme, timezone, and network. |
| `chrome_debugger` | Show, attach, or detach the CDP debugger for a tab. |

Full arguments for each tool are in `references/tool-reference.md`. Detailed recipes and diagnostics are in `references/troubleshooting.md`.

## Recipes

### Open a page and click a link

1. `chrome_navigate` with `action="goto"`, `url`, and, if needed, `newTab=true`.
2. `chrome_snapshot` with the chosen `tabId`.
3. `chrome_click` with the link ref (or `text`/`selector` when no ref exists).
4. `chrome_wait_for` with `urlIncludes` or `loadState="networkidle"`.
5. `chrome_snapshot` again to confirm the new page.

### Fill and submit a form

- For a few fields: `chrome_type` on each ref, `chrome_select` on `<select>` elements, then `chrome_click` on the submit button.
- For many fields: `chrome_fill_form` with a `fields` array; each item can use `ref` or `selector` plus `type` (`text`, `select`, `checkbox`, `radio`). Use `submit` to send it at the end.
- Prefer `chrome_wait_for` with a confirmation text or a URL change instead of assuming the submit finished.

### Dynamic content (SPA, search, modals)

1. Perform the action.
2. `chrome_wait_for` with a `selector` for the new content, `text`, `urlIncludes`, or `js`.
3. Take a new `chrome_snapshot`; the old refs may no longer be valid.
4. If the page is slow because of the network, use `loadState="networkidle"` with a reasonable `timeout`.

### Shadow DOM and iframes

- Open shadow DOM: use `chrome_dom` with a `selector` in the form `host >>> inner`, for example `#shadowHost >>> #shadowText`.
- Iframes: use `chrome_snapshot` with `allFrames=true`; the refs already encode the frame (`f123_e4`). Pass `frameId` when the tool asks for it.
- Trusted input through CDP is used in the main frame; inside iframes the agent may fall back to synthetic events. For flows that require `isTrusted`, open the iframe content directly when possible.

### Useful screenshot

- `chrome_screenshot` without a target: viewport.
- `fullPage=true`: the whole page; it can be limited on very tall pages.
- `ref` or `selector`: captures one element.
- `annotate=true`: draws the refs as labeled boxes.
- `grid=true`: adds a 100 px grid for coordinates.
- Prefer snapshots to read text; screenshots use more context.

### File upload

- Use `chrome_upload_file` with the `ref` or `selector` of the `<input type="file">` and `files` containing **absolute paths** on the machine running Chrome.
- Requires CDP and the main frame. If the input is inside an iframe, open the frame or use an alternative strategy.

### Console, network, and cookies

- `chrome_console`: logs/errors since page load; `action="clear"` empties the buffer.
- `chrome_network`: `filter` by URL fragment, `type` (`fetch`, `xmlhttprequest`, `image`), `status`, and `includeStatic=true` for static resources.
- `chrome_cookies`: provide `url` or `domain`; for focused reads, use `name` and `path`. Treat the values as secrets.

### Emulate a device

- `chrome_emulate` with `action="set"`, `width`, `height`, `mobile`, `userAgent`, `deviceScaleFactor`, `colorScheme`, `timezone`, or network conditions.
- Use `action="reset"` to clear the overrides. Requires CDP.

### Multiple tabs and windows

- `chrome_tabs` (`list`) shows every tab and window. Pass `tabId` on every call.
- `chrome_navigate` with `newTab=true` and `switchToNewTab=true` when the flow should continue in the new tab.
- After a click that opens a new tab, use `chrome_wait_for`/`chrome_tabs` to find and activate the correct tab.

## Error handling

| Symptom | What to do |
| --- | --- |
| `NOT_CONNECTED` / `NOT_READY` | Open the extension popup, click **Connect**, check the port, and reload the extension. |
| `TIMEOUT` | May be a native dialog, slow navigation, or a suspended service worker. Check `chrome_dialog`, try `chrome_wait_for`, and close the tab if it is stuck. |
| `PAGE_NOT_SCRIPTABLE` | The tab is `chrome://`, the Chrome Web Store, or a restricted page. Use an `http(s)` page or enable `file://` access. |
| `DEBUGGER_BUSY` | Close the DevTools for that tab or use `trusted:false` when possible. |
| Ref not found / stale | Take a new `chrome_snapshot`; do not reuse refs from an old tree. |
| Only 11 tools | Start a new OpenCode session or restart OpenCode; the MCP catalog may be frozen. |
| Upload fails | Confirm the absolute path, the input in the main frame, and that CDP is active. |

More detailed diagnostics: `references/troubleshooting.md`.

## Safety and responsibility

- The extension has broad access to the browser: tabs, DOM, cookies, screenshots, and the debugger. Use it only for the requested task.
- Do not exfiltrate cookies, tokens, or personal data. If you must inspect them, summarize or redact.
- Do not bypass authentication, CAPTCHAs, or site policies.
- Confirm irreversible actions with the user.
- Bridge traffic stays on loopback; do not expose the port to the network.

## Useful files

- `README.md` - installation, configuration, and reference.
- `extension/background.js` - service worker, routing, and commands.
- `extension/content/agent.js` - snapshot, refs, DOM, and interaction.
- `extension/content/page-hooks.js` - console, network, and dialogs in the MAIN world.
- `extension/lib/cdp.js` - trusted input, screenshots, and upload.
- `server/src/tools.js` - MCP tool definitions.
- `references/tool-reference.md` - arguments for every tool.
- `references/troubleshooting.md` - errors, connection, and session.
