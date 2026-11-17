# -*- coding: utf-8 -*-
"""The DeadLight icon set.

One coherent system, unlike the upstream set it replaces (which was mixed clipart --
some glyphs, some rasterised brand logos, some screenshots of rating cards).

Third-party services get LETTER BADGES rather than imitations of their marks: an
approximation of someone else's logo is worse than plainly naming it, and the badge
shape keeps the set visually consistent.
"""
import os
import math
from PIL import ImageDraw
from draw import Canvas, badge_text, W

OUT = os.path.join(os.path.dirname(__file__), 'out')


# ---------------------------------------------------------------- shared motifs
def _punch(c, cx, cy, r):
    """Erase a disc -- used to hollow filled silhouettes (gear centre, disc hub)."""
    s = c.n / 512.0
    ImageDraw.Draw(c.img).ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s],
                                  fill=(0, 0, 0, 0))


def _arrow(c, tip, ang, size=52, w=W):
    a = math.radians(ang)
    for d in (140, -140):
        b = a + math.radians(d)
        c.path([tip, (tip[0] + size * math.cos(b), tip[1] + size * math.sin(b))], w=w)


def _clock(c, cx, cy, r, w=26):
    c.circle(cx, cy, r, w=w)
    c.path([(cx, cy - r * 0.55), (cx, cy)], w=w)
    c.path([(cx, cy), (cx + r * 0.5, cy)], w=w)


def _lens_pts(cx, cy, rx, ry, rot=0.0, n=36):
    """Closed pointed-lens outline, built from two mirrored circular arcs and rotated.
    The arc geometry is what gives genuinely pointed tips -- an ellipse gives blunt
    ones, which reads as a seed rather than a leaf, and as a rhombus rather than an eye."""
    r = (rx * rx + ry * ry) / (2.0 * ry)
    d = r - ry
    span = math.degrees(math.asin(min(1.0, rx / r)))
    pts = []
    for i in range(n + 1):
        a = math.radians(270 - span + (2 * span) * i / n)
        pts.append((r * math.cos(a), d + r * math.sin(a)))
    for i in range(n + 1):
        a = math.radians(90 + span - (2 * span) * i / n)
        pts.append((r * math.cos(a), -d + r * math.sin(a)))
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def _eye(c, cx, cy, rx, ry, w=W):
    c.path(_lens_pts(cx, cy, rx, ry), w=w, close=True)
    c.circle(cx, cy, ry * 0.42, w=w * 0.8)


def _flame(c):
    c.path([(256, 96), (340, 206), (322, 236), (368, 300)], w=W)
    c.arc(256, 310, 136, -34, 214, w=W, caps=False)
    c.path([(256, 96), (176, 210), (196, 246), (148, 300)], w=W)


def _tv_body(c, top=120, bot=356):
    c.rrect(72, top, 440, bot, 36, w=W)
    c.path([(196, bot + 48), (316, bot + 48)], w=W)
    c.path([(256, bot), (256, bot + 48)], w=W)


def _person(c, cx=256, cy=236, r=78):
    c.circle(cx, cy, r, w=W)
    c.arc(cx, cy + 250, 176, 203, 337, w=W, caps=False)


# ---------------------------------------------------------------- content icons
def movies():
    c = Canvas()
    c.rrect(88, 128, 424, 384, 34, w=W)
    for y in (170, 246, 322):
        c.rrect(120, y - 20, 168, y + 20, 12, fill=True)
        c.rrect(344, y - 20, 392, y + 20, 12, fill=True)
    c.path([(216, 196), (216, 316), (312, 256)], w=W, close=True)
    return c


def tvshows():
    c = Canvas(); _tv_body(c); return c


def tv():
    c = Canvas(); _tv_body(c, top=176, bot=396)
    c.path([(256, 176), (176, 92)], w=W)
    c.path([(256, 176), (336, 92)], w=W)
    return c


def anime():
    c = Canvas()
    c.sparkle(232, 224, 168)
    c.sparkle(386, 352, 78)
    c.sparkle(132, 372, 54)
    return c


def search():
    c = Canvas(); c.circle(226, 226, 124, w=W); c.path([(318, 318), (410, 410)], w=W); return c


def settings2():
    c = Canvas()
    teeth, r_out, r_in = 8, 196, 150
    half = math.radians(360.0 / teeth / 4.0)
    pts = []
    for i in range(teeth):
        a = math.radians(i * 360.0 / teeth)
        for r, off in ((r_out, -half), (r_out, half), (r_in, half * 1.9),
                       (r_in, -half * 1.9 + math.radians(360.0 / teeth))):
            pts.append((256 + r * math.cos(a + off), 256 + r * math.sin(a + off)))
    c.poly(pts, fill=True)
    _punch(c, 256, 256, 74)
    return c


def favorites():
    c = Canvas(); c.star(256, 262, 176, 76); return c


def downloads():
    c = Canvas()
    c.path([(256, 104), (256, 300)], w=W)
    c.path([(160, 214), (256, 310), (352, 214)], w=W)
    c.path([(112, 360), (112, 412), (400, 412), (400, 360)], w=W)
    return c


def trending():
    c = Canvas()
    c.path([(96, 352), (208, 240), (288, 320), (416, 176)], w=W)
    c.path([(416, 264), (416, 176), (328, 176)], w=W)
    return c


def trending_recent():
    c = Canvas()
    c.path([(74, 330), (176, 228), (248, 300), (356, 192)], w=W)
    c.path([(356, 268), (356, 192), (280, 192)], w=W)
    _clock(c, 378, 372, 82, w=24)
    return c


def calender():
    c = Canvas()
    c.rrect(80, 128, 432, 424, 34, w=W)
    c.path([(80, 212), (432, 212)], w=W, caps=False)
    c.path([(168, 84), (168, 160)], w=W)
    c.path([(344, 84), (344, 160)], w=W)
    for r in (282, 360):
        for cx in (168, 256, 344):
            c.dot(cx, r, 22)
    return c


def calendar_decades():
    c = Canvas()
    c.path([(140, 92), (404, 92)], w=W)
    c.path([(120, 150), (424, 150)], w=W)
    c.rrect(88, 200, 424, 428, 32, w=W)
    c.path([(88, 272), (424, 272)], w=W, caps=False)
    c.text('10', 256, 356, 104, font='black')
    return c


def random():
    c = Canvas()
    c.path([(96, 176), (176, 176), (330, 336), (400, 336)], w=W)
    c.path([(96, 336), (176, 336), (330, 176), (400, 176)], w=W)
    _arrow(c, (400, 176), 0); _arrow(c, (400, 336), 0)
    return c


def live():
    c = Canvas()
    c.dot(256, 256, 52)
    c.arc(256, 256, 126, -52, 52, w=W, caps=False)
    c.arc(256, 256, 126, 128, 232, w=W, caps=False)
    c.arc(256, 256, 200, -46, 46, w=W, caps=False)
    c.arc(256, 256, 200, 134, 226, w=W, caps=False)
    return c


def player():
    c = Canvas(); c.circle(256, 256, 176, w=W)
    c.poly([(214, 172), (214, 340), (346, 256)], fill=True); return c


def folder():
    c = Canvas()
    c.path([(72, 388), (72, 152), (212, 152), (256, 208), (440, 208), (440, 388)],
           w=W, close=True)
    return c


def lists():
    c = Canvas()
    for y in (168, 256, 344):
        c.dot(120, y, 26)
        c.path([(196, y), (416, y)], w=W)
    return c


def genres():
    c = Canvas()
    c.path([(96, 256), (248, 104), (416, 104), (416, 272), (264, 424), (96, 256)], w=W, close=True)
    c.circle(346, 174, 32, w=26)
    return c


def languages():
    c = Canvas()
    c.circle(256, 256, 176, w=W)
    c.path([(80, 256), (432, 256)], w=W)
    for k in (0.52, 1.0):
        c.arc(256, 256, 176, 0, 360, w=0)  # no-op guard
    c.d.ellipse([(256 - 92) * 4, (256 - 176) * 4, (256 + 92) * 4, (256 + 176) * 4],
                outline=c.color, width=int(W * 4 * 0.8))
    return c


def discover():
    c = Canvas()
    c.circle(256, 256, 176, w=W)
    c.poly([(330, 182), (286, 286), (182, 330), (226, 226)], fill=True)
    return c


def providers():
    c = Canvas()
    c.arc(212, 268, 96, 180, 360, w=W, caps=False)
    c.arc(312, 250, 74, 200, 350, w=W, caps=False)
    c.path([(116, 268), (116, 336), (396, 336), (396, 250)], w=W)
    return c


def networks():
    c = Canvas()
    c.circle(256, 140, 54, w=26)
    for cx in (124, 256, 388):
        c.circle(cx, 384, 54, w=26)
        c.path([(256, 194), (cx, 330)], w=24)
    return c


def box_office():
    """Ticket stub: notched sides and a perforation."""
    c = Canvas()
    c.path([(96, 170), (416, 170)], w=W)
    c.path([(96, 342), (416, 342)], w=W)
    for x in (96, 416):
        c.path([(x, 170), (x, 214)], w=W)
        c.path([(x, 298), (x, 342)], w=W)
    c.arc(96, 256, 44, -90, 90, w=W, caps=False)
    c.arc(416, 256, 44, 90, 270, w=W, caps=False)
    for y in (196, 246, 296):
        c.path([(256, y), (256, y + 22)], w=22)
    return c


def intheatres():
    """Screen over seat backs."""
    c = Canvas()
    c.rrect(84, 96, 428, 276, 22, w=W)
    c.path([(256, 276), (256, 318)], w=24)
    c.arc(160, 430, 74, 190, 350, w=W, caps=False)
    c.arc(352, 430, 74, 190, 350, w=W, caps=False)
    c.path([(86, 430), (426, 430)], w=W)
    c.path([(150, 150), (362, 150)], w=22)
    c.path([(178, 210), (334, 210)], w=22)
    return c


def ontheair():
    c = Canvas()
    c.path([(190, 412), (256, 196), (322, 412)], w=W)
    c.path([(214, 336), (298, 336)], w=W)
    c.arc(256, 196, 108, 200, 250, w=26, caps=False)
    c.arc(256, 196, 108, 290, 340, w=26, caps=False)
    c.arc(256, 196, 168, 206, 244, w=26, caps=False)
    c.arc(256, 196, 168, 296, 334, w=26, caps=False)
    c.dot(256, 196, 34)
    return c


def next_episodes():
    c = Canvas()
    c.poly([(120, 148), (120, 364), (288, 256)], fill=True)
    c.rrect(320, 148, 380, 364, 28, fill=True)
    return c


def nextpage():
    c = Canvas(); c.path([(196, 120), (344, 256), (196, 392)], w=44); return c


def nextpage_landscape():
    c = Canvas()
    c.path([(140, 132), (272, 256), (140, 380)], w=42)
    c.path([(268, 132), (400, 256), (268, 380)], w=42)
    return c


def item_jump_landscape():
    c = Canvas()
    c.path([(96, 256), (336, 256)], w=W)
    _arrow(c, (336, 256), 0, size=62)
    c.path([(408, 132), (408, 380)], w=W)
    return c


def in_progress_tvshow():
    c = Canvas()
    c.rrect(72, 120, 440, 356, 36, w=W)
    c.path([(196, 404), (316, 404)], w=W)
    c.path([(256, 356), (256, 404)], w=W)
    c.path([(136, 292), (376, 292)], w=24)
    c.path([(136, 292), (272, 292)], w=44)
    return c


def watched_1():
    c = Canvas()
    c.circle(256, 256, 176, w=W)
    c.path([(168, 260), (228, 320), (352, 196)], w=W)
    return c


def watched_recent():
    c = Canvas()
    c.circle(232, 232, 150, w=W)
    c.path([(156, 236), (208, 288), (312, 184)], w=W)
    _clock(c, 384, 384, 82, w=24)
    return c


def most_watched():
    c = Canvas(); _eye(c, 256, 256, 190, 108); return c


def most_voted():
    c = Canvas()
    c.path([(196, 236), (268, 108), (300, 128), (272, 224), (404, 224), (388, 396),
            (196, 396)], w=W, close=True)
    c.rrect(92, 232, 168, 404, 22, w=W)
    return c


def popular():
    c = Canvas(); _flame(c); return c


def popular_today():
    c = Canvas()
    c.path([(230, 88), (306, 190), (290, 218), (330, 276)], w=W)
    c.arc(230, 288, 124, -34, 214, w=W, caps=False)
    c.path([(230, 88), (158, 194), (176, 228), (132, 278)], w=W)
    _clock(c, 388, 382, 76, w=24)
    return c


def premium():
    c = Canvas()
    c.path([(88, 372), (124, 152), (256, 268), (388, 152), (424, 372)], w=W, close=True)
    return c


def top():
    c = Canvas()
    c.rrect(84, 288, 172, 412, 18, w=W)
    c.rrect(212, 180, 300, 412, 18, w=W)
    c.rrect(340, 248, 428, 412, 18, w=W)
    c.star(256, 112, 58, 24)
    return c


def fresh():
    """Sprout: stem plus two pointed leaves with midribs."""
    c = Canvas()
    c.path([(256, 440), (256, 268)], w=W)
    c.path(_lens_pts(320, 196, 118, 62, rot=-38), w=W, close=True)
    c.path([(240, 258), (386, 140)], w=22)
    c.path(_lens_pts(176, 286, 92, 50, rot=34), w=W, close=True)
    c.path([(256, 330), (110, 246)], w=22)
    return c


def new():
    return badge_text('NEW', size=112)


def dvd():
    c = Canvas()
    c.circle(256, 256, 180, w=W)
    c.circle(256, 256, 52, w=W)
    c.arc(256, 256, 118, 200, 290, w=W, caps=False)
    return c


def empty_person():
    c = Canvas(); _person(c); return c


def people():
    """Two figures, the back one smaller and offset -- Search People, Images."""
    c = Canvas()
    _person(c, cx=344, cy=176, r=56)
    # the front figure hides what is behind it: a gap round its head, and everything under its shoulders
    _punch(c, 214, 262, 96)
    _punch(c, 214, 262 + 250, 198)
    _person(c, cx=214, cy=262, r=74)
    return c


def tv_anime():
    """The TV with the anime sparkle on screen -- Search TV Show & Anime."""
    c = Canvas(); _tv_body(c)
    c.sparkle(256, 238, 84)
    return c


def information():
    c = Canvas(); c.circle(256, 256, 180, w=W)
    c.dot(256, 168, 24)
    c.path([(256, 236), (256, 360)], w=W)
    return c


def updates():
    """Two chasing arrows round a circle -- the updater rows (the add-on asks for 'github')."""
    # Pillow strokes an arc INWARD from its box, so the line's centre is r - W/2: tips and the tail caps go there
    # (Canvas.arc's own caps sit at r, half a stroke outside).
    c, r = Canvas(), 170
    mid = r - W / 2.0
    at = lambda a: (256 + mid * math.cos(math.radians(a)), 256 + mid * math.sin(math.radians(a)))
    for a0, a1 in ((200, 330), (20, 150)):
        c.arc(256, 256, r, a0, a1, w=W, caps=False)
        c.dot(*at(a0), W / 2.0)
        _arrow(c, at(a1), a1 + 90, size=60)   # clockwise: the tangent at a1 points a1 + 90
    return c


def because_you_watched():
    c = Canvas(); _eye(c, 240, 240, 176, 100); c.sparkle(408, 400, 66); return c


def oscar_winners():
    c = Canvas()
    c.circle(256, 208, 132, w=W)
    c.path([(176, 314), (140, 444), (256, 388), (372, 444), (336, 314)], w=W, close=True)
    return c


def certifications():
    c = Canvas()
    c.path([(256, 76), (420, 148), (420, 268), (256, 436), (92, 268), (92, 148)],
           w=W, close=True)
    c.path([(180, 246), (238, 304), (340, 202)], w=W)
    return c


def audio():
    c = Canvas()
    c.path([(96, 200), (168, 200), (252, 124), (252, 388), (168, 312), (96, 312)],
           w=W, close=True)
    c.arc(268, 256, 96, -54, 54, w=26, caps=False)
    c.arc(268, 256, 156, -48, 48, w=26, caps=False)
    return c


def fenlight():
    """The DeadLight mark itself: bulb outline + the double-peak 'M'."""
    c = Canvas()
    c.circle(256, 214, 140, w=W)
    c.path([(186, 268), (224, 176), (256, 244), (288, 176), (326, 268)], w=W)
    c.path([(206, 356), (306, 356)], w=W)
    for y in (390, 424):
        c.path([(212, y), (300, y)], w=26)
    return c


# ---------------------------------------------------------------- content warnings
def bad_language():
    c = Canvas()
    c.rrect(72, 120, 440, 336, 40, w=W)
    c.path([(176, 336), (176, 424), (256, 336)], w=W, close=True)
    c.text('#*!', 256, 224, 108, font='black', spacing=6)
    return c


def drugs_alcohol():
    c = Canvas()
    c.path([(132, 128), (380, 128), (256, 276), (132, 128)], w=W, close=True)
    c.path([(256, 276), (256, 396)], w=W)
    c.path([(176, 408), (336, 408)], w=W)
    return c


def horror():
    """Skull: domed cranium over a narrower jaw."""
    c = Canvas()
    c.arc(256, 236, 150, 180, 360, w=W, caps=False)
    for x in (106, 406):
        c.path([(x, 236), (x, 300)], w=W)
    c.path([(106, 300), (176, 300)], w=W)
    c.path([(336, 300), (406, 300)], w=W)
    c.path([(176, 300), (176, 372)], w=W)
    c.path([(336, 300), (336, 372)], w=W)
    c.arc(256, 372, 80, 0, 180, w=W, caps=False)
    c.dot(196, 232, 42); c.dot(316, 232, 42)
    c.path([(256, 286), (238, 316), (274, 316)], w=20, close=True)
    return c


def sex_nudity():
    c = Canvas()
    c.arc(190, 212, 92, 180, 360, w=W, caps=False)
    c.arc(322, 212, 92, 180, 360, w=W, caps=False)
    c.path([(98, 212), (256, 400), (414, 212)], w=W)
    return c


def violence():
    c = Canvas()
    pts = []
    for i in range(12):
        a = math.radians(-90 + i * 30)
        r = 194 if i % 2 == 0 else 108
        pts.append((256 + r * math.cos(a), 256 + r * math.sin(a)))
    c.poly(pts, fill=False, w=W)
    return c


# ---------------------------------------------------------------- genres (Movies / TV / Anime > Genres)
# Named as DeadLight's meta_lists.*_genres() name them (genre_<icon>); 'TV Movie' reuses genre_soap.
def _ellipse_pts(cx, cy, rx, ry, rot=0.0, n=72):
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def _curve(c, cx, cy, r, a0, a1, w=W, n=24):
    """A short arc as a polyline: Pillow's thick arc() breaks into beads at small radii."""
    c.path([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)], w=w)


def _small_person(c, cx, cy, r):
    """_person scaled: head of radius r, shoulders below it."""
    c.circle(cx, cy, r, w=W)
    c.arc(cx, cy + r * 3.2, r * 2.25, 203, 337, w=W, caps=False)


def genre_action():
    """Lightning bolt."""
    c = Canvas()
    c.path([(292, 72), (148, 284), (246, 284), (214, 440), (366, 214), (268, 214)], w=W, close=True)
    return c


def genre_adventure():
    """Compass: ring and a tilted needle."""
    c = Canvas()
    c.circle(256, 256, 184, w=W)
    a = math.radians(40)
    tip = lambda r, ang: (256 + r * math.cos(ang), 256 + r * math.sin(ang))
    north = [tip(122, a - math.pi / 2), tip(34, a), tip(34, a + math.pi)]
    south = [tip(122, a + math.pi / 2), tip(34, a), tip(34, a + math.pi)]
    c.poly(north, fill=True)
    c.poly(south, fill=False, w=22)
    return c


def genre_animation():
    """Bouncing ball with motion lines."""
    c = Canvas()
    c.circle(318, 262, 112, w=W)
    _curve(c, 318, 262, 66, 200, 265, w=22)
    for y, x0 in ((196, 96), (262, 72), (328, 96)):
        c.path([(x0, y), (x0 + 80, y)], w=W)
    c.path([(206, 418), (430, 418)], w=W)
    return c


def genre_comedy():
    """Laughing face: closed eyes, wide smile."""
    c = Canvas()
    c.circle(256, 256, 184, w=W)
    _curve(c, 196, 226, 34, 200, 340, w=26)
    _curve(c, 316, 226, 34, 200, 340, w=26)
    _curve(c, 256, 276, 96, 20, 160, w=W)
    return c


def genre_crime():
    """Handcuffs: two cuffs joined by a link."""
    c = Canvas()
    c.circle(158, 318, 92, w=W)
    c.circle(354, 318, 92, w=W)
    c.circle(214, 176, 28, w=22)
    c.circle(298, 176, 28, w=22)
    c.path([(242, 176), (270, 176)], w=22)
    c.path([(196, 200), (176, 228)], w=22)
    c.path([(316, 200), (336, 228)], w=22)
    return c


def genre_documentary():
    """Film camera: body and lens hood."""
    c = Canvas()
    c.rrect(64, 192, 330, 384, 30, w=W)
    c.path([(330, 288), (444, 212), (444, 364)], w=W, close=True)
    c.circle(132, 132, 52, w=W)
    c.circle(258, 132, 52, w=W)
    return c


def genre_drama():
    """Tragedy mask: shield face, slanted eyes, downturned mouth."""
    c = Canvas()
    c.path([(116, 104), (396, 104), (396, 246)], w=W)
    c.path([(116, 104), (116, 246)], w=W)
    c.arc(256, 246, 140, 0, 180, w=W, caps=False)
    c.poly(_lens_pts(196, 204, 40, 16, rot=12), fill=True)
    c.poly(_lens_pts(316, 204, 40, 16, rot=-12), fill=True)
    _curve(c, 256, 338, 46, 215, 325, w=W)
    return c


def genre_family():
    """Two adults and a child, side by side (short shoulders so the three never touch)."""
    c = Canvas()
    for cx, cy, r, sr, hw in ((124, 160, 46, 96, W), (388, 160, 46, 96, W), (256, 300, 34, 70, 26)):
        c.circle(cx, cy, r, w=hw)
        _curve(c, cx, cy + r + sr + 18, sr, 215, 325, w=W)
    return c


def genre_fantasy():
    """Wizard hat with a star."""
    c = Canvas()
    c.path([(160, 372), (268, 92), (352, 372)], w=W)
    c.path([(84, 388), (428, 388)], w=W)
    c.sparkle(130, 150, 62)
    c.sparkle(392, 210, 40)
    return c


def genre_history():
    """Classical temple front."""
    c = Canvas()
    c.path([(84, 176), (256, 88), (428, 176)], w=W, close=True)
    for x in (148, 256, 364):
        c.path([(x, 222), (x, 360)], w=W)
    c.path([(96, 404), (416, 404)], w=W)
    return c


def genre_music():
    """Two beamed eighth notes."""
    c = Canvas()
    c.dot(170, 370, 50)
    c.dot(354, 336, 50)
    c.path([(206, 370), (206, 146)], w=W)
    c.path([(390, 336), (390, 112)], w=W)
    c.poly([(189, 129), (407, 95), (407, 151), (189, 185)], fill=True)
    return c


def genre_mystery():
    """Magnifier over a question mark."""
    c = Canvas()
    c.circle(224, 224, 136, w=W)
    c.path([(322, 322), (416, 416)], w=W + 8)
    c.text('?', 224, 222, 170, font='black')
    return c


def genre_romance():
    """Heart with a shine."""
    c = Canvas()
    c.arc(184, 214, 88, 150, 360, w=W, caps=False)
    c.arc(328, 214, 88, 180, 30, w=W, caps=False)
    c.path([(108, 258), (256, 410), (404, 258)], w=W)
    c.sparkle(392, 108, 50)
    return c


def genre_scifi():
    """Ringed planet."""
    c = Canvas()
    c.circle(256, 256, 116, w=W)
    c.path(_ellipse_pts(256, 256, 222, 62, rot=-22), w=W - 6, close=True)
    c.dot(410, 110, 14)
    c.dot(96, 400, 10)
    return c


def genre_soap():
    """Bubbles."""
    c = Canvas()
    c.circle(196, 300, 118, w=W)
    c.circle(356, 182, 72, w=W)
    c.circle(362, 384, 40, w=W)
    _curve(c, 196, 300, 74, 200, 262, w=22)
    return c


def genre_thriller():
    """Hourglass."""
    c = Canvas()
    c.path([(132, 92), (380, 92)], w=W)
    c.path([(132, 420), (380, 420)], w=W)
    c.path([(164, 92), (164, 150), (256, 256), (164, 362), (164, 420)], w=W)
    c.path([(348, 92), (348, 150), (256, 256), (348, 362), (348, 420)], w=W)
    c.poly([(210, 392), (302, 392), (256, 340)], fill=True)
    return c


def genre_war():
    """Crossed swords."""
    c = Canvas()
    for (x0, y0, x1, y1) in ((104, 104, 380, 380), (408, 104, 132, 380)):
        c.path([(x0, y0), (x1, y1)], w=W)
    c.path([(318, 404), (404, 318)], w=W)
    c.path([(108, 318), (194, 404)], w=W)
    c.dot(418, 418, 26)
    c.dot(94, 418, 26)
    return c


def genre_western():
    """Cowboy hat."""
    c = Canvas()
    c.path([(56, 286), (112, 334), (256, 356), (400, 334), (456, 286)], w=W)
    c.path([(152, 326), (172, 160), (222, 178), (256, 148), (290, 178), (340, 160), (360, 326)], w=W)
    c.path([(166, 272), (346, 272)], w=W - 8)
    return c


def genre_kids():
    """Balloon on a string."""
    c = Canvas()
    c.path(_ellipse_pts(256, 196, 116, 136), w=W, close=True)
    c.poly([(256, 330), (232, 362), (280, 362)], fill=True)
    c.path([(256, 362), (226, 404), (270, 436), (244, 470)], w=22)
    return c


def genre_news():
    """Newspaper: masthead block and columns."""
    c = Canvas()
    c.rrect(84, 104, 428, 408, 30, w=W)
    c.rrect(132, 150, 380, 206, 10, fill=True)
    for y in (264, 316, 368):
        c.path([(136, y), (236, y)], w=24)
    c.rrect(280, 250, 380, 372, 10, w=22)
    return c


def genre_reality():
    """A person framed by camera viewfinder corners."""
    c = Canvas()
    for (x, y, dx, dy) in ((84, 104, 1, 1), (428, 104, -1, 1), (84, 408, 1, -1), (428, 408, -1, -1)):
        c.path([(x, y + 70 * dy), (x, y), (x + 70 * dx, y)], w=W)
    _small_person(c, 256, 220, 58)
    c.dot(388, 150, 16)
    return c


def genre_talk():
    """Two speech bubbles."""
    c = Canvas()
    c.rrect(56, 88, 312, 252, 40, w=W)
    c.path([(112, 252), (104, 312), (168, 252)], w=W)
    c.rrect(200, 236, 456, 400, 40, w=W)
    c.path([(400, 400), (408, 460), (344, 400)], w=W)
    return c


# AniList's anime genres (DeadLight anilist_api.ANILIST_GENRES) that no TMDb genre covers.
def genre_ecchi():
    """Blushing face: winking eyes, hatched cheeks."""
    c = Canvas()
    c.circle(256, 256, 184, w=W)
    _curve(c, 196, 228, 30, 200, 340, w=26)
    c.path([(292, 212), (338, 228), (292, 244)], w=24)
    for cx in (164, 348):
        for dx in (-26, 0, 26):
            c.path([(cx + dx - 8, 312), (cx + dx + 8, 284)], w=16)
    _curve(c, 256, 300, 40, 30, 150, w=24)
    return c


def genre_hentai():
    """18+ in a ring."""
    c = Canvas()
    c.circle(256, 256, 184, w=W)
    c.text('18+', 256, 252, 150, font='black')
    return c


def genre_mahou_shoujo():
    """Magic wand: star on a staff, with sparkles."""
    c = Canvas()
    c.path([(108, 420), (262, 266)], w=W)
    star = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = 104 if i % 2 == 0 else 46
        star.append((320 + r * math.cos(a), 206 + r * math.sin(a)))
    c.poly(star, fill=False, w=26)
    c.sparkle(140, 140, 46)
    c.sparkle(424, 376, 36)
    return c


def genre_mecha():
    """Robot head: helmet, visor, antenna, jaw vents."""
    c = Canvas()
    c.rrect(116, 150, 396, 404, 46, w=W)
    c.rrect(160, 214, 352, 278, 24, fill=True)
    c.path([(256, 150), (256, 88)], w=W)
    c.dot(256, 76, 26)
    for x in (204, 256, 308):
        c.path([(x, 326), (x, 358)], w=22)
    c.path([(116, 260), (76, 260)], w=W)
    c.path([(396, 260), (436, 260)], w=W)
    return c


def genre_psychological():
    """Spiral."""
    c = Canvas()
    pts, turns, n = [], 2.75, 240
    for i in range(n + 1):
        t = i / float(n)
        a = 2 * math.pi * turns * t
        r = 30 + 156 * t
        pts.append((256 + r * math.cos(a), 256 + r * math.sin(a)))
    c.path(pts, w=28)
    return c


def genre_slice_of_life():
    """Cup of tea with steam."""
    c = Canvas()
    c.path([(104, 228), (128, 384), (152, 412), (312, 412), (336, 384), (360, 228)], w=W, close=True)
    _curve(c, 376, 302, 54, -80, 80, w=W)
    for x in (178, 254, 330):
        c.path([(x, 172), (x - 18, 142), (x, 112), (x - 18, 82)], w=22)
    return c


def genre_sports():
    """Ball with seams."""
    c = Canvas()
    c.circle(256, 256, 184, w=W)
    c.path([(256, 96), (256, 416)], w=26)
    c.path([(96, 256), (416, 256)], w=26)
    _curve(c, 40, 256, 152, -48, 48, w=26)
    _curve(c, 472, 256, 152, 132, 228, w=26)
    return c


def genre_supernatural():
    """Ghost: domed body, wavy hem, hollow eyes."""
    c = Canvas()
    body = [(256 + 140 * math.cos(math.radians(a)), 212 + 140 * math.sin(math.radians(a))) for a in range(180, 361, 6)]
    body += [(396, 420), (350, 384), (303, 420), (256, 384), (209, 420), (162, 384), (116, 420)]
    c.path(body, w=W, close=True)
    c.path(_ellipse_pts(208, 222, 22, 34), w=20, close=True)
    c.path(_ellipse_pts(304, 222, 22, 34), w=20, close=True)
    return c


GENRES = {
    'genre_action': genre_action, 'genre_adventure': genre_adventure, 'genre_animation': genre_animation,
    'genre_comedy': genre_comedy, 'genre_crime': genre_crime, 'genre_documentary': genre_documentary,
    'genre_drama': genre_drama, 'genre_family': genre_family, 'genre_fantasy': genre_fantasy,
    'genre_history': genre_history, 'genre_horror': horror, 'genre_kids': genre_kids, 'genre_music': genre_music,
    'genre_mystery': genre_mystery, 'genre_news': genre_news, 'genre_reality': genre_reality,
    'genre_romance': genre_romance, 'genre_scifi': genre_scifi, 'genre_soap': genre_soap, 'genre_talk': genre_talk,
    'genre_thriller': genre_thriller, 'genre_war': genre_war, 'genre_western': genre_western,
    'genre_ecchi': genre_ecchi, 'genre_hentai': genre_hentai, 'genre_mahou_shoujo': genre_mahou_shoujo,
    'genre_mecha': genre_mecha, 'genre_psychological': genre_psychological,
    'genre_slice_of_life': genre_slice_of_life, 'genre_sports': genre_sports,
    'genre_supernatural': genre_supernatural,
}


# ---------------------------------------------------------------- results layouts
def results_list():
    c = Canvas()
    for y in (150, 256, 362):
        c.rrect(88, y - 34, 424, y + 34, 18, w=26)
    return c


def results_row():
    c = Canvas()
    c.rrect(88, 176, 424, 336, 22, w=26)
    c.path([(140, 256), (372, 256)], w=24)
    return c


def results_widelist():
    c = Canvas()
    for y in (150, 256, 362):
        c.rrect(88, y - 34, 424, y + 34, 18, w=26)
        c.rrect(104, y - 20, 168, y + 20, 10, fill=True)
    return c


# ---------------------------------------------------------------- registry
ICONS = {
    'icons': {
        'movies': movies, 'tvshows': tvshows, 'tv': tv, 'anime': anime, 'search': search,
        'settings2': settings2, 'favorites': favorites, 'downloads': downloads,
        'trending': trending, 'trending_recent': trending_recent, 'calender': calender,
        'calendar_decades': calendar_decades, 'random': random, 'live': live,
        'player': player, 'folder': folder, 'lists': lists, 'genres': genres,
        'languages': languages, 'discover': discover, 'providers': providers,
        'networks': networks, 'box_office': box_office, 'intheatres': intheatres,
        'ontheair': ontheair, 'next_episodes': next_episodes, 'nextpage': nextpage,
        'nextpage_landscape': nextpage_landscape,
        'item_jump_landscape': item_jump_landscape,
        'in_progress_tvshow': in_progress_tvshow, 'watched_1': watched_1,
        'watched_recent': watched_recent, 'most_watched': most_watched,
        'most_voted': most_voted, 'popular': popular, 'popular_today': popular_today,
        'premium': premium, 'top': top, 'fresh': fresh, 'new': new, 'dvd': dvd,
        'empty_person': empty_person, 'because_you_watched': because_you_watched,
        'oscar_winners': oscar_winners, 'certifications': certifications,
        'audio': audio, 'fenlight': fenlight,
        'people': people, 'tv_anime': tv_anime, 'information': information, 'github': updates,
        'bad_language': bad_language, 'drugs_alcohol': drugs_alcohol, 'horror': horror,
        'sex_nudity': sex_nudity, 'violence': violence,
        **GENRES,
        # service letter-marks
        'aiostreams': lambda: badge_text('AIO'),
        'alldebrid': lambda: badge_text('AD'),
        'easynews': lambda: badge_text('EN'),
        'mdblist': lambda: badge_text('MDB'),
        'premiumize': lambda: badge_text('PM'),
        'realdebrid': lambda: badge_text('RD'),
        'tmdb': lambda: badge_text('TMDB', size=92),
        'torbox': lambda: badge_text('TB'),
        'trakt': lambda: badge_text('TRAKT', size=74, spacing=2),
        'flag_sd': lambda: badge_text('SD'),
    },
    'flags': {
        'flag_4k': lambda: badge_text('4K'),
        'flag_1080p': lambda: badge_text('1080'),
        'flag_720p': lambda: badge_text('720'),
        'flag_sd': lambda: badge_text('SD'),
    },
    'results': {
        'results_list': results_list,
        'results_row': results_row,
        'results_widelist': results_widelist,
    },
}


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
