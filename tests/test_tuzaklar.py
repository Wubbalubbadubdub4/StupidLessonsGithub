# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 3 – Görev 4: Varsayılan argüman tuzağı ve None kalıbı

import pytest


def yakit_ekle(miktar: int, depo: list[int] | None = None) -> list[int]:
    """Depoya yakıt ekler, varsayılan liste tuzağını önlemek için None kalıbı kullanılır."""
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo


def test_yakit_ekle_tuzak() -> None:
    """Boş bırakıldığında her çağrıda bağımsız yeni liste oluşmalıdır."""
    gemi1 = yakit_ekle(50)
    assert gemi1 == [50]

    gemi2 = yakit_ekle(30)
    assert gemi2 == [30]


def test_yakit_ekle_mevcut_depo() -> None:
    """Var olan bir depo verildiğinde liste üzerine ekleme yapmalıdır."""
    ozel_depo = [10, 20]
    sonuc = yakit_ekle(30, ozel_depo)
    assert sonuc == [10, 20, 30]
    assert sonuc is ozel_depo
