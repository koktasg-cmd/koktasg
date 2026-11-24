"""pro.py eklentisi: 'zoom' sahnesi (ekranın bir bölümünü büyütülmüş kart olarak gösterir)."""
import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro import *

import pro as _pro
_orig_pill = _pro.pill

class Promo2(Promo):
    def __init__(self, theme):
        super().__init__(theme)
        pt = theme.get('pilltext')
        def _pill(text, f, fg, bg, **kw):
            return _orig_pill(text, f, pt if (pt and tuple(fg[:3]) == tuple(theme['text'][:3])) else fg, bg, **kw)
        _pro.pill = _pill
        globals()['pill'] = _pill

    def prep_zoom(self, s):
        im = Image.open(s['image']).convert('RGB')
        if s.get('crop'): im = im.crop(s['crop'])
        zw = s.get('zw', 940); zh = int(im.height * zw / im.width)
        im = im.resize((zw, zh), Image.LANCZOS).convert('RGBA'); im.putalpha(rounded_mask(im.size, 44))
        frame = Image.new('RGBA', (zw + 24, zh + 24), (0, 0, 0, 0))
        ImageDraw.Draw(frame).rounded_rectangle([0, 0, zw + 23, zh + 23], 54, fill=(255, 255, 255, 255))
        frame.alpha_composite(im, (12, 12))
        sh, pad = shadow(frame.size, 54, blur=40, alpha=110)
        c = Image.new('RGBA', sh.size, (0, 0, 0, 0)); c.alpha_composite(sh); c.alpha_composite(frame, (pad, pad))
        s['zimg'], s['zpad'] = c, pad
        s['words'], s['hh'] = self.headline_layers(s['h1'], s.get('h2', ''), s.get('size', 84))
        if s.get('chip'): s['chip_img'] = pill(s['chip'], font(40, 'ExtraBold'), self.t['text'], (255, 255, 255, 245), dot=self.t['accent'])
        return s

    def draw_zoom(self, f, s, t):
        c, pad = s['zimg'], s['zpad']
        p = ease_out_cubic((t - s['t0'] - 0.1) / 0.55); ex = self._exit(s, t)
        k = (t - s['t0']) / max(0.1, s['t1'] - s['t0'])
        head_y = s.get('head_y', 330)
        cy = s.get('card_y', head_y + s['hh'] + 90)
        x = (W - c.width) // 2 - ex * 900
        y = cy - pad + (1 - p) * 160 + 6 * math.sin(t * 2.0)
        paste(f, c, x, y, alpha=min(1, p * 1.4) * (1 - ex), scale=(0.86 + 0.14 * ease_out_back(p, 1.2)) * (1 + 0.02 * k))
        self.draw_words(f, s, t, head_y)
        if 'chip_img' in s:
            cp = (t - s['t0'] - 0.75) / 0.45
            if cp > 0:
                ci = s['chip_img']
                paste(f, ci, (W - ci.width) // 2 - ex * 900, s.get('chip_y', cy + c.height - 2 * pad + 60), alpha=ease_out_cubic(cp) * (1 - ex), scale=0.6 + 0.4 * ease_out_back(cp))

    def render(self, scenes, total, out_path):
        for s in scenes:
            if s['kind'] == 'zoom' and 'zimg' not in s: self.prep_zoom(s)
        return super().render(scenes, total, out_path)

def sound_card(path, title, rows, accent=(228, 108, 80), text=(45, 52, 102)):
    """Uygulamadaki ses listesini anlatan sade kart (ekran görüntüsü yoksa)."""
    w, h = 540, 150 + 92 * len(rows)
    im = Image.new('RGB', (w, h), (255, 250, 246)); d = ImageDraw.Draw(im)
    d.text((32, 40), title, font=font(40, 'Black'), fill=text)
    y = 120
    for name, sub in rows:
        d.rounded_rectangle([24, y, w - 24, y + 76], 22, fill=(255, 255, 255), outline=(240, 226, 218), width=2)
        d.ellipse([42, y + 20, 78, y + 56], fill=accent)
        d.polygon([(55, y + 28), (55, y + 48), (70, y + 38)], fill=(255, 255, 255))
        d.text((96, y + 14), name, font=font(28, 'ExtraBold'), fill=text)
        d.text((96, y + 46), sub, font=font(20, 'SemiBold'), fill=(130, 134, 160))
        y += 92
    im.save(path); return path
