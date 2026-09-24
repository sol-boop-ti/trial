// Generates the six D7 pages (before = reconstruction, after = redesign) into ../pages/.
// Run: node src/build.js   (from deliverables/D7-pages)
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '..', 'pages');
fs.mkdirSync(OUT, { recursive: true });

// ---------- Lucide icons (2px stroke, round caps) ----------
const ICON = {
  'layout-grid': '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
  briefcase: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
  'gamepad-2': '<line x1="6" x2="10" y1="11" y2="11"/><line x1="8" x2="8" y1="9" y2="13"/><line x1="15" x2="15.01" y1="12" y2="12"/><line x1="18" x2="18.01" y1="10" y2="10"/><path d="M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z"/>',
  mic: '<path d="M12 19v3"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><rect x="9" y="2" width="6" height="13" rx="3"/>',
  'chevron-down': '<path d="m6 9 6 6 6-6"/>',
  'volume-2': '<path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.364 18.364a9 9 0 0 0 0-12.728"/>',
  play: '<polygon points="6 3 20 12 6 21 6 3"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
  'arrow-right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
};
const icon = (n, s = 16, fill = false) => `<svg class="pd-icon" width="${s}" height="${s}" viewBox="0 0 24 24" fill="${fill ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[n]}</svg>`;
const V = '<span class="verify">[verify]</span>';
const co = (n, side) => ` data-callout="${n}"${side ? ' data-side="right"' : ''}`;

// ---------- Video tile art (placeholder frames; the videos are the colour) ----------
function art(a) {
  const s = (o) => Object.entries(o).map(([k, v]) => `${k}:${v}`).join(';');
  switch (a.k) {
    case 'type': // big cropped display type, optionally dotted
      return `<div class="art" style="background:${a.bg}"><div class="big${a.dots ? ' dots' : ''}" style="${s({ color: a.fg, 'font-size': (a.size || 190) + 'px', left: (a.x ?? -8) + 'px', bottom: (a.y ?? -20) + 'px' })}">${a.w}</div>${a.sub ? `<div style="position:absolute;left:22px;top:66px;font:600 15px/1.2 Inter;color:${a.fg};opacity:.85">${a.sub}</div>` : ''}</div>`;
    case 'laptop':
      return `<div class="art" style="background:${a.bg}"><div class="scr" style="left:18%;right:18%;top:26%;bottom:22%"></div><div class="scr" style="left:12%;right:12%;bottom:18%;height:4%;border-radius:0 0 10px 10px;background:#bdb6aa"></div><div class="win" style="left:24%;top:32%;width:30%;height:5%;background:#3a3a3c"></div><div class="win" style="left:24%;top:41%;width:44%;height:4%;background:#2e2e30"></div><div class="pill" style="left:38%;top:48%;background:${a.acc};color:#2b1d00">${a.w}</div></div>`;
    case 'ui':
      return `<div class="art" style="background:${a.bg}"><div class="win" style="left:9%;top:18%;width:52%;height:58%"><div class="bar" style="left:12px;top:16px;width:40%"></div>${[0, 1, 2].map(i => `<div class="sw" style="left:12px;top:${38 + i * 30}px;width:14px;height:14px;border-radius:4px;background:${['#6b4eff', '#f2994a', '#222'][i]}"></div><div class="bar" style="left:34px;top:${42 + i * 30}px;width:38%"></div><div class="tog" style="right:12px;top:${40 + i * 30}px;background:${a.acc}"></div>`).join('')}</div><div class="win" style="left:48%;top:40%;width:44%;height:16%;border-radius:10px"><div class="bar" style="left:12px;top:18px;width:70%"></div></div>${a.w ? `<div style="position:absolute;left:9%;bottom:10%;font:700 22px/1 Inter;letter-spacing:-.02em;color:#fff">${a.w}</div>` : ''}</div>`;
    case 'pod': // podcast clip, bold captions
      return `<div class="art" style="background:${a.bg}"><div class="sw" style="left:50%;top:22%;width:96px;height:96px;margin-left:-48px;background:${a.face}"></div><div class="cap" style="top:52%;font-size:28px;color:#fff">${a.w1}</div><div class="cap" style="top:63%;font-size:28px;color:${a.hi}">${a.w2}</div><div class="wave" style="left:50%;top:75%;transform:translateX(-50%)">${[8, 16, 26, 12, 30, 18, 10, 24, 14, 8].map(h => `<span style="height:${h}px;background:${a.hi}"></span>`).join('')}</div></div>`;
    case 'phone':
      return `<div class="art" style="background:${a.bg}"><div class="win" style="left:50%;top:10%;width:46%;height:92%;margin-left:-23%;border-radius:22px;background:${a.scr}"><div class="sw" style="left:18%;top:18%;width:64%;height:auto;aspect-ratio:1;background:${a.acc}"></div><div class="pill" style="left:50%;bottom:22%;transform:translateX(-50%);background:#fff;color:#111;font-size:14px;white-space:nowrap">${a.w}</div></div></div>`;
    case 'split':
      return `<div class="art" style="background:linear-gradient(90deg,${a.bg} 0 50%,${a.bg2} 50% 100%)"><div class="big" style="color:${a.fg};font-size:${a.size || 40}px;left:22px;top:78px;line-height:1;white-space:normal;width:80%">${a.w}</div></div>`;
    case 'wash':
      return `<div class="art" style="background:linear-gradient(135deg,${a.bg},${a.bg2})"><div class="big" style="color:#fff;font-size:${a.size || 40}px;left:22px;top:78px;line-height:1;white-space:normal;width:84%;font-weight:700">${a.w}</div></div>`;
    case 'prod': // Poolday product UI frames (Meet Poolday steps)
      return a.html;
  }
}
function tile(t, extra = '') {
  return `<figure class="pd-card${t.span ? ' pd-card-wide' : ''}"${extra}>${art(t.a)}<div class="pd-card-title"><strong>${t.title}</strong>${t.tag ? `<span>${t.tag}</span>` : ''}</div><figcaption class="pd-card-caption">${t.recipe ? `<span class="pd-glass-chip">${t.recipe}</span>` : '<span></span>'}${t.sound === false ? '' : `<span class="pd-glass-chip snd" aria-label="Watch with sound">${icon('volume-2', 14)}</span>`}</figcaption></figure>`;
}

// ---------- Shared chrome ----------
function head(title, label, kind) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title>
<link rel="stylesheet" href="../../design/poolday-brand-kit/tokens.css"><link rel="stylesheet" href="../../design/poolday-brand-kit/components/bundle.css"><link rel="stylesheet" href="../src/d7.css"></head><body>
<div class="d7-label"><b>${kind}</b>${label}</div>`;
}
const nav = () => `<header class="pd-nav"><a class="pd-wordmark" href="#">Poolday.ai</a><nav class="pd-nav-links" aria-label="Main"><a class="pd-nav-link" href="#">Home</a><button class="pd-nav-link">Solutions${icon('chevron-down', 14)}</button><a class="pd-nav-link" href="#">Integrations</a><a class="pd-nav-link" href="#">Pricing</a><button class="pd-nav-link">Resources${icon('chevron-down', 14)}</button></nav><a class="pd-btn pd-btn-md" href="#">Book a 15 min demo</a></header>`;
const foot = () => `<footer class="foot"><span>© 2023 – 2026 Poolday AI</span><span><span>Privacy Policy</span><span>Terms of Service</span></span></footer><script src="../src/page.js"></script></body></html>`;
const tabs = () => `<div class="pd-tabs" role="tablist"><button class="pd-tab" aria-selected="true">${icon('layout-grid')}All</button><button class="pd-tab">${icon('briefcase')}Tech Industry</button><button class="pd-tab">${icon('gamepad-2')}Apps &amp; Games</button><button class="pd-tab">${icon('mic')}Podcasts</button></div>`;
const title2 = (lead, tail, attrs = '') => `<h2 class="pd-section-title"${attrs}>${lead}${tail ? ` <span class="pd-quiet">${tail}</span>` : ''}</h2>`;
const sk = (widths) => widths.map(w => `<span class="sk" style="width:${w}px"></span>`).join('');
const watch = () => `<a class="link-2" href="#"><span class="ring">${icon('play', 12, true)}</span>Watch a 2-min build</a>`;

// ---------- Home grid (18 tiles; titles + pairings illustrative) ----------
const HOME_TILES = [
  { span: 1, title: 'PostHog', tag: 'Launch video', recipe: 'Made with brand kit + single prompt', a: { k: 'type', bg: '#e0533d', fg: '#fff', w: 'SHIP IT', size: 230, dots: true, y: -40 } },
  { title: 'Lovable', tag: 'Feature video', recipe: 'Screen recording to pixel-perfect video', a: { k: 'laptop', bg: '#efe6d8', acc: '#f7c948', w: 'Ship it' } },
  { title: 'Marblism', tag: 'Product film', recipe: 'Made with brand kit + single prompt', a: { k: 'type', bg: '#f4f1ec', fg: '#e3342f', w: 'skyline', size: 120, y: 60, x: -30 } },
  { title: 'Dust', tag: 'Feature video', recipe: 'Figma file + brand kit', a: { k: 'ui', bg: 'linear-gradient(90deg,#f7a48b 0 50%,#8a6cf7 50%)', acc: '#ff8a3d' } },
  { title: 'ClickUp', tag: 'Launch video', recipe: 'Changelog + brand kit', a: { k: 'wash', bg: '#7b5cff', bg2: '#ff5fa2', w: 'Everything app, now faster.' } },
  { title: 'FullEnrich', tag: 'Explainer', recipe: 'Founder photos + voice', a: { k: 'split', bg: '#0f3d2e', bg2: '#16a34a', fg: '#eafff2', w: 'Find any email.' } },
  { title: 'Unity', tag: 'UA ad', recipe: 'Gameplay capture to 12 ad variants', a: { k: 'phone', bg: '#1b1b2f', scr: '#2a2250', acc: '#ffcc33', w: 'Play now' } },
  { title: 'Stillfront', tag: 'UA ad', recipe: 'App store page to UGC ad', a: { k: 'phone', bg: '#2e7d5b', scr: '#12372a', acc: '#f25c54', w: 'Download free' } },
  { title: 'Wildlife Studios', tag: 'UA ad', recipe: 'One prompt, 6 sizes', a: { k: 'type', bg: '#ffb627', fg: '#1d1300', w: 'LEVEL UP', size: 110, y: 30, x: 10 } },
  { title: 'WeWard', tag: 'App ad', recipe: 'Founder photo + voice clone + brand kit', a: { k: 'wash', bg: '#ffd84d', bg2: '#ff8a3d', w: 'Walk. Earn. Repeat.' } },
  { title: 'Podcast', tag: 'Clip', recipe: 'Full episode to snackable content for social', a: { k: 'pod', bg: '#141a2e', face: '#3a4a7a', hi: '#f7e64a', w1: 'This changed', w2: 'everything' } },
  { title: 'Podcast', tag: 'Clip', recipe: 'Full episode to snackable content for social', a: { k: 'pod', bg: '#2b1411', face: '#7a3a2a', hi: '#6ee7b7', w1: 'Nobody talks', w2: 'about this' } },
  { title: 'Lovable', tag: 'Social cut', recipe: 'Made with brand kit + single prompt', a: { k: 'type', bg: '#ff4f7b', fg: '#fff', w: 'build.', size: 170, y: -10 } },
  { title: 'PostHog', tag: 'Feature video', recipe: 'Screen recording to pixel-perfect video', a: { k: 'ui', bg: '#f1eadb', acc: '#f54e00', w: '' } },
  { title: 'Dust', tag: 'Explainer', recipe: 'Founder photos + voice', a: { k: 'split', bg: '#111827', bg2: '#1e3a8a', fg: '#dbeafe', w: 'Agents for every team.' } },
  { title: 'Podcast', tag: 'Edited episode', recipe: 'Full episode to snackable content for social', a: { k: 'pod', bg: '#1f1f1f', face: '#555', hi: '#fb923c', w1: 'Episode 112', w2: 'the full cut' } },
  { title: 'Stillfront', tag: 'UA ad', recipe: 'One prompt, 6 languages', a: { k: 'wash', bg: '#0ea5e9', bg2: '#312e81', w: 'Jugar ahora.' } },
  { title: 'ClickUp', tag: 'Launch video', recipe: 'Made with brand kit + single prompt', a: { k: 'type', bg: '#1a1a1a', fg: '#a78bfa', w: 'AI', size: 240, y: -40, x: 20 } },
];
HOME_TILES[0].span = 2; HOME_TILES[17].span = 2;

// Meet Poolday product frames
const PROD = [
  `<div class="prod"><div style="position:absolute;left:6%;top:10%;font:500 15px Inter;color:#939393">Brand kit · posthog.com</div>${['#f54e00', '#1d4aff', '#f9bd2b', '#151515', '#eeefe9'].map((c, i) => `<div style="position:absolute;left:${6 + i * 11}%;top:24%;width:9%;aspect-ratio:1;border-radius:50%;background:${c}"></div>`).join('')}<div style="position:absolute;left:6%;top:52%;font:600 64px/1 Inter;color:#f5f5f5;letter-spacing:-.03em">Aa</div><div style="position:absolute;left:22%;top:56%;font:400 15px/1.5 Inter;color:#939393">Headline · Inter Display<br>Body · Inter</div><div style="position:absolute;right:6%;top:24%;width:30%;height:62%;border-radius:10px;background:#f54e00"></div></div>`,
  `<div class="prod"><div style="position:absolute;left:6%;top:12%;max-width:58%;padding:14px 18px;border-radius:14px;background:#262626;font:400 16px/1.4 Inter;color:#f5f5f5">Launch video for the new session replay. 30s, 16:9 and 9:16.</div><div style="position:absolute;right:6%;top:38%;max-width:58%;padding:14px 18px;border-radius:14px;background:#1f1f1f;font:400 16px/1.4 Inter;color:#cfcfcf">Should it use the Figma frames from the release, or record the live product?</div><div style="position:absolute;left:6%;top:66%;max-width:40%;padding:14px 18px;border-radius:14px;background:#262626;font:400 16px/1.4 Inter;color:#f5f5f5">Live product.</div></div>`,
  `<div class="prod" style="background:#1b1b1b"><div style="position:absolute;left:8%;top:10%;right:8%;bottom:10%;border-radius:10px;background:#5b3df5"></div><div style="position:absolute;left:14%;top:24%;font:700 52px/1 Inter;color:#fff;letter-spacing:-.03em">Now in beta</div><div style="position:absolute;left:14%;top:48%;width:40%;height:22%;border-radius:8px;background:#fff"></div><div style="position:absolute;left:12.5%;top:21%;width:47%;height:18%;outline:2px solid #f5f5f5;border-radius:6px"></div><div style="position:absolute;left:44%;top:12%;padding:6px 12px;border-radius:999px;background:#f2f2f2;color:#050505;font:500 13px Inter">Make this bigger</div></div>`,
  `<div class="prod"><div style="position:absolute;inset:6%;display:grid;grid-template-columns:repeat(4,1fr);gap:8px">${['#e0533d', '#7b5cff', '#16a34a', '#ffb627', '#0ea5e9', '#ff4f7b', '#1e3a8a', '#f7c948'].map(c => `<div style="border-radius:8px;background:${c}"></div>`).join('')}</div></div>`,
];
const PILLARS = [
  ['Teach it your brand once:', 'logo, fonts, colors and Lottie, pixel-exact in every video.'],
  ['Prompt it with a storyboard, a URL, clips or an idea.', 'It asks what it needs, then finishes the job.'],
  ['Point to edit.', 'Click the exact element you want changed. Only that changes, nothing else.'],
  ['One prompt, infinite outputs:', 'hooks, actors, styles, key moments, languages and sizes.'],
];
const steps = () => `<div class="steps">${PILLARS.map((p, i) => `<div class="step"><div><span class="n">0${i + 1}</span><h3>${p[0]} <span>${p[1]}</span></h3></div>${PROD[i]}</div>`).join('')}</div>`;

const CUSTOMERS = [['Unity', ''], ['Stillfront', 'serif'], ['Wildlife Studios', 'caps'], ['WeWard', ''], ['PostHog', 'mono'], ['Lovable', ''], ['ClickUp', ''], ['Dust', 'caps'], ['Marblism', 'serif'], ['FullEnrich', '']];
const logoRow = (list, cls = '') => `<div class="logos ${cls}">${list.map(([n, c]) => `<span class="logo ${c}">${n}</span>`).join('')}</div>`;
const quotes = () => `<div class="quotes">${['CRO', 'Head of Partnerships', 'Product Designer', 'Marketing Director', 'CRO'].map(r => `<div class="quote"><div>${sk([340, 320, 300, 210]).replace(/margin: 10px auto 0/g, '')}</div><div class="who"><div class="face"></div><div><b>${r}</b><span>Customer name and logo</span></div></div></div>`).join('')}</div>`;

// ===================== HOME =====================
function homeBefore() {
  return head('Poolday home, before', 'Reconstruction of poolday.ai from the audit and page text, not a capture · tile titles illustrative · grey bars = copy not captured', 'Before') + nav() +
    `<section class="pd-hero d7-hero"><canvas class="pd-halftone" data-cx="0.47" data-cy="0.5"></canvas><div class="pd-hero-inner">
<h1 class="pd-display">The Media Superintelligence.</h1>
<p class="pd-lede">An AI agent that edits, generates and assembles on-brand videos.</p>
<a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a>
${title2('100M+ video edits made by Poolday.', 'Some examples here.')}${tabs()}</div></section>
<div class="grid-wrap"><div class="pd-grid">${HOME_TILES.map(t => tile(t)).join('')}</div></div>
<section class="sec">${title2('Meet Poolday.')}${steps()}</section>
<section class="sec">${title2('Trusted by leaders worldwide in every category')}${logoRow([...CUSTOMERS.slice(0, 4), ['Daphni', 'serif'], ...CUSTOMERS.slice(4, 8), ['LocalGlobe', ''], ...CUSTOMERS.slice(8)])}</section>
<section class="sec">${title2('From the teams running it')}${quotes()}</section>
<section class="closing"><canvas class="pd-halftone" data-cy="0.55"></canvas><div class="inner">${title2('See Poolday in action, live on a call.')}<div style="margin:-6px 0 36px">${sk([520, 380])}</div><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><div class="facts"><span>~$5–$25 per finished video</span><i>·</i><span>Month-to-month, no lock-in</span><i>·</i><span>First month $600</span></div></div></section>` + foot();
}
function homeAfter() {
  return head('Poolday home, after', 'Proposed redesign · same brand kit, same claims · tile titles illustrative · grey bars = copy unchanged', 'After') + nav() +
    `<section class="pd-hero d7-hero"><canvas class="pd-halftone" data-cx="0.47" data-cy="0.5"></canvas><div class="pd-hero-inner">
<h1 class="pd-display">The Media Superintelligence.</h1>
<p class="pd-lede">An AI agent that edits, generates and assembles on-brand videos.</p>
<div class="cta-row"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><span${co(1, 'right')}>${watch()}</span></div>
${title2('100M+ video edits made by Poolday.', 'Some examples here.')}${tabs()}</div></section>
<div class="grid-wrap"><div class="pd-grid">${HOME_TILES.map(t => tile(t)).join('')}</div></div>
<section class="sec sec-tight center"><div style="display:inline-flex;flex-direction:column;align-items:center"${co(2)}><p class="lede" style="margin-bottom:28px">Your brand, in videos like these. <span style="color:var(--ink-quiet)">It learns your brand once.</span></p><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div></section>
<section class="sec">${title2('Meet Poolday.', 'Not a tool you operate: an agent that plans, makes and fixes the whole video.', co(3))}${steps()}</section>
<section class="sec">${title2('Trusted by leaders worldwide in every category.', '', '')}<div${co(4)} style="max-width:1180px;margin:0 auto">${logoRow(CUSTOMERS)}<p class="backed">Backed by <b>Daphni</b><b>LocalGlobe</b></p></div></section>
<section class="sec">${title2('From the teams running it.')}${quotes()}</section>
<section class="closing"><canvas class="pd-halftone" data-cy="0.55"></canvas><div class="inner">${title2('See Poolday in action, live on a call.')}
<div class="callsteps"${co(5)}><div><span>Minute 1</span>You share your website.</div><div><span>Minutes 2–10</span>It builds your brand kit live and drafts a first video.${V}</div><div><span>Minutes 10–15</span>You leave with a plan and your $600 first month.</div></div>
<div class="cta-row"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a>${watch()}</div><div class="facts"><span>~$5–$25 per finished video</span><i>·</i><span>Month-to-month, no lock-in</span><i>·</i><span>First month $600</span></div></div></section>` + foot();
}

// ===================== B2B STARTUPS =====================
const USE = {
  launch: { title: 'Launch video on merge', recipe: 'Merged PR to launch video', a: { k: 'type', bg: '#e0533d', fg: '#fff', w: 'v2.4', size: 200, dots: true, y: -30, sub: 'Now live' }, big: { k: 'type', bg: '#e0533d', fg: '#fff', w: 'v2.4', size: 330, dots: true, y: 40, x: 34, sub: 'Session replay · now live' } },
  recap: { title: 'Post-call recap', recipe: 'Sales call recording to recap video', a: { k: 'split', bg: '#0f172a', bg2: '#1d4ed8', fg: '#e0e7ff', w: 'Your next steps, Maya.' } },
  demo: { title: 'The demo records itself', recipe: 'Screen recording to pixel-perfect video', a: { k: 'ui', bg: '#efe6d8', acc: '#16a34a', w: '' } },
  webinar: { title: 'Webinar to eight clips', recipe: 'Webinar recording to eight clips', a: { k: 'pod', bg: '#141a2e', face: '#3a4a7a', hi: '#f7e64a', w1: 'The one metric', w2: 'that matters' } },
  shipped: { title: 'What shipped this month', recipe: 'Changelog to monthly recap', a: { k: 'wash', bg: '#7b5cff', bg2: '#ff5fa2', w: 'September, shipped.' } },
  prospect: { title: 'One demo every prospect', recipe: 'CRM list to one demo per account', a: { k: 'laptop', bg: '#dbeafe', acc: '#fde047', w: 'Hi Acme' } },
  casestudy: { title: 'Call to case study', recipe: 'Customer call to case study', a: { k: 'split', bg: '#14532d', bg2: '#22c55e', fg: '#f0fdf4', w: 'How Acme ships weekly.' } },
  help: { title: 'Help center how-tos', recipe: 'Help article to how-to video', a: { k: 'ui', bg: 'linear-gradient(90deg,#fde68a 0 50%,#fca5a5 50%)', acc: '#2563eb', w: '' } },
  jd: { title: 'JD to recruiting video', recipe: 'Job description to recruiting video', a: { k: 'type', bg: '#111', fg: '#fbbf24', w: 'hiring', size: 150, y: 10, sub: 'Founding engineer' } },
};
const useTile = (u) => tile({ ...u, sound: false });
function b2bBefore() {
  const order = ['launch', 'recap', 'demo', 'webinar', 'shipped', 'prospect', 'casestudy', 'help', 'jd'];
  return head('Poolday for B2B startups, before', 'Reconstruction of /solutions/b2b-startups from the reported copy, not a capture · button label and layout assumed · grey bars = copy not captured', 'Before') + nav() +
    `<section class="pd-hero d7-hero" style="padding-bottom:88px"><canvas class="pd-halftone" data-cx="0.47" data-cy="0.55"></canvas><div class="pd-hero-inner">
<h1 class="pd-display">On-brand videos of any kind</h1>
<p class="pd-lede">Delegate your next video to the agent, while keeping full control. Your colors, your logo, your Figma, your animations.</p>
<a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div></section>
<div class="grid-wrap"><div class="grid3">${order.map(k => useTile(USE[k])).join('')}</div></div>
<section class="sec"><div class="feat">${['Indistinguishable from human-made', 'Built for teams', 'White-glove onboarding', '95% autonomy after 2 weeks'].map(h => `<div><h3>${h}</h3>${sk([440, 400, 260])}</div>`).join('')}</div></section>
<section class="closing"><canvas class="pd-halftone" data-cy="0.55"></canvas><div class="inner">${title2('See Poolday in action, live on a call.')}<div style="margin:-6px 0 36px">${sk([480])}</div><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div></section>` + foot();
}
function b2bAfter() {
  const order = ['shipped', 'prospect', 'casestudy', 'recap', 'demo', 'webinar', 'help', 'jd'];
  const proof = [
    { title: 'PostHog', tag: 'Launch video', recipe: 'Made with brand kit + single prompt', a: HOME_TILES[13].a },
    { title: 'Lovable', tag: 'Feature video', recipe: 'Screen recording to pixel-perfect video', a: HOME_TILES[1].a },
    { title: 'ClickUp', tag: 'Launch video', recipe: 'Changelog + brand kit', a: HOME_TILES[4].a },
    { title: 'Dust', tag: 'Feature video', recipe: 'Figma file + brand kit', a: HOME_TILES[3].a },
    { title: 'FullEnrich', tag: 'Explainer', recipe: 'Founder photos + voice', a: HOME_TILES[5].a },
  ];
  return head('Poolday for B2B startups, after', 'Proposed redesign · same brand kit, same claims · tile titles illustrative · customer videos assumed from the home grid', 'After') + nav() +
    `<section class="pd-hero d7-hero" style="padding-bottom:56px"><canvas class="pd-halftone" data-cx="0.47" data-cy="0.55"></canvas><div class="pd-hero-inner">
<h1 class="pd-display"${co(1)}>Every feature you ship, on video.</h1>
<p class="pd-lede">Delegate your next video to the agent, while keeping full control. Your colors, your logo, your Figma, your animations.</p>
<div class="cta-row"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><span class="url-field"${co(2, 'right')}><span class="badge">Free · limited</span>${icon('link')}<span class="ph">Paste your URL</span><span class="go">${icon('arrow-right')}</span></span></div>
<p class="url-note">Not ready for a call? Paste your site and get a free launch video made from it, by email.</p>
<div${co(3)} style="margin-top:56px">${logoRow([['PostHog', 'mono'], ['Lovable', ''], ['ClickUp', ''], ['Dust', 'caps'], ['Marblism', 'serif'], ['FullEnrich', '']], 'small')}</div></div></section>
<section class="sec" style="padding-top:64px">${title2('Merge a PR. Get a launch video.', 'Eight more videos your team never has time to make.', co(4))}<p class="sec-sub">Each one starts from something you already have.</p></section>
<div class="grid-wrap" style="margin-top:48px"><div class="grid3"><div style="grid-column:span 2;grid-row:span 2">${tile({ ...USE.launch, a: USE.launch.big, sound: false }).replace('class="pd-card"', 'class="pd-card" style="height:100%;aspect-ratio:auto"')}</div>${order.map(k => useTile(USE[k])).join('')}</div></div>
<section class="sec">${title2('Indistinguishable from human-made.', 'Judge for yourself: videos made for startups like yours.', co(5))}</section>
<div class="grid-wrap" style="margin-top:48px"><div class="row5">${proof.map(t => tile(t)).join('')}</div></div>
<section class="sec">${title2('White-glove onboarding.', 'Then it runs on its own.')}<div class="stats"${co(6)}><div class="stat"><div class="num">1-1</div><p><b>Onboarding.</b> Your agent configured on your brand, then 1-business-day support.</p></div><div class="stat"><div class="num">95%</div><p><b>autonomy after 2 weeks.</b></p></div><div class="stat"><div class="num">$600</div><p><b>Your first month.</b> Month-to-month, no lock-in.</p></div></div></section>
<section class="closing"><canvas class="pd-halftone" data-cy="0.55"></canvas><div class="inner">${title2('See Poolday in action, live on a call.')}<div><p class="sub" style="display:inline-block"${co(7)}>Bring your website. Watch Poolday make your video, live.${V}</p></div><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><div class="facts"><span>~$5–$25 per finished video</span><i>·</i><span>Month-to-month, no lock-in</span><i>·</i><span>First month $600</span></div></div></section>` + foot();
}

// ===================== PRICING =====================
const li = (t) => `<li>${icon('check', 16)}<span>${t}</span></li>`;
function pricingBefore() {
  return head('Poolday pricing, before', 'Reconstruction of /pricing from the reported copy and page text, not a capture · card styling and button label assumed', 'Before') + nav() +
    `<section class="pd-hero d7-hero" style="padding-bottom:64px"><canvas class="pd-halftone" data-cx="0.5" data-cy="0.3" data-rx="520"></canvas><div class="pd-hero-inner"><h1 class="pd-display">Simple pricing</h1></div></section>
<div class="plans">
<div class="plan"><h3>Business</h3><div class="price">$1,250<small>/mo</small></div><ul>${li('$1,250 of credits')}${li('1-1 onboarding')}${li('1-business-day support')}${li('Extra credits at 2× the included rate')}</ul><p class="first">Your first month at $600</p><p class="cfg">Book a call to get your agent configured</p><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div>
<div class="plan"><h3>Enterprise</h3><div class="price"><span class="from">from</span>$2,500<small>/mo</small></div><ul><li class="li-head">Everything in Business, plus</li>${li('SSO')}${li('MSA')}${li('A private Slack')}${li('API access')}${li('Unlimited users')}</ul><p class="first">Your first month at $600</p><p class="cfg">Book a call to get your agent configured</p><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div>
</div><div style="height:140px"></div>` + foot();
}
function pricingAfter() {
  const C = (cells, cls = '') => cells.map((c, i) => `<div class="${i === 0 ? 'rh' : ''}${i === 1 ? ' pd' : ''} ${cls}">${c}</div>`).join('');
  return head('Poolday pricing, after', 'Proposed redesign · same structure, prices and plan contents · [verify] = not confirmed from the live site', 'After') + nav() +
    `<section class="pd-hero d7-hero" style="padding-top:56px;padding-bottom:44px"><canvas class="pd-halftone" data-cx="0.5" data-cy="0.3" data-rx="520"></canvas><div class="pd-hero-inner"><h1 class="pd-display">Simple pricing.</h1>
<p class="pricing-lede" style="margin-top:22px"${co(1)}>Pay for finished videos, not seats. <span>~$5–$25 per finished video.</span>${V}</p></div></section>
<div class="plans tight">
<div class="plan"><h3>Business</h3><p class="persona-s"${co(3, 'right')}>For a startup team of 1–3 that ships every week.</p><div class="price">$1,250<small>/mo</small></div><p class="yield-s"${co(2, 'right')}>≈ 50–250 finished videos a month${V}</p><ul>${li('$1,250 of credits')}${li('1-1 onboarding')}${li('1-business-day support')}${li('Extra credits at 2× the included rate')}</ul><p class="first"${co(4, 'right')}>First month $600 <span class="pilot-s">· a pilot, no lock-in</span></p><p class="cfg">Book a call to get your agent configured</p><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div>
<div class="plan"><h3>Enterprise</h3><p class="persona-s">For teams that need SSO, an MSA and API access.</p><div class="price"><span class="from">from</span>$2,500<small>/mo</small></div><p class="yield-s">≈ 100–500+ finished videos a month${V}</p><ul><li class="li-head">Everything in Business, plus</li>${li('SSO')}${li('MSA')}${li('A private Slack')}${li('API access')}${li('Unlimited users')}</ul><p class="first">First month $600 <span class="pilot-s">· a pilot, no lock-in</span></p><p class="cfg">Book a call to get your agent configured</p><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a></div>
</div>
<section class="sec sec-tight center"><div${co(5)} style="display:inline-block"><p style="font-size:15px;color:var(--ink-muted)">Teams on Poolday</p>${logoRow(CUSTOMERS.slice(0, 8), 'small')}</div></section>
<section class="sec">${title2('Poolday vs the usual options.', 'Priced per finished video.', co(6))}
<div class="cmp">${C(['', 'Poolday', 'Agency', 'Freelancer', 'In-house editor'], 'h')}${C(['How you pay', '~$5–$25 per finished video', 'Per project', 'Per video or per hour', 'Salary plus tools'])}${C(['Commitment', 'Month-to-month', 'Project or retainer', 'Per job', 'A full-time hire'])}${C(['Your brand', 'Learned once, pixel-exact', 'Re-briefed each project', 'Re-briefed each job', 'Learned once'], 'last').replace('rh last', 'rh')}</div></section>
<section class="sec center"><p class="proc-line"${co(7)}><b>Ready for procurement on Enterprise:</b> SSO · MSA · private Slack · API access · unlimited users. Security documentation on request${V}</p></section>
<section class="sec" style="padding-top:96px">${title2('Questions.', 'Before the call.', co(8))}<div class="faq">
<div><h4>What is a credit?</h4><p>What the agent spends to make a video. A finished video typically uses ~$5–$25 of credits, depending on length and how much footage is generated.${V}</p></div>
<div><h4>What is the $600 first month?</h4><p>A pilot: your agent configured on your brand, 1-1 onboarding, first videos made together. Month-to-month after that, no lock-in.</p></div>
<div><h4>What happens if I run out of credits?</h4><p>Top up anytime at 2× the included rate. If that happens every month, the next plan is cheaper.</p></div>
<div><h4>Do we need a designer?</h4><p>No. Teach it your brand once: logo, fonts, colors and Lottie, pixel-exact in every video.</p></div>
</div></section>
<section class="closing"><canvas class="pd-halftone" data-cy="0.55"></canvas><div class="inner">${title2('See Poolday in action, live on a call.')}<div class="cta-row"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a>${watch()}</div></div></section>` + foot();
}

const pages = { 'home-before': homeBefore, 'home-after': homeAfter, 'b2b-before': b2bBefore, 'b2b-after': b2bAfter, 'pricing-before': pricingBefore, 'pricing-after': pricingAfter };
for (const [k, f] of Object.entries(pages)) fs.writeFileSync(path.join(OUT, k + '.html'), f());
console.log('built', Object.keys(pages).join(', '));
