// Motion library shared by the app and the style previews.
// Curves follow poolday/motion-design-for-agents.md (sections 3-5):
//   - author in frames at 30 fps; no default CSS eases
//   - exponential "never quite lands" settles (r ~ 0.77 / frame)
//   - ease-out power curves, steeper for size than for position
//   - opacity tied to motion (ink in over 2-8 frames)
//   - staggers of 3-6 frames; holds are never frozen (slow push / drift)
(function (g) {
  const FPS = 30;
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const seg = (t, a, b) => clamp((t - a) / (b - a));           // 0..1 progress of t in [a,b]
  const fr = (t, t0) => Math.max(0, (t - t0) * FPS);             // frames since t0
  // Exponential decay settle: 1 - r^tau. r = 0.77 lands ~95% in 11 frames, keeps creeping.
  const expo = (tau, r = 0.77) => (tau <= 0 ? 0 : 1 - Math.pow(r, tau));
  // Ink (opacity) arrives with the move: 1 - e^(-0.65 tau).
  const ink = (tau, k = 0.65) => (tau <= 0 ? 0 : 1 - Math.exp(-k * tau));
  const out3 = (u) => 1 - Math.pow(1 - clamp(u), 3);
  const out5 = (u) => 1 - Math.pow(1 - clamp(u), 5);
  const in3 = (u) => Math.pow(clamp(u), 3);
  const inOut3 = (u) => { u = clamp(u); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
  const smooth = (u) => { u = clamp(u); return u * u * (3 - 2 * u); };  // secondary only
  // Damped overshoot for UI cards (arrive past target, settle over 8-10 frames).
  const spring = (tau, w = 0.34, d = 0.2) => (tau <= 0 ? 0 : 1 - Math.exp(-d * tau) * Math.cos(w * tau));
  // Normalised exponential for a decelerating drum/scroll landing exactly at T.
  const drum = (t, t0, T, tauF = 14) => {
    const a = fr(t, t0), A = (T - t0) * FPS; if (a >= A) return 1;
    return (1 - Math.exp(-a / tauF)) / (1 - Math.exp(-A / tauF));
  };
  // Slow "alive hold": 1-3% push over a hold, linear-ish drift that never stops.
  const breathe = (t, period = 6, amp = 1) => Math.sin((t / period) * Math.PI * 2) * amp;
  // Deterministic pseudo-random (for grain seeds, jitter).
  const rnd = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  // Speed-weighted motion blur amount (manual section 6): 0 below threshold px/frame.
  const blurW = (speedPxPerFrame, threshold = 18, range = 30) => clamp((speedPxPerFrame - threshold) / range);
  g.M = { FPS, clamp, lerp, seg, fr, expo, ink, out3, out5, in3, inOut3, smooth, spring, drum, breathe, rnd, blurW };
})(window);
