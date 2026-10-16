# İleri Python - 4. Hafta Ödevi

**Ad Soyad:** Alp Dinçoğlu  
**Öğrenci No:** 20253006040  

Bu repoda uzay oyunu projesinin 4. hafta lab ödevi (üreteçler ve functools) yer alıyor.

- `uzay_oyunu/akis.py`: Fibonacci üreteci, yakıt göstergesi, seyir defteri boru hattı ve rota sayacı burada.
- `uzay_oyunu/istatistik.py`: map, filter, reduce ve partial fonksiyonları burada.
- `veri/seyir.txt`: Boru hattının okuduğu seyahat kayıtları.
- `tests/test_akis.py`: Tüm görevlerin testleri burada.

### Görev 4 Süre Ölçümü (adim=20)
- Önbelleksiz süre: 2.12 saniye
- `@lru_cache` ile süre: 0.0001 saniye
- `cache_info()` çıktısı: `CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)`

### Testleri Çalıştırma
```bash
uv run pytest
```
