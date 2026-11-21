import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro import *
N = f'{R}/ninniko/legal-site/img'
TH = dict(top=(255, 245, 239), bot=(252, 212, 194), accent=(228, 108, 80), text=(45, 52, 102), blob1=(255, 186, 156), blob2=(196, 202, 255),
          icon=f'{R}/ninniko/assets/brand/ninniko-playstore-ikon-512.png', name='Ninniko', sub='Bebek Takibi')
# times from the voiceover's pauses
S = [
    dict(kind='phone', t0=0.0, t1=3.2, screen=f'{N}/gece.webp', h1='Gece 3’te son emzirme', h2='ne zamandı?', size=86, chip='Gece modu', chip_y=1250),
    dict(kind='phone', t0=3.2, t1=7.0, screen=f'{N}/ana.webp', h1='Emzirme, uyku, bez', h2='tek dokunuşla', chip='1 saniyede kayıt', chip_side='left', chip_y=1180),
    dict(kind='phone', t0=7.0, t1=10.5, screen=f'{N}/emzirme.webp', h1='Sol mu, sağ mı?', h2='Ninniko hatırlar', chip='Emzirme sayacı', chip_y=1000),
    dict(kind='phone', t0=10.5, t1=14.6, screen=f'{N}/gelisim.webp', h1='Kilo ve boy', h2='DSÖ eğrileriyle', chip='Büyüme grafiği', chip_side='left', chip_y=1060),
    dict(kind='phone', t0=14.6, t1=18.6, screen=f'{N}/raporlar.webp', h1='Her hafta', h2='akıllı özet', chip='Uyku · Beslenme · Bez', chip_y=1240),
    dict(kind='phone', t0=18.6, t1=21.0, screen=f'{N}/aile.webp', h1='Bütün aile', h2='aynı kayıtta', chip='Anne · Baba · Anneanne', chip_side='left', chip_y=1300),
    dict(kind='end', t0=21.0, t1=99, pills_text=['Ücretsiz', 'Aile paylaşımı', 'Akıllı asistan']),
]
Promo(TH).render(S, 24.4, '/home/claude/media/out/ninniko-silent.mp4')
