# Halftone

The signature scan-dot ellipse, drawn on a canvas that fills its positioned parent.

- Provide: a `position: relative` parent with a size. Optional `centerX`/`centerY` (0–1, default 0.5/0.62), `radiusX`/`radiusY` in px, `animate` for a slow drift (stops under reduced motion).
- Dots every 4px (`space-1`) on 8px rows (`space-2`), coloured from `halftone-dot-dim` to `halftone-dot`, growing from 1px to 3px tall toward the centre.
- Always behind type, never above 20% brightness, never recoloured with brand-cyan.
