# -*- coding: utf-8 -*-
"""The solid pictogram style (2026-11-17): filled silhouettes with cut-outs (Canvas.erase), thin secondary lines
(antennae, legs, handles), the glyph kept to about 60% of the 512 canvas. Original drawings -- the look of the classic
Fen Light set, nothing copied from it. icons.py registers these over the older stroked glyphs (ICONS['icons'])."""
import math
from draw import Canvas

T = 14   # thin secondary line weight


# ---------------------------------------------------------------- helpers
def _arc(c, cx, cy, r, a0, a1, w=T, n=16):
    """an arc as a polyline of n segments (Pillow's thick arc() breaks into beads at small radii); a long arc wants more"""
    c.path([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / float(n))),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / float(n)))) for i in range(n + 1)], w=w)


def _lens(cx, cy, rx, ry, rot=0.0):
    """an almond / eye outline: two arcs meeting at points; rot in degrees"""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = [(-rx * math.cos(math.pi * i / 36.0), -ry * math.sin(math.pi * i / 36.0)) for i in range(37)]
    pts += [(rx * math.cos(math.pi * i / 36.0), ry * math.sin(math.pi * i / 36.0)) for i in range(1, 36)]
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def _clock_badge(c, cx=372, cy=372, r=58):
    """a small clock cut into the corner of a glyph ('recent' / 'today' variants)"""
    with c.erase():
        c.circle(cx, cy, r + 14, fill=True)
    c.circle(cx, cy, r, fill=True)
    with c.erase():
        c.path([(cx, cy - r * 0.62), (cx, cy), (cx + r * 0.45, cy + r * 0.2)], w=12)


def _flat_screen(c, x0=104, y0=136, x1=408, y1=330):
    """a flat-screen monitor on a stand; returns the screen's inner box"""
    c.rrect(x0, y0, x1, y1, 18, fill=True)
    inner = (x0 + 20, y0 + 20, x1 - 20, y1 - 20)
    with c.erase():
        c.rrect(*inner, 8, fill=True)
    cx = (x0 + x1) / 2.0
    c.poly([(cx - 30, y1), (cx + 30, y1), (cx + 44, y1 + 50), (cx - 44, y1 + 50)])
    c.rrect(cx - 92, y1 + 46, cx + 92, y1 + 64, 9, fill=True)
    return inner


def _flame(c, s=1.0, cx=256, cy=256):
    p = lambda x, y: (cx + (x - 256) * s, cy + (y - 256) * s)
    c.poly([p(256, 96), p(300, 170), p(346, 214), p(360, 286), p(336, 352), p(290, 396), p(222, 396), p(176, 352),
            p(152, 286), p(170, 224), p(206, 252), p(214, 190)])
    with c.erase():
        c.poly([p(256, 254), p(294, 318), p(286, 366), p(226, 366), p(218, 318)])


def _trend(c, s=1.0, cx=256, cy=256):
    p = lambda x, y: (cx + (x - 256) * s, cy + (y - 256) * s)
    pts = [p(120, 360), p(200, 270), p(262, 314), p(370, 180)]
    c.path(pts, w=(T + 4) * s)
    for x, y in pts[:-1]:
        c.dot(x, y, 22 * s)
    c.poly([p(330, 170), p(392, 156), p(382, 220)])
    c.path([p(110, 400), p(402, 400)], w=(T - 4) * s)


def _calendar(c, x0=124, y0=150, x1=388, y1=392):
    """calendar page with rings; returns the page's inner box"""
    c.rrect(x0, y0, x1, y1, 22, fill=True)
    inner = (x0 + 22, y0 + 72, x1 - 22, y1 - 22)
    with c.erase():
        c.rrect(*inner, 8, fill=True)
    for x in (x0 + 60, x1 - 60):
        with c.erase():
            c.rrect(x - 14, y0 - 18, x + 14, y0 + 40, 8, fill=True)
        c.rrect(x - 8, y0 - 30, x + 8, y0 + 32, 6, fill=True)
    return inner


# ---------------------------------------------------------------- batch 1: main menus
def movies():
    """movie camera on a tripod"""
    c = Canvas()
    c.rrect(136, 214, 330, 330, 18, fill=True)
    c.poly([(330, 246), (392, 214), (392, 330), (330, 298)])
    c.circle(178, 168, 44, fill=True)
    c.circle(282, 168, 44, fill=True)
    with c.erase():
        for x in (178, 282):
            c.circle(x, 168, 12, fill=True)
        c.rrect(160, 238, 214, 262, 8, fill=True)
    for x0, x1 in ((204, 170), (262, 296), (233, 233)):
        c.path([(x0, 330), (x1, 404)], w=T)
    return c


def _tv_set(c):
    """a set with an antenna and feet; returns the screen's centre"""
    c.rrect(116, 184, 396, 368, 26, fill=True)
    with c.erase():
        c.rrect(140, 206, 340, 346, 14, fill=True)
    c.dot(368, 236, 11)
    c.dot(368, 272, 11)
    c.path([(256, 184), (204, 120)], w=T)
    c.path([(256, 184), (318, 112)], w=T)
    c.path([(196, 368), (176, 404)], w=T)
    c.path([(316, 368), (336, 404)], w=T)
    return 240, 276


def tv():
    c = Canvas()
    _tv_set(c)
    return c


def tvshows():
    """flat screen with a play mark"""
    c = Canvas()
    x0, y0, x1, y1 = _flat_screen(c)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    c.poly([(cx - 30, cy - 40), (cx + 44, cy), (cx - 30, cy + 40)])
    return c


def anime():
    """big-eyed face under a spiky fringe"""
    c = Canvas()
    c.circle(256, 288, 106, w=T)
    hair = [(256 + 128 * math.cos(math.radians(a)), 262 + 128 * math.sin(math.radians(a))) for a in range(180, 361, 10)]
    hair += [(384, 340), (356, 290), (340, 236), (314, 266), (290, 222), (262, 264), (236, 220), (210, 264), (184, 234),
             (164, 290), (128, 340)]
    c.poly(hair)
    for x in (216, 296):
        c.poly(_lens(x, 322, 24, 28))
        with c.erase():
            c.dot(x + 8, 310, 7)
    c.path([(248, 368), (264, 368)], w=8)
    return c


def search():
    """magnifier with a glint"""
    c = Canvas()
    c.circle(226, 226, 96, fill=True)
    with c.erase():
        c.circle(226, 226, 72, fill=True)
    c.path([(296, 296), (384, 384)], w=40)
    _arc(c, 226, 226, 50, 200, 250, 12)
    return c


def trending():
    c = Canvas()
    _trend(c)
    return c


def trending_recent():
    c = Canvas()
    _trend(c, 0.86, 236, 236)
    _clock_badge(c)
    return c


def popular():
    """flame"""
    c = Canvas()
    _flame(c)
    return c


def popular_today():
    c = Canvas()
    _flame(c, 0.86, 230, 236)
    _clock_badge(c)
    return c


def genres():
    """clapperboard"""
    c = Canvas()
    c.rrect(128, 226, 384, 384, 18, fill=True)
    c.poly([(124, 206), (366, 134), (378, 176), (136, 248)])
    with c.erase():
        for i in range(4):
            x, dy = 160 + i * 56, i * 16
            c.poly([(x, 196 - dy), (x + 26, 188 - dy), (x + 48, 228 - dy), (x + 22, 236 - dy)])
        c.path([(152, 262), (360, 262)], w=10)
    return c


def _person(c, cx, cy, r, w, bottom):
    c.circle(cx, cy, r, fill=True)
    c.rrect(cx - w, cy + r + 12, cx + w, bottom + w, w, fill=True)   # round shoulders; cut flat below by the caller


def people():
    """three busts, the front one outlined off the two behind"""
    c = Canvas()
    for cx in (166, 346):
        _person(c, cx, 202, 36, 66, 380)
    with c.erase():
        _person(c, 256, 186, 56, 98, 380)
    _person(c, 256, 186, 44, 84, 380)
    with c.erase():
        c.rrect(0, 380, 512, 512, 0, fill=True)
    return c


def calender():
    """calendar with a grid of days"""
    c = Canvas()
    x0, y0, x1, y1 = _calendar(c)
    for row in range(3):
        for col in range(4):
            c.rrect(x0 + 18 + col * 50, y0 + 16 + row * 42, x0 + 50 + col * 50, y0 + 44 + row * 42, 5, fill=True)
    return c


def calendar_decades():
    """calendar page with a year span"""
    c = Canvas()
    x0, y0, x1, y1 = _calendar(c)
    c.text("'90s", (x0 + x1) / 2.0, (y0 + y1) / 2.0, 92, font='black')
    return c


def networks():
    """satellite dish"""
    c = Canvas()
    rot, cx, cy = -35, 210, 236   # the bowl, in its own frame: opening toward -y, then turned to face up and right
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    at = lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)
    c.poly([at(126 * math.cos(math.radians(a)), 74 * math.sin(math.radians(a))) for a in range(0, 181, 6)])
    with c.erase():   # hollow it: a shallower ellipse leaves the crescent of a bowl
        c.poly([at(112 * math.cos(math.radians(a)), 34 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
               + [at(112 * math.cos(math.radians(a)), -2) for a in (180, 0)])
    focus = at(0, -96)
    c.path([at(0, 30), focus], w=T)
    c.dot(focus[0], focus[1], 18)
    for r in (44, 80):
        _arc(c, focus[0], focus[1], r, -175, -85)
    c.path([at(0, 70), (cx + 30, 392)], w=T + 6)
    c.rrect(cx - 50, 388, cx + 110, 408, 10, fill=True)
    return c


def ontheair():
    """broadcast tower"""
    c = Canvas()
    c.poly([(256, 196), (310, 404), (282, 404), (256, 300), (230, 404), (202, 404)])
    c.dot(256, 178, 26)
    for r in (64, 104):
        _arc(c, 256, 178, r, -50, 50)
        _arc(c, 256, 178, r, 130, 230)
    c.path([(222, 340), (290, 340)], w=10)
    return c


def lists():
    """a stack of pages"""
    c = Canvas()
    for off in (40, 20):
        c.rrect(150 + off, 120 + off, 346 + off, 370 + off, 14, w=T - 2)
    c.rrect(150, 120, 346, 370, 14, fill=True)
    with c.erase():
        for y in (180, 222, 264, 306):
            c.path([(186, y), (306, y)], w=12)
    return c


def downloads():
    """arrow into a tray"""
    c = Canvas()
    c.poly([(116, 300), (180, 300), (196, 336), (316, 336), (332, 300), (396, 300), (396, 396), (116, 396)])
    c.rrect(222, 112, 290, 236, 10, fill=True)
    c.poly([(176, 226), (336, 226), (256, 312)])
    return c


def favorites():
    """star"""
    c = Canvas()
    c.star(256, 266, 156, 64)
    return c


def discover():
    """compass"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.circle(256, 256, 124, fill=True)
    a = math.radians(40)
    tip = lambda r, ang: (256 + r * math.cos(ang), 256 + r * math.sin(ang))
    c.poly([tip(104, a - math.pi / 2), tip(30, a), tip(30, a + math.pi)])
    c.poly([tip(104, a + math.pi / 2), tip(30, a), tip(30, a + math.pi)], fill=False, w=10)
    return c


def box_office():
    """admission ticket"""
    c = Canvas()
    c.rrect(96, 176, 416, 336, 18, fill=True)
    with c.erase():
        c.circle(96, 256, 30, fill=True)
        c.circle(416, 256, 30, fill=True)
        for y in range(196, 330, 26):
            c.rrect(300, y, 312, y + 14, 3, fill=True)
        c.star(206, 256, 46, 19)
    return c


def intheatres():
    """screen over rows of seats"""
    c = Canvas()
    c.rrect(116, 108, 396, 236, 10, w=T)
    c.path([(150, 236), (130, 262)], w=T - 4)
    c.path([(362, 236), (382, 262)], w=T - 4)
    for row, y in enumerate((300, 360)):
        n = 4 if row == 0 else 5
        span = 260 if row == 0 else 320
        x0 = 256 - span / 2.0
        for i in range(n):
            sx = x0 + i * span / (n - 1)
            c.rrect(sx - 24, y - 26, sx + 24, y + 18, 12, fill=True)
    return c


def next_episodes():
    """skip to next"""
    c = Canvas()
    c.poly([(136, 146), (300, 256), (136, 366)])
    c.rrect(316, 146, 360, 366, 12, fill=True)
    return c


def in_progress_tvshow():
    """flat screen with a half-filled progress bar"""
    c = Canvas()
    x0, y0, x1, y1 = _flat_screen(c)
    c.rrect(x0 + 24, y1 - 46, x1 - 24, y1 - 22, 12, w=8)
    c.rrect(x0 + 24, y1 - 46, (x0 + x1) / 2.0, y1 - 22, 12, fill=True)
    c.poly([(246, y0 + 34), (300, y0 + 66), (246, y0 + 98)])
    return c


def _check_disc(c, cx=256, cy=256, r=140):
    """a disc with a check mark cut out"""
    c.circle(cx, cy, r, fill=True)
    k = r / 128.0
    with c.erase():
        c.path([(cx - 58 * k, cy + 2 * k), (cx - 14 * k, cy + 46 * k), (cx + 66 * k, cy - 44 * k)], w=30 * k)


def watched_recent():
    """check mark in a disc, with a clock"""
    c = Canvas()
    _check_disc(c, 228, 228, 128)
    _clock_badge(c)
    return c


def _eye(c, cx=256, cy=256, s=1.0):
    c.poly(_lens(cx, cy, 170 * s, 96 * s))
    with c.erase():
        c.circle(cx, cy, 70 * s, fill=True)
    c.circle(cx, cy, 48 * s, fill=True)
    with c.erase():
        c.dot(cx + 18 * s, cy - 18 * s, 12 * s)


def most_watched():
    """an eye"""
    c = Canvas()
    _eye(c)
    return c


BATCH1 = {
    'movies': movies, 'tv': tv, 'tvshows': tvshows, 'anime': anime, 'search': search, 'trending': trending,
    'trending_recent': trending_recent, 'popular': popular, 'popular_today': popular_today, 'genres': genres,
    'people': people, 'calender': calender, 'calendar_decades': calendar_decades, 'networks': networks,
    'ontheair': ontheair, 'lists': lists, 'downloads': downloads, 'favorites': favorites, 'discover': discover,
    'box_office': box_office, 'intheatres': intheatres, 'next_episodes': next_episodes,
    'in_progress_tvshow': in_progress_tvshow, 'watched_recent': watched_recent, 'most_watched': most_watched,
}

# ---------------------------------------------------------------- batch 2: the other menu icons
def _sparkle_badge(c, cx=376, cy=376, r=62):
    """a four-point sparkle cut into the corner ('for you' / anime variants)"""
    with c.erase():
        c.sparkle(cx, cy, r + 22, waist=0.42)
    c.sparkle(cx, cy, r)


def settings2():
    """gear"""
    c = Canvas()
    teeth, pts = 8, []
    for i in range(teeth * 4):
        a = math.radians(i * 360.0 / (teeth * 4) - 90 + 360.0 / (teeth * 8))
        r = 150 if (i % 4) in (1, 2) else 116
        pts.append((256 + r * math.cos(a), 256 + r * math.sin(a)))
    c.poly(pts)
    with c.erase():
        c.circle(256, 256, 52, fill=True)
    return c


def _arrow_head(c, tip, ang, size=44):
    a = math.radians(ang)
    back = lambda da: (tip[0] - size * math.cos(a + da), tip[1] - size * math.sin(a + da))
    c.poly([tip, back(0.5), back(-0.5)])


def random():
    """shuffle: two crossing arrows"""
    c = Canvas()
    c.path([(110, 176), (178, 176), (300, 336), (356, 336)], w=26, caps=False)
    with c.erase():
        c.path([(196, 300), (276, 200)], w=58, caps=False)
    c.path([(110, 336), (178, 336), (300, 176), (356, 176)], w=26, caps=False)
    _arrow_head(c, (404, 176), 0, 60)
    _arrow_head(c, (404, 336), 0, 60)
    return c


def live():
    """on-air dot with waves either side"""
    c = Canvas()
    c.circle(256, 256, 46, fill=True)
    for r, w in ((96, 22), (146, 22)):
        _arc(c, 256, 256, r, -45, 45, w)
        _arc(c, 256, 256, r, 135, 225, w)
    return c


def player():
    """play button"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.poly([(220, 186), (330, 256), (220, 326)])
    return c


def folder():
    c = Canvas()
    c.poly([(104, 150), (204, 150), (232, 182), (408, 182), (408, 214), (104, 214)])
    c.rrect(104, 200, 408, 372, 16, fill=True)
    with c.erase():
        c.path([(104, 214), (408, 214)], w=10, caps=False)
    return c


def languages():
    """globe"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.path([(256, 106), (256, 406)], w=14, caps=False)
        c.path([(256 + 74 * math.cos(math.radians(a)), 256 + 150 * math.sin(math.radians(a))) for a in range(0, 361, 6)], w=14)
        for y in (190, 256, 322):
            half = math.sqrt(max(0, 150 ** 2 - (y - 256) ** 2))
            c.path([(256 - half, y), (256 + half, y)], w=14, caps=False)
    return c


def providers():
    """four app tiles"""
    c = Canvas()
    for x, y in ((132, 132), (268, 132), (132, 268)):
        c.rrect(x, y, x + 112, y + 112, 24, fill=True)
    c.rrect(268, 268, 380, 380, 24, fill=True)
    with c.erase():
        c.poly([(306, 296), (352, 324), (306, 352)])
    return c


def _chevron(c, x, w=120, h=240, t=56):
    cy = 256
    c.poly([(x, cy - h / 2.0), (x + t, cy - h / 2.0), (x + t + w, cy), (x + t, cy + h / 2.0), (x, cy + h / 2.0), (x + w, cy)])


def nextpage():
    c = Canvas()
    _chevron(c, 176)
    return c


def nextpage_landscape():
    c = Canvas()
    _chevron(c, 112)
    _chevron(c, 236)
    return c


def item_jump_landscape():
    """jump to: arrow into a bar"""
    c = Canvas()
    c.rrect(104, 230, 290, 282, 12, fill=True)
    c.poly([(270, 166), (366, 256), (270, 346)])
    c.rrect(376, 146, 420, 366, 12, fill=True)
    return c


def watched_1():
    c = Canvas()
    _check_disc(c)
    return c


def most_voted():
    """thumbs up"""
    c = Canvas()
    c.rrect(104, 228, 168, 396, 12, fill=True)
    c.poly([(186, 236), (252, 150), (266, 104), (300, 104), (318, 140), (300, 212), (390, 212), (414, 240), (382, 396),
            (186, 396)])
    with c.erase():
        for y in (262, 310, 356):
            c.path([(330, y), (420, y)], w=8, caps=False)
    return c


def premium():
    """crown"""
    c = Canvas()
    c.poly([(108, 356), (124, 160), (196, 256), (256, 132), (316, 256), (388, 160), (404, 356)])
    for x, y in ((124, 148), (256, 118), (388, 148)):
        c.dot(x, y, 22)
    c.rrect(108, 372, 404, 404, 10, fill=True)
    with c.erase():
        for x in (180, 256, 332):
            c.dot(x, 314, 16)
    return c


def top():
    """podium with a star"""
    c = Canvas()
    c.rrect(104, 296, 204, 400, 8, fill=True)
    c.rrect(206, 236, 306, 400, 8, fill=True)
    c.rrect(308, 330, 408, 400, 8, fill=True)
    with c.erase():
        c.text('1', 256, 314, 84, font='black')
    c.star(256, 156, 70, 29)
    return c


def fresh():
    """a sprout"""
    c = Canvas()
    c.path([(256, 400), (256, 250)], w=T + 6)
    # two leaves from the stem top, their long axes up-left and up-right (rot 45 / -45), each with a cut-out vein
    for (cx, cy, rx, ry, rot) in ((190, 196, 84, 38, 45), (330, 172, 100, 44, -45)):
        c.poly(_lens(cx, cy, rx, ry, rot))
        dx, dy = math.cos(math.radians(rot)) * rx * 0.7, math.sin(math.radians(rot)) * rx * 0.7
        with c.erase():
            c.path([(cx - dx, cy - dy), (cx + dx, cy + dy)], w=8)
    c.rrect(176, 392, 336, 412, 10, fill=True)
    return c


def new():
    """NEW tag"""
    c = Canvas()
    c.rrect(88, 176, 424, 336, 30, fill=True)
    with c.erase():
        c.text('NEW', 256, 252, 112, font='black')
    return c


def dvd():
    """disc"""
    c = Canvas()
    c.circle(256, 256, 152, fill=True)
    with c.erase():
        c.circle(256, 256, 40, fill=True)
        _arc(c, 256, 256, 104, 200, 250, 12)
        _arc(c, 256, 256, 80, 210, 240, 10)
    c.circle(256, 256, 18, fill=True)
    return c


def empty_person():
    """one bust"""
    c = Canvas()
    _person(c, 256, 178, 66, 120, 392)
    with c.erase():
        c.rrect(0, 392, 512, 512, 0, fill=True)
    return c


def because_you_watched():
    c = Canvas()
    _eye(c, 236, 236, 0.86)
    _sparkle_badge(c)
    return c


def oscar_winners():
    """award rosette"""
    c = Canvas()
    c.poly([(196, 260), (150, 404), (196, 384), (222, 420), (250, 290)])
    c.poly([(316, 260), (362, 404), (316, 384), (290, 420), (262, 290)])
    pts = []
    for i in range(32):
        a = math.radians(i * 360 / 32.0)
        r = 120 if i % 2 == 0 else 106
        pts.append((256 + r * math.cos(a), 206 + r * math.sin(a)))
    with c.erase():
        c.circle(256, 206, 132, fill=True)
    c.poly(pts)
    with c.erase():
        c.circle(256, 206, 82, fill=True)
    c.star(256, 210, 66, 27)
    return c


def certifications():
    """shield with a check"""
    c = Canvas()
    c.poly([(256, 100), (392, 150), (392, 250), (372, 320), (320, 376), (256, 414), (192, 376), (140, 320), (120, 250),
            (120, 150)])
    with c.erase():
        c.path([(196, 258), (240, 302), (320, 214)], w=30)
    return c


def audio():
    """speaker with sound waves"""
    c = Canvas()
    c.poly([(104, 206), (168, 206), (252, 130), (252, 382), (168, 306), (104, 306)])
    for r in (64, 112):
        _arc(c, 262, 256, r, -48, 48, 22)
    return c


def fenlight():
    """light bulb"""
    c = Canvas()
    c.circle(256, 208, 112, fill=True)
    c.poly([(186, 280), (326, 280), (306, 336), (206, 336)])
    with c.erase():
        c.path([(214, 204), (236, 240), (256, 204), (276, 240), (298, 204)], w=12)
        c.path([(236, 240), (236, 320)], w=12)
        c.path([(276, 240), (276, 320)], w=12)
    for y in (352, 384):
        c.rrect(206, y, 306, y + 20, 10, fill=True)
    c.rrect(230, 412, 282, 426, 7, fill=True)
    return c


def tv_anime():
    """the TV set with a sparkle on its screen"""
    c = Canvas()
    x, y = _tv_set(c)
    c.sparkle(x, y, 54)
    c.sparkle(x + 60, y - 38, 20)
    return c


def information():
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.dot(256, 176, 22)
        c.rrect(236, 220, 276, 350, 12, fill=True)
    return c


def updates():
    """two circling arrows"""
    c = Canvas()
    r = 128
    at = lambda ang: (256 + r * math.cos(math.radians(ang)), 256 + r * math.sin(math.radians(ang)))
    for start in (200, 20):
        end = start + 112
        _arc(c, 256, 256, r, start, end, 30)
        (ex, ey), tip = at(end), at(end + 30)
        # aimed along the chord from the arc's end to the tip, so the head's base sits on the arc
        _arrow_head(c, tip, math.degrees(math.atan2(tip[1] - ey, tip[0] - ex)), 76)
    return c


BATCH2 = {
    'settings2': settings2, 'random': random, 'live': live, 'player': player, 'folder': folder,
    'languages': languages, 'providers': providers, 'nextpage': nextpage, 'nextpage_landscape': nextpage_landscape,
    'item_jump_landscape': item_jump_landscape, 'watched_1': watched_1, 'most_voted': most_voted,
    'premium': premium, 'top': top, 'fresh': fresh, 'new': new, 'dvd': dvd, 'empty_person': empty_person,
    'because_you_watched': because_you_watched, 'oscar_winners': oscar_winners,
    'certifications': certifications, 'audio': audio, 'fenlight': fenlight, 'tv_anime': tv_anime,
    'information': information, 'github': updates,
}

# ---------------------------------------------------------------- batch 3: genres (TMDb's and AniList's)
# Named as DeadLight asks for them: meta_lists.*_genres() icons and navigator.anilist_genres ('Sci-Fi' -> genre_scifi).
def _ring(c, cx, cy, r, t):
    c.circle(cx, cy, r, fill=True)
    with c.erase():
        c.circle(cx, cy, r - t, fill=True)


def genre_action():
    """explosion: a ring of spikes around a core"""
    c = Canvas()
    pts = []
    for i in range(22):
        a = math.radians(-90 + i * 360 / 22.0)
        r = (150 if i % 2 == 0 else 82) * (0.85 + 0.25 * ((i * 7) % 5) / 4.0)
        pts.append((256 + r * math.cos(a), 268 + r * math.sin(a) * 0.82))
    c.poly(pts)
    with c.erase():
        c.poly([(256 + 0.45 * (x - 256), 268 + 0.45 * (y - 268)) for x, y in pts])
    c.poly([(256 + 0.25 * (x - 256), 268 + 0.25 * (y - 268)) for x, y in pts])
    return c


def genre_adventure():
    """mountains with a flag on the peak"""
    c = Canvas()
    c.poly([(84, 396), (226, 168), (296, 280), (334, 226), (428, 396)])
    with c.erase():
        c.poly([(226, 168), (262, 226), (240, 216), (222, 238), (200, 214), (190, 226)])
    c.path([(226, 168), (226, 96)], w=10)
    c.poly([(230, 96), (300, 116), (230, 138)])
    return c


def genre_animation():
    """a bouncing ball with motion streaks"""
    c = Canvas()
    c.circle(310, 236, 104, fill=True)
    with c.erase():
        _arc(c, 310, 236, 66, 200, 260, 14)
    for y, x0, x1 in ((180, 92, 180), (236, 70, 176), (292, 92, 180)):
        c.path([(x0, y), (x1, y)], w=T + 4)
    c.rrect(220, 372, 400, 392, 10, fill=True)
    return c


def genre_comedy():
    c = Canvas()
    _mask(c, 256, 250, 1.15, True)
    return c


def genre_crime():
    """handcuffs"""
    c = Canvas()
    for cx in (166, 346):
        _ring(c, cx, 300, 84, 30)
        c.rrect(cx - 26, 196, cx + 26, 228, 10, fill=True)
    for x in (214, 256, 298):
        _ring(c, x, 182, 26, 12)
    return c


def genre_documentary():
    """camcorder"""
    c = Canvas()
    c.rrect(104, 186, 336, 350, 22, fill=True)
    c.poly([(336, 232), (412, 190), (412, 346), (336, 304)])
    with c.erase():
        c.circle(186, 268, 50, fill=True)
    c.circle(186, 268, 30, fill=True)
    c.rrect(236, 150, 310, 186, 8, fill=True)
    with c.erase():
        c.dot(300, 222, 12)
    return c


def _mask(c, cx, cy, s, smile):
    """theatre mask: broad brow, tapering to a rounded chin; almond eyes; a crescent mouth"""
    pts = []
    for i in range(72):
        a = 2 * math.pi * i / 72
        x, y = math.sin(a), -math.cos(a)
        w = 112 * (1 - 0.4 * max(0, y) ** 1.4)        # widest at the brow, narrowing to the chin
        top = 70 * (1 - 0.25 * abs(x) ** 3)            # a flatter brow line, slightly lower at the temples
        pts.append((cx + s * w * x, cy + s * (120 if y > 0 else top) * y))
    c.poly(pts)
    with c.erase():
        slant = 12 if smile else -12
        c.poly(_lens(cx - 42 * s, cy - 18 * s, 30 * s, 13 * s, slant))
        c.poly(_lens(cx + 42 * s, cy - 18 * s, 30 * s, 13 * s, -slant))
        mouth_y, mr = cy + (40 if smile else 54) * s, (40 if smile else 30) * s
        c.circle(cx, mouth_y, mr, fill=True)
    # the crescent: fill back the part of the hole away from the open side
    c.circle(cx, mouth_y + (-20 if smile else 16) * s, mr * 1.05, fill=True)


def genre_drama():
    c = Canvas()
    _mask(c, 256, 250, 1.15, False)
    return c


def genre_family():
    """two adults and a child"""
    c = Canvas()
    for cx in (150, 362):
        _person(c, cx, 170, 44, 74, 392)
    with c.erase():
        _person(c, 256, 250, 44, 66, 392)
    _person(c, 256, 250, 32, 54, 392)
    with c.erase():
        c.rrect(0, 392, 512, 512, 0, fill=True)
    return c


def genre_fantasy():
    """wizard hat with stars"""
    c = Canvas()
    c.poly([(150, 360), (236, 186), (262, 104), (330, 84), (300, 120), (296, 200), (362, 360)])
    c.rrect(92, 352, 420, 392, 20, fill=True)
    with c.erase():
        c.star(242, 270, 34, 14)
        c.path([(162, 340), (350, 340)], w=12, caps=False)
    c.sparkle(392, 186, 40)
    c.sparkle(128, 230, 26)
    return c


def genre_history():
    """classical temple"""
    c = Canvas()
    c.poly([(96, 184), (256, 100), (416, 184)])
    c.rrect(104, 190, 408, 214, 4, fill=True)
    for x in (140, 214, 298, 372):
        c.rrect(x - 18, 226, x + 18, 352, 4, fill=True)
    c.rrect(92, 362, 420, 384, 4, fill=True)
    c.rrect(80, 392, 432, 410, 4, fill=True)
    with c.erase():
        c.circle(256, 156, 16, fill=True)
    return c


def genre_horror():
    """skull"""
    c = Canvas()
    c.circle(256, 226, 132, fill=True)
    c.rrect(176, 290, 336, 392, 30, fill=True)
    with c.erase():
        c.poly(_lens(206, 240, 40, 34, 10))
        c.poly(_lens(306, 240, 40, 34, -10))
        c.poly([(256, 282), (276, 320), (236, 320)])
        for x in (218, 256, 294):
            c.rrect(x - 4, 346, x + 4, 400, 3, fill=True)
    return c


def genre_kids():
    """balloon on a string"""
    c = Canvas()
    c.poly([(256 + 112 * math.cos(math.radians(a)), 200 + 132 * math.sin(math.radians(a))) for a in range(0, 360, 6)])
    c.poly([(256, 326), (234, 356), (278, 356)])
    with c.erase():
        _arc(c, 256, 200, 82, 200, 250, 16)
    c.path([(256, 356), (230, 396), (270, 424)], w=10)
    return c


def genre_music():
    """two beamed notes"""
    c = Canvas()
    for x, y in ((170, 366), (354, 332)):
        c.poly(_lens(x, y, 52, 38, -20))
    c.rrect(204, 140, 228, 366, 6, fill=True)
    c.rrect(388, 106, 412, 332, 6, fill=True)
    c.poly([(204, 128), (412, 94), (412, 152), (204, 186)])
    return c


def genre_mystery():
    """keyhole plate"""
    c = Canvas()
    c.rrect(156, 96, 356, 416, 40, fill=True)
    with c.erase():
        c.circle(256, 216, 44, fill=True)
        c.poly([(236, 236), (276, 236), (296, 340), (216, 340)])
    for y in (132, 380):
        with c.erase():
            c.dot(256, y, 10)
    return c


def genre_news():
    """newspaper"""
    c = Canvas()
    c.rrect(92, 116, 400, 396, 18, fill=True)
    c.rrect(400, 176, 430, 396, 12, fill=True)
    with c.erase():
        c.rrect(124, 148, 368, 196, 6, fill=True)
        c.rrect(124, 226, 236, 334, 6, fill=True)
        for y in (234, 266, 298, 330, 362):
            c.path([(264, y), (366, y)], w=12, caps=False)
        c.path([(124, 362), (236, 362)], w=12, caps=False)
    return c


def genre_reality():
    """a person framed by viewfinder corners"""
    c = Canvas()
    for (x, y, dx, dy) in ((96, 112, 1, 1), (416, 112, -1, 1), (96, 400, 1, -1), (416, 400, -1, -1)):
        c.path([(x, y + 64 * dy), (x, y), (x + 64 * dx, y)], w=T + 6)
    _person(c, 256, 196, 48, 80, 350)
    with c.erase():
        c.rrect(170, 350, 342, 450, 0, fill=True)   # cut the bust flat, between the bottom corners
    c.dot(376, 152, 16)
    return c


def genre_romance():
    """heart"""
    c = Canvas()
    c.circle(196, 210, 80, fill=True)
    c.circle(316, 210, 80, fill=True)
    c.poly([(122, 240), (256, 396), (390, 240), (256, 200)])
    with c.erase():
        _arc(c, 196, 210, 48, 200, 260, 14)
    return c


def genre_scifi():
    """rocket"""
    c = Canvas()
    c.poly([(256, 100), (300, 160), (314, 230), (314, 330), (198, 330), (198, 230), (212, 160)])
    c.poly([(198, 270), (150, 330), (150, 372), (198, 344)])
    c.poly([(314, 270), (362, 330), (362, 372), (314, 344)])
    with c.erase():
        c.circle(256, 218, 24, fill=True)
    c.poly([(226, 340), (286, 340), (256, 416)])
    with c.erase():
        c.poly([(244, 346), (268, 346), (256, 382)])
    return c


def genre_soap():
    """bubbles"""
    c = Canvas()
    for cx, cy, r in ((206, 296, 108), (346, 186, 66), (352, 362, 40)):
        c.circle(cx, cy, r, fill=True)
        with c.erase():
            _arc(c, cx, cy, r * 0.66, 200, 255, max(8, r * 0.13))
    return c


def genre_talk():
    """two speech bubbles"""
    c = Canvas()
    c.rrect(84, 104, 324, 262, 40, fill=True)
    c.poly([(132, 250), (124, 318), (190, 250)])
    with c.erase():
        c.rrect(170, 214, 444, 400, 54, fill=True)
    c.rrect(188, 232, 428, 384, 40, fill=True)
    c.poly([(380, 372), (392, 440), (320, 372)])
    with c.erase():
        for x in (254, 308, 362):
            c.dot(x, 308, 16)
    return c


def genre_thriller():
    """hourglass"""
    c = Canvas()
    c.rrect(124, 88, 388, 120, 10, fill=True)
    c.rrect(124, 392, 388, 424, 10, fill=True)
    c.poly([(160, 120), (352, 120), (352, 150), (270, 256), (352, 362), (352, 392), (160, 392), (160, 362), (242, 256),
            (160, 150)])
    with c.erase():
        c.poly([(184, 142), (328, 142), (262, 226), (250, 226)])
        c.poly([(256, 290), (328, 372), (184, 372)])
    c.poly([(200, 368), (312, 368), (256, 318)])
    c.poly([(220, 168), (292, 168), (256, 212)])
    return c


def genre_war():
    """crossed swords"""
    c = Canvas()
    for sign in (1, -1):
        x = lambda v: 256 + sign * (v - 256)   # the second sword is the first mirrored
        c.poly([(x(112), 96), (x(150), 106), (x(336), 292), (x(310), 318), (x(122), 132)])   # blade, pointed at the top
        c.path([(x(274), 342), (x(362), 254)], w=26)                                        # cross guard
        c.path([(x(330), 310), (x(384), 364)], w=28)                                        # grip
        c.dot(x(398), 378, 24)                                                              # pommel
    return c


def genre_western():
    """cowboy hat"""
    c = Canvas()
    # crown: two lobes with a pinch on top
    c.poly([(170, 296), (178, 196), (200, 160), (236, 158), (256, 182), (276, 158), (312, 160), (334, 196), (342, 296)])
    # brim: curls up at both ends, dips under the crown
    brim = [(64, 244), (110, 284), (170, 300), (256, 306), (342, 300), (402, 284), (448, 244),
            (436, 300), (390, 336), (320, 354), (256, 358), (192, 354), (122, 336), (76, 300)]
    c.poly(brim)
    with c.erase():
        c.path([(176, 264), (336, 264)], w=18, caps=False)
    return c


def genre_ecchi():
    """blushing face: closed eyes, hatched cheeks"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        _arc(c, 200, 230, 30, 200, 340, 16)
        _arc(c, 312, 230, 30, 200, 340, 16)
        for cx in (172, 340):
            for dx in (-22, 0, 22):
                c.path([(cx + dx - 7, 312), (cx + dx + 7, 286)], w=12)
        _arc(c, 256, 290, 36, 30, 150, 14)
    return c


def genre_hentai():
    """18+"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.text('18+', 256, 250, 136, font='black')
    return c


def genre_mahou_shoujo():
    """magic wand: a star on a staff, with sparkles"""
    c = Canvas()
    c.path([(110, 416), (236, 290)], w=26)
    c.star(300, 222, 132, 56)
    with c.erase():
        c.star(300, 228, 46, 19)
    c.sparkle(126, 150, 40)
    c.sparkle(424, 372, 34)
    return c


def genre_mecha():
    """robot head: helmet, visor, antenna, ear bolts"""
    c = Canvas()
    c.rrect(128, 152, 384, 392, 46, fill=True)
    with c.erase():
        c.rrect(160, 214, 352, 278, 24, fill=True)
        for x in (208, 256, 304):
            c.rrect(x - 8, 318, x + 8, 362, 6, fill=True)
    c.rrect(176, 230, 336, 262, 14, fill=True)
    with c.erase():
        c.rrect(196, 238, 244, 254, 6, fill=True)
        c.rrect(268, 238, 316, 254, 6, fill=True)
    c.path([(256, 152), (256, 96)], w=T)
    c.dot(256, 86, 22)
    c.rrect(92, 230, 128, 300, 10, fill=True)
    c.rrect(384, 230, 420, 300, 10, fill=True)
    return c


def genre_psychological():
    """a spiral cut into a disc"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    pts, turns, n = [], 2.6, 220
    for i in range(n + 1):
        t = i / float(n)
        a = 2 * math.pi * turns * t
        r = 18 + 112 * t
        pts.append((256 + r * math.cos(a), 256 + r * math.sin(a)))
    with c.erase():
        c.path(pts, w=18)
    return c


def genre_slice_of_life():
    """a cup of tea with steam, on a saucer"""
    c = Canvas()
    c.poly([(132, 222), (348, 222), (334, 340), (300, 376), (180, 376), (146, 340)])
    _arc(c, 352, 284, 44, -80, 80, 22)
    c.rrect(104, 384, 376, 408, 12, fill=True)
    with c.erase():
        _arc(c, 240, 222, 78, 30, 60, 12)
    for x in (192, 240, 288):
        c.path([(x, 176), (x - 16, 148), (x, 120), (x - 16, 92)], w=T)
    return c


def genre_sports():
    """a ball with seams cut in"""
    c = Canvas()
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        c.path([(256, 106), (256, 406)], w=16, caps=False)
        c.path([(106, 256), (406, 256)], w=16, caps=False)
        _arc(c, 40, 256, 160, -50, 50, 16)
        _arc(c, 472, 256, 160, 130, 230, 16)
    return c


def genre_supernatural():
    """ghost"""
    c = Canvas()
    body = [(256 + 132 * math.cos(math.radians(a)), 220 + 132 * math.sin(math.radians(a))) for a in range(180, 361, 6)]
    body += [(388, 410), (344, 376), (300, 410), (256, 376), (212, 410), (168, 376), (124, 410)]
    c.poly(body)
    with c.erase():
        c.poly(_lens(208, 232, 22, 34, 90))
        c.poly(_lens(304, 232, 22, 34, 90))
        c.circle(256, 300, 22, fill=True)
    return c


BATCH3 = {
    'genre_action': genre_action, 'genre_adventure': genre_adventure, 'genre_animation': genre_animation,
    'genre_comedy': genre_comedy, 'genre_crime': genre_crime, 'genre_documentary': genre_documentary,
    'genre_drama': genre_drama, 'genre_family': genre_family, 'genre_fantasy': genre_fantasy,
    'genre_history': genre_history, 'genre_horror': genre_horror, 'genre_kids': genre_kids, 'genre_music': genre_music,
    'genre_mystery': genre_mystery, 'genre_news': genre_news, 'genre_reality': genre_reality,
    'genre_romance': genre_romance, 'genre_scifi': genre_scifi, 'genre_soap': genre_soap, 'genre_talk': genre_talk,
    'genre_thriller': genre_thriller, 'genre_war': genre_war, 'genre_western': genre_western,
    'genre_ecchi': genre_ecchi, 'genre_hentai': genre_hentai, 'genre_mahou_shoujo': genre_mahou_shoujo,
    'genre_mecha': genre_mecha, 'genre_psychological': genre_psychological,
    'genre_slice_of_life': genre_slice_of_life, 'genre_sports': genre_sports, 'genre_supernatural': genre_supernatural,
}

# ---------------------------------------------------------------- batch 4: account, library and list icons
def solid_badge(label, size=None):
    """a solid rounded badge with its letters cut out (the service marks and the quality flags)"""
    c = Canvas()
    c.rrect(64, 160, 448, 352, 40, fill=True)
    if size is None:
        size = {1: 170, 2: 150, 3: 120, 4: 96, 5: 80}.get(len(label), 70)
    with c.erase():
        c.text(label, 256, 252, size, font='black')
    return c


def _document(c, x0=144, y0=96, x1=368, y1=416, fold=64):
    """a page with a folded corner; returns the box its lines go in"""
    c.poly([(x0, y0), (x1 - fold, y0), (x1, y0 + fold), (x1, y1), (x0, y1)])
    with c.erase():
        c.poly([(x1 - fold + 14, y0 - 4), (x1 + 4, y0 + fold - 14), (x1 + 4, y0 - 4)])
        c.poly([(x1 - fold, y0 + 12), (x1 - fold, y0 + fold), (x1 - 12, y0 + fold)])
    return x0 + 34, y0 + fold + 28, x1 - 34, y1 - 34


def _doc_lines(c, box, n=4):
    x0, y0, x1, y1 = box
    with c.erase():
        for i in range(n):
            y = y0 + i * (y1 - y0) / float(max(1, n - 1)) if n > 1 else y0
            c.path([(x0, y), (x1 - (40 if i == n - 1 else 0), y)], w=14)


def _disc_with(c, cut):
    """a disc with a shape cut out of it (pause bars, a cross, an arrow)"""
    c.circle(256, 256, 150, fill=True)
    with c.erase():
        cut()


def account():
    """ID card"""
    c = Canvas()
    c.rrect(76, 136, 436, 376, 26, fill=True)
    with c.erase():
        c.circle(170, 226, 36, fill=True)
        c.rrect(116, 276, 224, 340, 30, fill=True)
        for y, x1 in ((216, 392), (256, 392), (296, 350)):
            c.path([(262, y), (x1, y)], w=16)
    return c


def airing_last_season():
    """calendar with a back arrow"""
    c = Canvas()
    x0, y0, x1, y1 = _calendar(c)
    cy = (y0 + y1) / 2.0
    c.rrect(x0 + 74, cy - 14, x1 - 34, cy + 14, 8, fill=True)
    c.poly([(x0 + 26, cy), (x0 + 96, cy - 48), (x0 + 96, cy + 48)])
    return c


def changelog():
    c = Canvas()
    box = _document(c, 128, 90, 348, 404)
    _doc_lines(c, box, 4)
    _clock_badge(c, 368, 372, 62)
    return c


def clear_cache():
    """bin"""
    c = Canvas()
    c.rrect(120, 136, 392, 168, 10, fill=True)
    c.rrect(210, 104, 302, 136, 10, fill=True)
    c.poly([(140, 188), (372, 188), (348, 412), (164, 412)])
    with c.erase():
        for x in (204, 256, 308):
            c.rrect(x - 9, 226, x + 9, 372, 6, fill=True)
    return c


def _cloud(c, s=1.0, cx=256, cy=256):
    p = lambda x, y: (cx + (x - 256) * s, cy + (y - 256) * s)
    for x, y, r in ((186, 276, 76), (270, 226, 104), (346, 286, 66)):   # puffs whose bottoms meet the base (352)
        c.circle(*p(x, y), r * s, fill=True)
    c.rrect(*p(110, 280), *p(412, 352), 36 * s, fill=True)


def cloud():
    c = Canvas()
    _cloud(c)
    return c


def code():
    """</>"""
    c = Canvas()
    c.path([(184, 160), (88, 256), (184, 352)], w=40)
    c.path([(328, 160), (424, 256), (328, 352)], w=40)
    c.path([(292, 116), (220, 396)], w=34)
    return c


def collection():
    """books on a shelf"""
    c = Canvas()
    for x0, x1, top in ((108, 166, 132), (180, 238, 108), (252, 310, 150)):
        c.rrect(x0, top, x1, 380, 8, fill=True)
        with c.erase():
            c.path([(x0 + 4, top + 40), (x1 - 4, top + 40)], w=10, caps=False)
            c.path([(x0 + 4, 336), (x1 - 4, 336)], w=10, caps=False)
    c.poly([(324, 152), (380, 140), (430, 372), (374, 384)])   # one leaning
    c.rrect(88, 386, 432, 412, 8, fill=True)
    return c


def database():
    """stacked discs"""
    c = Canvas()
    ellipse = lambda y, rx, ry, a0=0, a1=360: [(256 + rx * math.cos(math.radians(a)), y + ry * math.sin(math.radians(a)))
                                              for a in range(a0, a1 + 1, 6)]
    c.rrect(116, 120, 396, 392, 0, fill=True)
    c.poly(ellipse(120, 140, 44))
    c.poly(ellipse(392, 140, 44))
    with c.erase():
        for y in (212, 302):   # the seams between the discs: the lower half of an ellipse
            c.path(ellipse(y, 140, 44, 0, 180), w=14)
        c.path(ellipse(120, 112, 28), w=12, close=True)   # the top rim
    return c


def dropped():
    """a disc with a cross"""
    c = Canvas()
    _disc_with(c, lambda: (c.path([(196, 196), (316, 316)], w=34), c.path([(316, 196), (196, 316)], w=34)))
    return c


def history():
    """a clock face inside a counter-clockwise arrow"""
    c = Canvas()
    r = 150
    at = lambda ang: (256 + r * math.cos(math.radians(ang)), 256 + r * math.sin(math.radians(ang)))
    _arc(c, 256, 256, r, -140, 170, 26, n=72)
    (ex, ey), tip = at(-140), at(-170)   # the head runs on counter-clockwise past the arc's start
    _arrow_head(c, tip, math.degrees(math.atan2(tip[1] - ey, tip[0] - ex)), 76)
    c.circle(256, 256, 104, fill=True)
    with c.erase():
        c.path([(256, 186), (256, 256), (306, 290)], w=22)
    return c


def images():
    """picture: mountains and a sun"""
    c = Canvas()
    c.rrect(84, 120, 428, 392, 24, fill=True)
    with c.erase():
        c.rrect(112, 148, 400, 364, 10, fill=True)
    c.poly([(112, 364), (210, 240), (268, 310), (318, 262), (400, 364)])
    c.circle(330, 196, 30, fill=True)
    return c


def keyword():
    """#"""
    c = Canvas()
    for x0, x1 in ((216, 192), (330, 306)):
        c.path([(x0, 104), (x1, 408)], w=36)
    for y in (204, 312):
        c.path([(112, y), (412, y)], w=36)
    return c


def _list_rows(c, x0=104, x1=360, rows=(160, 256, 352)):
    for y in rows:
        c.dot(x0 + 20, y, 22)
        c.rrect(x0 + 62, y - 16, x1, y + 16, 10, fill=True)


def liked_lists():
    c = Canvas()
    _list_rows(c, 96, 330)
    with c.erase():
        c.circle(370, 360, 92, fill=True)
    for dx in (-26, 26):
        c.circle(370 + dx, 340, 34, fill=True)
    c.poly([(312, 352), (370, 418), (428, 352), (370, 330)])
    return c


def _link_loop(c, cx, cy, ang):
    """one chain link: a stadium outline, turned to ang degrees"""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for a in range(90, 271, 10):
        pts.append((-60 + 50 * math.cos(math.radians(a)), 50 * math.sin(math.radians(a))))
    for a in range(-90, 91, 10):
        pts.append((60 + 50 * math.cos(math.radians(a)), 50 * math.sin(math.radians(a))))
    c.path([(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts], w=32, close=True)


def link():
    c = Canvas()
    _link_loop(c, 200, 312, -45)
    _link_loop(c, 312, 200, -45)
    return c


def log():
    c = Canvas()
    box = _document(c)
    _doc_lines(c, box, 5)
    return c


def on_hold():
    c = Canvas()
    _disc_with(c, lambda: (c.rrect(206, 186, 240, 326, 8, fill=True), c.rrect(272, 186, 306, 326, 8, fill=True)))
    return c


def recommended():
    """heart with a sparkle"""
    c = Canvas()
    for x in (190, 298):
        c.circle(x, 222, 72, fill=True)
    c.poly([(124, 250), (244, 388), (364, 250), (244, 212)])
    _sparkle_badge(c, 376, 150, 58)
    return c


def settings():
    """three sliders"""
    c = Canvas()
    for y, kx in ((156, 196), (256, 316), (356, 236)):
        c.rrect(96, y - 12, 416, y + 12, 12, fill=True)
        with c.erase():
            c.circle(kx, y, 44, fill=True)
        c.circle(kx, y, 32, fill=True)
    return c


def update():
    """down arrow in a disc"""
    c = Canvas()
    _disc_with(c, lambda: (c.rrect(238, 160, 274, 268, 8, fill=True), c.poly([(184, 250), (328, 250), (256, 340)])))
    return c


def upload():
    """arrow out of a tray"""
    c = Canvas()
    c.poly([(116, 300), (180, 300), (196, 336), (316, 336), (332, 300), (396, 300), (396, 396), (116, 396)])
    c.rrect(222, 180, 290, 300, 10, fill=True)
    c.poly([(176, 190), (336, 190), (256, 104)])
    return c


def user_lists():
    """a person beside list rows"""
    c = Canvas()
    _person(c, 172, 196, 48, 74, 368)
    with c.erase():
        c.rrect(0, 368, 512, 512, 0, fill=True)
    _list_rows(c, 268, 432, rows=(200, 272, 344))
    return c


def views():
    """a layout: one wide tile over two"""
    c = Canvas()
    c.rrect(104, 112, 408, 236, 22, fill=True)
    c.rrect(104, 268, 238, 400, 22, fill=True)
    c.rrect(274, 268, 408, 400, 22, fill=True)
    return c


def watchlist():
    """bookmark with a plus"""
    c = Canvas()
    c.poly([(152, 96), (360, 96), (360, 420), (256, 336), (152, 420)])
    with c.erase():
        c.rrect(238, 156, 274, 280, 8, fill=True)
        c.rrect(194, 200, 318, 236, 8, fill=True)
    return c


BATCH4 = {
    'account': account, 'airing_last_season': airing_last_season, 'changelog': changelog, 'clear_cache': clear_cache,
    'cloud': cloud, 'code': code, 'collection': collection, 'database': database, 'dropped': dropped,
    'history': history, 'images': images, 'keyword': keyword, 'liked_lists': liked_lists, 'link': link, 'log': log,
    'on_hold': on_hold, 'recommended': recommended, 'settings': settings, 'update': update, 'upload': upload,
    'user_lists': user_lists, 'views': views, 'watchlist': watchlist,
}

# ---------------------------------------------------------------- batch 5: content warnings, service marks, flags, layouts
def bad_language():
    """speech bubble with #*! cut out"""
    c = Canvas()
    c.rrect(72, 116, 440, 336, 44, fill=True)
    c.poly([(150, 330), (140, 420), (236, 330)])
    with c.erase():
        c.text('#*!', 256, 222, 116, font='black')
    return c


def drugs_alcohol():
    """cocktail glass with an olive"""
    c = Canvas()
    c.poly([(116, 120), (396, 120), (256, 276)])
    with c.erase():
        c.circle(300, 168, 34, fill=True)
        c.path([(300, 168), (382, 92)], w=16)
    c.circle(300, 168, 22, fill=True)
    c.path([(300, 168), (370, 104)], w=8)
    c.rrect(244, 270, 268, 384, 6, fill=True)
    c.poly([(166, 404), (346, 404), (300, 376), (212, 376)])
    return c


def sex_nudity():
    """lips"""
    c = Canvas()
    upper = [(84, 262), (150, 196), (208, 176), (256, 202), (304, 176), (362, 196), (428, 262)]
    lower = [(428, 262), (372, 318), (300, 344), (256, 348), (212, 344), (140, 318), (84, 262)]
    c.poly(upper + lower)
    with c.erase():
        c.path([(104, 262), (190, 254), (256, 268), (322, 254), (408, 262)], w=16)
    with c.erase():
        _arc(c, 210, 312, 34, 200, 250, 10)
    return c


def violence():
    """an impact: a jagged burst with a crack through it"""
    c = Canvas()
    pts = []
    for i in range(16):
        a = math.radians(-90 + i * 360 / 16.0)
        r = (164 if i % 2 == 0 else 96) * (1.0 if i % 4 else 0.86)
        pts.append((256 + r * math.cos(a), 256 + r * math.sin(a)))
    c.poly(pts)
    with c.erase():
        c.path([(196, 150), (250, 236), (220, 266), (300, 362)], w=16)
    return c


BATCH5 = {
    'bad_language': bad_language, 'drugs_alcohol': drugs_alcohol, 'horror': genre_horror,
    'sex_nudity': sex_nudity, 'violence': violence,
    # services get their names on a badge: an approximation of someone else's logo is worse than plainly naming it
    'aiostreams': lambda: solid_badge('AIO'),
    'alldebrid': lambda: solid_badge('AD'),
    'easynews': lambda: solid_badge('EN'),
    'mdblist': lambda: solid_badge('MDB'),
    'premiumize': lambda: solid_badge('PM'),
    'realdebrid': lambda: solid_badge('RD'),
    'tmdb': lambda: solid_badge('TMDB'),
    'torbox': lambda: solid_badge('TB'),
    'trakt': lambda: solid_badge('TRAKT'),
    'flag_sd': lambda: solid_badge('SD'),
}

# the quality flags (packages/media/flags)
FLAGS = {
    'flag_4k': lambda: solid_badge('4K'),
    'flag_1080p': lambda: solid_badge('1080'),
    'flag_720p': lambda: solid_badge('720'),
    'flag_sd': lambda: solid_badge('SD'),
}


# the results window's layout choices (packages/media/results)
def results_list():
    c = Canvas()
    for y in (150, 256, 362):
        c.rrect(88, y - 36, 424, y + 36, 18, fill=True)
    return c


def results_row():
    c = Canvas()
    c.rrect(88, 172, 424, 340, 24, fill=True)
    with c.erase():
        c.path([(140, 256), (372, 256)], w=22)
    return c


def results_widelist():
    c = Canvas()
    for y in (150, 256, 362):
        c.rrect(88, y - 36, 424, y + 36, 18, fill=True)
        with c.erase():
            c.rrect(106, y - 22, 172, y + 22, 10, fill=True)
    return c


RESULTS = {'results_list': results_list, 'results_row': results_row, 'results_widelist': results_widelist}

SOLID = {**BATCH1, **BATCH2, **BATCH3, **BATCH4, **BATCH5}
