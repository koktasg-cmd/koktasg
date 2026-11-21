# Ninniko sosyal medya: haftalık üretim rehberi

Bu dosya, her hafta çalışan zamanlanmış görevin talimatıdır. Hesap sahibiyle Türkçe konuş.

## Takvim (değişmez kurallar)

- **TikTok (Ninniko Apps):** 2 günde bir, **18:00** (Europe/Istanbul). Sıra dönüşümlü:
  Ninniko Bebek Takibi → Ninniko El Ele → Ninniko Eğlence Bahçesi → tekrar.
  Başlangıç: 2026-11-23 Ninniko, 25 El Ele, 27 Eğlence Bahçesi, 29 Ninniko, 1 Aralık El Ele…
  (Bir tarihin uygulaması: 2026-11-23'ten bu yana geçen gün sayısı / 2, mod 3 → 0 Ninniko, 1 El Ele, 2 Eğlence Bahçesi.)
- **Instagram (ninniko.elele):** yalnız **El Ele**, 2 günde bir, **10:00**, 2026-11-23'ten başlayarak.
  Türler dönüşümlü: Reels (video) → karusel (eğitici/faydalı) → tek görsel → karusel…
- Metricool marka kimliği (blogId): **8276082**, saat dilimi Europe/Istanbul.

## Her çalıştırmada

1. `getScheduledPosts` ile yarından itibaren 10 gün içinde planlanmış gönderilere bak. Yalnız **boş kalan** yuvaları doldur; var olanı değiştirme, silme, kopyalama.
2. Depoları klonla (`/home/claude/` altına): `koktasg-cmd/koktasg` (yazma), `ninniko`, `ninniko-el-ele`, `ninniko-oyun-bahcesi` (okuma). Ekran görüntüleri:
   - Ninniko: `ninniko/legal-site/img/*.webp` (gece, ana, emzirme, gelisim, raporlar, aile, gunluk, topluluk)
   - El Ele: `ninniko-el-ele/store/screenshots/*.png`
   - Eğlence Bahçesi: `ninniko-oyun-bahcesi/store/site-ekranlar/tr/*.png`, `store/tanitim-2026-11/ios-6.3/tr/*.png`, karakter sahnesi `scripts/tanitim-source/tanitim-dikey-1.png`; hazır Türkçe seslendirme `scripts/tanitim-source/ses/tr/NN.mp3` (metinleri `seslendirme.json`) ve müzik `muzik-1.mp3`.
3. **Her yeni gönderi öncekilerden farklı olsun** (farklı açılış cümlesi, farklı ekranlar, farklı özellik). Geçmiş gönderileri `getScheduledPosts` ve depodaki `sosyal/` klasörlerinden kontrol et. Fikir havuzu:
   - Ninniko: gece emzirmeleri, uyku düzeni, aşı takvimi, büyüme grafiği, aile paylaşımı, haftalık özet, asistana soru sorma, topluluk ("Annelere sor"), günlük akış.
   - El Ele: nasıl çalışır, güvenlik kuralları, rozetler ve puan, "dolaptaki 5 eşya", mevsim geçişinde küçülen kıyafetler, komşuluk, sürdürülebilirlik.
   - Eğlence Bahçesi: harfler, hayvan sesleri, boyama, piyano, sesli masallar, vücudumuz, mevsimler, meslekler, ekran süresi kontrolü, reklamsız ve verisiz.
   - Yalnız uygulamada gerçekten olan özellikleri anlat (depodaki CLAUDE.md/AGENTS.md ve store/PLAY_CONSOLE.md'ye bak). Sağlık iddiası yok; ücretsiz/reklamsız gibi iddiaları mağaza metinlerinden doğrula.
4. **Video** (TikTok ve Instagram Reels, 1080×1920, 20–30 sn):
   - Seslendirme: ElevenLabs `creative_generate_speech`, model `eleven_v4`, `generations_count` 1. Ses: Ninniko → Mahidevran (`PdYVUd1CAGSXsTvZZTNn`); El Ele → Çağlayan (`sJ0xHHPzz1LOio4QNlB0`); Eğlence Bahçesi → depodaki hazır kayıtlar ya da Mahidevran.
   - Müzik: ElevenLabs `music` düğümü (`eleven_music_v2_5`, instrumental, video süresi + 2 sn). Aynı akışta tut.
   - Cümle aralarını ElevenLabs sandbox'ında `silencedetect` ile ölç; sahneleri bu zamanlara göre ayarla.
   - Görüntüyü `arac/pro.py` ile üret (örnekler: `v_ninniko.py`, `v_elele.py`, `v_oyun.py`): telefon maketi, kelime kelime gelen başlık, özellik etiketi, kapanışta ikon + resmi mağaza rozetleri.
   - Sessiz videoyu `koktasg` deposuna `sosyal/<yıl>-w<hafta>/` altına it, `creative_attach_reference_file` ile akışa ekle, sandbox'ta ses + müziği karıştır (müzik ~0.3 ses, `sidechaincompress` ile konuşmanın altında kısılır, `loudnorm I=-15`), çıktıyı tek girişli bir `composition` düğümünden geçir ve generation'ın `full_res_url`'ini kullan. Bu adres ~2 saat geçerli: **hemen** Metricool'a ver (Metricool dosyayı kendi sunucusuna kopyalar).
   - Eğlence Bahçesi videosu depodaki ses ve müzikle tamamen yerelde karışabilir (bkz. `v_oyun.py`).
5. **Görsel** (Instagram 1080×1350): `arac/ig_pro.py` stilinde (gece mavisi/krem zemin, yumuşak ışık lekeleri, telefon maketi, sayfa sayacı, "Kaydır" etiketi, son sayfada mağaza rozetleri). Depoya it, `raw.githubusercontent.com` adresini kullan.
6. Göndermeden önce her videodan ve görselden kare alıp **gözle kontrol et**: yazı taşması, üst üste binme, Türkçe karakterler, boşluk.
7. Metricool `createScheduledPost`: `autoPublish: true`, `draft: false`. TikTok'ta `privacyOption: PUBLIC_TO_EVERYONE`, `commercialContentOwnBrand: true`. Instagram videoda `instagramData.type: REEL`. Açıklamalar Türkçe, samimi, 1–2 emoji, sonda 6–9 alakalı hashtag; El Ele'de "Google Play ve App Store'da 'Ninniko El Ele' diye ara".
8. Bitince hesap sahibine kısa bir özet gönder: hangi gün hangi gönderi, Metricool planner linki.

## Yapma

- Takip/beğeni/yorum otomasyonu, sahte etkileşim, başka hesapları etiketleme.
- Var olan planlı gönderileri silme veya değiştirme (sahip isterse ayrı).
- Gerçek kişi/çocuk fotoğrafı, tanınmış karakter, telifli müzik.
