# Reference: the user's Pletor "UGC farm" pipeline (Casey AI format)

Screenshot: `deliverables/assets/pletor-ugc-farm.webp` (4 personas: @casey_ai, @mailia_ai, @brooke_ai, @ciara_ai; dozens of shock-face variants per persona). It goes in the final deliverable's appendix.

**Format:** shock face (a candid iPhone-selfie reaction) → product demo filmed on an iPhone.
**Chain:** (1) base character image → (2) shock-face image conditioned on (1) → (3) image-to-video with Kling 2.6/3.
**Image model used:** ChatGPT image generation. **Video model used:** Kling 2.6 / 3.

## 1. Base character (image)
A 24-year-old American woman just looked up from her MacBook at 10:47pm. She grabbed her iPhone off the couch cushion next to her to film herself. The front camera opened mid-motion — the frame caught her before she was ready. Honey brown hair, one chunk stuck to her left cheek from lying on the couch, rest falling unevenly over her right shoulder. Faint mascara smudge under her right eye only. One small red pimple on her left jawline. Asymmetric lazy eye — right eye slightly more open. Warm uneven lamp light from her right side only, left side of face in shadow. Slightly greasy T-zone. Grey faded university crewneck. Thin gold chain sitting crooked. Face 85% of frame, off-center left, head tilted right, eyes angled 25 degrees left of lens looking at laptop. Lips slightly parted, lower lip dry. She has not spoken yet. Phone auto-exposure blowing out slightly on her right cheekbone. Barrel distortion warping her nose wider. Chromatic aberration on hair edges. JPEG compression artifacts in shadow areas. 9:16 vertical. IMG_0029.JPG iPhone 13 front camera 0.5x. Snapchat 2023. --ar 9:16 --style raw --stylize 0 --weird 5 --chaos 10

## 2. Shock face (image, conditioned on 1)
A 24-year-old American woman just saw something on her MacBook screen at 10:47pm and grabbed her iPhone to film her reaction. The front camera opened mid-motion — the frame caught her looking down and away at the laptop, not at the lens. Honey brown hair, one chunk stuck to her left cheek from lying on the couch, rest falling unevenly over her right shoulder. Faint mascara smudge under her right eye only. One small red pimple on her left jawline. Asymmetric lazy eye — right eye slightly more open. Her eyes are locked downward at roughly 40 degrees off-lens, pupils tracking something on the screen, wide open in disbelief, whites of eyes visible above the iris. Eyebrows raised unevenly, the right one higher. Mouth fully open in a slack soft 'O', lower jaw dropped, lower lip dry. No hand in frame yet. Warm uneven lamp light from her right side only, left side of face in shadow, blue cool glow from the laptop screen lighting her chin and the underside of her jaw from below. Slightly greasy T-zone. Grey faded university crewneck. Thin gold chain sitting crooked. Face 85% of frame, off-center left, head tilted forward and slightly right. Phone auto-exposure confused by mixed warm and cool light, slightly blown on her right cheekbone, slightly underexposed in the shadow. Barrel distortion warping her nose wider. Chromatic aberration on hair edges, stronger because of the mixed color temperature. JPEG compression artifacts in shadow areas. 9:16 vertical. IMG_0042.JPG iPhone 13 front camera 0.5x. Snapchat 2023. --ar 9:16 --style raw --stylize 0 --weird 5 --chaos 10

## 3. Video (Kling 2.6 / 3)
A 24-year-old American woman, filmed from a three-quarter side angle at 11:38pm, face turned 25 degrees away from camera, right cheek closer to lens. She is holding her iPhone out to her right side at arm's length. Honey brown hair, one chunk stuck to her left cheek, rest falling unevenly over her right shoulder closer to the lens. Faint mascara smudge under her right eye only. One small red pimple on her left jawline, partially visible. Asymmetric lazy eye — right eye more open and closer to camera. Left hand up flat against the lower half of her face, palm pressed flat covering her entire mouth and chin, fingers spread, no ring. Only eyes and nose uncovered. Eyebrows pulled together, forehead slightly creased. Eyes wide, looking sideways at the camera at a sharp angle. Warm dim bedside lamp light hitting the back of her head and right ear strongly, front of face in softer shadow. Cream ribbed cotton tank top with thin straps sitting evenly on both shoulders. Thin gold chain sitting crooked, partially hidden by the hand. Face 70% of frame, off-center right, head tilted slightly down. Blurred pillow and headboard behind her. Phone auto-exposure blowing out on her right ear and hair behind it. Strong barrel distortion on her hand closest to lens. Chromatic aberration on hair edges. JPEG compression artifacts in shadow areas. 9:16 vertical. IMG_0043.JPG iPhone 13 front camera 0.5x. Snapchat 2023. --ar 9:16 --style raw --stylize 0 --weird 5 --chaos 10

## Redoing it in Poolday, the intended way (intent-level brief, Align mode)
```
I want to produce [6] AI UGC Reels for Instagram (9:16, 10–15s) that drive
B2B marketers and founders to Poolday. Format that already worked for me:
a candid iPhone-selfie "shock face" reaction (2s) → a screen recording of
Poolday making a video (the reason for the shock) → a one-line CTA.
Attached: my character and shock-face prompts from a previous project as the
look reference (raw, imperfect, front camera 0.5x, lamp light, JPEG noise).
Steps, wait for my choice at each one:
1. Generate 30 actor photos across 3 distinct personas. I pick 3.
2. For each persona, 6 shock-face variants. I pick the best.
3. 5 hook lines + on-screen text options. I pick.
Then build the videos as variants in this conversation.
You decide the models, the animation and the edit.
```
