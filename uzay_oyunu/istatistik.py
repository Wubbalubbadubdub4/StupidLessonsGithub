# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Görev 5: map, filter, reduce ve partial ile Galaksi İstatistikleri

import functools
from typing import Any, Callable


# ==============================================================================
# Soru 1: Gezegen Adlarının Büyük Harfli Listesi
# Beklenen: ['DÜNYA', 'CENTAURI', 'SIRIUS', 'ORION', 'KARA_DELIK']
# ==============================================================================

def gezegen_adlari_buyuk_map(galaksi: dict[str, Any]) -> list[str]:
    """map() kullanarak gezegen adlarının büyük harfli listesini üretir."""
    return list(map(str.upper, galaksi["gezegenler"]))


def gezegen_adlari_buyuk_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci (comprehension) kullanarak gezegen adlarını büyük harfe çevirir."""
    return [gezegen.upper() for gezegen in galaksi["gezegenler"]]


# ==============================================================================
# Soru 2: En Az İki Bağlantısı Olan Gezegenler
# Beklenen: ['dünya', 'centauri', 'sirius', 'orion']
# ==============================================================================

def en_az_iki_baglanti_filter(galaksi: dict[str, Any]) -> list[str]:
    """filter() kullanarak en az iki bağlantısı olan gezegenleri döndürür."""
    baglantilar = galaksi["baglantilar"]
    return list(filter(lambda g: len(baglantilar.get(g, [])) >= 2, galaksi["gezegenler"]))


def en_az_iki_baglanti_comprehension(galaksi: dict[str, Any]) -> list[str]:
    """Liste üreteci kullanarak en az iki bağlantısı olan gezegenleri döndürür."""
    baglantilar = galaksi["baglantilar"]
    return [g for g in galaksi["gezegenler"] if len(baglantilar.get(g, [])) >= 2]


# ==============================================================================
# Soru 3: Toplam Bağlantı Sayısı
# Beklenen: 10
# ==============================================================================

def toplam_baglanti_reduce(galaksi: dict[str, Any]) -> int:
    """functools.reduce() kullanarak galaksideki toplam bağlantı sayısını hesaplar."""
    baglantilar = galaksi["baglantilar"]
    return functools.reduce(lambda acc, b: acc + len(b), baglantilar.values(), 0)


def toplam_baglanti_sum(galaksi: dict[str, Any]) -> int:
    """sum() ve üreteç ifadesi kullanarak galaksideki toplam bağlantı sayısını hesaplar."""
    return sum(len(b) for b in galaksi["baglantilar"].values())


# ==============================================================================
# functools.partial ile Hızlı Yolculuk Türetimi
# ==============================================================================

def yolculuk(mesafe: float, hiz: float = 1.0) -> float:
    """Belirtilen mesafeyi verilen hızda gitmek için gereken seyahat süresini hesaplar.

    Args:
        mesafe: Kat edilecek uzay mesafesi (ışık yılı vb.).
        hiz: Seyahat hızı (varsayılan 1.0).

    Returns:
        float: Harcanan süre (mesafe / hiz).

    Raises:
        ValueError: Hız sıfır veya negatif olursa.
    """
    if hiz <= 0:
        raise ValueError("Seyahat hızı sıfırdan büyük olmalıdır.")
    return mesafe / hiz


# functools.partial ile hız parametresi 3 olarak sabitlenmiş yeni fonksiyon
hizli_yolculuk: Callable[..., float] = functools.partial(yolculuk, hiz=3)


# ==============================================================================
# Okunabilirlik Karşılaştırması ve Değerlendirme:
#
# Python ekosisteminde ve 'The Zen of Python' (PEP 20 - "Readability counts")
# prensiplerinde, Liste Üreteçleri (Comprehensions) ve yerleşik sum() fonksiyonu,
# map/filter/reduce fonksiyonel araçlarına göre çok daha okunabilir ve anlaşılırdır.
#
# 1. map ve filter yapıları ek lambda yazımı ve akabinde list(...) sarmalaması
#    gerektirdiği için kodda fazladan parantez ve görsel gürültü oluşturur.
#    Buna karşılık [g.upper() for g in gezegenler] ifadesi doğrudan konuşma diline
#    yakındır ve ne yaptığı ilk bakışta anlaşılır.
#
# 2. reduce fonksiyonu ise birikimli (accumulator) durum mantığı nedeniyle takip
#    edilmesi en zor yapıdır. Guido van Rossum da bu nedenle reduce'u Python 3'te
#    çekirdek dilden çıkarıp functools modülüne taşımıştır. Toplama işlemleri için
#    sum(len(b) for b in baglantilar.values()) ifadesi hem çok daha niyet-belirtici
#    (declarative) hem de Python C düzeyinde son derece hızlı ve temizdir.
# ==============================================================================
