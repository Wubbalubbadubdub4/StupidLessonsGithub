# İleri Python Programlama - Hafta 4 Lab Ödevi

**Öğrenci Adı Soyadı:** Alp Dinçoğlu  
**Öğrenci Numarası:** 20253006040  
**Kurum:** İstanbul Nişantaşı Üniversitesi  
**Ders:** İleri Python Programlama  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  
**GitHub Deposu:** https://github.com/Wubbalubbadubdub4/StupidLessonsGithub  

---

## Proje Hakkında

Bu ödevde uzay oyunu projesi üzerine üreteçler (generators), veri işleme boru hattı, `@functools.lru_cache` ile önbellekli rota sayacı, fonksiyonel programlama araçları (`map`, `filter`, `reduce`, `partial`) ve meşgul bekleme (busy waiting) zamanlayıcısı eklenmiştir.

Tüm geliştirmeler `uzay_oyunu/akis.py` ve `uzay_oyunu/istatistik.py` modüllerinde toplanmış, testler ise `tests/test_akis.py` dosyasında yazılmıştır.

---

## Görevlerin Özeti

### Görev 1: Fibonacci Üreteci
`uzay_oyunu/akis.py` içinde sonsuz `fibonacci()` üreteci yazılmıştır.
Değerler 3 farklı yöntemle çekilmiştir:
- `next()` ile ilk 3 eleman: `(0, 1, 1)`
- `itertools.islice()` ile ilk 12 eleman: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`
- `itertools.takewhile()` ile 100'den küçük elemanlar: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]`

Üretecin tek kullanımlık olduğu (aynı üreteçten yapılan ardışık `islice` çağrılarının farklı sonuç verdiği) test edilmiştir.

### Görev 2: Yakıt Göstergesi
`yakit_gostergesi(yakit, tuketim)` üreteci her adımda yakıtı tüketim kadar azaltıp kalan değeri döndürür, yakıt sıfıra inince durur.
- `list(yakit_gostergesi(100, 30))` çağrısı `[70, 40, 10, 0]` üretir.
- `travel()` döngüsüne entegre edilmiştir. Her seyahat hamlesinde göstergeden bir değer çekilir.
- Yakıt bittiğinde fırlatılan `StopIteration` yakalanarak oyuncuya "Yakıtın bitti, uzayda sürükleniyorsun…" mesajı verilir ve oyun biter.

### Görev 3: Seyir Defteri Boru Hattı
`veri/seyir.txt` dosyasındaki verileri bellek dostu şekilde işleyen 3 aşamalı üreteç boru hattı kurulmuştur:
1. `satirlari_oku(yol)`: Dosyayı satır satır okur, `#` ile başlayan yorumları ve boş satırları atlar.
2. `ayristir(satirlar)`: Her satırdan `(kaynak, hedef, yakit)` demeti üretir.
3. `uzun_yolculuklar(kayitlar, esik)`: Yakıtı eşikten büyük olanları süzer.

Hiçbir aşamada dosyanın tamamı listeye okunmamıştır.
- Toplam yakıt: `88`
- Eşik 10 için uzun yolculuk hedefleri: `['sirius', 'centauri', 'orion', 'kara_delik']`

### Görev 4: Önbellekli Rota Sayacı ve Süre Ölçümü
`rota_sayaci(baglantilar)` fonksiyonu, içinde `@lru_cache(maxsize=None)` ile süslenmiş `rota_sayisi(gezegen, adim)` fonksiyonunu döndürür.
- `say("dünya", 3)` -> `9`
- `say("dünya", 10)` -> `2185`
- `say("dünya", 40)` -> `16832258606399`

#### Süre Karşılaştırması ve `cache_info()` Çıktısı (`adim=20`)

Ölçümler `time.perf_counter()` ile yapılmıştır:

| Yöntem | Başlangıç | Adım | Rota Sayısı | Süre (sn) | `cache_info()` Çıktısı |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Önbelleksiz Saf Özyineleme** | dünya | 20 | 4.315.343 | **2.123026 sn** | - |
| **Önbellekli (`@lru_cache`)** | dünya | 20 | 4.315.343 | **0.000119 sn** | `CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)` |

Önbellek sayesinde aynı alt problemler tekrar hesaplanmamış ve işlem yaklaşık 17.800 kat hızlanmıştır.

### Görev 5: map, filter, reduce ve partial
`uzay_oyunu/istatistik.py` modülünde galaksi verisi üzerinde 3 soru ikişer yolla yanıtlanmıştır:
1. Gezegen adlarının büyük harfli listesi: `map` ve liste üreteci (`['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']`)
2. En az 2 bağlantısı olan gezegenler: `filter` ve liste üreteci (`['dünya', 'centauri', 'sirius', 'orion']`)
3. Toplam bağlantı sayısı: `reduce` ve `sum` (`10`)
4. `functools.partial` ile `yolculuk` fonksiyonundan `hiz=3` sabitlenerek `hizli_yolculuk` türetilmiştir.

**Okunabilirlik Değerlendirmesi:**
Liste üreteçleri (`[x for x in ...]`) ve yerleşik `sum()` fonksiyonu; `map`, `filter` ve `reduce` yapılarına göre çok daha okunabilirdir. `map` ve `filter` yazarken ekstra `lambda` fonksiyonu ve `list()` sarmalaması gerektiği için kod görsel olarak kalabalıklaşır. `reduce` ise akümülatör yapısı nedeniyle zihinde takip etmesi zor bir fonksiyondur. Liste üreteci ve `sum()` ise doğrudan konuşma diline yakındır ve ne yaptığı ilk bakışta anlaşılır.

### Bonus (+10): zamanlayici() Üreteci ve Meşgul Bekleme
`uzay_oyunu/akis.py` içinde `zamanlayici(aralik)` üreteci yazılmış ve 10 saniye boyunca her 2 saniyede "tik", her 5 saniyede "tak" basan `tik_tak_programi()` fonksiyonu eklenmiştir.

**Neden Meşgul Bekleme (Busy Waiting)?**
Fonksiyon süre dolana kadar bir `while` döngüsü içinde sürekli saati sorgulamaktadır (`pass`). Bu süreçte CPU hiç dinlenmez, sürekli döngü komutlarını çalıştırır. Bu durum tek bir işlemci çekirdeğinin %100 kullanım oranına çıkmasına neden olur.

**`time.sleep` ile Farkı:**
`time.sleep()` fonksiyonunda Python, işletim sistemi çekirdeğine (kernel) sistem çağrısı yapar. İşletim sistemi iş parçacığını uyku/bekleme kuyruğuna alır ve CPU'yu tamamen serbest bırakır. CPU başka işlerle ilgilenebilir veya boştaysa uyku durumuna geçerek güç tasarrufu sağlar (%0 CPU kullanımı). Süre dolduğunda donanım zamanlayıcı kesmesi programı uyandırır.

---

## Testlerin Çalıştırılması

Tüm testler `uv run pytest` ile çalıştırılabilir:

```bash
uv run pytest
```

39 testin tamamı başarıyla geçmektedir.
