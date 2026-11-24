import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
N = f'{R}/ninniko/legal-site/img'
TH = dict(top=(58, 66, 128), bot=(30, 37, 78), accent=(246, 196, 83), text=(255, 255, 255), blob1=(120, 110, 220), blob2=(244, 165, 130), pilltext=(45, 52, 102),
          icon=f'{R}/ninniko/assets/brand/ninniko-playstore-ikon-512.png', name='Ninniko', sub='Bebek Takibi')
snd = sound_card('/home/claude/media/check/sesler.png', 'Uyku sesleri', [
    ('Beyaz gürültü', 'Gürültüler'), ('Pembe gürültü', 'Gürültüler'), ('Anne karnı', 'Gürültüler'),
    ('Saç kurutma makinesi', 'Gürültüler'), ('Çamaşır makinesi', 'Gürültüler')])
S = [
    dict(kind='phone', t0=0.0, t1=5.7, screen=f'{N}/gece.webp', h1='Gece uyanınca', h2='gözün kamaşmasın', size=90, chip='Gece modu', chip_y=1200),
    dict(kind='zoom', t0=5.7, t1=8.46, image=f'{N}/ana.webp', crop=(16, 186, 524, 436), h1='Uyku başladı mı?', h2='Tek dokunuş yeter', head_y=460, chip='Uyudu · Emzir · Bez'),
    dict(kind='zoom', t0=8.46, t1=14.84, image=snd, zw=760, h1='Uyku sesleri', h2='uygulamanın içinde', head_y=250, chip='Ninniler · Müzik kutusu'),
    dict(kind='zoom', t0=14.84, t1=18.25, image=f'{N}/raporlar.webp', crop=(30, 240, 510, 500), h1='Haftanın uykusu', h2='bir bakışta', head_y=460, chip='Haftalık özet'),
    dict(kind='end', t0=18.25, t1=99, pills_text=['Gece modu', 'Uyku sesleri', 'Haftalık özet']),
]
Promo2(TH).render(S, 23.0, '/home/claude/media/out/ninniko-reel-w49-silent.mp4')
