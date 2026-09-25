// D7 round 4: AFTER pages rebuilt on the REAL live structure (screenshots in ../real/).
// BEFOREs are the live screenshots themselves (see render.js). Output: ../pages/*-after.html
// Run from deliverables/D7-pages:  node src/build.js
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '..', 'pages');
fs.mkdirSync(OUT, { recursive: true });

// ---------- Lucide icons ----------
const ICON = {
  'layout-grid': '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
  briefcase: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
  'gamepad-2': '<line x1="6" x2="10" y1="11" y2="11"/><line x1="8" x2="8" y1="9" y2="13"/><line x1="15" x2="15.01" y1="12" y2="12"/><line x1="18" x2="18.01" y1="10" y2="10"/><path d="M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z"/>',
  mic: '<path d="M12 19v3"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><rect x="9" y="2" width="6" height="13" rx="3"/>',
  'chevron-down': '<path d="m6 9 6 6 6-6"/>', 'chevron-left': '<path d="m15 18-6-6 6-6"/>', 'chevron-right': '<path d="m9 18 6-6-6-6"/>',
  play: '<polygon points="6 3 20 12 6 21 6 3"/>', check: '<path d="M20 6 9 17l-5-5"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
  'arrow-right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', 'arrow-up': '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
  sparkles: '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
  info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
  film: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/>',
  'mouse-pointer': '<path d="M4.037 4.688a.495.495 0 0 1 .651-.651l16 6.5a.5.5 0 0 1-.063.947l-6.124 1.58a2 2 0 0 0-1.438 1.435l-1.579 6.126a.5.5 0 0 1-.947.063z"/>',
  'git-merge': '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>',
};
const icon = (n, s = 16, fill = false) => `<svg class="pd-icon" width="${s}" height="${s}" viewBox="0 0 24 24" fill="${fill ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[n]}</svg>`;
const V = '<span class="verify">[verify]</span>';
const co = (n, side) => ` data-callout="${n}"${side ? ' data-side="right"' : ''}`;
const esc = (t) => t.replace(/&/g, '&amp;');

// ---------- Real logos (see CREDITS.md) ----------
function svgLogo(file, h) {
  let t = fs.readFileSync(path.join(__dirname, 'logos', file), 'utf8');
  t = t.replace(/<\?xml[^>]*>/g, '').replace(/<!DOCTYPE[^>]*>/g, '').replace(/<title>[^<]*<\/title>/g, '');
  t = t.replace(/fill="(?!none)[^"]*"/g, 'fill="currentColor"').replace(/stroke="(?!none)[^"]*"/g, 'stroke="currentColor"');
  t = t.replace(/<svg([^>]*?)\s(width|height)="[^"]*"/g, '<svg$1').replace(/<svg([^>]*?)\s(width|height)="[^"]*"/g, '<svg$1').replace(/style="[^"]*"/, '');
  t = t.replace('<svg', `<svg aria-hidden="true" style="height:${h}px;width:auto;display:block"`);
  if (!/fill="currentColor"/.test(t)) t = t.replace('<svg', '<svg fill="currentColor"');
  return t.trim();
}
const LOGOS = {
  PostHog: () => `<span class="rl">${svgLogo('posthog.svg', 22)}<b style="font-weight:700;letter-spacing:-0.035em">PostHog</b></span>`,
  Lovable: () => `<span class="rl" style="gap:7px">${svgLogo('lovable-mark.svg', 22)}${svgLogo('lovable-wordmark.svg', 21)}</span>`,
  ClickUp: () => `<span class="rl">${svgLogo('clickup.svg', 22)}<b style="font-weight:700;letter-spacing:-0.04em">ClickUp</b></span>`,
  Dust: () => `<span class="rl">${svgLogo('dust.svg', 20)}</span>`,
  Marblism: () => `<span class="rl"><b style="font-weight:600;letter-spacing:-0.03em">Marblism</b></span>`,
  FullEnrich: () => `<span class="rl">${svgLogo('fullenrich.svg', 24)}<b style="font-weight:600;letter-spacing:-0.03em">FullEnrich</b></span>`,
};
const realLogoRow = (names) => `<div class="rlogos">${names.map(n => LOGOS[n]()).join('')}</div>`;

// ---------- Placeholder video art (the videos are the colour; never stock) ----------
function art(a) {
  const bg = a.bg || '#1a1a1a';
  switch (a.k) {
    case 'img': return `<div class="art"><img src="../tiles/${a.src}.png" alt="" style="width:100%;height:100%;object-fit:cover;object-position:${a.pos || 'center'};${a.filter ? 'filter:' + a.filter : ''}"></div>`;
    case 'type': return `<div class="art" style="background:${bg}"><div class="big${a.dots ? ' dots' : ''}" style="color:${a.fg};font-size:${a.size || 120}px;left:${a.x ?? 10}px;bottom:${a.y ?? -10}px">${a.w}</div></div>`;
    case 'head': return `<div class="art" style="background:${bg}"><div class="hd" style="color:${a.fg || '#fff'};font-size:${a.size || 34}px;${a.center ? 'left:0;right:0;text-align:center;top:40%' : 'left:22px;top:22px;right:22px'}">${a.w}</div></div>`;
    case 'arrow': return `<div class="art" style="background:${bg}"><div class="ring" style="border-color:#111"><span style="color:#111">${icon('arrow-up', 42)}</span></div></div>`;
    case 'braces': return `<div class="art" style="background:#f7f7f5"><div class="hd" style="left:0;right:0;top:26%;text-align:center;font-size:84px;font-weight:300"><span style="color:#2563eb">{</span><span style="font-size:14px;color:#111;vertical-align:28px;margin:0 16px">are guesses</span><span style="color:#ea580c">}</span></div></div>`;
    case 'paper': return `<div class="art" style="background:#dcd6cc"><div style="position:absolute;left:30%;top:28%;width:32%;height:40%;background:#efebe4;transform:rotate(-8deg);border-radius:3px"></div><div style="position:absolute;left:44%;top:40%;width:26%;height:34%;background:#e6e1d8;transform:rotate(6deg);border-radius:3px"></div></div>`;
    case 'wood': return `<div class="art" style="background:linear-gradient(#e9e3da 0 45%,#8a5a3b 45% 100%)"><div style="position:absolute;left:18%;right:18%;top:36%;height:20%;border-radius:50%;background:#5b3a26"></div></div>`;
    case 'scene': return `<div class="art" style="background:${bg}">${(a.dots || [[35, 45], [62, 42]]).map(([x, y]) => `<div style="position:absolute;left:${x}%;top:${y}%;width:17%;aspect-ratio:1;border-radius:50%;background:${a.fg || '#3a3a3a'}"></div><div style="position:absolute;left:${x - 5}%;top:${y + 22}%;width:27%;height:40%;border-radius:40% 40% 0 0;background:${a.fg || '#3a3a3a'}"></div>`).join('')}</div>`;
    case 'founder': return `<div class="art" style="background:#0b0b0b"><div style="position:absolute;right:-10%;top:-20%;width:60%;height:60%;border-radius:50%;background:#f59e0b;opacity:.85"></div><div style="position:absolute;left:14%;right:10%;top:52%;height:16%;background:#1e1e1e;transform:rotate(-8deg);border-radius:4px"></div><div class="hd" style="left:40%;top:52%;font-size:12px;letter-spacing:.2em;color:#ddd;transform:rotate(-8deg)">FOUNDER STORY</div></div>`;
    case 'phone': return `<div class="art" style="background:${bg}"><div style="position:absolute;left:34%;top:12%;width:32%;height:80%;border-radius:18px;background:${a.scr}"><div class="hd" style="left:0;right:0;top:30%;text-align:center;font-size:20px;color:#dfffe9">09:41</div></div></div>`;
    case 'face': return `<div class="art" style="background:${bg}"><div style="position:absolute;left:50%;top:${a.top || 26}%;width:${a.w || 30}%;aspect-ratio:.82;margin-left:-${(a.w || 30) / 2}%;border-radius:48%;background:${a.fg}"></div><div style="position:absolute;left:50%;bottom:-10%;width:${(a.w || 30) * 2.1}%;height:36%;margin-left:-${(a.w || 30) * 1.05}%;border-radius:50% 50% 0 0;background:${a.body || a.fg}"></div>${a.txt ? `<div class="hd" style="left:0;right:0;top:8%;text-align:center;font-size:${a.ts || 22}px;font-weight:800;color:#fff">${a.txt}</div>` : ''}</div>`;
    case 'ui': return `<div class="art" style="background:${bg}"><div class="win" style="left:9%;top:14%;width:82%;height:72%;background:${a.win || '#fff'}">${[0, 1, 2, 3].map(i => `<div class="bar" style="left:16px;top:${22 + i * 22}px;width:${[46, 70, 58, 36][i]}%;background:${a.line || 'rgba(0,0,0,.12)'}"></div>`).join('')}${a.chart ? `<svg viewBox="0 0 100 30" preserveAspectRatio="none" style="position:absolute;left:8%;right:8%;bottom:10%;width:84%;height:40%"><polyline points="0,24 12,20 24,22 36,12 48,16 60,8 72,11 84,5 100,9" fill="none" stroke="${a.chart}" stroke-width="1.6"/></svg>` : ''}</div></div>`;
    case 'stats': return `<div class="art" style="background:#15151a"><div class="hd" style="left:6%;top:9%;font-size:18px;color:#fff">45,000+</div><div class="hd" style="left:40%;top:9%;font-size:18px;color:#fff">10x</div><div class="hd" style="left:68%;top:9%;font-size:18px;color:#fff">&lt; 1%</div>${[0, 1, 2, 3].map(i => `<div style="position:absolute;left:${6 + (i % 2) * 46}%;top:${34 + Math.floor(i / 2) * 30}%;width:42%;height:24%;border-radius:6px;background:#23232b"></div>`).join('')}</div>`;
    case 'logo': return `<div class="art" style="background:${bg}"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff">${a.html}</div></div>`;
    case 'wash': return `<div class="art" style="background:linear-gradient(135deg,${a.bg},${a.bg2})"><div class="hd" style="left:22px;top:22px;right:22px;font-size:${a.size || 30}px;color:${a.fg || '#fff'}">${a.w}</div></div>`;
  }
  return `<div class="art" style="background:${bg}"></div>`;
}
// Caption bar, like the live tiles: icon, "Brand – Title", recipe, tag or "See the prompt"
function capBar(t) {
  const right = t.prompt ? `<span class="cb-prompt">${icon('layout-grid', 11)}See the prompt</span>` : `<span class="cb-tag">${icon(t.tagIcon || 'briefcase', 11)}${t.tag || 'Tech'}</span>`;
  return `<div class="cb"><span class="cb-ic">${icon('film', 12)}</span><span class="cb-tx"><b>${esc(t.title)}</b><i>${esc(t.recipe)}</i></span>${right}</div>`;
}
const vtile = (t, h) => `<figure class="vt"${h ? ` style="--h:${h}px"` : ''}><div class="vm">${art(t.a)}</div>${capBar(t)}</figure>`;

// ---------- Shared chrome ----------
const head = (title, label) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title>
<link rel="stylesheet" href="../../design/poolday-brand-kit/tokens.css"><link rel="stylesheet" href="../../design/poolday-brand-kit/components/bundle.css"><link rel="stylesheet" href="../src/d7.css"><link rel="stylesheet" href="../src/d7-v4.css"></head><body>
<div class="d7-label"><b>After</b>${label}</div>`;
const nav = () => `<header class="pd-nav"><a class="pd-wordmark" href="#">Poolday.ai</a><nav class="pd-nav-links" aria-label="Main"><a class="pd-nav-link" href="#">Home</a><button class="pd-nav-link">Solutions${icon('chevron-down', 14)}</button><a class="pd-nav-link" href="#">Integrations</a><a class="pd-nav-link" href="#">Pricing</a><button class="pd-nav-link">Resources${icon('chevron-down', 14)}</button></nav><a class="pd-btn pd-btn-md" href="#">Book a 15 min demo</a></header>`;
const foot = () => `<footer class="foot wrapc"><span>© 2023 – 2026 Poolday AI.</span><span><span>Privacy Policy</span><span>Terms of Service</span></span></footer><script src="../src/page.js"></script></body></html>`;
const tabs = () => `<div class="pd-tabs" role="tablist"><button class="pd-tab" aria-selected="true">${icon('layout-grid')}All</button><button class="pd-tab">${icon('briefcase')}Tech Industry</button><button class="pd-tab">${icon('gamepad-2')}Apps &amp; Games</button><button class="pd-tab">${icon('mic')}Podcasts</button></div>`;
const title2 = (lead, tail, attrs = '') => `<h2 class="pd-section-title"${attrs}>${lead}${tail ? ` <span class="pd-quiet">${tail}</span>` : ''}</h2>`;
const watch = (dark) => `<a class="link-2${dark ? ' on-light' : ''}" href="#"><span class="ring">${icon('play', 12, true)}</span>Watch a 2-min build</a>`;
const rule = () => `<hr class="rule">`;
const ctaCard = (inner) => `<section class="wrapc" style="padding:88px 0 40px"><div class="cta-card">${inner}</div></section>`;
const CTA_SUB = 'Book a 15-minute call to get a walkthrough of the platform, discuss your specific needs and map out your first month.';

// ===================== HOME =====================
const GROUPS = [
  ['Launch films', [
    { title: 'Marblism – Product Launch Video', recipe: 'Made with brand kit + single prompt', a: { k: 'arrow', bg: '#ffd21f' } },
    { title: 'PostHog – AI Feature Launch', recipe: 'Imported Lottie files for motion graphics', a: { k: 'ui', bg: '#ece6da', win: '#fbfaf7', chart: '#f54e00' } },
    { title: 'ClickUp – Product Feature Video', recipe: 'Automated video update from roadmap', a: { k: 'wash', bg: '#ff4fa8', bg2: '#7b5cff', w: 'BRAIN<br><span style="opacity:.8;font-size:.62em">CONNECTED APPS</span>', size: 38 } },
    { title: 'Poolday – Founder Launch Video', recipe: 'Founder photos + voice', a: { k: 'scene', bg: '#20242a', fg: '#3b4047' } },
  ]],
  ['Product demos & explainers', [
    { title: 'Dust – Agent demo video', recipe: 'Screen recording to pixel-perfect video', a: { k: 'face', bg: '#d9f99d', fg: '#8b6f5a', body: '#374151', w: 22, top: 22 } },
    { title: 'PostHog – Product Video', recipe: 'Two prompts and one brand kit', a: { k: 'braces' } },
    { title: 'FullEnrich – Explainer Video', recipe: 'Knowledge base to paper-craft explainer', a: { k: 'paper' } },
    { title: 'Oreo – Every Motion Controllable', recipe: 'Every motion controllable', a: { k: 'wood' } },
  ]],
  ['Ads & testimonials', [
    { title: 'Lovable – Instagram Ad', recipe: 'Made with founder photo + voice', a: { k: 'face', bg: '#2f3b4a', fg: '#9a7b67', body: '#1f2937', txt: 'ONE PAGER', ts: 20 } },
    { title: 'Verde – Product Ad', recipe: 'Made with app UI + YouTube footage', a: { k: 'phone', bg: '#0e1f17', scr: '#12372a' } },
    { title: 'Vybe – Cinematic Brand Ad', recipe: 'AI-generated footage for a cinematic spot', a: { k: 'face', bg: '#7d8ea3', fg: '#6b5446', body: '#2b3440', w: 26 } },
    { title: 'Braavo – Customer Testimonial', recipe: 'Interview recording to founder story', a: { k: 'founder' } },
  ]],
  ['Podcasts', [
    { title: 'Smart Reframe Highlights', recipe: 'Auto-reframed highlights', tag: 'Podcasts', tagIcon: 'mic', a: { k: 'face', bg: '#f1eee8', fg: '#7a5a48', body: '#e5e7eb', txt: 'Answer the Internet', ts: 18, w: 24 } },
    { title: 'Full Podcast Editing', recipe: 'Raw multi-cam recording to fully edited episode', tag: 'Podcasts', tagIcon: 'mic', a: { k: 'scene', bg: '#2a2622', fg: '#4a423b', dots: [[22, 40], [60, 40]] } },
    { title: 'Key Moments Extraction', recipe: 'Full episode to key moments', tag: 'Podcasts', tagIcon: 'mic', a: { k: 'head', bg: '#0b0b0b', fg: '#fbbf24', w: 'COMMUNICATION IS<br><span style="color:#fff">EVERYTHING</span>', size: 20, center: true } },
    { title: 'Podcast to Social Clips', recipe: 'Full episode to snackable content for social', tag: 'Podcasts', tagIcon: 'mic', a: { k: 'face', bg: '#b45347', fg: '#6b3f35', body: '#3f2a26', w: 26 } },
  ]],
];
// Real frames cut from the live home screenshot (src/tiles.js)
const HOME_IMG = [['h-marblism'], ['h-posthog-ai'], ['h-clickup'], ['h-poolday-founder'], ['h-dust', 'center 40%'], ['h-posthog-pv'], ['h-fullenrich'], ['h-oreo'],
  ['h-lovable', 'center 6%'], ['h-verde'], ['h-vybe', 'center 30%'], ['h-braavo'], ['h-smart', 'center 64%'], ['h-podcast-man', 'center 40%', 'brightness(1.8) contrast(1.05)'], ['h-comm', 'center 22%'], ['h-woman', 'center 28%']];
GROUPS.flatMap(g => g[1]).forEach((t, i) => { const [src, pos, filter] = HOME_IMG[i]; t.a = { k: 'img', src, pos, filter }; });
const groupedGrid = () => `<div class="ggrid">${GROUPS.map(([label, items]) => `<div><h3 class="glabel">${label}</h3><div class="gtiles">${items.map(t => vtile(t)).join('')}</div></div>`).join('')}</div>`;

// Meet Poolday: four animated features in device frames, live copy and line breaks
const MEET = [
  ['Teach it your brand once:<br>logo, fonts, colors and Lottie,<br>pixel-exact in every video.',
    `<div class="scr light"><div class="bk-logo an" style="--d:.2s"><span class="oa">◎</span>OpenAI</div><span class="chip an" style="left:39%;top:10%;--d:.9s">${icon('check', 10)}On brand</span>
     <div class="bk-h an" style="--d:.4s">Introducing our latest<br>models</div><span class="chip an" style="left:67%;top:38%;--d:1.3s">${icon('check', 10)}On brand</span>
     <div class="bk-btn an" style="--d:.6s">Try ChatGPT</div><span class="chip an" style="left:33%;top:77%;--d:1.7s">${icon('check', 10)}On brand</span>
     <div class="bk-fig an" style="--d:1.1s"><i style="background:#f24e1e"></i><i style="background:#ff7262"></i><i style="background:#a259ff"></i><i style="background:#1abcfe"></i><i style="background:#0acf83"></i><small>Figma · Design system</small></div></div>`],
  ['Prompt it with a storyboard,<br>a URL, clips or an idea.<br>It asks what it needs,<br>then finishes the job.',
    `<div class="scr"><div class="cmp-box"><div class="type" style="--w:100%">Here are videos from our event. Give me five short clips for social media</div><div class="clips">${['#3b3f8f', '#5b4636', '#7a5a2b', '#394b5a'].map((c, i) => `<i style="background:${c}"><b>${['12:48', '4:18', '8:42', '1:15'][i]}</b></i>`).join('')}</div></div>
     <div class="q an" style="--d:2.2s"><b>Add a call to action at the end?</b>${['Yes, include our standard end card', 'Yes, a custom CTA', 'No CTA'].map((o, i) => `<span${i === 0 ? ' class="on"' : ''}><em></em>${o}</span>`).join('')}<div class="q-f"><small>Question 2 of 2</small><u>Confirm</u></div></div></div>`],
  ['Click the exact element<br>you want changed. Only<br>that changes, nothing else.',
    `<div class="scr black"><div class="pe"><div class="an" style="--d:.2s">Don’t re-generate the entire video.</div><div class="an" style="--d:.6s"><b>Only update what you <span class="sel">select<i class="selbox"></i></span>.</b></div></div><span class="cursor">${icon('mouse-pointer', 18, true)}</span></div>`],
  ['One prompt, infinite outputs:<br>hooks, actors, styles, key<br>moments, languages and sizes.',
    `<div class="scr"><div class="vars">${Array.from({ length: 12 }, (_, i) => `<i class="an" style="--d:${(0.15 * i).toFixed(2)}s;background:${['#e8553f', '#f06b52', '#d9483a', '#f28a6b'][i % 4]}"><b></b><small>${['Stay cold. Stay you.', 'Cold in 3 seconds.', 'Still drinking tap?', 'Meet the red one.'][i % 4]}</small></i>`).join('')}</div><div class="count an" style="--d:1.9s"><b>12</b><small>variants</small></div></div>`],
];
const meet = () => `<div class="meet">${MEET.map(([copy, media]) => `<div class="mf"><p>${copy}</p><div class="device">${media}</div></div>`).join('')}</div>`;

const QUOTES = [
  ['AI video was never good enough for us to use in production. Until Poolday’s agent. Phenomenal quality and support.', 'Emilien E.', 'CRO', 'adikteev'],
  ['After extensive evaluation, Poolday.ai stands out as the most intelligent and flexible video editing agent we’ve seen. Hands down the best in the market.', 'Vladimir Karyshev', 'Head of Partnerships', 'Higgsfield'],
  ['Poolday’s been a revelation. We asked for one looping event video and what came back was miles better than what we put in. Our whole design system lives in there, so everything’s on-brand without us thinking about it. Now we use it for everything. Honestly brilliant.', 'Flavie D.', 'Senior Product Designer', ''],
];
const quotes = () => `<div class="qwrap"><span class="qarrow">${icon('chevron-left', 16)}</span><div class="qrow">${QUOTES.map(([q, n, r, c]) => `<div class="qc"><p>“${q}”</p><div class="qwho"><span class="qav"></span><span><b>${n}</b><i>${r}</i></span><em>${c}</em></div></div>`).join('')}</div><span class="qarrow">${icon('chevron-right', 16)}</span></div>`;

function homeAfter() {
  return head('Poolday home, after', 'Proposed redesign on the live page structure · tile groupings illustrative, titles from the live grid') + nav() +
    `<section class="pd-hero d7-hero"><canvas class="pd-halftone" data-cx="0.47" data-cy="0.5"></canvas><div class="pd-hero-inner">
<h1 class="pd-display">The Media Superintelligence.</h1>
<p class="pd-lede">An AI agent that edits, generates and assembles on-brand videos.</p>
<div class="cta-row"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><span${co(1, 'right')}>${watch()}</span></div>
${title2('100M+ video edits made by Poolday.', 'Some examples here.')}${tabs()}</div></section>
<div class="wrapc"${co(2)}>${groupedGrid()}</div>
<section class="sec" style="padding-top:140px">${title2('Meet Poolday.', 'An agent that plans, makes and fixes the whole video.', co(3))}${meet()}
<div class="center" style="margin-top:72px"><a class="pd-btn pd-btn-lg" href="#"${co(4, 'right')}>Book a 15 min demo</a></div></section>
<div class="wrapc" style="margin-top:110px">${rule()}</div>
<section class="wrapc center" style="padding-top:64px"><p class="caps">Trusted by leaders worldwide in every category</p>
<div${co(5)} style="display:inline-block;margin-top:26px;padding:0 12px"><div class="mq">
<span class="mql">${svgLogo('unity.svg', 22)}<b>Unity</b></span><span class="mql" style="font-weight:900;font-style:italic;letter-spacing:-.02em">WILDLIFE</span><span class="mql" style="font-weight:800;letter-spacing:-.03em">⫽ Stillfront</span><span class="mql" style="font-weight:500">⁝⁝ adikteev</span><span class="mql" style="font-weight:700">♥ WeWard</span><span class="mql" style="font-weight:600;letter-spacing:.06em">VERAXEN</span></div>
<p class="backed">Backed by <b>LocalGlobe</b><b>daphni</b></p></div></section>
<section class="wrapc center" style="padding-top:64px"><p class="caps">From the teams running it</p>${quotes()}</section>
<div class="wrapc" style="margin-top:72px">${rule()}</div>
${ctaCard(`<h2>See Poolday in action, live on a call.</h2><p class="cc-sub">${CTA_SUB}</p>
<div class="cc-steps"${co(6)}><div><span>Minute 1</span>You share your website.</div><div><span>Minutes 2–10</span>It builds your brand kit live and drafts a first video.${V}</div><div><span>Minutes 10–15</span>You leave with a plan for your first month.</div></div>
<div class="cta-row"><a class="pd-btn pd-btn-lg dark" href="#">Book a 15 min demo</a>${watch(true)}</div><div class="cc-checks"><span>${icon('check', 13)}~$5–$25 per finished video</span><span>${icon('check', 13)}Month-to-month, no lock-in</span><span>${icon('check', 13)}First month $600</span></div>`)}` + foot();
}

// ===================== B2B STARTUPS =====================
const B2B_TOP = [
  [{ title: 'Cal.com – Loom-style video without recording', recipe: '1 screenshot + 1 presenter photo to full animated Loom-style walkthrough', prompt: true, a: { k: 'img', src: 'b-cal' } }, 274],
  [{ title: 'PostHog – Product marketing video', recipe: 'Product UI screenshots + brand kit to typographic marketing video', prompt: true, a: { k: 'img', src: 'b-posthog' } }, 274],
  [{ title: 'AI creator UGC for SaaS', recipe: 'Talking-head prompt + product images to UGC ad', prompt: true, a: { k: 'img', src: 'b-aicreator' } }, 598],
  [{ title: 'Plausible – Localizations in one workflow', recipe: 'One workflow for localized video versions', prompt: true, a: { k: 'img', src: 'b-plausible' } }, 160],
  [{ title: 'Feature launch, resized for every channel', recipe: 'One prompt to 4 sizes (landscape, square, vertical)', prompt: true, a: { k: 'img', src: 'b-feature' } }, 160],
  [{ title: 'Customer testimonial, from a photo', recipe: '1 photo to lipsynced testimonial', prompt: true, a: { k: 'img', src: 'b-testimonial' } }, 158],
];
const topMasonry = () => { const t = B2B_TOP.map(([x, h]) => vtile(x, h)); return `<div class="mas"><div>${t[0]}${t[1]}</div><div>${t[2]}</div><div>${t[3]}${t[4]}${t[5]}</div></div>`; };

// Use cases: live titles + body copy, each with a small animated preview (input -> output)
const USE = [
  ['Post-call recap', 'AEs paste the call recording and get a 30-second video answering the prospect’s questions.',
    `<div class="uin wave an">${[10, 22, 14, 30, 18, 26, 12, 20, 8, 24, 16, 28].map(h => `<i style="height:${h}px"></i>`).join('')}</div>`, { bg: '#1d4ed8', w: 'Your next steps, Maya.' }],
  ['Launch video on merge', 'Product marketers connect GitHub and every shipped feature becomes a launch video for LinkedIn.',
    `<div class="uin pr an"><span class="merged">${icon('git-merge', 11)}Merged</span><b>#482 feat: session replay</b><i class="add"></i><i class="add" style="width:60%"></i><i class="del"></i></div>`, { bg: '#e0533d', w: 'v2.4 is live.' }],
  ['The demo records itself', 'Founders point the agent at the live product and it records the demo itself.',
    `<div class="uin app an"><i></i><i style="width:55%"></i><i style="width:70%"></i><span class="cursor2">${icon('mouse-pointer', 14, true)}</span></div>`, { bg: '#efe6d8', fg: '#1c1917', w: 'Product tour, 45s.' }],
  ['Webinar to eight clips', 'Demand gen teams upload the webinar and get 8 captioned clips for LinkedIn.',
    `<div class="uin tl an"><div class="tlbar">${Array.from({ length: 8 }, () => '<i></i>').join('')}</div><small>webinar.mp4 · 58:12</small></div>`, { eight: true }],
  ['What shipped this month', 'Product marketers set a monthly schedule and release notes become a 60-second LinkedIn video.',
    `<div class="uin list an">${['Sep 3 · SSO for teams', 'Sep 11 · Faster search', 'Sep 19 · New API', 'Sep 26 · Dark mode'].map((t, i) => `<span class="an" style="--d:${0.2 + i * 0.25}s">${t}</span>`).join('')}</div>`, { bg: 'linear-gradient(135deg,#7b5cff,#ff5fa2)', w: 'September, shipped.' }],
  ['One demo, every prospect', 'Sales engineers record one demo and get a version in each prospect’s own brand.',
    `<div class="uin list an">${['Acme', 'Globex', 'Initech', 'Umbrella'].map((t, i) => `<span class="an" style="--d:${0.2 + i * 0.25}s"><em style="background:${['#f59e0b', '#10b981', '#6366f1', '#ef4444'][i]}"></em>${t}</span>`).join('')}</div>`, { bg: '#dbeafe', fg: '#1e3a8a', w: 'Hi Acme, here’s your demo.' }],
  ['Call to case study', 'Customer marketers paste a call recording and get a case-study video for the website.',
    `<div class="uin chat an"><span class="an" style="--d:.2s">We cut onboarding from weeks to days.</span><span class="an r" style="--d:.6s">What changed?</span><span class="an" style="--d:1s">The agent did the first draft.</span></div>`, { bg: '#14532d', fg: '#dcfce7', w: 'How Acme ships weekly.' }],
  ['Help center how-tos', 'Customer success turns each help article into a how-to clip for the help center.',
    `<div class="uin doc an"><b>How to connect Slack</b><i></i><i style="width:80%"></i><i style="width:65%"></i><i style="width:75%"></i></div>`, { bg: '#fde68a', fg: '#1c1917', w: 'Step 1 · Connect Slack' }],
  ['JD to recruiting video', 'Recruiters paste the job description and get a recruiting video for the careers page.',
    `<div class="uin doc an"><b>Founding engineer</b><i></i><i style="width:85%"></i><i style="width:60%"></i><i style="width:70%"></i></div>`, { bg: '#111', fg: '#fbbf24', w: 'We’re hiring.' }],
];
function useCard([t, body, input, out]) {
  const output = out.eight
    ? `<div class="uout an eight" style="--d:1.6s">${Array.from({ length: 8 }, (_, i) => `<i style="background:${['#0ea5e9', '#6366f1', '#f59e0b', '#ef4444', '#10b981', '#ec4899', '#8b5cf6', '#14b8a6'][i]}"></i>`).join('')}</div>`
    : `<div class="uout an" style="--d:1.6s;background:${out.bg}"><b style="color:${out.fg || '#fff'}">${out.w}</b><span class="prog"><i></i></span></div>`;
  return `<div class="uc"><div class="device small"><div class="scr uscr">${input}<span class="uarrow an" style="--d:1.2s">${icon('arrow-right', 14)}</span>${output}</div></div><h4>${t}</h4><p>${body}</p></div>`;
}
const WHY = [
  ['100% on-brand', 'Upload your logo, guidelines, fonts, colors, assets and animations once. Every output stays on-brand. Guaranteed.'],
  ['Indistinguishable from human-made', 'Ranked #1 worldwide in agentic video editing. You won’t tell the difference between a video the agent made and one you made.'],
  ['Built for teams', 'Teach the agent your process once. Everyone on your team inherits it.'],
  ['Connects to your stack', '150+ connectors plus any custom MCP. Poolday pulls the assets and context it needs from the tools you already use.'],
  ['White-glove onboarding', 'Great outputs come from good structure. We set it up with you, so your first videos are already your best.'],
  ['95% autonomy after 2 weeks', 'The agent learns from every review. Two weeks in, 95% of your videos need zero edits from your team.'],
];
const MADE = [
  ['PostHog – Product Video', 'Two prompts and one brand kit to create a product film', { k: 'braces' }],
  ['FullEnrich – Explainer Video', 'Knowledge base to paper-craft explainer', { k: 'paper' }],
  ['Poolday – Stars', 'One prompt to a finished launch film', { k: 'ui', bg: '#1f2937', win: '#111827', line: 'rgba(255,255,255,.15)' }],
  ['Dust – Agent demo video', 'Screen recording to pixel-perfect video', { k: 'face', bg: '#d9f99d', fg: '#8b6f5a', body: '#374151', w: 22, top: 22 }],
  ['Braavo – Customer Testimonial from a photo', 'Interview recording to founder story', { k: 'founder' }],
  ['Vybe – Cinematic Brand Ad', 'AI-generated footage for cinematic brand spot', { k: 'face', bg: '#94a3b8', fg: '#6b5446', body: '#334155', w: 26 }],
  ['Adikteev – Retain to reign', 'Product ad, kinetic type', { k: 'head', bg: '#fff', fg: '#111', w: '<span style="color:#7c3aed">WAITING 7 DAYS</span><br>TO RETARGET IS LATE.', size: 22 }],
  ['Adjust – Trust the growth', 'Customer ad, built on a stat', { k: 'head', bg: '#0b1a3a', fg: '#fff', w: '2×', size: 60, center: true }],
  ['Jev – Intelligence beyond chat', 'Launch film', { k: 'wash', bg: '#fbcfe8', bg2: '#a78bfa', fg: '#111', w: 'Superhuman At Chat For Years.', size: 24 }],
  ['Upflow – Faster payments', 'Typographic ad', { k: 'head', bg: '#fafafa', fg: '#444', w: 'Did Acme pay invoice #204?', size: 13, center: true }],
  ['Poolday – Founder Launch Video', 'Founder photos + voice', { k: 'scene', bg: '#20242a', fg: '#3b4047' }],
  ['ClickUp – Product Feature Video', 'Automated video update from roadmap', { k: 'logo', bg: 'radial-gradient(circle at 70% 30%,#7c3aed,#1e1b4b 60%,#0f172a)', html: `<span style="background:#fff;color:#111;border-radius:8px;padding:10px 14px;display:flex;gap:6px;align-items:center">${svgLogo('clickup.svg', 16)}<b style="font:700 14px Inter">ClickUp</b></span>` }],
  ['PostHog – AI Feature Launch', 'Imported Lottie files for motion graphics + brand kit', { k: 'ui', bg: '#ece6da', win: '#fbfaf7', chart: '#f54e00' }],
  ['Verde – Product Ad', 'Made with app UI + YouTube-trained motion graphics', { k: 'phone', bg: '#0e1f17', scr: '#12372a' }],
  ['Marblism – Product Launch Video', 'Made with brand kit + single prompt', { k: 'head', bg: '#ffd21f', fg: '#111', w: 'MEET YOUR<br>EMPLOYEES', size: 30, center: true }],
  ['Oreo – Every Motion Controllable', 'Every motion controllable', { k: 'wood' }],
];
const MADE_IMG = ['posthog-pv', 'fullenrich', 'stars', 'dust', 'braavo', 'vybe', 'adikteev', 'adjust', 'jev', 'upflow', 'poolday-founder', 'clickup', 'posthog-ai', 'verde', 'marblism', 'oreo'];
function b2bAfter() {
  return head('Poolday for B2B startups, after', 'Proposed redesign on the live page structure · everything unmarked is the live page, kept') + nav() +
    `<section class="pd-hero d7-hero b2b-hero"><canvas class="pd-halftone" data-cx="0.5" data-cy="0.45"></canvas><div class="pd-hero-inner">
<p class="crumb">← All solutions</p>
<h1 class="b2b-h1"${co(1)}>Every feature you ship, on video.</h1>
<p class="b2b-sub">Delegate your next video to the agent, while keeping full control.<br>Your colors, your logo, your Figma, your animations.</p>
<div class="cta-row" style="margin-top:28px"><a class="pd-btn pd-btn-lg" href="#">Book a 15 min demo</a><span class="url-field"${co(2, 'right')}><span class="sticker">NEW</span>${icon('link')}<span class="ph">Paste your URL</span><span class="go">${icon('arrow-right')}</span></span></div>
<p class="url-note">Not ready for a call? Paste your site and get a free launch video made from it, by email.</p>
<div${co(3)} style="margin-top:44px">${realLogoRow(['PostHog', 'Lovable', 'ClickUp', 'Dust', 'Marblism', 'FullEnrich'])}</div></div></section>
<section class="wrapc"><h2 class="lt">Tech startups use Poolday for</h2>${topMasonry()}</section>
<div class="wrapc" style="margin-top:56px">${rule()}</div>
<section class="wrapc" style="padding-top:48px"><h2 class="lt"${co(4)}>Most common use cases for tech</h2><div class="ucgrid">${USE.map(useCard).join('')}</div></section>
<div class="wrapc" style="margin-top:56px">${rule()}</div>
<section class="wrapc" style="padding-top:48px"><h2 class="lt">Why tech startups love Poolday</h2><div class="why">${WHY.map(([t, b]) => `<div><h4>${t}</h4><p>${b}</p></div>`).join('')}</div></section>
<div class="wrapc" style="margin-top:56px">${rule()}</div>
<section class="wrapc" style="padding-top:48px"><h2 class="lt">Made in Poolday</h2><div class="made">${MADE.map(([t, r], i) => vtile({ title: t, recipe: r, a: { k: 'img', src: 'm-' + MADE_IMG[i] } })).join('')}</div></section>
${ctaCard(`<h2>See Poolday in action, live on a call.</h2><p class="cc-sub">${CTA_SUB}</p><a class="pd-btn pd-btn-lg dark" href="#">Book a 15 min demo</a>`)}` + foot();
}

// ===================== PRICING =====================
const li = (t, head) => `<li${head ? ' class="li-head"' : ''}>${icon('check', 15)}<span>${t}</span></li>`;
const creditsBox = (amount, vids, attrs = '') => `<div class="cbox"${attrs}><span class="cb-spark">${icon('sparkles', 16)}</span><span><b>${amount} in credits</b><i>≈ ${vids} finished videos</i></span><span class="cb-info">${icon('info', 16)}</span></div>`;
function pricingAfter() {
  const C = (cells, cls = '') => cells.map((c, i) => `<div class="${i === 0 ? 'rh' : ''}${i === 1 ? ' pd' : ''} ${cls}">${c}</div>`).join('');
  return head('Poolday pricing, after', 'Proposed redesign on the live pricing page · plan contents and CTAs unchanged') + nav() +
    `<section class="pd-hero d7-hero" style="padding-top:64px;padding-bottom:52px"><canvas class="pd-halftone" data-cx="0.62" data-cy="0.55" data-rx="560"></canvas><div class="pd-hero-inner"><h1 class="pd-display" style="max-width:none">Simple pricing</h1><p class="pr-sub">Month-to-month plans, or yearly plans for discounts.</p></div></section>
<div class="pcards">
<div class="pc light"><h3>Business</h3><div class="pp"><b>$1,250</b><small>/ month</small></div><p class="pfirst"${co(2)}>Your first month at $600 · no lock-in</p>${creditsBox('$1,250', '50–250', co(1, 'right'))}<a class="pbtn dark" href="#">Book a call to get your agent configured</a><ul>${li('1-1 onboarding')}${li('1 business day support time')}${li('Additional credits at 2× your included rate')}</ul></div>
<div class="pc dark"><h3>Enterprise</h3><div class="pp"><small class="from">Starting at</small><b>$2,500</b><small>/ month</small></div><p class="pfirst">Your first month at $600 · no lock-in</p>${creditsBox('$2,500', '100–500')}<a class="pbtn light" href="#">Book a call to get your agent configured</a><ul>${li('Everything in Business, plus:')}${li('3-day on-site or peer-prompting to set up your account')}${li('Unlimited users')}${li('Control which models are available to your org')}${li('SSO, MSA &amp; redlines')}${li('Private slack channel')}${li('Invoicing')}</ul></div>
</div>
<section class="sec sec-tight center"><div${co(3)} style="display:inline-block"><p class="caps">Teams on Poolday</p><div style="margin-top:22px">${realLogoRow(['PostHog', 'Lovable', 'ClickUp', 'Dust', 'Marblism', 'FullEnrich'])}</div></div></section>
<section class="sec">${title2('Poolday vs the usual options.', 'Priced per finished video.', co(4))}
<div class="cmp">${C(['', 'Poolday', 'Agency', 'Freelancer', 'In-house editor'], 'h')}${C(['How you pay', '~$5–$25 per finished video', 'Per project', 'Per video or per hour', 'Salary plus tools'])}${C(['Commitment', 'Month-to-month, no lock-in', 'Project or retainer', 'Per job', 'A full-time hire'])}${C(['Your brand', 'Learned once, pixel-exact', 'Re-briefed each project', 'Re-briefed each job', 'Learned once'], 'last').replace('rh last', 'rh')}</div></section>
<section class="sec" style="padding-top:110px">${title2('Questions.', 'Before the call.', co(5))}<div class="faq">
<div><h4>What is a credit?</h4><p>What the agent spends to make a video. Business includes $1,250/mo in credits, and a finished video typically costs ~$5–$25, so that is roughly 50–250 videos a month.</p></div>
<div><h4>What is the $600 first month?</h4><p>Your first month on either plan costs $600, with your agent configured on a call. Plans are month-to-month, so there is no lock-in.</p></div>
<div><h4>What if I run out of credits?</h4><p>Additional credits cost 2× your included rate. If that happens every month, the next plan is cheaper.</p></div>
<div><h4>Is there a yearly plan?</h4><p>Yes. Month-to-month plans, or yearly plans for discounts.</p></div>
</div></section><div style="height:120px"></div>` + foot();
}

const pages = { 'home-after': homeAfter, 'b2b-after': b2bAfter, 'pricing-after': pricingAfter };
// Stagger is baked into keyframes (popN) so staggered items still leave together at the loop end.
const stagger = (html) => html.replace(/class="([^"]*\ban\b[^"]*)" style="([^"]*?)--d:([\d.]+)s;?/g, (m, c, st, d) => `class="${c} s${Math.min(10, Math.round(parseFloat(d) / 0.25))}" style="${st}`);
for (const [k, f] of Object.entries(pages)) fs.writeFileSync(path.join(OUT, k + '.html'), stagger(f()));
console.log('built', Object.keys(pages).join(', '));
