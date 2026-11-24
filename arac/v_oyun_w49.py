import sys, subprocess; sys.path.insert(0, '/home/claude/koktasg/arac')
from pro2 import *
O = f'{R}/ninniko-oyun-bahcesi'; T = f'{O}/store/tanitim-2026-11/ios-6.3/tr'; V = f'{O}/scripts/tanitim-source/ses/tr'
TH = dict(top=(255, 246, 236), bot=(214, 232, 252), accent=(230, 118, 84), text=(47, 58, 110), blob1=(246, 196, 83), blob2=(143, 207, 192),
          icon=f'{O}/store/graphics/icon-512.png', name='Ninniko Eğlence Bahçesi', sub='2–4 yaş için oyunlar')
HOOK = 2.85; gap = 0.35
lines = ['08', '03', '06', '09', '11']
dur = [float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{V}/{l}.mp3'])) for l in lines]
starts = []; t = 0.2 + HOOK + gap
for d in dur: starts.append(t); t += d + gap
total = t + 1.4
b = [0] + [s - gap / 2 for s in starts]
mid06 = starts[2] + dur[2] * 0.48
S = [
    dict(kind='art', t0=0, t1=b[1], image=f'{O}/scripts/tanitim-source/tanitim-aksam-dikey-1.png', h1='Akşam oldu,', h2='masal vakti mi?', size=92, head_y=1450),
    dict(kind='card', t0=b[1], t1=b[2], image=f'{T}/07-masallar.png'),
    dict(kind='phone', t0=b[2], t1=b[3], screen=f'{O}/store/site-ekranlar/tr/oyun-cadiri.png', h1='Oyun Çadırı’nda', h2='öğretici oyunlar', chip='Reklamsız · Güvenli', chip_y=1300),
    dict(kind='card', t0=b[3], t1=mid06, image=f'{T}/05-vucut.png'),
    dict(kind='card', t0=mid06, t1=b[4], image=f'{T}/06-mevsim-meslek.png'),
    dict(kind='card', t0=b[4], t1=b[5], image=f'{T}/09-sarki-sinema.png'),
    dict(kind='end', t0=b[5], t1=99, pills_text=['Reklam yok', 'Veri toplanmaz', 'İnternetsiz']),
]
out = '/home/claude/media/out'
Promo2(TH).render(S, total, f'{out}/oyun-w49-silent.mp4')
inp = []; flt = []
for k, l in enumerate(lines):
    inp += ['-i', f'{V}/{l}.mp3']; flt.append(f'[{k}:a]adelay={int(starts[k]*1000)}|{int(starts[k]*1000)},aformat=channel_layouts=stereo[v{k}]')
n = len(lines)
flt.append(''.join(f'[v{k}]' for k in range(n)) + f'amix=inputs={n}:normalize=0,apad,atrim=0:{total:.2f}[vo]')
flt.append(f'[{n}:a]atrim=0:{total:.2f},volume=0.33,afade=t=in:d=0.6,afade=t=out:st={total-1.6:.2f}:d=1.6[mu]')
flt.append('[vo]asplit[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350[mud];[vo1][mud]amix=inputs=2:normalize=0[a]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inp, '-i', f'{O}/scripts/tanitim-source/muzik-1.mp3', '-i', f'{out}/oyun-w49-silent.mp4',
                '-filter_complex', ';'.join(flt), '-map', f'{n+1}:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{out}/oyun-w49-premix.mp4'], check=True)
print(total, starts)
