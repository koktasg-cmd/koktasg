"""Professional animated vertical promo renderer (silent video; audio is mixed later)."""
import math, subprocess, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

R = '/home/claude'
FONT = f'{R}/ninniko/legal-site/Nunito.ttf'
W, H, FPS = 1080, 1920, 30
NAVY = (30, 37, 71)

@lru_cache(None)
def font(size, weight='ExtraBold'):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def ease_out_cubic(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_in_cubic(x): x = min(max(x, 0), 1); return x ** 3
def ease_out_back(x, s=1.6):
    x = min(max(x, 0), 1); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2

def rounded_mask(size, r):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255); return m

def shadow(size, r, blur=40, alpha=110, off=(0, 30), pad=90):
    s = Image.new('RGBA', (size[0] + pad * 2, size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([pad + off[0], pad + off[1], pad + off[0] + size[0], pad + off[1] + size[1]], r, fill=(20, 16, 50, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad

def phone(screen_path, sw=540):
    """Device mockup with bezel, island and soft shadow. Returns RGBA and its (ox, oy) of the device inside."""
    im = Image.open(screen_path).convert('RGB')
    sh = int(im.height * sw / im.width)
    im = im.resize((sw, sh), Image.LANCZOS)
    bz = 16; r_in = 58; r_out = r_in + bz
    dw, dh = sw + bz * 2, sh + bz * 2
    dev = Image.new('RGBA', (dw, dh), (0, 0, 0, 0))
    d = ImageDraw.Draw(dev)
    d.rounded_rectangle([0, 0, dw - 1, dh - 1], r_out, fill=(22, 24, 40, 255))
    d.rounded_rectangle([3, 3, dw - 4, dh - 4], r_out - 3, outline=(70, 74, 100, 255), width=2)
    scr = im.convert('RGBA'); scr.putalpha(rounded_mask((sw, sh), r_in))
    dev.alpha_composite(scr, (bz, bz))
    s, pad = shadow((dw, dh), r_out, blur=45, alpha=120, off=(0, 40))
    out = Image.new('RGBA', s.size, (0, 0, 0, 0)); out.alpha_composite(s); out.alpha_composite(dev, (pad, pad))
    return out, pad

def gradient(top, bot, w=W, h=H):
    g = Image.linear_gradient('L').resize((w, h))
    a = Image.new('RGB', (w, h), top); b = Image.new('RGB', (w, h), bot)
    return Image.composite(b, a, g)

def blob(rad, color, alpha=150):
    s = rad * 2 + 240
    m = Image.new('L', (s, s), 0)
    ImageDraw.Draw(m).ellipse([120, 120, 120 + rad * 2, 120 + rad * 2], fill=alpha)
    b = Image.new('RGBA', (s, s), (*color, 0)); b.putalpha(m.filter(ImageFilter.GaussianBlur(80)))
    return b

def text_img(text, f, fill):
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    asc, desc = f.getmetrics()
    w = int(d.textlength(text, font=f)) + 12
    im = Image.new('RGBA', (w, asc + desc + 8), (*fill[:3], 0))
    ImageDraw.Draw(im).text((6, 4 + asc), text, font=f, fill=fill, anchor='ls')
    return im

def pill(text, f, fg, bg, padx=34, pady=18, dot=None):
    t = text_img(text, f, fg)
    extra = 34 if dot else 0
    w, h = t.width + padx * 2 + extra, t.height + pady * 2
    im = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    s, pad = shadow((w, h), h // 2, blur=16, alpha=70, off=(0, 8), pad=30)
    im.alpha_composite(s)
    ImageDraw.Draw(im).rounded_rectangle([30, 30, 30 + w, 30 + h], h // 2, fill=bg)
    if dot: ImageDraw.Draw(im).ellipse([30 + padx - 4, 30 + h // 2 - 11, 30 + padx + 18, 30 + h // 2 + 11], fill=dot)
    im.alpha_composite(t, (30 + padx + extra, 30 + pady))
    return im

def paste(base, im, x, y, alpha=1.0, scale=1.0):
    if alpha <= 0.01: return
    if scale != 1.0:
        nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
        im2 = im.resize((nw, nh), Image.BILINEAR); x += (im.width - nw) // 2; y += (im.height - nh) // 2; im = im2
    if alpha < 0.999:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(x), int(y))) if 0 <= x and 0 <= y and x + im.width <= base.width and y + im.height <= base.height else _safe(base, im, int(x), int(y))

def _safe(base, im, x, y):
    bx0, by0 = max(x, 0), max(y, 0); bx1, by1 = min(x + im.width, base.width), min(y + im.height, base.height)
    if bx1 <= bx0 or by1 <= by0: return
    base.alpha_composite(im.crop((bx0 - x, by0 - y, bx1 - x, by1 - y)), (bx0, by0))

class Promo:
    def __init__(self, theme):
        self.t = theme
        self.bg = gradient(theme['top'], theme['bot']).convert('RGBA')
        self.blobs = [(blob(260, theme['blob1'], 120), 0.12, 0.18, 0.0), (blob(320, theme['blob2'], 110), 0.85, 0.55, 2.0),
                      (blob(220, theme['blob1'], 90), 0.25, 0.88, 4.0)]
        ic = Image.open(theme['icon']).convert('RGB').resize((76, 76), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((76, 76), 20))
        self.icon_small = ic
        nm = text_img(theme['name'], font(38, 'Black'), theme['text'])
        chip = Image.new('RGBA', (76 + 18 + nm.width + 10, 80), (0, 0, 0, 0)); chip.alpha_composite(ic, (0, 2)); chip.alpha_composite(nm, (94, 40 - nm.height // 2))
        self.brand = chip
        gp = Image.open(f'{R}/ninniko-oyun-bahcesi/store/afis/rozetler/google-play-tr.png').convert('RGBA'); gp = gp.crop(gp.getbbox())
        ap = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'appstore.png')).convert('RGBA'); ap = ap.crop(ap.getbbox())
        bh = 112
        self.badges = [b.resize((int(b.width * bh / b.height), bh), Image.LANCZOS) for b in (gp, ap)]

    def background(self, t):
        f = self.bg.copy()
        for b, fx, fy, ph in self.blobs:
            x = fx * W + 60 * math.sin(t * 0.5 + ph) - b.width / 2; y = fy * H + 50 * math.cos(t * 0.4 + ph) - b.height / 2
            _safe(f, b, int(x), int(y))
        return f

    def headline_layers(self, l1, l2, size, c1=None, c2=None):
        """Return list of (word_img, x, y) laid out centered from y=0; and total height."""
        out, y = [], 0
        for text, col in ((l1, c1 or self.t['text']), (l2, c2 or self.t['accent'])):
            if not text: continue
            f = font(size, 'Black')
            words = text.split(); imgs = [text_img(w, f, col) for w in words]; sp = int(size * 0.28)
            # wrap
            lines, cur, cw = [], [], 0
            for im in imgs:
                if cur and cw + sp + im.width > W - 120: lines.append(cur); cur, cw = [], 0
                cw += (sp if cur else 0) + im.width; cur.append(im)
            lines.append(cur)
            for ln in lines:
                lw = sum(i.width for i in ln) + sp * (len(ln) - 1); x = (W - lw) // 2
                for im in ln: out.append((im, x, y)); x += im.width + sp
                y += int(size * 1.12)
        return out, y

    def render(self, scenes, total, out_path):
        prepared = []
        for s in scenes:
            p = dict(s)
            if s['kind'] == 'phone':
                p['dev'], p['pad'] = phone(s['screen'], s.get('sw', 580))
                p['words'], p['hh'] = self.headline_layers(s['h1'], s.get('h2', ''), s.get('size', 80))
                if s.get('chip'): p['chip_img'] = pill(s['chip'], font(40, 'ExtraBold'), self.t['text'], (255, 255, 255, 245), dot=self.t['accent'])
            elif s['kind'] == 'art':
                im = Image.open(s['image']).convert('RGB'); sc = max(W / im.width, H / im.height) * 1.08
                p['art'] = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS).convert('RGBA')
                p['words'], p['hh'] = self.headline_layers(s['h1'], s.get('h2', ''), s.get('size', 84), (255, 255, 255), (255, 214, 102))
            elif s['kind'] == 'card':
                im = Image.open(s['image']).convert('RGB'); chh = s.get('card_h', 1540); cw = int(im.width * chh / im.height)
                im = im.resize((cw, chh), Image.LANCZOS).convert('RGBA'); im.putalpha(rounded_mask(im.size, 54))
                sh, pad = shadow(im.size, 54, blur=40, alpha=110); c = Image.new('RGBA', sh.size, (0, 0, 0, 0)); c.alpha_composite(sh); c.alpha_composite(im, (pad, pad))
                p['card'], p['pad'] = c, pad
            prepared.append(p)
        proc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out_path], stdin=subprocess.PIPE)
        n = int(total * FPS)
        for i in range(n):
            t = i / FPS
            f = self.background(t)
            for s in prepared:
                if s['t0'] - 0.01 <= t < s['t1'] + 0.45:
                    getattr(self, 'draw_' + s['kind'])(f, s, t)
            # brand chip + progress
            if not any(s['kind'] in ('end', 'art') and s['t0'] <= t < s['t1'] for s in prepared):
                paste(f, self.brand, 60, 96, alpha=ease_out_cubic(t / 0.5))
            pr = min(t / total, 1); d = ImageDraw.Draw(f)
            d.rounded_rectangle([60, 56, W - 60, 62], 3, fill=(*self.t['text'], 40))
            d.rounded_rectangle([60, 56, 60 + int((W - 120) * pr), 62], 3, fill=(*self.t['accent'], 255))
            proc.stdin.write(f.convert('RGB').tobytes())
        proc.stdin.close(); proc.wait()

    def _exit(self, s, t):
        """Returns exit progress 0..1 during the last 0.4s overlap after t1."""
        return ease_out_cubic((t - s['t1']) / 0.35) if t >= s['t1'] else 0.0

    def draw_words(self, f, s, t, y0, stagger=0.07):
        ex = self._exit(s, t)
        for k, (im, x, y) in enumerate(s['words']):
            p = (t - s['t0'] - 0.05 - k * stagger) / 0.45
            if p <= 0: continue
            a = ease_out_cubic(p) * (1 - ex); sc = 0.7 + 0.3 * ease_out_back(p)
            paste(f, im, x - ex * 300, y0 + y + (1 - ease_out_cubic(p)) * 40, alpha=a, scale=sc)

    def draw_phone(self, f, s, t):
        dev, pad = s['dev'], s['pad']
        p = ease_out_cubic((t - s['t0'] - 0.1) / 0.55); ex = self._exit(s, t)
        x = (W - dev.width) // 2 + (1 - p) * 800 - ex * 900
        top = s.get('phone_y', s.get('head_y', 190) + s['hh'] + 60)
        y = top - pad + 8 * math.sin(t * 2.2) + (1 - p) * 120
        paste(f, dev, x, y, alpha=min(1, p * 1.4) * (1 - ex))
        self.draw_words(f, s, t, s.get('head_y', 190))
        if 'chip_img' in s:
            cp = (t - s['t0'] - 0.75) / 0.45
            if cp > 0:
                ci = s['chip_img']; side = s.get('chip_side', 'right')
                cx = (W - ci.width - 20) if side == 'right' else 20
                paste(f, ci, cx - ex * 900, s.get('chip_y', 1320) + 6 * math.sin(t * 2.6 + 1), alpha=ease_out_cubic(cp) * (1 - ex), scale=0.6 + 0.4 * ease_out_back(cp))

    def draw_art(self, f, s, t):
        art = s['art']; dur = s['t1'] - s['t0']; k = (t - s['t0']) / dur
        sc = 1.0 + 0.06 * k
        nw, nh = int(art.width * sc), int(art.height * sc)
        im = art.resize((nw, nh), Image.BILINEAR)
        ex = self._exit(s, t)
        a = min(1, (t - s['t0']) / 0.3) * (1 - ex)
        paste(f, im, (W - nw) // 2, (H - nh) // 2, alpha=a)
        # bottom scrim for legibility
        if 'scrim' not in s:
            g = Image.linear_gradient('L').resize((W, 760)); sc_ = Image.new('RGBA', (W, 760), (*NAVY, 0)); sc_.putalpha(g.point(lambda v: int(min(255, v * 1.3) * 0.85))); s['scrim'] = sc_
        paste(f, s['scrim'], 0, H - 760, alpha=a)
        words = [(im_, x, y) for im_, x, y in s['words']]
        self.draw_words(f, dict(s, words=words), t, s.get('head_y', 1380))

    def draw_card(self, f, s, t):
        c = s['card']; p = ease_out_cubic((t - s['t0'] - 0.1) / 0.55); ex = self._exit(s, t)
        dur = s['t1'] - s['t0']; k = (t - s['t0']) / dur
        sc = (0.9 + 0.1 * p) * (1 + 0.025 * k)
        x = (W - c.width) // 2 + (1 - p) * 700 - ex * 900; y = s.get('card_y', 210) - s['pad']
        paste(f, c, x, y, alpha=min(1, p * 1.4) * (1 - ex), scale=sc)

    def draw_end(self, f, s, t):
        if 'ic' not in s:
            ic = Image.open(self.t['icon']).convert('RGB').resize((340, 340), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((340, 340), 80))
            sh, pad = shadow((340, 340), 80, blur=40, alpha=120); c = Image.new('RGBA', sh.size, (0, 0, 0, 0)); c.alpha_composite(sh); c.alpha_composite(ic, (pad, pad))
            s['ic'], s['icpad'] = c, pad
            s['nm'] = text_img(self.t['name'], font(84 if len(self.t['name']) < 16 else 70, 'Black'), self.t['text'])
            s['sub'] = text_img(self.t['sub'], font(46, 'Bold'), self.t['accent'])
            s['pills'] = [pill(x, font(38, 'ExtraBold'), self.t['text'], (255, 255, 255, 240)) for x in s['pills_text']]
            s['url'] = text_img('ninniko.com', font(40, 'Bold'), self.t['text'])
        d = t - s['t0']
        p = ease_out_back(d / 0.6, 1.3)
        paste(f, s['ic'], (W - s['ic'].width) // 2, 440 - s['icpad'], alpha=min(1, d / 0.3), scale=max(0.01, p))
        for k, (im, y) in enumerate(((s['nm'], 850), (s['sub'], 960))):
            q = ease_out_cubic((d - 0.25 - k * 0.12) / 0.45)
            if q > 0: paste(f, im, (W - im.width) // 2, y + (1 - q) * 40, alpha=q)
        # pills row(s)
        pills = s['pills']; gap = 16; tw = sum(p_.width for p_ in pills) - 60 * len(pills) + gap * (len(pills) - 1)
        if tw < W - 80:
            x = (W - tw) // 2 - 30
            for k, pl in enumerate(pills):
                q = ease_out_cubic((d - 0.5 - k * 0.1) / 0.4)
                if q > 0: paste(f, pl, x, 1070 + (1 - q) * 30, alpha=q)
                x += pl.width - 60 + gap
        else:
            for k, pl in enumerate(pills):
                q = ease_out_cubic((d - 0.5 - k * 0.1) / 0.4)
                if q > 0: paste(f, pl, (W - pl.width) // 2, 1070 + k * 110 + (1 - q) * 30, alpha=q)
        by = 1270 if tw < W - 80 else 1310 + 110 * (len(pills) - 1)
        q = ease_out_cubic((d - 0.8) / 0.45)
        if q > 0:
            b1, b2 = self.badges; gap = 28; tw2 = b1.width + b2.width + gap; x = (W - tw2) // 2
            paste(f, b1, x, by + (1 - q) * 40, alpha=q); paste(f, b2, x + b1.width + gap, by + (1 - q) * 40, alpha=q)
            paste(f, s['url'], (W - s['url'].width) // 2, by + 150, alpha=q)
