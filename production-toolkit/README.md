# MFM production toolkit (@melaninfitmen)

Unzip, `cd mfm-toolkit`, and run Python from this folder (helpers import `mfm`).

- `mfm.py` — constants (1080x1350, GOLD/DGOLD/WHITE), fonts (`anton`, `raleway`, `comic`), `cover_fit`, `wrap`, `pill` (slide counter), `logo` (MF badge top-left), `full`, `bubble`, `END` (follow end card path).
- `build21h.py` — `grad` (top/bottom gradients), `label`, `arrow`, `ctext`, `toppill`, `tag` (COUCH DAD / KING DAD pills).
- `build22.py` — split-slide helpers: `fitf` (crop with focus), `banded` (top/bottom split with black title band), `two` (two-color headline), `letter` (letterboxed wide scene on blurred bg), `fin` (logo + counter + save). Example posts: `sunday`, `dnt`, `week4`. NOTE: paths at the top (K, K16, O) point at the old session; set your own scene folder and output folder.
- `build24.py` — `strip` (gold "COMMENT KEYWORD · OFFER" CTA strip), `close`/`lclose` (closing slides), `splits` (multi-slide split posts). Examples: `ysiw4`, `tboost`, `hours`, `archer`.
- `build23.py` — 1080x1920 side-by-side split reel with zoom + crossfades + end card via ffmpeg rawvideo pipe.
- `cta_strip.py` — stamp a CTA strip onto an existing slide.
- `sleep_pdf_build.py` — reportlab lead-magnet PDF in the locked black/gold template.
- Fonts: Anton (headlines), Raleway (body), Comic Neue (dialogue). Use "·" not "→" (Raleway lacks the arrow glyph).
- `stories.py` — 1080x1920 Instagram Story builder (`story(out, fn, img_or_pair, fy, kicker, lines, sub, band)`): gold kicker pill, Anton headline, scene band in the middle, empty dark area at the bottom for the IG sticker. 2 stories a day: AM interactive (poll/quiz/slider/questions), PM push to that day's post or a keyword reply.
