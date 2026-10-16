# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve Akış Testleri

import itertools
import pytest
from uzay_oyunu.akis import fibonacci


# ==============================================================================
# Görev 1 Testleri – Fibonacci Üreteci
# ==============================================================================

def test_fibonacci_next() -> None:
    """next() çağrıları ile Fibonacci serisinin ilk 3 elemanını test eder."""
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice() -> None:
    """itertools.islice ile Fibonacci serisinin ilk 12 elemanını test eder."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(itertools.islice(fibonacci(), 12))
    assert sonuc == beklenen


def test_fibonacci_takewhile() -> None:
    """itertools.takewhile ile 100'den küçük Fibonacci sayılarını test eder."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    sonuc = list(itertools.takewhile(lambda x: x < 100, fibonacci()))
    assert sonuc == beklenen


def test_fibonacci_tek_kullanimlik() -> None:
    """Üretecin tek kullanımlık olduğunu ve tükenerek ilerlediğini test eder.

    Aynı üreteç nesnesinden yapılan ikinci 5 elemanlık islice çağrısı ilkine göre
    farklı sonuçlar vermelidir.
    """
    g = fibonacci()
    ilk_5 = list(itertools.islice(g, 5))
    ikinci_5 = list(itertools.islice(g, 5))

    assert ilk_5 == [0, 1, 1, 2, 3]
    assert ikinci_5 == [5, 8, 13, 21, 34]
    assert ilk_5 != ikinci_5
