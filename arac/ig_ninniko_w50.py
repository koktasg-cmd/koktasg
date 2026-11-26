"""Ninniko Instagram 5 Aralık karuseli: Anne topluluğu."""
import sys; sys.path.insert(0, '/home/claude/koktasg/arac')
from ig_ninniko import *
OUT2 = '/home/claude/media/out/ig50'; os.makedirs(OUT2, exist_ok=True)
import ig_ninniko; ig_ninniko.OUT = OUT2

CATS = [('🌙', 'Uyku', (123, 111, 216)), ('🍼', 'Emzirme ve Beslenme', (233, 135, 95)), ('🥣', 'Ek Gıda', (63, 174, 140)),
        ('🌱', 'Gelişim', (75, 146, 219)), ('💛', 'Annelik', (212, 111, 166)), ('💬', 'Genel', (94, 139, 224))]

def cat_pills(b, y0):
    x, y = 64, y0
    for _, name, col in CATS:
        p = pill(name, font(40, 'ExtraBold'), T['text'], (255, 255, 255, 245), dot=col)
        if x + p.width - 60 > CW - 64: x, y = 64, y + 116
        b.alpha_composite(p, (x - 30, y)); x += p.width - 60 + 18
    return y + 116

def check_list(b, y, items, dark=False):
    for h, s in items:
        d = ImageDraw.Draw(b); d.ellipse([64, y + 8, 102, y + 46], fill=T['accent'])
        d.line([(74, y + 28), (81, y + 36), (93, y + 20)], fill=WHITE, width=5)
        write(b, 126, y, h, 42, WHITE if dark else T['text'], 'ExtraBold', maxw=CW - 200)
        write(b, 126, y + 54, s, 32, (205, 210, 235) if dark else (95, 100, 140), 'SemiBold', maxw=CW - 200)
        y += 140
    return y

def carousel():
    n = 6; out = []
    b = canvas(dark=True, seed=21); brand(b, True); counter(b, 1, n, True)
    y = write(b, 64, 210, 'Gecenin 3’ünde', 88, WHITE, maxw=620)
    y = write(b, 64, y, 'aklına takılan', 88, WHITE, maxw=620)
    y = write(b, 64, y, 'soru yalnız', 88, T['moon'], maxw=620)
    y = write(b, 64, y, 'kalmasın', 88, T['moon'], maxw=620)
    write(b, 64, y + 30, 'Ninniko’nun anne topluluğunda sor, deneyimini paylaş.', 40, SUB, 'Bold', maxw=520, lh=1.3)
    phone_at(b, f'{N}/topluluk.webp', 340, CW - 340 - 90, 520)
    swipe(b); out.append(save(b, 'ne1'))

    b = step_slide(2, n, '1', 'Konuna göre bul', 'Konular altı başlıkta toplanır; ilgilendiğin başlığa dokun, o konudaki soruları gör.',
                   lambda b: zoom_at(b, f'{N}/topluluk.webp', (16, 255, 524, 380), 820, (CW - 840) // 2, cat_pills(b, 540) + 40))
    swipe(b); out.append(save(b, 'ne2'))

    b = step_slide(3, n, '2', 'Konu aç, yorum yaz', 'Rumuzunla yaz. Bir konuyu “Takip et”, yeni yorumları kaçırma.',
                   lambda b: zoom_at(b, f'{N}/topluluk.webp', (16, 450, 524, 880), 680, (CW - 700) // 2, 540))
    swipe(b); out.append(save(b, 'ne3'))

    b = step_slide(4, n, '3', 'Takip ettiklerim', 'Açtığın, yorum yazdığın ve takip ettiğin konular tek listede; dönüp bakması kolay.',
                   lambda b: phone_at(b, f'{N}/topluluk.webp', 330, (CW - 330 - 32) // 2, 530))
    swipe(b); out.append(save(b, 'ne4'))

    def safe(b):
        check_list(b, 500, [('Topluluk kuralları', 'Yazmadan önce kuralları okuyup kabul edersin'),
                            ('Şikâyet et', 'Uygunsuz içerik, kişisel bilgi ya da tehlikeli sağlık tavsiyesi'),
                            ('Engelle', 'İstemediğin kişinin yazılarını görme'),
                            ('Yönetici denetimi', 'Şikâyetler ekibimizce incelenir')])
    b = step_slide(5, n, '4', 'Güvenli bir ortam', 'Annelerin rahatça yazabilmesi için:', safe)
    swipe(b); out.append(save(b, 'ne5'))

    b = canvas(dark=True, seed=21); brand(b, True); counter(b, n, n, True)
    final(b, n, 'Annelik paylaştıkça', 'hafifler')
    write(b, 0, CH - 100, 'Topluluktaki yazılar kullanıcı deneyimidir, tıbbi tavsiye değildir;', 27, (190, 196, 225), 'SemiBold', center=True)
    write(b, 0, CH - 64, 'sağlık soruların için doktoruna danış.', 27, (190, 196, 225), 'SemiBold', center=True)
    out.append(save(b, 'ne6'))
    return out

if __name__ == '__main__':
    print(carousel())
