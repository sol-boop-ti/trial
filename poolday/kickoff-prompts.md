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
