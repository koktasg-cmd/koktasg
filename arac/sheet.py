import sys, subprocess, os
from PIL import Image
v, out = sys.argv[1], sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]
ims = []
for t in ts:
    p = f'/tmp/_f{t}.png'; subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', v, '-frames:v', '1', p], check=True)
    ims.append(Image.open(p).convert('RGB').resize((360, 640)))
c = Image.new('RGB', (360 * len(ims), 640), 'white')
for k, i in enumerate(ims): c.paste(i, (k * 360, 0))
c.save(out)
