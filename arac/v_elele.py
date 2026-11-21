import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro import *
E = f'{R}/ninniko-el-ele/store/screenshots'
TH = dict(top=(255, 248, 241), bot=(252, 224, 204), accent=(230, 120, 80), text=(47, 58, 110), blob1=(244, 165, 130), blob2=(246, 196, 83),
          icon=f'{R}/ninniko-el-ele/store/graphics/icon-512.png', name='Ninniko El Ele', sub='Çocuk eşyası hediye & takas')
S = [
    dict(kind='phone', t0=0.0, t1=3.1, screen=f'{E}/02-ilan.png', h1='Çocuğun büyüdü,', h2='eşyaları dolapta mı kaldı?', size=80, chip='Hediye · Takas', chip_y=1150),
    dict(kind='phone', t0=3.1, t1=9.3, screen=f'{E}/01-kesfet.png', h1='Yakınındaki ebeveynlere', h2='hediye et ya da takasla', chip='Aynı mahalle', chip_side='left', chip_y=1120),
    dict(kind='phone', t0=9.3, t1=14.1, screen=f'{E}/05-ilan-ver.png', h1='Fotoğrafını çek,', h2='1 dakikada ilan ver', chip='5 kolay adım', chip_y=1250),
    dict(kind='phone', t0=14.1, t1=16.7, screen=f'{E}/03-sohbet.png', h1='Numaranı vermeden', h2='güvenle mesajlaş', chip='Numaran gizli kalır', chip_side='left', chip_y=1180),
    dict(kind='phone', t0=16.7, t1=18.7, screen=f'{E}/07-rozetler.png', h1='Hediye ettikçe', h2='rozet ve puan kazan', chip='Cömert Komşu', chip_y=1220),
    dict(kind='end', t0=18.7, t1=99, pills_text=['Satış yok', 'Ücret yok', 'Kargo yok']),
]
Promo(TH).render(S, 23.4, '/home/claude/media/out/elele-silent.mp4')
