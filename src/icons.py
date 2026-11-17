# -*- coding: utf-8 -*-
"""The DeadLight icon set: the registry and the build.

Every glyph is drawn in solid.py (the solid pictogram style, 2026-11-17). Third-party services get LETTER BADGES
rather than imitations of their marks: an approximation of someone else's logo is worse than plainly naming it, and
the badge shape keeps the set visually consistent.

    python icons.py      # writes ./out/{icons,icons_white,flags,results}
"""
import os
from solid import SOLID, FLAGS, RESULTS

OUT = os.path.join(os.path.dirname(__file__), 'out')

ICONS = {'icons': SOLID, 'flags': FLAGS, 'results': RESULTS}


def whiten(img):
    """icons_white, the folder DeadLight loads: the same alpha with white RGB (as the set was first made, b278809)."""
    alpha = img.getchannel('A')
    out = img.copy()
    out.paste((255, 255, 255, 255), (0, 0) + img.size)
    out.putalpha(alpha)
    return out


if __name__ == '__main__':
    n = 0
    white = os.path.join(OUT, 'icons_white')
    os.makedirs(white, exist_ok=True)
    for folder, items in ICONS.items():
        d = os.path.join(OUT, folder)
        os.makedirs(d, exist_ok=True)
        for name, fn in items.items():
            img = fn().save(os.path.join(d, name + '.png'))
            if folder == 'icons':
                whiten(img).save(os.path.join(white, name + '.png'))
            n += 1
    print('rendered %d icons across %d folders (+ icons_white)' % (n, len(ICONS)))
