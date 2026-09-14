# -*- coding: utf-8 -*-
"""Minimal stroked-glyph drawing DSL for the DeadLight icon set.

Everything is drawn on a 4x supersampled canvas and downsampled with LANCZOS, which is
what gives the diagonals and curves clean edges. Coordinates are always expressed in a
512-unit design space regardless of the supersample factor.

Style rules, taken from the DeadLight addon icon (resources/media/addon_icons):
  * accent  #4CD8D0  (sampled: rgb 72,216,208)
  * stroked, not filled, with round caps and round joins
  * 512x512, transparent ground -- matches the upstream icons pulled out of Kodi's
    texture cache, which are 512x512 and 80-90% transparent
"""
from PIL import Image, ImageDraw, ImageFont
import math

SS = 4                       # supersample factor
SIZE = 512                   # design space / final size
ACCENT = (76, 216, 208)      # #4CD8D0
W = 34                       # default stroke weight in design units

FONTS = {
    'bold': 'C:/Windows/Fonts/segoeuib.ttf',
    'black': 'C:/Windows/Fonts/seguibl.ttf',
}


class Canvas:
    def __init__(self, color=ACCENT):
        self.n = SIZE * SS
        self.img = Image.new('RGBA', (self.n, self.n), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.color = color + (255,)

    # ---- primitives (design-space coords) ----
    def _s(self, v):
        return v * SS

    def _disc(self, x, y, r, fill=None):
        x, y, r = self._s(x), self._s(y), self._s(r)
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill or self.color)

    def path(self, pts, w=W, close=False, caps=True):
        """Polyline with round joins and round caps."""
        p = [(self._s(x), self._s(y)) for x, y in pts]
        if close:
            p = p + [p[0]]
        self.d.line(p, fill=self.color, width=int(self._s(w)), joint='curve')
        if caps or close:
            ends = p if close else [p[0], p[-1]]
            for x, y in ends:
                r = self._s(w) / 2.0
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=self.color)

    def poly(self, pts, fill=True, w=W):
        if fill:
            self.d.polygon([(self._s(x), self._s(y)) for x, y in pts], fill=self.color)
        else:
            self.path(pts, w=w, close=True)

    def circle(self, cx, cy, r, w=W, fill=False):
        if fill:
            self._disc(cx, cy, r)
            return
        x, y, rr = self._s(cx), self._s(cy), self._s(r)
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=self.color,
                       width=int(self._s(w)))

    def arc(self, cx, cy, r, a0, a1, w=W, caps=True):
        x, y, rr = self._s(cx), self._s(cy), self._s(r)
        self.d.arc([x - rr, y - rr, x + rr, y + rr], a0, a1, fill=self.color,
                   width=int(self._s(w)))
        if caps:
            for a in (a0, a1):
                ax = cx + r * math.cos(math.radians(a))
                ay = cy + r * math.sin(math.radians(a))
                self._disc(ax, ay, w / 2.0)

    def rrect(self, x0, y0, x1, y1, rad, w=W, fill=False):
        box = [self._s(x0), self._s(y0), self._s(x1), self._s(y1)]
        if fill:
            self.d.rounded_rectangle(box, radius=self._s(rad), fill=self.color)
        else:
            self.d.rounded_rectangle(box, radius=self._s(rad), outline=self.color,
                                     width=int(self._s(w)))

    def dot(self, x, y, r):
        self._disc(x, y, r)

    def text(self, s, cx, cy, size, font='black', spacing=0):
        f = ImageFont.truetype(FONTS[font], int(self._s(size)))
        if spacing:
            # manual tracking
            widths = [self.d.textlength(ch, font=f) for ch in s]
            total = sum(widths) + self._s(spacing) * (len(s) - 1)
            x = self._s(cx) - total / 2.0
            asc, desc = f.getmetrics()
            y = self._s(cy) - (asc - desc) / 2.0
            for ch, wdt in zip(s, widths):
                self.d.text((x, y), ch, font=f, fill=self.color)
                x += wdt + self._s(spacing)
        else:
            self.d.text((self._s(cx), self._s(cy)), s, font=f, fill=self.color,
                        anchor='mm')

    def star(self, cx, cy, r_out, r_in, points=5, rot=-90):
        pts = []
        for i in range(points * 2):
            a = math.radians(rot + i * 180.0 / points)
            r = r_out if i % 2 == 0 else r_in
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.poly(pts, fill=True)

    def sparkle(self, cx, cy, r, waist=0.30):
        """Four-point concave star -- the 'shine' motif."""
        k = r * waist
        pts = []
        for i in range(4):
            a = math.radians(-90 + i * 90)
            b = a + math.radians(45)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            pts.append((cx + k * math.cos(b), cy + k * math.sin(b)))
        self.poly(pts, fill=True)

    def save(self, path):
        out = self.img.resize((SIZE, SIZE), Image.LANCZOS)
        out.save(path)
        return out


def badge_text(label, size=None, font='black', spacing=0, pad=None):
    """A rounded-rect badge with a letterform inside -- used for third-party service
    names and quality flags. Deliberately a letter badge rather than an imitation of
    someone else's logo: approximating a brand mark would be worse than naming it."""
    c = Canvas()
    x0, y0, x1, y1 = 40, 128, 472, 384
    c.rrect(x0, y0, x1, y1, 56, w=W)
    n = len(label)
    if size is None:
        size = {1: 190, 2: 160, 3: 118, 4: 92, 5: 76}.get(n, 68)
    c.text(label, (x0 + x1) / 2.0, (y0 + y1) / 2.0 - 4, size, font=font, spacing=spacing)
    return c
