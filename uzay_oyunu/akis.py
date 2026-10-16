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
