import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
N = f'{R}/ninniko/legal-site/img'
TH = dict(top=(244, 246, 255), bot=(214, 222, 255), accent=(228, 108, 80), text=(45, 52, 102), blob1=(196, 202, 255), blob2=(255, 196, 170),
          icon=f'{R}/ninniko/assets/brand/ninniko-playstore-ikon-512.png', name='Ninniko', sub='Bebek Takibi')
S = [
    dict(kind='phone', t0=0.0, t1=3.55, screen=f'{N}/gunluk.webp', h1='Son bez', h2='ne zamandı?', size=96, chip='Kimse hatırlamıyor mu?', chip_y=1240),
    dict(kind='zoom', t0=3.55, t1=6.43, image=f'{N}/gunluk.webp', crop=(0, 445, 540, 1010), zw=760, h1='Günün akışı', h2='saat saat önünde', chip='Beslenme · Uyku · Bez'),
    dict(kind='phone', t0=6.43, t1=10.45, screen=f'{N}/ana.webp', h1='Bugün hangi', h2='gelişim atağında?', chip='Atak takvimi', chip_side='left', chip_y=760),
    dict(kind='zoom', t0=10.45, t1=15.1, image=f'{N}/ana.webp', crop=(16, 458, 524, 642), h1='Aklına takılanı', h2='Asistan’a sor', head_y=520, chip='Kayıtlarına ve rehbere göre'),
    dict(kind='phone', t0=15.1, t1=18.05, screen=f'{N}/topluluk.webp', h1='Annelere sor,', h2='deneyimini paylaş', chip='Topluluk', chip_y=1250),
    dict(kind='end', t0=18.05, t1=99, pills_text=['Ücretsiz', 'Reklamsız', 'Aile paylaşımı']),
]
Promo2(TH).render(S, 23.4, '/home/claude/media/out/ninniko-w49-silent.mp4')
