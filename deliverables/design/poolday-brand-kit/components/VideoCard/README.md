# VideoCard

A 12px-radius tile that plays one customer video, with its recipe caption and a sound cue.

- Provide: `src` (muted autoplay loop) or `poster`, `title`, `tag` (vertical), `recipe` (the inputs line), `span={2}` for the lead tile, `sound={false}` to hide the sound chip.
- The video fills the tile edge to edge; never letterbox inside a coloured frame.
- Recipe copy follows the formula `<input> + <input>` or `<input> to <output>`.
- Placement of the title and chips is inferred (the live overlay was not captured): keep them small and on dark translucent chips so the video stays the hero.
