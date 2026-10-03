#!/usr/bin/env python3
"""
Generates seamless PCB-style background tiles (dark + light) as SVG.

    python3 tools/gen_pcb.py            # writes public/pcb-dark.svg and public/pcb-light.svg
    python3 tools/gen_pcb.py 12         # same, with another random seed

How it works
  * The board is a torus: everything is drawn up to 9 times (shifted by one tile in every
    direction) so the pattern repeats with no visible seam.
  * Routing happens on a grid (G px). Traces only run horizontal, vertical or at 45 degrees,
    like on a real PCB, and keep one grid step of clearance from each other.
  * A few "chips" fan out parallel buses (offset polylines with mitered corners); the rest of
    the space is filled with random single traces ending in vias and pads.
"""
import math
import os
import random
import sys

W = H = 960          # tile size in px
G = 12               # routing grid in px
N = W // G           # grid nodes per side
DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

THEMES = {
    # opacity values are tuned so the text on top stays readable
    "dark":  dict(main="#22d3ee", accent="#f0468a", trace=0.16, pad=0.13, body=0.24, acc=0.15),
    "light": dict(main="#0e7490", accent="#d6246e", trace=0.12, pad=0.10, body=0.18, acc=0.10),
}


def unit(d):
    ux, uy = DIRS[d]
    n = math.hypot(ux, uy)
    return ux / n, uy / n


class Board:
    def __init__(self, seed):
        self.r = random.Random(seed)
        self.occ = {}     # grid node -> trace id
        self.items = []   # (svg, bbox)
        self.tid = 0

    # ---- occupancy -------------------------------------------------------------------
    def key(self, x, y):
        return (x % N, y % N)

    def clear(self, x, y, tid):
        """node has no foreign trace in its 3x3 neighbourhood"""
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                o = self.occ.get(self.key(x + dx, y + dy))
                if o is not None and o != tid:
                    return False
        return True

    def new_id(self):
        self.tid += 1
        return self.tid

    def add(self, svg, pts, pad=8):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.items.append((svg, (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)))

    # ---- primitives ------------------------------------------------------------------
    @staticmethod
    def path(pts, cls="t"):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<path class="{cls}" d="{d}"/>'

    @staticmethod
    def via(x, y):
        return (f'<circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="4"/>'
                f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="1.4"/>')

    @staticmethod
    def pad(x, y):
        return f'<circle class="pad" cx="{x:.1f}" cy="{y:.1f}" r="3.4"/>'

    # ---- chip + bus ------------------------------------------------------------------
    def place_chip(self):
        r = self.r
        for _ in range(80):
            pins = r.choice([6, 7, 8])
            pitch = 10
            side = r.randrange(4)
            o = DIRS[side * 2]
            t = (-o[1], o[0])
            along = pins * pitch + 14
            depth = r.choice([48, 60, 72])
            cx, cy = r.randrange(N) * G, r.randrange(N) * G
            hw, hh = (depth / 2, along / 2) if o[0] != 0 else (along / 2, depth / 2)
            x0, y0, x1, y1 = cx - hw, cy - hh, cx + hw, cy + hh
            halo = [(ix, iy)
                    for ix in range(int(x0 // G) - 1, int(x1 // G) + 3)
                    for iy in range(int(y0 // G) - 1, int(y1 // G) + 3)]
            if any(self.occ.get(self.key(ix, iy)) is not None for ix, iy in halo):
                continue
            tid = self.new_id()
            bus = self.make_bus(tid, cx, cy, o, t, depth, pins, pitch)
            if bus is None:
                continue
            for ix, iy in halo:
                self.occ[self.key(ix, iy)] = tid
            self.draw_chip(cx, cy, hw, hh, o, t, depth, pins, pitch)
            for svg, pts in bus:
                self.add(svg, pts)
            return True
        return False

    def draw_chip(self, cx, cy, hw, hh, o, t, depth, pins, pitch):
        parts = [f'<rect class="body" x="{cx - hw:.1f}" y="{cy - hh:.1f}" '
                 f'width="{2 * hw:.1f}" height="{2 * hh:.1f}" rx="2.5"/>']
        for sign in (1, -1):                       # pins on the outward edge and the opposite one
            for k in range(pins):
                off = (k - (pins - 1) / 2) * pitch
                ex = cx + sign * o[0] * depth / 2 + t[0] * off
                ey = cy + sign * o[1] * depth / 2 + t[1] * off
                px, py = ex + sign * o[0] * 4, ey + sign * o[1] * 4
                parts.append(f'<rect class="pin" x="{px - (4 if o[0] else 2):.1f}" '
                             f'y="{py - (2 if o[0] else 4):.1f}" '
                             f'width="{8 if o[0] else 4}" height="{4 if o[0] else 8}"/>')
        # pin-1 marker
        mx = cx - hw + 7
        my = cy - hh + 7
        parts.append(f'<circle class="dot" cx="{mx:.1f}" cy="{my:.1f}" r="2"/>')
        pts = [(cx - hw - 10, cy - hh - 10), (cx + hw + 10, cy + hh + 10)]
        self.add("".join(parts), pts)

    def make_bus(self, tid, cx, cy, o, t, depth, n, pitch):
        r = self.r
        sx = cx + o[0] * (depth / 2 + 8)
        sy = cy + o[1] * (depth / 2 + 8)
        d0 = DIRS.index(o)
        for _ in range(50):
            verts = [(sx, sy)]
            d, x, y = d0, sx, sy
            dirs = []
            for i in range(r.randint(3, 5)):
                length = G * (r.randint(4, 9) if i == 0 else r.randint(3, 8))
                ux, uy = DIRS[d]
                x, y = x + ux * length, y + uy * length
                verts.append((x, y))
                dirs.append(d)
                d = (d + r.choice([-1, 1])) % 8
            lines = []
            for k in range(n):
                off = (k - (n - 1) / 2) * pitch
                us = [unit(dd) for dd in dirs]
                ns = [(-u[1], u[0]) for u in us]
                pts = [(verts[0][0] + off * ns[0][0], verts[0][1] + off * ns[0][1])]
                for i in range(1, len(verts) - 1):
                    n1, n2 = ns[i - 1], ns[i]
                    den = 1 + n1[0] * n2[0] + n1[1] * n2[1]
                    pts.append((verts[i][0] + off * (n1[0] + n2[0]) / den,
                                verts[i][1] + off * (n1[1] + n2[1]) / den))
                pts.append((verts[-1][0] + off * ns[-1][0], verts[-1][1] + off * ns[-1][1]))
                # stagger the line ends
                cut = r.choice([0, 6, 12, 18, 24, 30])
                ux, uy = us[-1]
                ex, ey = pts[-1]
                seg = math.hypot(ex - pts[-2][0], ey - pts[-2][1])
                cut = min(cut, max(0, seg - 14))
                pts[-1] = (ex - ux * cut, ey - uy * cut)
                lines.append(pts)
            # occupancy test
            cells = set()
            ok = True
            for pts in lines:
                for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                    steps = max(1, int(math.hypot(bx - ax, by - ay) / 4))
                    for s in range(steps + 1):
                        px = ax + (bx - ax) * s / steps
                        py = ay + (by - ay) * s / steps
                        c = (round(px / G), round(py / G))
                        cells.add(c)
                        if not self.clear(c[0], c[1], tid):
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
            if not ok:
                continue
            for c in cells:
                self.occ[self.key(*c)] = tid
            out = []
            for pts in lines:
                accent = r.random() < 0.08
                svg = self.path(pts, "a" if accent else "t") + self.via(*pts[-1])
                out.append((svg, pts))
            return out
        return None

    # ---- random single traces -------------------------------------------------------------
    def random_trace(self):
        r = self.r
        tid = self.new_id()
        sx, sy = r.randrange(N), r.randrange(N)
        if self.occ.get(self.key(sx, sy)) is not None or not self.clear(sx, sy, tid):
            return False
        d = r.randrange(8)
        x, y = sx, sy
        own = {self.key(x, y)}
        nodes = [(x, y)]
        verts = [(x * G, y * G)]
        budget = r.randint(10, 46)
        while len(nodes) < budget:
            want = r.randint(2, 9)
            moved = 0
            for _ in range(want):
                nx, ny = x + DIRS[d][0], y + DIRS[d][1]
                k = self.key(nx, ny)
                if k in own or self.occ.get(k) is not None or not self.clear(nx, ny, tid):
                    break
                x, y = nx, ny
                own.add(k)
                nodes.append((x, y))
                moved += 1
            if moved:
                verts.append((x * G, y * G))
            turn = r.choice([-1, 1])
            if not moved:
                # blocked right away: try the other way once, else stop
                alt = (d + turn) % 8
                nx, ny = x + DIRS[alt][0], y + DIRS[alt][1]
                if self.key(nx, ny) in own or self.occ.get(self.key(nx, ny)) is not None \
                        or not self.clear(nx, ny, tid):
                    break
            d = (d + turn) % 8
        if len(nodes) < 8 or len(verts) < 2:
            return False
        for nx, ny in nodes:
            self.occ[self.key(nx, ny)] = tid
        accent = r.random() < 0.1
        svg = self.path(verts, "a" if accent else "t")
        ex, ey = verts[-1]
        svg += self.via(ex, ey) if r.random() < 0.6 else self.pad(ex, ey)
        bx, by = verts[0]
        svg += self.pad(bx, by) if r.random() < 0.5 else self.via(bx, by)
        self.add(svg, verts)
        return True

    # ---- output -----------------------------------------------------------------------------
    def render(self, theme):
        c = THEMES[theme]
        style = (
            f".t,.a{{fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}}"
            f".t{{stroke:{c['main']};stroke-opacity:{c['trace']}}}"
            f".a{{stroke:{c['accent']};stroke-opacity:{c['acc']}}}"
            f".ring{{fill:none;stroke:{c['main']};stroke-opacity:{c['trace'] + 0.04};stroke-width:1.5}}"
            f".dot{{fill:{c['main']};fill-opacity:{c['trace'] + 0.04}}}"
            f".pad{{fill:{c['main']};fill-opacity:{c['pad']}}}"
            f".body{{fill:{c['main']};fill-opacity:0.03;stroke:{c['main']};stroke-opacity:{c['body']};stroke-width:1.5}}"
            f".pin{{fill:{c['main']};fill-opacity:{c['body']}}}"
        )
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
               f"<style>{style}</style>"]
        for svg, (x0, y0, x1, y1) in self.items:
            for sx in (-1, 0, 1):
                for sy in (-1, 0, 1):
                    if x1 + sx * W >= 0 and x0 + sx * W <= W and y1 + sy * H >= 0 and y0 + sy * H <= H:
                        if sx == 0 and sy == 0:
                            out.append(f"<g>{svg}</g>")
                        else:
                            out.append(f'<g transform="translate({sx * W} {sy * H})">{svg}</g>')
        out.append("</svg>")
        return "\n".join(out)


def build(seed):
    b = Board(seed)
    for _ in range(1):
        b.place_chip()
    placed = 0
    for _ in range(15):
        if b.random_trace():
            placed += 1
    return b, placed


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    board, placed = build(seed)
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "..", "public")
    os.makedirs(assets, exist_ok=True)
    for theme in THEMES:
        with open(os.path.join(assets, f"pcb-{theme}.svg"), "w") as f:
            f.write(board.render(theme))
    print(f"seed {seed}: {len(board.items)} items ({placed} random traces)")
