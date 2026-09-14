# deadlight-media

Menu artwork for the **DeadLight** Kodi add-on (`plugin.video.fenlight`).

DeadLight fetches its menu icons over HTTP at render time rather than bundling them,
so this repository has to stay public: Kodi requests these files from
`raw.githubusercontent.com` with no credentials.

## Why this exists

The add-on previously pulled icons from upstream Fen Light's site repo. That repo was
renamed and its `packages/media/` tree no longer exists, so **every icon URL returned
404**. Icons still appeared only because Kodi had them in its local texture cache; a
cache clear or a fresh install showed none. The shipped default in the add-on
(`FenlightAnonyMouse`) points at an account that does not exist at all.

## Layout

The paths mirror what `kodi_utils.get_icon()` builds:

```
https://raw.githubusercontent.com/pitou212/deadlight-media/main/packages/media/<folder>/<name>.<ext>
```

| Folder | Count | Used for |
|---|---|---|
| `packages/media/icons`   | 62 | menu rows, service entries, content-warning flags |
| `packages/media/flags`   |  4 | quality badges (4K / 1080 / 720 / SD) |
| `packages/media/results` |  3 | results-window layout glyphs |

## Design

One coherent system, unlike the mixed clipart it replaces.

- 512×512 PNG, transparent ground — matching what the add-on and skin expect
- Accent `#4CD8D0`, sampled from the DeadLight add-on icon
- Stroked geometry, round caps and joins, 34px stroke in the 512 design space
- Drawn at 4× and downsampled (LANCZOS), which is what keeps curves and diagonals clean

Third-party services (Trakt, TMDB, MDBList, Real-Debrid, …) get **letter badges**, not
imitations of their marks. Approximating someone else's logo would be worse than plainly
naming it, and the badge shape keeps the set consistent.

## Regenerating

Everything here is generated, not hand-drawn:

```
cd src && python icons.py      # writes ./out/{icons,flags,results}
```

Requires Pillow. `draw.py` is the drawing DSL; `icons.py` defines every glyph.
To change a glyph, edit its function and re-run — do not hand-edit the PNGs, they are
build output.

## Not included

`network_icons/` (TV network logos) and `rpdb_posters/` (RatingPosterDB sample posters)
are third-party images, not part of this set. They were already 404ing upstream, so
nothing regresses by their absence.
