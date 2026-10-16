# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 3 – Görev 5 & Bonus: Closure, lambda sıralaması ve süre ölçen dekoratör

import functools
import time
from typing import Any, Callable


def hamle_sayaci() -> Callable[[], int]:
    """Her çağrıldığında 1 artan bir sayaç fonksiyonu (closure) döndürür."""
    sayac = 0

    def artir() -> int:
        nonlocal sayac
        sayac += 1
        return sayac

    return artir


def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Verilen fonksiyonun çalışma süresini ölçüp ekrana yazdıran dekoratör."""
    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        print(f"{fonksiyon.__name__} süresi: {bitis - baslangic:.6f} saniye")
        return sonuc

    return sarmalayici


def en_bagli_gezegenler(galaksi: dict[str, Any]) -> list[str]:
    """Gezegenleri bağlantı sayısına göre azalan, eşitlikte alfabetik sırayla döndürür."""
    baglantilar = galaksi.get("baglantilar", {})
    gezegenler = galaksi.get("gezegenler", list(baglantilar.keys()))
    return sorted(
        gezegenler,
        key=lambda g: (-len(baglantilar.get(g, [])), g),
    )
