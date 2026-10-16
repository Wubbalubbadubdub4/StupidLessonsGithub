# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Görev 5: map, filter, reduce ve partial ile Galaksi İstatistikleri

import functools
from typing import Any, Callable


# Soru 1: Gezegen adlarının büyük harfli listesi
def gezegen_adlari_buyuk_map(galaksi: dict[str, Any]) -> list[str]:
    """map() ile gezegen adlarını büyük harfli liste yapar."""
    return list(map(str.upper, galaksi["gezegenler"]))


def gezegen_adlari_buyuk_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci ile gezegen adlarını büyük harfli liste yapar."""
    return [gezegen.upper() for gezegen in galaksi["gezegenler"]]


# Soru 2: En az iki bağlantısı olan gezegenler
def en_az_iki_baglanti_filter(galaksi: dict[str, Any]) -> list[str]:
    """filter() ile en az 2 bağlantısı olan gezegenleri bulur."""
    baglantilar = galaksi["baglantilar"]
    return list(filter(lambda g: len(baglantilar.get(g, [])) >= 2, galaksi["gezegenler"]))


def en_az_iki_baglanti_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci ile en az 2 bağlantısı olan gezegenleri bulur."""
    baglantilar = galaksi["baglantilar"]
    return [g for g in galaksi["gezegenler"] if len(baglantilar.get(g, [])) >= 2]


# Soru 3: Toplam bağlantı sayısı
def toplam_baglanti_reduce(galaksi: dict[str, Any]) -> int:
    """functools.reduce() ile toplam bağlantı sayısını hesaplar."""
    baglantilar = galaksi["baglantilar"]
    return functools.reduce(lambda acc, b: acc + len(b), baglantilar.values(), 0)


def toplam_baglanti_sum(galaksi: dict[str, Any]) -> int:
    """sum() kullanarak toplam bağlantı sayısını hesaplar."""
    return sum(len(b) for b in galaksi["baglantilar"].values())


# functools.partial ile hiz=3 sabit hızlı yolculuk fonksiyonu
def yolculuk(mesafe: float, hiz: float = 1.0) -> float:
    """Mesafeyi hıza bölerek seyahat süresini hesaplar."""
    if hiz <= 0:
        raise ValueError("Hız 0 veya negatif olamaz.")
    return mesafe / hiz


hizli_yolculuk: Callable[..., float] = functools.partial(yolculuk, hiz=3)


# Okunabilirlik Yorumu:
# Bence liste üreteçleri (list comprehension) ve yerleşik sum() fonksiyonu, map/filter/reduce
# yapılarına göre çok daha okunabilir ve anlaşılır. Çünkü map ve filter kullanırken ekstra
# lambda fonksiyonu tanımlamak ve sonucu list() içine almak gerekiyor, bu da satırı uzatıyor.
# reduce() ise ara toplam mantığı yüzünden takip etmesi zor bir fonksiyon.
# Liste üreteci ve sum() ise konuşma diline çok daha yakın, doğrudan ne yaptığı anlaşılıyor.
