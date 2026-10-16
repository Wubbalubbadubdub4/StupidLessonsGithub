# İleri Python Programlama – Hafta 4 Lab Ödevi: Üreteçler ve functools

**Öğrenci Adı Soyadı:** Alp Dinçoğlu  
**Öğrenci Numarası:** 20253006040  
**Kurum:** İstanbul Nişantaşı Üniversitesi  
**Ders:** İleri Python Programlama  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  
**GitHub Deposu:** https://github.com/Wubbalubbadubdub4/StupidLessonsGithub  

---

## 🚀 Proje Özeti ve Genel Mimari

Bu lab çalışmasında, Hafta 3'te fonksiyonel hale getirilen **Uzay Oyunu** projesine; Python üreteçleri (generators), tembel değerlendirme (lazy evaluation) boru hatları, `@functools.lru_cache` tabanlı rota sayacı, fonksiyonel programlama araçları (`map`, `filter`, `reduce`, `partial`) ve meşgul bekleme (busy waiting) zamanlayıcısı entegre edilmiştir.

Proje yapısı modüler ve test odaklı (TDD) olarak organize edilmiştir:
- `uzay_oyunu/akis.py`: Görev 1 (Fibonacci), Görev 2 (Yakıt göstergesi), Görev 3 (Boru hattı) ve Görev 4 (Önbellekli rota sayacı).
- `uzay_oyunu/istatistik.py`: Görev 5 (Galaksi istatistikleri ve `hizli_yolculuk` partial fonksiyonu).
- `uzay_oyunu/bonus.py`: Bonus (+10) `zamanlayici()` üreteci ile 10 saniyelik tik-tak programı ve meşgul bekleme analizi.
- `uzay_oyunu/oyun.py`: `yakit_gostergesi` entegrasyonu yapılmış ana seyahat (`travel`) döngüsü.
- `veri/seyir.txt`: Boru hattı tarafından işlenen seyir defteri kayıt dosyası.
- `tests/`: 40 adet kapsamlı birim test (`test_akis.py`, `test_istatistik.py`, `test_bonus.py`, `test_fonksiyonlar.py`, `test_tuzaklar.py`).

---

## 📋 Görev Detayları ve Uygulama

### Görev 1 – Fibonacci Üreteci (15 puan)
`uzay_oyunu/akis.py` içerisinde `fibonacci()` sonsuz üreteci yazılmıştır:
- Sonsuz Fibonacci serisi (`0, 1, 1, 2, 3, 5, 8...`) bellekte liste oluşturmadan `yield` anahtar kelimesi ile tembel üretilir.
- Değerler üç farklı yolla alınmıştır:
  1. `next()` ile ilk 3 değer: `(0, 1, 1)`
  2. `itertools.islice()` ile ilk 12 değer: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`
  3. `itertools.takewhile()` ile 100'den küçük değerler: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`
- Üretecin **tek kullanımlık (single-use)** olduğu test edilmiş; aynı üreteç nesnesinden yapılan ardışık `islice` çağrılarının farklı sonuçlar ürettiği gösterilmiştir.

---

### Görev 2 – Yakıt Göstergesi (20 puan)
`yakit_gostergesi(yakit: int, tuketim: int)` üreteci:
- Her `next()` çağrısında yakıtı `tuketim` kadar azaltarak kalan yakıtı üretir.
- Yakıt sıfıra inince veya tükendiğinde `0` ürettikten sonra durur ve bir sonraki çağrıda `StopIteration` fırlatır.
- `travel()` seyahat döngüsü içine entegre edilmiştir. Galaksideki başlangıç yakıtıyla gösterge oluşturulur, her yolculuk adımında `next(gosterge)` çağrılır.
- `StopIteration` yakalandığında oyuncu *"Yakıtın bitti, uzayda sürükleniyorsun…"* mesajıyla oyunu kaybeder.

Örnek Çıktı:
```python
>>> list(yakit_gostergesi(100, 30))
[70, 40, 10, 0]
```

---

### Görev 3 – Seyir Defteri Boru Hattı (25 puan)
`veri/seyir.txt` dosyasındaki uçuş kayıtlarını işleyen 3 aşamalı tembel boru hattı kurulmuştur:
1. `satirlari_oku(yol)`: Dosyayı satır satır okur, `#` ile başlayan yorumları ve boş satırları atlar.
2. `ayristir(satirlar)`: Her satırdan `(kaynak, hedef, yakit)` demeti üretir.
3. `uzun_yolculuklar(kayitlar, esik)`: Yakıtı verilen eşikten büyük olan seyahatleri süzer.

> **Önemli İlke:** Hiçbir aşama tüm dosyayı tek seferde belleğe/listeye yüklemez. Tüm veri akışı `Generator` üzerinden tembel (lazy) akar.

Örnek Boru Hattı Sonuçları:
```python
>>> sum(y for _, _, y in ayristir(satirlari_oku("veri/seyir.txt")))
88
>>> kayitlar = ayristir(satirlari_oku("veri/seyir.txt"))
>>> [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
['sirius', 'centauri', 'orion', 'kara_delik']
```

---

### Görev 4 – Önbellekli Rota Sayacı ve Başarım Ölçümü (25 puan)
`rota_sayaci(baglantilar)` fonksiyonu, içinde `@functools.lru_cache(maxsize=None)` ile dekore edilmiş `rota_sayisi(gezegen, adim)` fonksiyonunu döndürür:
- Başlangıç gezegeninden çıkıp tam `adim` uzunluğundaki farklı geçerli rotaların toplam sayısını hesaplar.
- Çakışan alt problemleri (overlapping subproblems) önbelleğe alarak $O(b^n)$ üstel karmaşıklığı $O(V \cdot n)$ doğrusal karmaşıklığa indirir.

Doğrulama Sonuçları:
```python
>>> say = rota_sayaci(galaksi["baglantilar"])
>>> say("dünya", 3), say("dünya", 10), say("dünya", 40)
(9, 2185, 16832258606399)
```

#### Performans Karşılaştırma Tablosu (`adim = 20`)

Ölçümler `time.perf_counter()` kullanılarak aynı donanım ortamında gerçekleştirilmiştir:

| Yöntem | Başlangıç | Adım (`adim`) | Hesaplanan Rota Sayısı | Çalışma Süresi (sn) | Önbellek Bilgisi (`cache_info`) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Önbelleksiz Saf Özyineleme** | dünya | 20 | 4.315.343 | **2.123026 sn** | Önbellek Yok |
| **Önbellekli (`@lru_cache`)** | dünya | 20 | 4.315.343 | **0.000119 sn** | `CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)` |

> **Analiz:** `@lru_cache` kullanımı sayesinde 20 adımlık rota hesabı yaklaşık **17.840 kat** hızlanmıştır. `adim=40` için önbelleksiz sürümün hesaplanması günler sürecekken, önbellekli sürüm 0.0002 saniyede `16.832.258.606.399` sonucuna ulaşmaktadır.

---

### Görev 5 – map, filter, reduce ve partial (15 puan)
`uzay_oyunu/istatistik.py` modülünde 3 temel soru hem fonksiyonel araçlarla (`map`/`filter`/`reduce`) hem de Pythonik yapılarla (`list comprehension` ve `sum`) çözülmüştür:

1. **Gezegen Adlarının Büyük Harfli Listesi:**
   - `gezegen_adlari_buyuk_map`: `list(map(str.upper, galaksi["gezegenler"]))`
   - `gezegen_adlari_buyuk_comprehension`: `[g.upper() for g in galaksi["gezegenler"]]`
   - *Çıktı:* `['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']`

2. **En Az İki Bağlantısı Olan Gezegenler:**
   - `en_az_iki_baglanti_filter`: `list(filter(lambda g: len(baglantilar.get(g, [])) >= 2, gezegenler))`
   - `en_az_iki_baglanti_comprehension`: `[g for g in gezegenler if len(baglantilar.get(g, [])) >= 2]`
   - *Çıktı:* `['dünya', 'centauri', 'sirius', 'orion']`

3. **Toplam Bağlantı Sayısı:**
   - `toplam_baglanti_reduce`: `functools.reduce(lambda acc, b: acc + len(b), baglantilar.values(), 0)`
   - `toplam_baglanti_sum`: `sum(len(b) for b in baglantilar.values())`
   - *Çıktı:* `10`

4. **`functools.partial` ile `hizli_yolculuk`:**
   `yolculuk(mesafe, hiz=1.0)` fonksiyonundan `hiz=3` sabitlenerek `hizli_yolculuk` türetilmiştir:
   ```python
   hizli_yolculuk = functools.partial(yolculuk, hiz=3)
   # hizli_yolculuk(30) -> 10.0
   ```

#### 💡 Okunabilirlik Değerlendirmesi (Zen of Python / PEP 20)
> *“Readability counts.” (Okunabilirlik önemlidir)*  
>
> Python tasarım felsefesinde Liste Üreteçleri (`[x for x in ...]`) ve yerleşik `sum()` fonksiyonu; `map`, `filter` ve `reduce` fonksiyonel yapılarına göre çok daha üstün bir okunabilirliğe sahiptir.
>
> 1. `map` ve `filter` çoğu durumda ek bir `lambda` tanımı ve sonucun listeye çevrilmesi için `list(...)` sarmalaması gerektirir; bu da kodda görsel gürültü ve iç içe parantez karmaşası yaratır. Liste üreteci ise konuşma diline (`[g.upper() for g in gezegenler]`) çok yakındır.
> 2. `reduce` fonksiyonu akümülatör mekanizması nedeniyle kodu okuyan kişinin zihninde ara durumları takip etmesini zorlaştırır. Nitekim Python'ın yaratıcısı Guido van Rossum da bu gerekçeyle `reduce`'u Python 3'te yerleşik fonksiyonlar arasından çıkarmış ve `functools` modülüne taşımıştır. `sum(len(b) for b in baglantilar.values())` yazımı hem niyet-belirtici (declarative) hem de C seviyesinde optimize olduğu için açık ara daha temizdir.

---

### Bonus (+10) – zamanlayici() Üreteci ve Meşgul Bekleme Analizi
`uzay_oyunu/bonus.py` dosyasında `zamanlayici(aralik)` üreteci kullanılarak 10 saniye boyunca her 2 saniyede *"tik"*, her 5 saniyede *"tak"* yazdıran program geliştirilmiştir.

#### Meşgul Bekleme (Busy Waiting / Spinning) Nedir ve `time.sleep` ile Farkı
1. **Meşgul Bekleme (Busy Waiting / Spinlock):**
   - Program hedef sürenin dolmasını beklerken `while time.perf_counter() < hedef: pass` şeklinde sıkı bir döngüde işlemci saatini sürekli yoklar (polling).
   - İşletim sistemine beklemede olduğu bildirilmez.
   - Bu durum bir CPU çekirdeğinin bekleme boyunca **%100 yük altında** çalışmasına, aşırı güç tüketimine ve ısınmaya neden olur.
2. **`time.sleep()` ile Farkı:**
   - `time.sleep(sure)` bir işletim sistemi sistem çağrısıdır (syscall).
   - İşletim sistemi çekirdeği (kernel), ilgili iş parçacığını (thread) *uyku/bloke* (sleep/blocked) kuyruğuna taşır ve işlemciyi derhal serbest bırakır.
   - CPU başka süreçleri yürütür ya da boştaysa düşük güç durumuna (C-states) geçer; CPU kullanımı **%0** olur.
   - Süre dolduğunda donanım zamanlayıcı kesmesi (hardware timer interrupt) iş parçacığını uyandırır ve CPU hazır kuyruğuna geri alır.

---

## 🧪 Testlerin Çalıştırılması

Tüm eski (Hafta 3) ve yeni (Hafta 4) birim testler `uv run pytest` komutu ile eksiksiz olarak çalıştırılabilir:

```bash
uv run pytest
```

### Test Özeti
```text
tests/test_akis.py .................                                     [ 42%]
tests/test_bonus.py ...                                                  [ 50%]
tests/test_fonksiyonlar.py ..............                                [ 85%]
tests/test_istatistik.py ....                                            [ 95%]
tests/test_tuzaklar.py ..                                                [100%]

============================= 40 passed in 0.15s ==============================
```

- **Toplam Test Sayısı:** 40
- **Test Kapsamı:** Tek kullanımlık Fibonacci üreteci, `StopIteration` yakıt tüketimi ve travel entegrasyonu, tembel boru hattı okuması, `@lru_cache` rota sayacı doğrulaması ve hit artışı, `map`/`filter`/`reduce`/`partial` istatistikleri, meşgul bekleme zamanlayıcısı ve Hafta 3 fonksiyon/tuzak testleri.
