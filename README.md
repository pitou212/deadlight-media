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
| `packages/media/icons`   | 120 | menu rows, service entries, content-warning flags, genre menus (`genre_*`) — teal |
| `packages/media/icons_white` | 120 | the same icons in white; **this is the folder DeadLight loads**. `python icons.py` writes the white copy of every glyph (same alpha, white RGB) |
| `packages/media/flags`   |  4 | quality badges (4K / 1080 / 720 / SD) |
| `packages/media/results` |  3 | results-window layout glyphs |
| `packages/media/network_icons` | 75 | TV Shows > Networks logos, named by the ids in DeadLight's `meta_lists.networks()` (copied from the imgur images those ids name) |
| `packages/media/studio_icons` | 40 | Anime > Studios logos, named by AniList studio id (`meta_lists.anime_studios()`); TMDb company logos, dark ones recoloured white for a dark background |

## Design

One coherent system, unlike the mixed clipart it replaces.

- 512×512 PNG, transparent ground — matching what the add-on and skin expect
- Accent `#4CD8D0`, sampled from the DeadLight add-on icon
- **Solid pictograms**: filled silhouettes with cut-out details, thin secondary lines (antennae, legs,
  handles), the glyph kept to about 60% of the canvas -- the look of the classic Fen Light set, all of
  it drawn here, nothing copied from it
- Drawn at 4× and downsampled (LANCZOS), which is what keeps curves and diagonals clean

Third-party services (Trakt, TMDB, MDBList, Real-Debrid, …) get **solid letter badges**, not
imitations of their marks. Approximating someone else's logo would be worse than plainly
naming it, and the badge shape keeps the set consistent.

## Regenerating

Everything here is generated, not hand-drawn:

```
cd src && python icons.py      # writes ./out/{icons,icons_white,flags,results}
```

Requires Pillow. `draw.py` is the drawing DSL (`Canvas.erase()` cuts the details out of a solid
shape); `solid.py` draws every glyph; `icons.py` is the registry and the build.
To change a glyph, edit its function and re-run — do not hand-edit the PNGs, they are
build output.

## Not included

`rpdb_posters/` (RatingPosterDB sample posters) is third-party and not part of this set.
`network_icons/` and `studio_icons/` are third-party logos too, copied here so DeadLight does
not depend on the hosts they came from (see the table above).
