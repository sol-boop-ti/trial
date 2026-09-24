/* @ds-bundle: {"format":4,"namespace":"Poolday","components":[{"name":"Button"},{"name":"NavBar"},{"name":"FilterTabs"},{"name":"VideoCard"},{"name":"VideoGrid"},{"name":"SectionTitle"},{"name":"Halftone"},{"name":"Hero"},{"name":"Icon"}]} */
(function () {
  var React = window.React, h = React.createElement;
  var ICONS = {"layout-grid": [["rect", {"width": "7", "height": "7", "x": "3", "y": "3", "rx": "1"}], ["rect", {"width": "7", "height": "7", "x": "14", "y": "3", "rx": "1"}], ["rect", {"width": "7", "height": "7", "x": "14", "y": "14", "rx": "1"}], ["rect", {"width": "7", "height": "7", "x": "3", "y": "14", "rx": "1"}]], "briefcase": [["path", {"d": "M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"}], ["rect", {"width": "20", "height": "14", "x": "2", "y": "6", "rx": "2"}]], "gamepad-2": [["line", {"x1": "6", "x2": "10", "y1": "11", "y2": "11"}], ["line", {"x1": "8", "x2": "8", "y1": "9", "y2": "13"}], ["line", {"x1": "15", "x2": "15.01", "y1": "12", "y2": "12"}], ["line", {"x1": "18", "x2": "18.01", "y1": "10", "y2": "10"}], ["path", {"d": "M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z"}]], "mic": [["path", {"d": "M12 19v3"}], ["path", {"d": "M19 10v2a7 7 0 0 1-14 0v-2"}], ["rect", {"x": "9", "y": "2", "width": "6", "height": "13", "rx": "3"}]], "chevron-down": [["path", {"d": "m6 9 6 6 6-6"}]], "volume-2": [["path", {"d": "M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"}], ["path", {"d": "M16 9a5 5 0 0 1 0 6"}], ["path", {"d": "M19.364 18.364a9 9 0 0 0 0-12.728"}]]};
  function cx() { return Array.prototype.filter.call(arguments, Boolean).join(' '); }
  function omit(o, keys) { var r = {}; for (var k in o) if (keys.indexOf(k) < 0) r[k] = o[k]; return r; }

  function Icon(p) {
    var parts = ICONS[p.name] || [];
    var s = p.size || 16;
    return h('svg', { className: cx('pd-icon', p.className), width: s, height: s, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round', 'aria-hidden': true },
      parts.map(function (e, i) {
        var a = {}; for (var k in e[1]) a[k.replace(/-([a-z])/g, function (m, c) { return c.toUpperCase(); })] = e[1][k];
        a.key = i; return h(e[0], a);
      }));
  }

  function Button(p) {
    var size = p.size || 'md';
    var rest = omit(p, ['size', 'className', 'children', 'href', 'icon']);
    var tag = p.href ? 'a' : 'button';
    if (p.href) rest.href = p.href; else rest.type = rest.type || 'button';
    rest.className = cx('pd-btn', 'pd-btn-' + size, p.className);
    return h(tag, rest, p.icon ? h(Icon, { name: p.icon }) : null, p.children);
  }

  var DEFAULT_LINKS = [
    { label: 'Home', href: '#' }, { label: 'Solutions', menu: true }, { label: 'Integrations', href: '#' },
    { label: 'Pricing', href: '#' }, { label: 'Resources', menu: true }
  ];
  function NavBar(p) {
    var links = p.links || DEFAULT_LINKS;
    return h('header', { className: cx('pd-nav', p.className) },
      h('a', { className: 'pd-wordmark', href: p.homeHref || '#' }, 'Poolday.ai'),
      h('nav', { className: 'pd-nav-links', 'aria-label': 'Main' },
        links.map(function (l, i) {
          return l.menu
            ? h('button', { key: i, type: 'button', className: 'pd-nav-link', 'aria-haspopup': 'menu' }, l.label, h(Icon, { name: 'chevron-down', size: 14 }))
            : h('a', { key: i, className: 'pd-nav-link', href: l.href || '#' }, l.label);
        })),
      h(Button, { size: 'md', href: p.ctaHref }, p.cta || 'Book a 15 min demo'));
  }

  var DEFAULT_TABS = [
    { id: 'all', label: 'All', icon: 'layout-grid' },
    { id: 'tech', label: 'Tech Industry', icon: 'briefcase' },
    { id: 'apps', label: 'Apps & Games', icon: 'gamepad-2' },
    { id: 'podcasts', label: 'Podcasts', icon: 'mic' }
  ];
  function FilterTabs(p) {
    var items = p.items || DEFAULT_TABS;
    var st = React.useState(p.defaultValue || items[0].id);
    var value = p.value != null ? p.value : st[0];
    function pick(id) { st[1](id); if (p.onChange) p.onChange(id); }
    return h('div', { className: cx('pd-tabs', p.className), role: 'tablist' },
      items.map(function (t) {
        var on = t.id === value;
        return h('button', { key: t.id, type: 'button', role: 'tab', 'aria-selected': on, className: 'pd-tab', onClick: function () { pick(t.id); } },
          t.icon ? h(Icon, { name: t.icon }) : null, t.label);
      }));
  }

  function VideoCard(p) {
    var media = p.src
      ? h('video', { className: 'pd-card-media', src: p.src, poster: p.poster, muted: true, autoPlay: true, loop: true, playsInline: true })
      : p.poster
        ? h('img', { className: 'pd-card-media', src: p.poster, alt: '' })
        : h('div', { className: 'pd-card-media pd-card-placeholder', style: p.tint ? { background: p.tint } : null });
    return h('figure', { className: cx('pd-card', p.span === 2 && 'pd-card-wide', p.className) },
      media,
      h('figcaption', { className: 'pd-card-caption' },
        p.recipe ? h('span', { className: 'pd-glass-chip' }, p.recipe) : null,
        p.sound === false ? null : h('span', { className: 'pd-glass-chip pd-chip-sound' }, h(Icon, { name: 'volume-2', size: 14 }), 'Watch with sound')),
      p.title ? h('div', { className: 'pd-card-title' }, h('strong', null, p.title), p.tag ? h('span', null, p.tag) : null) : null);
  }

  function VideoGrid(p) {
    return h('div', { className: cx('pd-grid', p.className) }, p.children);
  }

  function SectionTitle(p) {
    return h(p.as || 'h2', { className: cx('pd-section-title', p.className) }, p.lead, p.tail ? ' ' : null, p.tail ? h('span', { className: 'pd-quiet' }, p.tail) : null);
  }

  function readColor(el, name, fb) {
    var v = getComputedStyle(el).getPropertyValue(name).trim();
    var m = /^#([0-9a-f]{6})$/i.exec(v);
    if (!m) return fb;
    var n = parseInt(m[1], 16); return [n >> 16 & 255, n >> 8 & 255, n & 255];
  }
  function Halftone(p) {
    var ref = React.useRef(null);
    React.useEffect(function () {
      var cv = ref.current; if (!cv) return;
      var raf = 0, t0 = performance.now();
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      function draw(now) {
        var r = cv.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
        var w = Math.max(1, Math.round(r.width)), hgt = Math.max(1, Math.round(r.height));
        if (cv.width !== w * dpr) { cv.width = w * dpr; cv.height = hgt * dpr; }
        var ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, w, hgt);
        var hi = readColor(cv, '--halftone-dot', [45, 45, 50]), lo = readColor(cv, '--halftone-dot-dim', [16, 16, 18]);
        var drift = p.animate && !reduce ? Math.sin((now - t0) / 4000) * 24 : 0;
        var cxp = w * (p.centerX != null ? p.centerX : 0.5) + drift, cyp = hgt * (p.centerY != null ? p.centerY : 0.62);
        var rx = p.radiusX || Math.min(w * 0.42, 490), ry = p.radiusY || rx * 0.66;
        for (var y = 0; y < hgt; y += 8) {
          for (var x = 0; x < w; x += 4) {
            var dx = (x - cxp) / rx, dy = (y - cyp) / ry, d = Math.sqrt(dx * dx + dy * dy);
            var k = 1 - d; if (k <= 0) continue;
            k = k * k * (3 - 2 * k);
            var c0 = Math.round(lo[0] + (hi[0] - lo[0]) * k), c1 = Math.round(lo[1] + (hi[1] - lo[1]) * k), c2 = Math.round(lo[2] + (hi[2] - lo[2]) * k);
            ctx.fillStyle = 'rgb(' + c0 + ',' + c1 + ',' + c2 + ')';
            var dh = 1 + 2 * k; ctx.fillRect(x, y - dh / 2, 1.5 + 0.5 * k, dh);
          }
        }
        if (p.animate && !reduce) raf = requestAnimationFrame(draw);
      }
      draw(performance.now());
      var ro = window.ResizeObserver ? new ResizeObserver(function () { draw(performance.now()); }) : null;
      if (ro) ro.observe(cv);
      return function () { cancelAnimationFrame(raf); if (ro) ro.disconnect(); };
    }, [p.animate, p.centerX, p.centerY, p.radiusX, p.radiusY]);
    return h('canvas', { ref: ref, className: cx('pd-halftone', p.className), 'aria-hidden': true });
  }

  function Hero(p) {
    return h('section', { className: cx('pd-hero', p.className) },
      h(Halftone, { animate: p.animate }),
      h('div', { className: 'pd-hero-inner' },
        h('h1', { className: 'pd-display' }, p.title || 'The Media Superintelligence.'),
        h('p', { className: 'pd-lede' }, p.lede || 'An AI agent that edits, generates and assembles on-brand videos.'),
        h(Button, { size: 'lg', href: p.ctaHref }, p.cta || 'Book a 15 min demo')));
  }

  window.Poolday = Object.assign(window.Poolday || {}, {
    Icon: Icon, Button: Button, NavBar: NavBar, FilterTabs: FilterTabs, VideoCard: VideoCard,
    VideoGrid: VideoGrid, SectionTitle: SectionTitle, Halftone: Halftone, Hero: Hero
  });
})();
