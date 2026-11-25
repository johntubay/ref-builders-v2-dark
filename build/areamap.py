# -*- coding: utf-8 -*-
"""Illustrated, interactive service-area map for the homepage.

Positions come from real latitude/longitude, projected onto a 700 x 760 canvas
(the full view adds room above it for the "Now viewing" card)
(about 15 units per mile), so the bay, freeways and cities sit where they
really are. Distances are straight-line miles from the Campbell office.
Clicking a pin zooms in (see the "area map" block in site.js).
"""
import html

E = html.escape
VB_X, VB_Y, VB_W, VB_H = 0, -110, 700, 900


def smooth(pts, closed=False):
    """Catmull-Rom spline through the points, written as cubic Bezier path."""
    p = list(pts)
    if closed:
        p = [p[-1]] + p + [p[0], p[1]]
    else:
        p = [p[0]] + p + [p[-1]]
    d = f"M{p[1][0]:.0f} {p[1][1]:.0f}"
    for i in range(1, len(p) - 2):
        x0, y0 = p[i - 1]; x1, y1 = p[i]; x2, y2 = p[i + 1]; x3, y3 = p[i + 2]
        c1 = (x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6)
        c2 = (x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6)
        d += f" C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {x2:.0f} {y2:.0f}"
    return d + (" Z" if closed else "")


# --------------------------------------------------------------- geography
OCEAN = [(84, -300), (72, -150), (60, -20), (52, 40), (40, 90), (34, 130), (36, 190), (49, 269), (70, 350),
         (99, 435), (118, 540), (140, 652), (178, 820), (200, 940), (-60, 940), (-60, -300)]
BAY = [(45, 64), (100, 56), (140, 36), (150, -40), (146, -150), (140, -300), (280, -300), (268, -150), (262, -40), (240, 40), (214, 100),
       (240, 170), (290, 230), (314, 262), (352, 322), (396, 372), (440, 418), (472, 452),
       (432, 452), (372, 436), (320, 410), (272, 374), (240, 342), (206, 322), (172, 252),
       (142, 182), (126, 122), (116, 96), (90, 80), (50, 78)]
SERVICE = [(44, 70), (130, 34), (252, 26), (336, 150), (470, 286), (604, 420), (644, 556),
           (590, 704), (476, 736), (384, 704), (266, 608), (156, 526), (96, 404), (52, 250)]
ROADS = {
    "101": [(118, 128), (150, 210), (205, 300), (271, 385), (345, 448), (420, 500), (500, 540), (560, 570), (640, 620), (760, 690), (860, 740)],
    "280": [(100, 140), (120, 222), (160, 320), (220, 410), (290, 490), (380, 556), (470, 588), (556, 576)],
    "880": [(215, 92), (250, 170), (320, 270), (410, 380), (480, 460), (530, 530), (548, 564)],
    "17":  [(548, 566), (512, 600), (494, 632), (482, 690), (470, 820), (464, 940)],
}
SHIELDS = [("101", 186, 262), ("280", 168, 348), ("880", 362, 322), ("17", 478, 734)]
COUNTY_LINES = [
    [(36, 176), (140, 176)],
    [(372, 436), (330, 470), (290, 520), (250, 580), (190, 630), (140, 652)],
    [(440, 424), (520, 410), (600, 400), (720, 390)],
    [(250, 18), (400, 58), (720, 78)],
    [(140, 652), (300, 700), (430, 820)],
]
COUNTY_LABELS = [("San Mateo County", 92, 392), ("Alameda County", 498, 226),
                 ("Santa Clara County", 566, 476), ("Contra Costa County", 470, 36)]

# (slug, name, x, y, miles, label side)  service cities that have their own page
CITIES = [
    ("redwood-city", "Redwood City", 255, 404, 21, "r"),
    ("stanford", "Stanford", 312, 466, 16, "l"),
    ("palo-alto", "Palo Alto", 337, 455, 15, "r"),
    ("saratoga", "Saratoga", 427, 642, 5, "l"),
    ("los-gatos", "Los Gatos", 485, 673, 4, "r"),
]
# other places already named on the site (county list), shown as open circles
NEARBY = [("San Francisco", 107, 114, "r"), ("Fremont", 460, 342, "r"), ("San Jose", 543, 559, "r")]
HOME = ("Campbell", 493, 611)


def _label(name, sub, side, dark=False, dim=False):
    """Rounded label card next to a pin. Coordinates are relative to the pin."""
    w = max(len(name) * 8.4, len(sub) * 6.4) + 26
    h = 44
    x = 14 if side == "r" else -14 - w
    y = -h / 2
    cls = "am-lb" + (" am-lb--dark" if dark else "") + (" am-lb--dim" if dim else "")
    return (f'<g class="{cls}"><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="10"/>'
            f'<text class="am-lb__n" x="{x + 13:.0f}" y="{y + 19:.0f}">{E(name)}</text>'
            f'<text class="am-lb__s" x="{x + 13:.0f}" y="{y + 34:.0f}">{E(sub)}</text></g>')


def _pin(kind, name, x, y, sub, side, meta, href=""):
    dark = kind == "home"
    dot = {"home": '<circle class="am-ring" r="9"/><circle class="am-hq" r="9"/><circle class="am-hq__c" r="3.6"/>',
           "city": '<circle class="am-dot" r="6.5"/>',
           "near": '<circle class="am-open" r="6"/>'}[kind]
    data = f'data-x="{x}" data-y="{y}" data-name="{E(name)}" data-meta="{E(meta)}"' + (f' data-href="{href}"' if href else "")
    return (f'<g class="am-pin am-pin--{kind}" transform="translate({x} {y})" tabindex="0" role="button" '
            f'aria-label="Zoom to {E(name)}. {E(meta)}" {data}><g class="am-k">{dot}{_label(name, sub, side, dark=dark, dim=kind == "near")}</g></g>')


def area_map():
    roads = "".join(f'<path class="am-road__c" d="{smooth(p)}"/>' for p in ROADS.values())
    roads += "".join(f'<path class="am-road" d="{smooth(p)}"/>' for p in ROADS.values())
    shields = "".join(f'<g class="am-k-s" transform="translate({x} {y})"><g class="am-k"><rect class="am-shield" x="-15" y="-10" width="30" height="20" rx="5"/>'
                      f'<text class="am-shield__t" y="4">{n}</text></g></g>' for n, x, y in SHIELDS)
    lines = "".join(f'<path class="am-county" d="{smooth(p)}"/>' for p in COUNTY_LINES)
    clabels = "".join(f'<g transform="translate({x} {y})"><g class="am-k"><text class="am-cl">{E(t.upper())}</text></g></g>' for t, x, y in COUNTY_LABELS)
    contours = "".join(f'<ellipse class="am-topo" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})"/>'
                       for cx, cy, rot in [(272, 640, -42), (646, 560, -60)] for rx, ry in [(70, 34), (48, 22), (26, 11)])
    pins = "".join(_pin("near", n, x, y, "Also served", s, "Also served from our Campbell office") for n, x, y, s in NEARBY)
    pins += "".join(_pin("city", n, x, y, f"~{mi} mi", s, f"About {mi} miles from our Campbell office", f"{slug}.html") for slug, n, x, y, mi, s in CITIES)
    pins += _pin("home", HOME[0], HOME[1], HOME[2], "Home base", "r", "Home base: our office at 710 E McGlincy Ln, Campbell")
    svg = f'''<svg class="am-svg" viewBox="{VB_X} {VB_Y} {VB_W} {VB_H}" preserveAspectRatio="xMidYMid slice">
  <rect class="am-land" x="-400" y="-400" width="1500" height="1560"/>
  {contours}
  <path class="am-water" d="{smooth(OCEAN, True)}"/>
  <path class="am-water" d="{smooth(BAY, True)}"/>
  <path class="am-area" d="{smooth(SERVICE, True)}"/>
  {lines}
  {roads}
  <g transform="translate(26 520)"><g class="am-k"><text class="am-sea" transform="rotate(-90)">PACIFIC OCEAN</text></g></g>
  <g transform="translate(300 292)"><g class="am-k"><text class="am-sea" transform="rotate(50)">SAN FRANCISCO BAY</text></g></g>
  <g transform="translate(226 610)"><g class="am-k"><text class="am-mtn" transform="rotate(-52)">Santa Cruz Mountains</text></g></g>
  {clabels}
  {shields}
  {pins}
</svg>'''
    return f'''<div class="amap rv" data-amap="{VB_X} {VB_Y} {VB_W} {VB_H}">
  <p class="sr-only">Map of the REF Builders service area around the San Francisco Bay. Our office is in Campbell. Service cities: Los Gatos (about 4 miles away), Saratoga (about 5), Palo Alto (about 15), Stanford (about 16) and Redwood City (about 21). We also serve San Jose, Fremont and San Francisco.</p>
  {svg}
  <div class="amap__now" aria-live="polite"><small>Now viewing</small><b data-am-name>Full service area</b><span class="amap__meta" data-am-meta>Office in Campbell, CA</span><span class="amap__acts"><a class="amap__go" data-am-go hidden href="#">View city page</a><button type="button" class="amap__reset" data-am-reset hidden>Full area</button></span></div>
  <div class="amap__compass" aria-hidden="true"><svg viewBox="0 0 12 12"><path d="M6 1 9 9 6 7.4 3 9z"/></svg>N</div>
  <ul class="amap__legend" aria-hidden="true"><li><i class="lg-home"></i>Home base</li><li><i class="lg-city"></i>Service city</li><li><i class="lg-area"></i>Service area</li></ul>
  <div class="amap__hint" aria-hidden="true">Tap a pin to zoom in</div>
  <div class="amap__scale" aria-hidden="true"><span data-am-scale></span><small>5 mi</small></div>
</div>'''
