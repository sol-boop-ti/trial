# Poolday kickoff prompts: prospect videos (D2)

How the skill (`ref-replicate-skill.md`, "Reference Teaser") works:
- **Inputs:** a reference video **link** plus a brand URL. It needs a watchable video link (YouTube, TikTok, IG, X). Drive and Dropbox links don't work, so upload the file instead.
- It writes the brand kit, story brief, swap table and keyframes on its own, then asks you **once** at a single gate: script, look (keyframes next to reference frames plus a 3s render), and routing (Remotion vs. Seedance).
- It targets about 20s and keeps the reference's cut rhythm, and the reference's look wins over the brand's. **So the reference video you pick is the single biggest creative decision.**

## Picking the reference (do this yourself: taste is your job)
- Pick a 30–60s launch video you genuinely love, with dense cuts and strong kinetic type or UI motion. Examples of the genre: Linear, Arc, Raycast, Apple product launches, Vercel Ship.
- Match the reference to the brand's world:
  - **Wispr Flow:** voice → text flowing into apps. A kinetic-typography or UI-heavy launch reference.
  - **Flam:** immersive mixed-reality content. A reference with camera moves through 3D space and physical-world shots (this uses the skill's Seedance routing).
- In the prompt, **write what you like about the reference** (pacing, type treatment, transitions), as the agent guide recommends.

## Kickoff (Align mode, Max or Ultra tier). Keep it short and let the skill drive.

```
[drop the skill file]
Use this skill. Reference: <VIDEO LINK>. Brand: https://wisprflow.ai
What I love in the reference: <2–3 specific things: e.g. the hard cuts on the
kick, the oversized type that wipes across UI, the one continuous camera move
at the end>.
Objective: a teaser I'll send to Wispr Flow's VP Product Marketing, framed as
"what your meetings launch could look like". 16:9, sent by email + LinkedIn.
Make it the most impressive video possible: rich visual detail, seamless
continuity from start to finish.
You have creative freedom on everything not fixed by the reference and the brand.
```

The same prompt works for Flam (`https://flamapp.ai`, framed as "your Series B announcement film").

Alternative from the brief to test **in a separate conversation** (compare the two and keep the best):
```
Build a video for Wispr Flow in threejs. Make the most impressive video possible.
Rich visual detail, seamless continuity from start to finish.
```

## After the first one is final
"Save this flow as a skill and a `/prospect-video` command that takes a company URL + reference link." The agent loop (D3) then generates only that 2-line call.

---

## v2: the three-input setup (updated after the reference videos and the motion manual)

Give Poolday three things, each with one job:
1. **Taste = the reference video** (`references/`). Say in words what you love: for ImagineArt it's the easing, the speed, and the tiles → fan → carousel continuity.
2. **Craft = the motion manual** (`poolday/motion-design-for-agents.md`). Do this once per workspace: *"Create a skill from this document called motion-craft. Apply it to every motion-design video."* It holds the measured rules: exponential settles, staggers of 3–6 frames, holds that stay alive, one accent colour, big type on one line, motion blur on fast moves, sound synced to events.
3. **Process = the ref-teaser skill** (`poolday/ref-replicate-skill.md`): beat list → brand kit → swap table → one approval gate → build.

Plus **brand fidelity**: build the brand kit first. Feed it the logo, fonts, product screenshots (rebuilt into animatable pieces) and the brand's visual medium (flat 2D, 3D, photo…), not only the URL. That's the lesson from the PostHog review.

Kickoff (Align mode, Max tier):
```
Use the ref-teaser skill and my motion-craft skill.
Reference: <link or attached file>. Brand: brand:<name> (or <url>).
What I love in the reference: <the easing / speed / the continuity from X to Y>.
Keep its motion exactly; change only content (words, images, palette, logo).
Objective: a ~20s teaser I'll send to <role> at <company> about <angle>.
Hard rules: show the real product UI at least once; one line of type per shot;
the end card is animated, never a static slide.
You have creative freedom on everything else.
```
