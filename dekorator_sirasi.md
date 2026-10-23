# Dekoratör Sırası Analizi – Fibonacci Çağrı Sayıları

**Ad:** Alp Dinçoğlu | **Numara:** 20253006040  
**Ders:** İleri Python Programlama – Hafta 5

---

## Sonuçlar

| Uygulama Biçimi              | fib(20) için @say çağrı sayısı |
|------------------------------|-------------------------------|
| Yalnızca `@say`              | **21 891**                    |
| `@say` üstte, `@lru_cache` altta | **39**               |
| `@lru_cache` üstte, `@say` altta | **21**               |

---

## Neden Farklı?

### 1. Yalnızca `@say` → 21 891

`@lru_cache` yoktur; her `fib(n)` çağrısı özyinelemeli olarak ağaç genişliğinde açılır.  
`fib(20)` için yapılan toplam çağrı sayısı `2·fib(20) - 1 = 21891`'dir çünkü klasik  
özyinelemeli Fibonacci üstel sayıda çağrı üretir.

```
fib(20) → fib(19) + fib(18)
              ↓          ↓
         fib(18)+fib(17)  fib(17)+fib(16)
         …                …
```

---

### 2. `@say` üstte, `@lru_cache` altta → 39

Dekoratör yığını şöyle oluşur:

```python
@say          # En dışta
@lru_cache    # İçte
def fib(n): …
```

`fib` değişkeni `say_sarmalayici → lru_cache_sarmalayici → asıl_fib` zincirini gösterir.  
Her **dış çağrı** önce `say`'ı çarpar, ardından `lru_cache`'i kontrol eder.  
`lru_cache` miss olduğunda `asıl_fib` içinden yapılan özyinelemeli çağrılar da  
`fib(n-1)` yani yeniden `say → lru_cache` yolunu izler.

- İlk açılımda 0..20 için 21 benzersiz değer hesaplanır.  
- Her benzersiz değer için: bir kez "miss → asıl_fib çağır" → `say` 1 artırır.  
- Sonraki örtüşen çağrılar cache'den döner ama dış `say` sarmalayıcısı yine tetiklenir.

Toplam: **39** (21 yeni hesap + 18 örtüşen cache hit sayısı).

---

### 3. `@lru_cache` üstte, `@say` altta → 21

```python
@lru_cache    # En dışta
@say          # İçte
def fib(n): …
```

`fib` değişkeni `lru_cache_sarmalayici → say_sarmalayici → asıl_fib` zincirini gösterir.  
`lru_cache` **en dışta** olduğundan:

- `fib(20)` ilk çağrıldığında cache'de yoktur; `say_sarmalayici` çalışır, sayaç artar.  
- Özyinelemeli `fib(n-1)` ve `fib(n-2)` çağrılarında, daha önce hesaplananlar  
  doğrudan `lru_cache` tarafından yakalanır; `say_sarmalayici`'ya **ulaşılmaz**.

Dolayısıyla `say` yalnızca **gerçekten yeni hesaplanan 21 benzersiz değer** için tetiklenir.

> **Not:** Sayacı okumak için `fib.__wrapped__.cagri` kullanılır, çünkü `fib` artık  
> `lru_cache` sarmalayıcısıdır ve doğrudan `.cagri` niteliği taşımaz;  
> `__wrapped__` orijinal `say_sarmalayici`'ya ulaştırır.

---

## Özet İlke

> Hangi dekoratör **dışarıda** ise o, her çağrıda **ilk** çalışır.  
> `@lru_cache` dışarıdaysa tekrarlanan girişleri içteki fonksiyona iletmeden keser,  
> bu nedenle `@say` daha az kez tetiklenir ve daha az çağrı sayar.
