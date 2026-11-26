import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
N = f'{R}/ninniko/legal-site/img'
TH = dict(top=(236, 248, 244), bot=(196, 226, 236), accent=(228, 108, 80), text=(45, 52, 102), blob1=(160, 214, 200), blob2=(255, 196, 170),
          icon=f'{R}/ninniko/assets/brand/ninniko-playstore-ikon-512.png', name='Ninniko', sub='Bebek Takibi')

def pdf_card(path):
    """PDF raporunu anlatan sade çizim (veri yok, yalnız başlıklar)."""
    w, h = 560, 700
    im = Image.new('RGB', (w, h), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([28, 28, 168, 88], 18, fill=(228, 108, 80)); d.text((52, 34), 'PDF', font=font(40, 'Black'), fill=(255, 255, 255))
    d.text((32, 120), 'Bebek raporu', font=font(46, 'Black'), fill=(45, 52, 102))
    d.text((32, 182), 'Son 7 · 14 · 30 gün', font=font(26, 'Bold'), fill=(130, 134, 160))
    y = 250
    for name, col in [('Beslenme', (233, 135, 95)), ('Uyku', (123, 111, 216)), ('Bez', (63, 174, 140)), ('Gelişim', (75, 146, 219))]:
        d.rounded_rectangle([28, y, w - 28, y + 96], 22, fill=(248, 247, 252))
        d.ellipse([48, y + 30, 84, y + 66], fill=col)
        d.text((104, y + 26), name, font=font(32, 'ExtraBold'), fill=(45, 52, 102))
        for k, ln in enumerate([150, 110]):
            d.rounded_rectangle([w - 60 - ln, y + 28 + k * 26, w - 60, y + 42 + k * 26], 7, fill=(225, 226, 238))
        y += 112
    im.save(path); return path

pdf = pdf_card('/home/claude/media/check/pdf-card.png')
S = [
    dict(kind='phone', t0=0.0, t1=4.7, screen=f'{N}/emzirme.webp', h1='“Günde kaç kez', h2='besleniyor?”', size=92, chip='Kontrolde aklın karıştı mı?', chip_y=1250),
    dict(kind='phone', t0=4.7, t1=6.9, screen=f'{N}/raporlar.webp', h1='Haftalık özet', h2='hazır', chip='Raporlar', chip_side='left', chip_y=1150),
    dict(kind='zoom', t0=6.9, t1=9.7, image=f'{N}/raporlar.webp', crop=(16, 170, 524, 730), zw=800, h1='Uyku, beslenme', h2='ve bez bir arada', head_y=300, chip='Bu haftanın özeti'),
    dict(kind='zoom', t0=9.7, t1=13.25, image=f'{N}/raporlar.webp', crop=(16, 765, 524, 1020), h1='Son 7, 14', h2='ya da 30 gün', head_y=430, chip='Tek dokunuşla'),
    dict(kind='zoom', t0=13.25, t1=15.8, image=pdf, zw=600, h1='Raporu PDF', h2='olarak paylaş', head_y=300, chip='Kontrole hazır'),
    dict(kind='zoom', t0=15.8, t1=18.9, image=f'{N}/ana.webp', crop=(16, 790, 524, 1019), h1='Sonraki beslenme', h2='ne zaman?', head_y=440, chip='Ana ekranda'),
    dict(kind='end', t0=18.9, t1=99, pills_text=['Haftalık özet', 'PDF rapor', 'Aile paylaşımı']),
]
Promo2(TH).render(S, 24.0, '/home/claude/media/out/ninniko-w50-silent.mp4')
