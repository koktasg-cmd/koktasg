"""Professional Instagram 4:5 posts for El Ele."""
import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro import *
from pro import _safe
E = f'{R}/ninniko-el-ele/store/screenshots'
CW, CH = 1080, 1350
T = dict(top=(255, 248, 241), bot=(252, 224, 204), accent=(230, 120, 80), text=(47, 58, 110), night=(47, 58, 110), moon=(246, 196, 83),
         icon=f'{R}/ninniko-el-ele/store/graphics/icon-512.png')
OUT = '/home/claude/media/out/ig'; os.makedirs(OUT, exist_ok=True)

def canvas(dark=False):
    if dark:
        base = gradient((54, 66, 122), (36, 44, 90), CW, CH).convert('RGBA')
        for (x, y, r, c, a) in [(150, 200, 260, (246, 196, 83), 60), (950, 1100, 320, (244, 165, 130), 70)]:
            b = blob(r, c, a); base.alpha_composite(b, (x - b.width // 2, y - b.height // 2))
        d = ImageDraw.Draw(base)
        import random; rnd = random.Random(4)
        for _ in range(28):
            x, y, s = rnd.randint(0, CW), rnd.randint(0, CH), rnd.choice([2, 3, 4])
            d.ellipse([x, y, x + s, y + s], fill=(255, 240, 200, rnd.randint(90, 200)))
        return base
    base = gradient(T['top'], T['bot'], CW, CH).convert('RGBA')
    for (x, y, r, c, a) in [(120, 150, 240, (244, 165, 130), 110), (980, 1150, 300, (246, 196, 83), 90)]:
        b = blob(r, c, a); base.alpha_composite(b, (x - b.width // 2, y - b.height // 2))
    return base

def brand(base, dark=False, y=60):
    ic = Image.open(T['icon']).convert('RGB').resize((64, 64), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((64, 64), 16))
    base.alpha_composite(ic, (64, y))
    nm = text_img('Ninniko El Ele', font(34, 'Black'), (255, 255, 255) if dark else T['text'])
    base.alpha_composite(nm, (144, y + 32 - nm.height // 2))

def counter(base, i, n, dark=False):
    t = text_img(f'{i}/{n}', font(30, 'Bold'), (255, 255, 255) if dark else T['text'])
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

def swipe(base, dark=False):
    fg = T['text'] if not dark else T['text']
    t = text_img('Kaydır', font(32, 'ExtraBold'), fg)
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

# --- Carousel A: 3 adımda hediye et
def carousel_a():
    n = 5; out = []
    b = canvas(dark=True); brand(b, True); counter(b, 1, n, True)
    y = write(b, 64, 200, 'Küçülen eşyalar', 96, (255, 255, 255))
    y = write(b, 64, y, 'komşunun işine yarasın', 96, T['moon'])
    write(b, 64, y + 30, '3 adımda hediye et ya da takasla. Satış yok, ücret yok.', 42, (225, 228, 245), 'Bold', maxw=430, lh=1.3)
    phone_at(b, f'{E}/01-kesfet.png', 400, CW - 400 - 90, 720)
    swipe(b, True); out.append(save(b, 'a1'))
    steps = [('1', 'İlan ver', 'Fotoğrafını çek, yaşını ve durumunu seç. Ekibimiz kontrol eder, yayına alır.', '05-ilan-ver.png'),
             ('2', 'Mesajlaş', 'İsteyenlerle uygulama içinden konuş. Telefon numaran hep gizli kalır.', '03-sohbet.png'),
             ('3', 'Teslim et', 'Buluş, teslim et, değerlendir. Her hediyende rozet ve puan kazan.', '04-hareketlerim.png')]
    for k, (num, h, sub, shot) in enumerate(steps):
        b = canvas(); brand(b); counter(b, k + 2, n)
        d = ImageDraw.Draw(b); d.ellipse([64, 190, 184, 310], fill=T['accent'])
        ni = text_img(num, font(76, 'Black'), (255, 255, 255)); b.alpha_composite(ni, (124 - ni.width // 2, 250 - ni.height // 2))
        write(b, 214, 196, h, 88, T['text'])
        write(b, 64, 350, sub, 40, T['text'], 'SemiBold', maxw=CW - 128, lh=1.3)
        phone_at(b, f'{E}/{shot}', 400, (CW - 400 - 32) // 2, 520)
        if k < 2: swipe(b)
        out.append(save(b, f'a{k + 2}'))
    b = canvas(dark=True); brand(b, True); counter(b, n, n, True)
    ic = Image.open(T['icon']).convert('RGB').resize((240, 240), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((240, 240), 56))
    b.alpha_composite(ic, ((CW - 240) // 2, 250))
    y = write(b, 0, 560, 'Komşudan komşuya,', 84, (255, 255, 255), center=True)
    y = write(b, 0, y, 'el ele.', 84, T['moon'], center=True)
    for k, ptxt in enumerate(['Satış yok', 'Ücret yok', 'Kargo yok']):
        pl = pill(ptxt, font(36, 'ExtraBold'), T['text'], (255, 255, 255, 240)); b.alpha_composite(pl, (int(70 + k * 320), int(y + 30)))
    pr = Promo(dict(T, blob1=(0, 0, 0), blob2=(0, 0, 0), bot=T['bot'], name='', sub=''))
    b1, b2 = pr.badges; bw = b1.width + b2.width + 28; bx = (CW - bw) // 2
    b.alpha_composite(b1, (bx, int(y + 200))); b.alpha_composite(b2, (bx + b1.width + 28, int(y + 200)))
    write(b, 0, y + 340, '“Ninniko El Ele” diye ara · ücretsiz', 36, (225, 228, 245), 'Bold', center=True)
    out.append(save(b, 'a5'))
    return out

# --- Single post B: benefits
def post_b():
    b = canvas(dark=True); brand(b, True)
    y = write(b, 64, 190, 'Çocuk eşyalarına', 92, (255, 255, 255))
    y = write(b, 64, y, 'ikinci bir hayat', 92, T['moon'])
    feats = [('Onaylı ilanlar', 'Her ilan ekibimizce kontrol edilir'), ('Numaran gizli', 'Uygulama içinden mesajlaş'),
             ('Aynı mahalle', 'Yakınındaki ebeveynler'), ('Tamamen ücretsiz', 'Satış, ücret, kargo yok')]
    yy = y + 50
    for h, s in feats:
        d = ImageDraw.Draw(b); d.ellipse([64, yy + 10, 100, yy + 46], fill=T['accent'])
        ck = text_img('✓', font(28, 'Black'), (255, 255, 255)) if False else None
        d.line([(73, yy + 28), (80, yy + 36), (92, yy + 20)], fill=(255, 255, 255), width=5)
        write(b, 124, yy, h, 44, (255, 255, 255), 'ExtraBold', maxw=520)
        write(b, 124, yy + 54, s, 32, (205, 210, 235), 'SemiBold', maxw=470)
        yy += 128
    phone_at(b, f'{E}/02-ilan.png', 360, CW - 360 - 70, 470)
    return save(b, 'b1')

# --- Carousel C: safety tips
def carousel_c():
    tips = [('Fotoğrafta çocuk olmasın', 'Eşyayı tek başına, gün ışığında çek. Yüz, okul arması ya da adres görünmesin.'),
            ('Adresini paylaşma', 'Park, kafe gibi kalabalık ve açık bir yerde buluş. El Ele GPS konumunu hiç istemez.'),
            ('Mesajlaşmayı uygulamada tut', 'Numaranı vermeden konuş. Bir şey ters giderse şikâyet et ya da engelle.'),
            ('Yasaklı ürünleri verme', 'Oto koltuğu, mama, ilaç ve açılmış bakım ürünleri güvenlik için listede yok.'),
            ('Teslimden sonra değerlendir', 'Karşılıklı yıldız vermek güvenilir komşuları öne çıkarır.')]
    n = len(tips) + 2; out = []
    b = canvas(dark=True); brand(b, True); counter(b, 1, n, True)
    y = write(b, 64, 330, 'Güvenli takas için', 96, (255, 255, 255))
    y = write(b, 64, y, '5 altın kural', 120, T['moon'])
    write(b, 64, y + 40, 'Bebek eşyası hediye ederken ya da alırken bunlara dikkat et.', 46, (225, 228, 245), 'Bold', maxw=880, lh=1.25)
    swipe(b, True); out.append(save(b, 'c1'))
    for k, (h, s) in enumerate(tips):
        b = canvas(); brand(b); counter(b, k + 2, n)
        big = text_img(f'{k + 1:02d}', font(300, 'Black'), (*T['accent'], 255)); a = big.getchannel('A').point(lambda v: int(v * 0.9)); big.putalpha(a)
        b.alpha_composite(big, (50, 250))
        y = write(b, 64, 640, h, 80, T['text'], maxw=950)
        ImageDraw.Draw(b).rounded_rectangle([64, 610, 184, 620], 5, fill=T['accent'])
        write(b, 64, y + 30, s, 46, T['text'], 'SemiBold', maxw=930, lh=1.35)
        swipe(b); out.append(save(b, f'c{k + 2}'))
    b = canvas(dark=True); brand(b, True); counter(b, n, n, True)
    ic = Image.open(T['icon']).convert('RGB').resize((200, 200), Image.LANCZOS).convert('RGBA'); ic.putalpha(rounded_mask((200, 200), 48))
    b.alpha_composite(ic, ((CW - 200) // 2, 230))
    y = write(b, 0, 500, 'Kaydet,', 100, (255, 255, 255), center=True)
    y = write(b, 0, y, 'bir ebeveyne gönder', 76, T['moon'], center=True)
    pr = Promo(dict(T, blob1=(0, 0, 0), blob2=(0, 0, 0), name='', sub='')); b1, b2 = pr.badges; bw = b1.width + b2.width + 28; bx = (CW - bw) // 2
    b.alpha_composite(b1, (bx, int(y + 70))); b.alpha_composite(b2, (bx + b1.width + 28, int(y + 70)))
    write(b, 0, y + 220, '“Ninniko El Ele” diye ara · ücretsiz', 36, (225, 228, 245), 'Bold', center=True)
    out.append(save(b, f'c{n}'))
    return out

if __name__ == '__main__':
    a = carousel_a(); bb = post_b(); c = carousel_c()
    print(a, bb, c)
