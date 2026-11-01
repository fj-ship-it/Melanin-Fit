# MFM music library (branch `music-library`)

Theme music for @melaninfitmen reels. Instagram's music library can't be used on auto-posted reels, so every reel has a royalty-free instrumental baked in. To save vidIQ and Higgsfield credits, tracks are kept here and reused by theme.

- `library.json` lists the themes and every track: file, themes, where it came from, the prompt, length, good start points, and which posts used it.
- `tracks/` holds the audio (mp3/m4a/wav).

How the build uses it: for each post, pick the theme, use a library track for that theme (rotate tracks and start points; don't use the same track + start on both posts in a day). Only generate a new track (vidIQ first, Higgsfield if vidIQ blocks it) when a theme has fewer than 2 tracks, then add it here. Update `used_on` each build.

Adding Frank's older tracks: drop the file in `tracks/` named `<style>-<theme>-NN.<ext>` and add an entry to `library.json` (source "Frank upload").
