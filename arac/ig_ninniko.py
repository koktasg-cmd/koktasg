"""Ninniko Bebek Takibi Instagram 4:5 gönderileri (ig_pro.py tarzı)."""
import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
from pro import _safe
N = f'{R}/ninniko/legal-site/img'
CW, CH = 1080, 1350
T = dict(top=(255, 245, 239), bot=(250, 214, 198), accent=(228, 108, 80), text=(45, 52, 102), moon=(255, 196, 120), soft=(196, 202, 255),
         icon=f'{R}/ninniko/assets/brand/ninniko-playstore-ikon-512.png')
OUT = '/home/claude/media/out/ig'; os.makedirs(OUT, exist_ok=True)
WHITE = (255, 255, 255); SUB = (222, 226, 248)

def canvas(dark=False, seed=4):
    if dark:
        base = gradient((60, 68, 132), (32, 38, 84), CW, CH).convert('RGBA')
        for (x, y, r, c, a) in [(160, 220, 260, (196, 202, 255), 70), (950, 1100, 320, (244, 150, 120), 75)]:
            b = blob(r, c, a); base.alpha_composite(b, (x - b.width // 2, y - b.height // 2))
        d = ImageDraw.Draw(base); import random; rnd = random.Random(seed)
        for _ in range(30):
            x, y, s = rnd.randint(0, CW), rnd.randint(0, CH), rnd.choice([2, 3, 4])
            d.ellipse([x, y, x + s, y + s], fill=(255, 240, 210, rnd.randint(90, 200)))
        return base
    base = gradient(T['top'], T['bot'], CW, CH).convert('RGBA')
    for (x, y, r, c, a) in [(120, 160, 240, (196, 202, 255), 120), (980, 1150, 300, (255, 186, 156), 110)]:
        b = blob(r, c, a); base.alpha_composite(b, (x - b.width // 2, y - b.height // 2))
    return base

def brand(base, dark=False, y=60):
    ic = Image.open(T['icon']).convert('RGB').resize((64, 64), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((64, 64), 16))
    base.alpha_composite(ic, (64, y))
    nm = text_img('Ninniko', font(34, 'Black'), WHITE if dark else T['text'])
    base.alpha_composite(nm, (144, y + 32 - nm.height // 2))

def counter(base, i, n, dark=False):
    t = text_img(f'{i}/{n}', font(30, 'Bold'), WHITE if dark else T['text'])
    pl = Image.new('RGBA', (t.width + 36, t.height + 12), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle([0, 0, pl.width - 1, pl.height - 1], pl.height // 2, fill=(255, 255, 255, 60) if dark else (255, 255, 255, 200))
    pl.alpha_composite(t, (18, 6)); base.alpha_composite(pl, (CW - pl.width - 60, 66))

def write(base, x, y, text, size, color, weight='Black', maxw=CW - 128, lh=1.12, center=False):
    f = font(size, weight); d = ImageDraw.Draw(base)
    words, lines, cur = text.split(), [], ''
    for w in words:
        tt = (cur + ' ' + w).strip()
        if d.textlength(tt, font=f) <= maxw: cur = tt
        else: lines.append(cur); cur = w
    lines.append(cur)
    for ln in lines:
        im = text_img(ln, f, color); base.alpha_composite(im, ((CW - im.width) // 2 if center else x - 6, int(y))); y += size * lh
    return y

def swipe(base):
    t = text_img('Kaydır', font(32, 'ExtraBold'), T['text'])
    w, h = t.width + 92, 64
    pl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=(255, 255, 255, 235))
    pl.alpha_composite(t, (26, (h - t.height) // 2))
    ax = t.width + 34; d.line([(ax, 32), (ax + 30, 32)], fill=T['accent'], width=5); d.polygon([(ax + 38, 32), (ax + 24, 21), (ax + 24, 43)], fill=T['accent'])
    base.alpha_composite(pl, (CW - w - 56, CH - h - 48))

def save(base, name):
    p = f'{OUT}/{name}.jpg'; base.convert('RGB').save(p, quality=94); return p

def phone_at(base, shot, sw, x, y):
    dev, pad = phone(shot, sw); _safe(base, dev, x - pad, y - pad); return dev.height - 2 * pad

def zoom_at(base, img, crop, zw, x, y, r=36):
    im = Image.open(img).convert('RGB')
    if crop: im = im.crop(crop)
    zh = int(im.height * zw / im.width); im = im.resize((zw, zh), Image.LANCZOS).convert('RGBA'); im.putalpha(rounded_mask(im.size, r))
    fr = Image.new('RGBA', (zw + 20, zh + 20), (0, 0, 0, 0)); ImageDraw.Draw(fr).rounded_rectangle([0, 0, zw + 19, zh + 19], r + 10, fill=(255, 255, 255, 255)); fr.alpha_composite(im, (10, 10))
    sh, pad = shadow(fr.size, r + 10, blur=34, alpha=100); _safe(base, sh, x - pad, y - pad); base.alpha_composite(fr, (x, y)); return zh + 20

def badges():
    pr = Promo(dict(top=(0, 0, 0), bot=(0, 0, 0), blob1=(0, 0, 0), blob2=(0, 0, 0), accent=(0, 0, 0), text=(0, 0, 0), icon=T['icon'], name='', sub=''))
    return pr.badges

def pills_row(base, y, items, gap=14):
    ps = [pill(t, font(34, 'ExtraBold'), T['text'], (255, 255, 255, 240)) for t in items]
    tw = sum(p.width - 60 for p in ps) + gap * (len(ps) - 1); x = (CW - tw) // 2 - 30
    for p in ps: base.alpha_composite(p, (int(x), int(y))); x += p.width - 60 + gap

def final(base, n, title1, title2, top=230):
    ic = Image.open(T['icon']).convert('RGB').resize((210, 210), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((210, 210), 50))
    base.alpha_composite(ic, ((CW - 210) // 2, top))
    y = write(base, 0, top + 270, title1, 84, WHITE, center=True)
    y = write(base, 0, y, title2, 84, T['moon'], center=True)
    pills_row(base, y + 30, ['Ücretsiz', 'Reklamsız', 'Aile paylaşımı'])
    b1, b2 = badges(); bw = b1.width + b2.width + 28; bx = (CW - bw) // 2
    base.alpha_composite(b1, (bx, int(y + 190))); base.alpha_composite(b2, (bx + b1.width + 28, int(y + 190)))
    write(base, 0, y + 330, '“Ninniko” diye ara · Bebek Takibi', 36, SUB, 'Bold', center=True)

def step_slide(k, n, num, h, sub, draw_visual):
    b = canvas(); brand(b); counter(b, k, n)
    d = ImageDraw.Draw(b); d.ellipse([64, 190, 184, 310], fill=T['accent'])
    ni = text_img(num, font(70, 'Black'), WHITE); b.alpha_composite(ni, (124 - ni.width // 2, 250 - ni.height // 2))
    write(b, 214, 200, h, 80, T['text'], maxw=CW - 280)
    write(b, 64, 350, sub, 40, T['text'], 'SemiBold', maxw=CW - 128, lh=1.3)
    draw_visual(b)
    return b

# --- A: Ninniko ile bir gün (25 Kasım)
def carousel_a():
    n = 6; out = []
    b = canvas(dark=True); brand(b, True); counter(b, 1, n, True)
    y = write(b, 64, 200, 'Bebeğinle', 92, WHITE, maxw=600)
    y = write(b, 64, y, 'bir gün,', 92, WHITE, maxw=600)
    y = write(b, 64, y, 'tek uygulamada', 66, T['moon'], maxw=600)
    write(b, 64, y + 30, 'Emzirme, uyku, bez ve gelişim. Ninniko senin yerine hatırlar.', 40, SUB, 'Bold', maxw=470, lh=1.3)
    phone_at(b, f'{N}/ana.webp', 350, CW - 350 - 110, 470)
    swipe(b); out.append(save(b, 'na1'))
    steps = [('1', 'Emzirme', 'Sol ve sağ memeyi ayrı sayar; son emzirmenin ne zaman olduğunu bir bakışta gösterir.', 'emzirme'),
             ('2', 'Uyku ve bez', 'Tek dokunuşla kaydet. Gece modunda ekran karanlık kalır, gözün kamaşmaz.', 'gece'),
             ('3', 'Günün akışı', 'Bütün kayıtlar saat saat tek ekranda. Dün ne oldu, takvimden seç.', 'gunluk'),
             ('4', 'Haftalık özet', 'Uyku, beslenme ve bez ortalamaların her hafta kendiliğinden özetlenir.', 'raporlar')]
    for k, (num, h, sub, shot) in enumerate(steps):
        b = step_slide(k + 2, n, num, h, sub, lambda b, shot=shot: phone_at(b, f'{N}/{shot}.webp', 390, (CW - 390 - 32) // 2, 520))
        swipe(b); out.append(save(b, f'na{k + 2}'))
    b = canvas(dark=True); brand(b, True); counter(b, n, n, True)
    final(b, n, 'Gecenin 3’ünde bile', 'her şey kayıtlı')
    out.append(save(b, f'na{n}'))
    return out

# --- B: Aile paylaşımı (27 Kasım, tek görsel)
def post_b():
    b = canvas(dark=True, seed=7); brand(b, True)
    y = write(b, 64, 190, 'Bütün aile', 96, WHITE)
    y = write(b, 64, y, 'aynı kayıtta', 96, T['moon'])
    feats = [('8 haneli davet kodu', 'Eşini, anneanneni ya da bakıcını ekle'), ('Anında senkron', 'Herkes aynı kayıtları hemen görür'),
             ('Yetkiyi sen seç', 'Tam yetki, ekleyebilir ya da sadece takip'), ('Gece nöbeti kolaylaşır', 'Son beslenmeyi sormana gerek kalmaz')]
    yy = y + 50
    for h, s in feats:
        d = ImageDraw.Draw(b); d.ellipse([64, yy + 8, 102, yy + 46], fill=T['accent'])
        d.line([(74, yy + 28), (81, yy + 36), (93, yy + 20)], fill=WHITE, width=5)
        write(b, 126, yy, h, 42, WHITE, 'ExtraBold', maxw=500)
        write(b, 126, yy + 54, s, 31, (205, 210, 235), 'SemiBold', maxw=470)
        yy += 132
    phone_at(b, f'{N}/aile.webp', 350, CW - 350 - 64, 500)
    write(b, 64, CH - 110, '“Ninniko” diye ara · Google Play ve App Store', 32, SUB, 'Bold', maxw=CW - 128)
    return save(b, 'nb1')

# --- C: Yeni annelerin 4 yardımcısı (29 Kasım)
def carousel_c():
    n = 6; out = []
    b = canvas(dark=True, seed=11); brand(b, True); counter(b, 1, n, True)
    y = write(b, 64, 300, 'Aklına takılanlar için', 76, WHITE, maxw=900)
    y = write(b, 64, y + 10, '4 yardımcı', 140, T['moon'])
    write(b, 64, y + 40, 'Asistan, bakım rehberi, uyku sesleri ve anne topluluğu. Hepsi Ninniko’nun içinde.', 44, SUB, 'Bold', maxw=900, lh=1.3)
    swipe(b); out.append(save(b, 'nc1'))
    snd = sound_card('/home/claude/media/check/sesler-ig.png', 'Uyku sesleri', [('Beyaz gürültü', 'Gürültüler'), ('Anne karnı', 'Gürültüler'),
                     ('Saç kurutma makinesi', 'Gürültüler'), ('Ninniler', 'Ninniler'), ('Müzik kutusu', 'Müzik kutusu')])
    def topics(b):
        items = ['Emzirme pozisyonları', 'Gaz çıkarma', 'Güvenli uyku', 'Ağlayan bebeği sakinleştirme', 'Banyo', 'Göbek bakımı', 'Tırnak bakımı']
        x, y = 64, 560
        for t in items:
            p = pill(t, font(38, 'ExtraBold'), T['text'], (255, 255, 255, 245), dot=T['accent'])
            if x + p.width - 60 > CW - 64: x, y = 64, y + 112
            b.alpha_composite(p, (x - 30, y)); x += p.width - 60 + 18
    slides = [('1', 'Ninniko Asistan', 'Sorunu yaz; bebeğinin kayıtlarına ve bakım rehberine göre yanıtlasın. (İsteğe bağlı)',
               lambda b: zoom_at(b, f'{N}/ana.webp', (16, 458, 524, 642), 860, 110, 640)),
              ('2', 'Bakım rehberi', 'Kısa ve sade rehberler:', topics),
              ('3', 'Uyku sesleri', 'Gürültüler, ninniler ve müzik kutusu. Uygulamadaki sesler internetsiz de çalar.',
               lambda b: zoom_at(b, snd, None, 560, (CW - 580) // 2, 540)),
              ('4', 'Anne topluluğu', 'Annelere sor, deneyimini paylaş, konulara yorum yaz. Yalnızca yazı paylaşılır.',
               lambda b: phone_at(b, f'{N}/topluluk.webp', 390, (CW - 390 - 32) // 2, 560))]
    for k, (num, h, sub, vis) in enumerate(slides):
        b = step_slide(k + 2, n, num, h, sub, vis); swipe(b); out.append(save(b, f'nc{k + 2}'))
    b = canvas(dark=True, seed=11); brand(b, True); counter(b, n, n, True)
    final(b, n, 'Kaydet,', 'bir anneye gönder')
    write(b, 0, CH - 90, 'Ninniko tıbbi tavsiye vermez; sağlık soruların için doktoruna danış.', 28, (190, 196, 225), 'SemiBold', center=True)
    out.append(save(b, f'nc{n}'))
    return out

# --- D: Büyüme grafiği ve atak takvimi (3 Aralık, tek görsel)
def post_d():
    b = canvas(); brand(b)
    y = write(b, 64, 180, 'Büyümesini', 92, T['text'], maxw=560)
    y = write(b, 64, y, 'adım adım izle', 92, T['accent'], maxw=560)
    feats = [('Boy, kilo, baş çevresi', 'Ölçümleri kaydet, grafikte gör'), ('DSÖ ortanca eğrisi', 'İstersen grafikte birlikte göster'),
             ('Atak takvimi', 'Yaşına göre olası büyüme ve gelişim atakları')]
    yy = y + 40
    for h, s in feats:
        d = ImageDraw.Draw(b); d.ellipse([64, yy + 8, 102, yy + 46], fill=T['accent'])
        d.line([(74, yy + 28), (81, yy + 36), (93, yy + 20)], fill=WHITE, width=5)
        write(b, 126, yy, h, 40, T['text'], 'ExtraBold', maxw=430)
        write(b, 126, yy + 52, s, 30, (95, 100, 140), 'SemiBold', maxw=420)
        yy += 128
    phone_at(b, f'{N}/gelisim.webp', 360, CW - 360 - 64, 470)
    zoom_at(b, f'{N}/ana.webp', (16, 186, 524, 270), 520, 64, int(yy + 26), r=28)
    write(b, 64, CH - 100, 'Ninniko tıbbi cihaz değildir; değerlendirme için doktoruna danış.', 28, (95, 100, 140), 'SemiBold', maxw=CW - 128)
    return save(b, 'nd1')

if __name__ == '__main__':
    print(carousel_a(), post_b(), carousel_c(), post_d())
