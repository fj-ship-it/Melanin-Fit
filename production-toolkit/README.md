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
- `fuel_chart.py` + `fuel_chart_reel.py` — "food ranking chart" format (recreate of @elevatemindhq's 7.4K-send post): 7–8 food columns per chart, value + serving above, label below, source line. `food_library/` holds 39 reusable food-column images (black background, gold rim light). Reel version animates the columns rising. Add new foods to the library with the same Higgsfield prompt (see `S` specs and the column() cropper). All numbers must come from USDA FoodData Central / NIH ODS / a cited study.
- `split_reel_animated_example.py` — turns a split carousel into a reel whose opening split MOVES: a 5s Kling 3.0 clip (generate_video, model kling3_0, mode std, duration 5, medias=[{role:"start_image", value:<still's job id>}]) is composited into the bottom half of slide 1, then the remaining slides play with slow zooms and crossfades, then the end card. Writes cover.png (slide 1) for the Reel cover.
