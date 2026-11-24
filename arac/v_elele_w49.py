import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
E = f'{R}/ninniko-el-ele/store/screenshots'
TH = dict(top=(234, 244, 255), bot=(255, 222, 200), accent=(230, 120, 80), text=(47, 58, 110), blob1=(180, 205, 245), blob2=(246, 196, 83),
          icon=f'{R}/ninniko-el-ele/store/graphics/icon-512.png', name='Ninniko El Ele', sub='Çocuk eşyası hediye & takas')
S = [
    dict(kind='phone', t0=0.0, t1=3.76, screen=f'{E}/01-kesfet.png', h1='Kışlıklar çıktı,', h2='geçen yılın montu küçük mü?', size=82, chip='Mevsim geçişi', chip_y=1200),
    dict(kind='phone', t0=3.76, t1=8.95, screen=f'{E}/02-ilan.png', h1='İlan ver, komşu', h2='“İstiyorum” desin', chip='Hediye · Takas', chip_side='left', chip_y=1150),
    dict(kind='phone', t0=8.95, t1=13.18, screen=f'{E}/08-bildirimler.png', h1='İstek gelince haber verir,', h2='sen seçersin', size=74, chip='Kime vereceğin senin kararın', chip_y=1300),
    dict(kind='phone', t0=13.18, t1=16.23, screen=f'{E}/04-hareketlerim.png', h1='Teslim et,', h2='karşılıklı değerlendir', chip='Teslim edildi', chip_side='left', chip_y=1060),
    dict(kind='phone', t0=16.23, t1=19.06, screen=f'{E}/06-profil.png', h1='Her hediyede', h2='puan ve rozet', chip='El Ele puanların', chip_y=1180),
    dict(kind='end', t0=19.06, t1=99, pills_text=['Satış yok', 'Ücret yok', 'Kargo yok']),
]
Promo2(TH).render(S, 25.6, '/home/claude/media/out/elele-w49-silent.mp4')
