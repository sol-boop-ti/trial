# Making motion design that looks designed, not generated

A working manual for an AI agent that builds motion-design scenes (type, UI, logos, product
moments) in code: HTML/CSS render engines, keyframe systems, compositing scripts. It gathers what
separated scenes a senior motion designer would sign from scenes that read as "AI template".

Read it once end to end. Then use section 12 as a checklist on every scene.

---

## 1. The one rule: measure, don't guess

The single biggest quality lever is to **rebuild a real reference frame-accurately before changing
anything**, then change only content: words, images, palette, fonts, logos. Never simplify the motion
while re-skinning. Every simplification (dropping a stagger, a colour trail, a settle, a blur) is
exactly what makes the result look generic.

- Your eye is a poor instrument for motion. It misreads a slide as a zoom, a growing object as a
  camera push, and an ease-out as linear. Trust numbers taken from the pixels.
- Work from the reference's own frames: position, size, rotation, opacity, colour, sampled every 1–2
  frames and resampled to your frame rate.
- Judge the rebuild **side by side with the reference at the same frame numbers** (key-frame pair
  plates), never from memory.
- Expect 1–4 correction passes per scene. The first pass is always wrong somewhere: a baseline, an
  offset, a birth frame, a speed.

---

## 2. What makes motion read as "AI" or "template"

| Tell | What a designer does instead |
|---|---|
| Everything eases with the same default curve | Different curves per property and per role (see §4) |
| Everything starts and stops together | Staggers and overlaps: things are born a few frames apart and settle at different times |
| Motion lands dead on its target | Asymptotic settles, tiny overshoots, a last creep of a few px |
| Symmetric, centred, static layouts | Off-centre composition, a line that recentres as it grows, drift during holds |
| Uniform fade-ins | Opacity tied to motion (ink arrives with the move), colour trails on the newest element |
| Clean vector perfection | Grain, soft edges, motion blur on fast moves, texture in grounds |
| Holds that are frozen | Nothing is ever fully still: a 1–3% slow push, drift, or breathing during a hold |
| Many effects at once | One idea per shot, executed with precision |
| Three lines of text, small type | One line (two at most), big type, high contrast |
| Generic gradients | Gradients with measured stops, often fixed in screen space while type moves under them |

---

## 3. Timing

**Frame rate and resampling**
- Author in frames, not seconds. 30 fps is a good master rate; resample references (24/25/60) to it.
  For 60 fps sources, take every second sample; do not average.
- Sub-frame births are fine (e.g. a word born at frame 8.1). Compute the continuous curve and sample
  it per frame.

**Shot and beat lengths (short-form ads, product films)**
- Hook or title card: 1.5–2.5 s.
- A claim over footage: 2–3 s, often spanning 2–3 cuts of 0.7–1 s each under the same text.
- Fast montage: cuts every 0.4–0.8 s.
- Logo lockup: 2–3 s, including a hold of at least 0.6 s once everything has landed.
- Whole film: 15–18 s for a launch or announcement.

**Stagger and overlap**
- Words in a line: born 3–6 frames apart. Letters in a typed line: about 1.5 frames per glyph.
- Stacked items (cards, notifications): each new item arrives while the previous one is still
  settling.
- Secondary elements (chips, cursors, decorations) arrive 5–15 frames after the hero, on their own
  curves, and keep drifting slowly afterwards.

**Anticipation and follow-through**
- Before a big move, a small counter-move: a tile rocks back ~25° before sliding off.
- After an arrival: a settle of 3–10 frames (rotation overshoot of ~3–4°, scale 1.2 → 1.0).

---

## 4. Easing: the curves that work

Default CSS eases (`ease`, `ease-in-out`) are the fastest way to look templated. Compute your own curve
per frame and bake it into keyframes.

**Exponential decay (the "never quite lands" settle)**
- `offset(τ) = A · r^τ`, with τ = frames since birth and r ≈ 0.77 per frame at 30 fps.
- Words rising into a line: A ≈ 1.1–1.5 × font size. Opacity `1 − e^(−0.65 τ)`, so the ink is mostly
  in by 4–5 frames while the position keeps easing for 15+ frames.
- It reads as natural because it keeps moving imperceptibly; nothing snaps.

**Ease-out cubic / power curves**
- `e(u) = 1 − (1 − u)^3` for most arrivals (position, scale).
- Use a **steeper power for size than for rotation or position**, e.g. size `1 − (1 − u)^5` with
  rotation `1 − (1 − u)^3`. A logo that shrinks to size fast but keeps turning a little longer feels
  crafted.

**Normalised exponential for a decelerating scroll (drum / slot / reel)**
- `p(t) = S · (1 − e^(−(t − t0)/τ)) / (1 − e^(−(T − t0)/τ))`, with τ ≈ 14 frames. It lands exactly on the
  target item at frame T while still creeping at the cut.
- Early speed can be very high (half an item per frame). Add motion blur there (see §6).

**Smoothstep** `u²(3 − 2u)`
- Only for small secondary transitions (a pile shifting one step, a cross-state blend). Too soft for
  hero moves.

**Speed ramps for pans**
- A camera or line pan often runs fast → slow → fast again (an S-shaped velocity): it enters quickly,
  eases through the readable moment, then accelerates out into the cut.
- Measure the velocity per frame from the reference. Do not assume linear.

**Springs / overshoot (use sparingly)**
- For UI cards: arrive at 1.15–1.2× scale with a +3–4° tilt overshoot, then settle to 1.0× and −1°
  over 8–10 frames.
- A small tilt at rest (−1°) reads as real.

**Timing rule of thumb**
- Hero arrivals: 12–25 frames.
- Settles: 6–15 frames.
- Opacity-in: 2–8 frames.
- Colour trail on a typing head: about 8 frames from accent back to ink.

---

## 5. The motion vocabulary that reads as designed

- **Typewriter with an accent head**: glyphs appear one by one (1.5 frames each); the newest glyph
  is in the accent colour and fades back to ink over ~8 frames. The block recentres slightly as it
  grows (drift ~40–60 px, then eases back).
- **Sentence with embedded thumbnails**: square rounded image slots inside a line of display type
  (slot ≈ 0.85–0.9 × font size). They land with the typing, then **keep swapping every 4–8 frames**.
  Stop swapping ~5 frames before the end so the last frame is not a blank.
- **Word rise**: each word rises into place on the exponential curve, staggered 3 frames.
  Excellent over footage.
- **Decelerating drum**: a vertical column of pills scrolling up and decelerating onto one item.
  - The centre item is larger (×1.29 vs neighbours).
  - Opacity is asymmetric: the neighbour above stays at ~90%, the one below at ~40%, the far ones
    ~30% then 0.
  - Motion blur while fast.
- **Screen-fixed gradient under moving type**: the gradient stays put while the word slides
  through it, so each letter changes colour as it travels. Combine with a vertical fade: full ink on
  the upper half of the letters, fading to the ground colour at the baseline.
- **Reveal from behind an object**: the name slides out from under a logo tile, visible only right
  of the tile's edge.
  - A cheap, robust mask: a ground-coloured rectangle riding the tile's edge whose **width is
    animated** from the text's left end to the tile's right edge.
  - It only works where the ground under it is a flat colour.
- **Fly-in with rock**: a tile enters already rotated (−37°) and fast, straightens on an ease-out
  while landing, rocks back (−25°) as anticipation, then slides to its lockup position.
- **Counter-rotating orbits**: two concentric rings opening on ease-out; dots and arrowheads on each
  ring turn in opposite directions (≈ ±0.37–0.38°/frame at 60 fps). The dots grow with the rings.
  - Rings are not a camera push: the centre disc keeps its size while they open. Always verify which
    is happening.
- **Multiplayer cursors / name chips**: coloured pills with a pointer aimed at the focal point.
  They slide in from the edges on ease-out and keep drifting slowly the whole shot.
- **Notification pile**: cards spring in from a corner (tiny, −30° tilt, motion-smeared) to 1.2× above
  the pile, then settle. Older cards sink behind to peek 7 and 13 px below, slightly narrower.
- **End pan / whip**: in the last 20–40 frames everything accelerates in one direction into the
  cut. Motion into the next shot beats a fade.
- **Logo end card**: small mark on a light ground, arriving at 0.82× scale on an ease-out over 14
  frames, holding, then easing to ~45% grey in the final third of a second.

---

## 6. Texture, blur, colour: the non-motion half of "designed"

**Motion blur**
- For fast moves, render a duplicate of the element with a static blur (5–7 px) on the same
  animation track.
- Weight it by speed: `wb = clamp((speed − threshold) / range)`, with the sharp copy at
  `1 − 0.4·wb` and the blurred copy at `0.9·wb`.
- Set the threshold high enough (e.g. 18 px/frame) that settles stay crisp. A blur that lingers
  makes the element look washed out.

**Grain and film finish**
- A fine grain over grounds and footage, slight halation on highlights, lifted blacks and a gentle
  vignette.
- It unifies generated images and hides the too-clean look.

**Gradients and blooms**
- Rebuild a reference gradient by decomposing each pixel into weights of its 2–3 key colours
  (least squares against base, colour 1, colour 2), then recomposing with your own palette at the
  same weights. You keep the exact shape and falloff and change only the colours.
- Mask out type and objects before decomposing (inpaint small strokes only; large inpaints bleed
  colour into the wrong places).
- Pre-render them as images if your engine can't paint radial gradients.

**Palette discipline**
- One accent colour per shot. Grounds are off-white or near-black, never pure `#fff` or `#000`.
- Type is ink on light or white on dark, with a real contrast ratio.

**Text over footage**
- White, weight 500–600, with a soft wide shadow (`0 2px 28px rgba(0,0,0,.28)`) for legibility.
- Centred type is fine. Avoid boxes and pills behind the text.

---

## 7. Typography

- Display type: tracking **−0.02 to −0.04 em**; tighter as the size grows.
- **Identify a reference face by fitting cap height AND set width together**. When substituting a
  different face, decide consciously which one to match:
  - width, if colour or position depends on where each letter lands;
  - cap height, if it sits in a lockup next to a mark.
- Sizes at 1080p:
  - hero single word: 300–400 px;
  - display sentence: 120–200 px;
  - titles over footage: 64–72 px (a model or product name ~1.5× larger);
  - UI labels: 36–46 px inside chips.
- Never three lines. One line is best; two at most. Hand-break lines rather than relying on
  soft-wrap.
- Place type by **baseline**, not by box top. Compute the top from the baseline and the font's
  metrics.
- Per-glyph elements let you animate colour, birth and position per letter. Build lines that way
  whenever the reference treats letters individually.

---

## 8. Composition

- Off-centre by default. A lockup can sit slightly off the frame centre, as long as it keeps the
  reference's centre.
- A line that grows recentres; a line that is complete drifts a few px.
- Leave generous empty space. Reduce the element count before you reduce the element size.
- When re-skinning a lockup with different proportions (a shorter name, a different mark), keep the
  **centre** of the original lockup and scale the travel distances by the same ratio. The motion
  stays identical in feel.

---

## 9. Measurement techniques (how to read a reference)

- **Contact sheets**: one frame every 2–5 frames, labelled with frame numbers. Read these first to
  understand the structure: shots, cuts, what enters and exits.
- **Ink bounding boxes**: threshold by darkness or saturation, take connected components and track
  their bbox per frame. That gives position, size and birth frame per word.
- **Rotation**: take the minimum-area rectangle of an element's mask. Angles are ambiguous modulo
  90°, so unwrap them using continuity.
- **Separate touching elements** by restricting the mask to a disc around a robust centre (median,
  then iterate).
- **Radii of circular things**: use a radial profile (the farthest white pixel along several rays,
  then the median), NOT sqrt(area/π). Area-based radius shrinks when something covers the centre.
  This is a classic trap.
- **Rings and dots on orbits**: convert blob centroids to polar coordinates around the centre. Fit
  angle vs frame linearly to get the angular speed.
- **Colours**: sample the darkest or most saturated pixels in a band along the line at several x
  positions and several frames. If the colour at a given screen x is constant across frames while
  the type moves, the gradient is screen-fixed.
- **Opacity ramps**: track the minimum grey value of a glyph over frames. Ink darkness gives the
  real birth frame, often several frames before a strict threshold detects the glyph.
- **Cuts inside a clip**: a mean absolute frame difference on a downscaled greyscale version, with a
  threshold (e.g. > 25/255).
- **Velocity**: difference positions frame to frame. Look at the velocity profile to choose the
  curve (constant, decaying, S-shaped ramp).
- **Validate every assumption numerically**: "Is it a camera push?" "Does it land?" "Is it
  linear?" Each of these, judged by eye, has been wrong at least once.

---

## 10. Rendering-engine pitfalls (HTML/CSS → video engines)

These show up across headless-browser and custom compositors. Check them early in yours.

- **One `animation` declaration per element.** Merge multiple keyframe tracks into one declaration,
  or put each track on its own element.
- **Don't animate children inside animated parents** if the engine composites poorly. Give every
  moving element its own single track. Static scaling wrappers are usually fine.
- **Frame offset**: many engines evaluate frame k at time (k+1)/fps. Shift your tracks one frame so
  the value authored for k is the one rendered at k.
- **Base state**: an element revealed by a delayed animation needs `opacity:0` in its base style.
  `fill-mode` does not cover the delay in every engine.
- **Unsupported effects**: pre-render them to images or frames, rather than faking them badly:
  - radial gradients;
  - masks;
  - multi-layer backgrounds;
  - `background-clip:text`;
  - blur on animated content;
  - crops under rotation.
- **Clip-path** is often limited: percentage polygons only, no rounded insets. Animating `width` is
  a robust alternative for wipes and reveals.
- **Percentage translates** may not resolve. Use px.
- **Video layers** may play from document time 0 regardless of placement. Pre-cut one background
  plate that already carries the whole edit and put the graphics over it.
- **Inline SVG** may not paint, or may not paint under opacity. Rasterise icons to PNG.
- **Always render and inspect real frames.** Never trust that CSS "should" work.

---

## 11. Generated imagery and footage inside motion pieces

When a scene uses AI-generated photos or video, realism is part of the craft.

**Prompting for real photos**
- Write like a photographer: camera and lens, film stock and scan (e.g. "35mm, Portra 400, lab
  scan"), fine grain, low contrast, lifted blacks, soft edges.
- Explicitly say no HDR, no sharpening, no retouching, no beauty filter.
- Avoid the words that trigger the glossy AI look: "ultra-realistic", "8K", "cinematic",
  "extremely detailed".

**Imperfections and framing**
- Describe imperfections in moderation: pores, flyaway hairs, a fingerprint on glass, crumbs,
  lived-in clothes. Over-specifying (e.g. "frayed", "stained") produces exaggerated damage.
- Prefer candid moments (mid-sip, glancing away), off-centre framing and ordinary settings. Avoid
  sunsets behind products, saturated neon and symmetric product centring.

**Night scenes**
- A direct-flash snapshot or a noisy, slightly shaky phone photo reads far more real than a graded
  "cinematic" night.

**Making products desirable**
- Realism alone can be dull. Add campaign intent: hard raking sunlight making liquids glow, leaf
  shadows, noble materials, a human touch (a hand, a wrist), intimate night light.

**Consistency across shots**
- Some models reproduce a reference's composition instead of its identity. Test before committing.
- A workable pattern: generate the most realistic "source" image with one model, then derive
  variants with a model that preserves identity from references. Pass the same reference every
  time.

**Video**
- Always start from a still image (image-to-video), never text-to-video, for realism.
- Motion prompts should describe small, physical, natural motion (breeze, light shift, a sip, a
  glance) and forbid morphing.
- **Avoid close-ups of liquids** (pours, drops, latte art, water running down glass) and **faces in
  motion at large size**: models fail there first (gel-like fluids, smoothed skin). Choose actions
  models handle well: hands doing tactile work, light changing, fabric moving, camera drift.
- Test 2 clips before generating a batch. Then review every clip frame by frame and trim to the
  good portion. Many clips have 1–2 s of excellent footage and a weak end (the object leaves the
  frame, the push crops the subject, physics breaks).

---

## 12. Sound

Sound makes motion feel physical; silence makes it feel like a render.

- UI and type SFX, synced to the exact frames of the events:
  - soft key clicks for typing (vary pitch and level per key, avoid machine-gun regularity);
  - small pops or ticks when thumbnails swap;
  - an airy whoosh on fast moves (band-passed noise with a fast attack and a longer release, with
    the pitch following speed);
  - a soft low thud or hit when a logo lands;
  - a tail of room tone.
- Music: a minimal, confident bed at 100–124 BPM. Cut the edit on beats or half-beats. A riser
  into the logo, and a hit plus silence or a tail at the end.
- Mix: music around −16 LUFS integrated for social; SFX sit 3–6 dB under the music's peaks except on
  hero hits. A short fade-out, never a hard stop.

---

## 13. Per-scene checklist

1. Is there a reference? Build a contact sheet and list the beats with frame numbers.
2. Measure every moving element per frame: position, size, rotation, opacity, colour, birth.
3. Identify each curve from its velocity profile (decay, ease-out power, S-ramp, linear) and
   reproduce it numerically.
4. Staggers, overlaps and settles present? Nothing starts or stops in unison unless the reference does.
5. Holds alive (slow push, drift, breathing)?
6. Type: fitted size, tracking −0.02 to −0.04 em, baseline-placed, one or two lines, strong
   contrast, one accent.
7. Texture: grain, soft edges, motion blur on fast moves only.
8. Re-skin only content. The motion and geometry stay identical; lockup centres are kept and travels
   scaled.
9. Render, then make pair plates against the reference at 4–6 key frames. Fix and repeat until
   they match.
10. Check the first and last frames specifically (blank slots, elements still fading, text
    leaving early).
11. Add sound synced to events.
12. Watch it once at full speed without analysing. Does it feel inevitable? If a beat feels
    arbitrary, measure it again.
