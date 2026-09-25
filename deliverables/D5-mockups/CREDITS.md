# Credits: third-party reference footage in the mockups

Used for mockup purposes only, to show what each style looks like. The footage is not Poolday's and not ours.

| Where | Source | Notes |
|---|---|---|
| "Kinetic Typo" style preview (`src/assets/footage/kinetic/`, `loop-kinetic-typo.mp4`) | X video "stretching creativity to its limits" (brand unknown), 0:00–0:14.2, unedited | Reference collected by the user |
| "Apple Motion Style" preview | **Pending:** the Langease video (YouTube SgmuplXU2iY). YouTube is blocked from the build environment. Until the file is supplied, the tile shows our own liquid-glass loop (`previews/glass.html`) | Drop the mp4 in, then run `src/tools/make-footage.sh apple <file.mp4> <start> <duration>` |
| "Storytelling Film" preview | **Pending:** a founder video the user will provide. Fallback: our own founder loop (`previews/founder.html`) | `src/tools/make-footage.sh storytelling <file.mp4> <start> <duration>` |

Once a footage folder exists, the tile switches to it automatically (`app.js` checks `assets/footage/<name>/manifest.json`).
