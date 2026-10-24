// Measure the bytes on the wire for one or more pages in headless Chrome.
// It adds Network.loadingFinished.encodedDataLength for every request (transfer size, with headers).
// Usage: node measure_page_weight.mjs <url> [<url> ...]   (set BLOCK=1 to block images and fonts)
// Needs Node.js 22 or later (built-in WebSocket) and Google Chrome. Set CHROME to the Chrome binary if it is not at the macOS default path.
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const urls = process.argv.slice(2);
if (urls.length === 0) { console.error("usage: node measure_page_weight.mjs <url> [<url> ...]"); process.exit(2); }
const port = Number(process.env.PORT || 9333);
const chromePath = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const profile = mkdtempSync(join(tmpdir(), "page-weight-"));
const chrome = spawn(chromePath, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--window-size=1366,900", "--lang=en-US", "--accept-lang=en-US", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); } catch {}
}
if (!target) { chrome.kill(); throw new Error("Chrome did not start"); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map(); const listeners = [];
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); } else listeners.forEach((f) => f(m));
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Network.enable");
await send("Page.enable");
await send("Network.setCacheDisabled", { cacheDisabled: true });
if (process.env.BLOCK) {
  await send("Network.setBlockedURLs", { urls: ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*.avif", "*.woff2", "*.woff", "*.ttf", "*.svg", "*.mp4", "*.m3u8"] });
}
const waitMs = Number(process.env.WAIT_MS || 15000);
for (const url of urls) {
  let bytes = 0, requests = 0; const byType = {}; const types = new Map();
  const onEvent = (m) => {
    if (m.method === "Network.responseReceived") types.set(m.params.requestId, m.params.type);
    if (m.method === "Network.loadingFinished") {
      requests++; bytes += m.params.encodedDataLength;
      const t = types.get(m.params.requestId) || "Other";
      byType[t] = (byType[t] || 0) + m.params.encodedDataLength;
    }
  };
  listeners.push(onEvent);
  await send("Page.navigate", { url });
  await sleep(waitMs);
  listeners.splice(listeners.indexOf(onEvent), 1);
  const title = (await send("Runtime.evaluate", { expression: "document.title", returnByValue: true })).result.value;
  console.log(JSON.stringify({ url, title: title.slice(0, 80), requests, bytes, byType, measuredAt: new Date().toISOString() }));
}
chrome.kill();
process.exit(0);
