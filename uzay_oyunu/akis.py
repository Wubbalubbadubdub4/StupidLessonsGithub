# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve functools: Akış ve Boru Hattı Modülü

from collections.abc import Generator
import itertools


# ==============================================================================
# Görev 1 – Fibonacci Üreteci (15 puan)
# ==============================================================================

def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreten üreteç (generator).

    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89... şeklinde sonsuza kadar devam eder.
    Bellekte tüm listeyi tutmak yerine her adımda bir sonraki değeri tembel (lazy) üretir.

    Yields:
        int: Sıradaki Fibonacci sayısı.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# ==============================================================================
# Görev 2 – Yakıt Göstergesi Üreteci (20 puan)
# ==============================================================================

def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tuketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'a inince veya altına düşünce 0 üretir ve durur (StopIteration fırlatır).

    Örnek:
    >>> list(yakit_gostergesi(100, 30))
    [70, 40, 10, 0]

    Args:
        yakit: Başlangıçtaki mevcut yakıt miktarı.
        tuketim: Her yolculuk adımında harcanacak yakıt.

    Yields:
        int: Kalan güncel yakıt miktarı (en az 0).

    Raises:
        ValueError: Tüketim sıfır veya negatif verilirse.
    """
    if tuketim <= 0:
        raise ValueError("Tüketim miktarı pozitif bir tam sayı olmalıdır.")

    kalan = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan

