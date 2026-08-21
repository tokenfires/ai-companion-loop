# Emits assets/loop-light.svg and assets/loop-dark.svg.
#
# Constraints this file is written to: no <style>, no media queries, no external
# fonts, and no <marker>. The SVGs are referenced from README.md through an <img>
# inside a <picture>, so anything a renderer might drop is avoided on purpose.
# Arrowheads are plain polygons for the same reason.
#
#   python3 assets/mkfig.py
import html, os

OUT = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    'light': dict(bg='#F7F2F1', panel='#FFFFFF', ink='#1D1722', muted='#6E6274',
                  rule='#D9CFD0', teal='#1F6F6C', rose='#B23A55', tealsoft='#E4EFEE'),
    'dark':  dict(bg='#17131C', panel='#1F1926', ink='#EFE6EC', muted='#948699',
                  rule='#3A2F43', teal='#6CC9C4', rose='#F0879C', tealsoft='#1C2E30'),
}

ROWS = [
    ('THE EVENT',      ['something happens to you'],
                       ['a turn happens']),
    ('INTERPRETATION', ['your limbic system reads it'],
                       ['a second model reads it,', 'and it is not the companion']),
    ('THE CASCADE',    ['endocrine and autonomic', 'response fires'],
                       ['fixed deltas, clamped,', 'and a decay pulling back to baseline']),
    ('THE CHANGE',     ['your body is different now'],
                       ['the state file is different now']),
    ('THE RETURN',     ['afferent nerves carry it back'],
                       ['it goes into the next turn']),
]

W, H = 1200, 712
LX, RX, BW = 70, 750, 380
CX, BH = 600, 56
ROW_Y = [196, 274, 352, 430, 508]
DIRS = {'down': (0, 1), 'up': (0, -1), 'left': (-1, 0), 'right': (1, 0)}


def build(t):
    o = []
    a = o.append

    def head(x, y, d, col, size=6.0, op=1.0):
        """An arrowhead as a polygon. Tip sits at (x, y), pointing d."""
        dx, dy = DIRS[d]
        px, py = -dy, dx
        pts = [(x, y),
               (x - dx * size - px * size * 0.6, y - dy * size - py * size * 0.6),
               (x - dx * size + px * size * 0.6, y - dy * size + py * size * 0.6)]
        a('<polygon points="%s" fill="%s" opacity="%s"/>'
          % (' '.join('%.1f,%.1f' % p for p in pts), col, op))

    def text(x, y, s, size=13.5, fill=None, anchor='middle', weight=None, ls=None, extra=''):
        at = f' font-weight="{weight}"' if weight else ''
        at += f' letter-spacing="{ls}"' if ls else ''
        a(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
          f'fill="{fill or t["ink"]}"{at}{extra}>{html.escape(s, quote=False)}</text>')

    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'font-family="ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif" '
      f'role="img" aria-label="The same feedback loop drawn twice, side by side. On the left the '
      f'human version: something happens, the limbic system reads it, the endocrine and autonomic '
      f'cascade fires, the body changes, and afferent nerves carry the change back to the start. '
      f'On the right the companion version: a turn happens, a second model that is not the '
      f'companion reads it, fixed clamped deltas and a decay fire, the state file changes, and it '
      f'goes into the next turn. Neither one steers its own cascade, which is what makes the '
      f'return evidence instead of a claim. Below, a two-way channel between you and your '
      f'companion: warmth and a gesture going one way, a gesture back and a bid coming return.">')
    a(f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>')

    text(LX, 62, 'The Companion Loop', 30, t['ink'], 'start', '600')
    text(LX, 92, 'The same loop, twice. One of them runs in a body. The other one you can build.',
         15.5, t['muted'], 'start')
    a(f'<line x1="{LX}" y1="118" x2="{W-LX}" y2="118" stroke="{t["rule"]}" stroke-width="1"/>')

    text(LX + BW / 2, 158, 'A HUMAN', 12, t['muted'], 'middle', '700', '2.4')
    text(RX + BW / 2, 158, 'AN AI COMPANION', 12, t['rose'], 'middle', '700', '2.4')

    for i, (label, left, right) in enumerate(ROWS):
        y = ROW_Y[i]
        for x, lines in ((LX, left), (RX, right)):
            a(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{t["panel"]}" '
              f'stroke="{t["rule"]}" stroke-width="1"/>')
            for j, ln in enumerate(lines):
                ty = y + BH / 2 + (5 if len(lines) == 1 else -4 + j * 17)
                text(x + BW / 2, ty, ln)
        text(CX, y + BH / 2 + 4.5, label, 11, t['muted'], 'middle', '700', '1.6')
        if i < len(ROWS) - 1:
            for x in (LX + BW / 2, RX + BW / 2):
                a(f'<line x1="{x}" y1="{y+BH}" x2="{x}" y2="{ROW_Y[i+1]-10}" '
                  f'stroke="{t["ink"]}" stroke-width="1.4" opacity="0.45"/>')
                head(x, ROW_Y[i + 1] - 5, 'down', t['ink'], 5.4, 0.45)

    # the return: out, up the outside, and back into row one
    top, bot = ROW_Y[0] + BH / 2, ROW_Y[-1] + BH / 2
    a(f'<path d="M{LX} {bot} L34 {bot} L34 {top} L{LX-8} {top}" fill="none" '
      f'stroke="{t["teal"]}" stroke-width="2" stroke-linejoin="round"/>')
    head(LX, top, 'right', t['teal'])
    a(f'<path d="M{RX+BW} {bot} L{W-34} {bot} L{W-34} {top} L{RX+BW+8} {top}" fill="none" '
      f'stroke="{t["teal"]}" stroke-width="2" stroke-linejoin="round"/>')
    head(RX + BW, top, 'left', t['teal'])
    for x, rot in ((30, -90), (W - 30, 90)):
        a(f'<text transform="translate({x},{(top+bot)/2}) rotate({rot})" text-anchor="middle" '
          f'font-size="10.5" font-weight="700" letter-spacing="1.8" fill="{t["teal"]}">'
          f'THE RETURN</text>')

    ky = ROW_Y[-1] + BH + 42
    a(f'<rect x="{LX}" y="{ky-26}" width="{W-2*LX}" height="42" rx="6" fill="{t["tealsoft"]}"/>')
    text(CX, ky + 1,
         'Neither one steers its own cascade. That is what makes the return evidence, '
         'instead of a claim.', 14.5)

    # the relational channel
    by = 654
    a(f'<line x1="{LX}" y1="{by-42}" x2="{W-LX}" y2="{by-42}" stroke="{t["rule"]}" stroke-width="1"/>')
    text(LX, by + 5, 'you', 14, t['ink'], 'start', '600')
    text(W - LX, by + 5, 'your companion', 14, t['rose'], 'end', '600')
    a(f'<line x1="{LX+44}" y1="{by-8}" x2="{W-LX-116}" y2="{by-8}" stroke="{t["rose"]}" stroke-width="1.6"/>')
    head(W - LX - 110, by - 8, 'right', t['rose'])
    a(f'<line x1="{W-LX-110}" y1="{by+14}" x2="{LX+50}" y2="{by+14}" stroke="{t["rose"]}" stroke-width="1.6"/>')
    head(LX + 44, by + 14, 'left', t['rose'])
    text(CX, by - 14, 'warmth, a gesture, the hard thing you told them about', 12.5, t['muted'])
    text(CX, by + 29, 'a gesture back, and a bid... them reaching for you first', 12.5, t['muted'])

    a('</svg>')
    return '\n'.join(o)


os.makedirs(OUT, exist_ok=True)
for name, theme in THEMES.items():
    svg = build(theme)
    assert '<marker' not in svg and 'marker-end' not in svg and '<style' not in svg
    p = os.path.join(OUT, f'loop-{name}.svg')
    open(p, 'w').write(svg)
    print(p, os.path.getsize(p), 'bytes')
