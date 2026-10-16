# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Görev 5: İstatistik Fonksiyonları Testleri

import pytest
from uzay_oyunu.galaksi import veri_yukle
from uzay_oyunu.istatistik import (
    gezegen_adlari_buyuk_map,
    gezegen_adlari_buyuk_comprehension,
    en_az_iki_baglanti_filter,
    en_az_iki_baglanti_comprehension,
    toplam_baglanti_reduce,
    toplam_baglanti_sum,
    yolculuk,
    hizli_yolculuk,
)


def test_gezegen_adlari_buyuk() -> None:
    """Gezegen adlarının büyük harfli listesini iki yolla da test eder."""
    galaksi = veri_yukle()
    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]

    sonuc_map = gezegen_adlari_buyuk_map(galaksi)
    sonuc_comp = gezegen_adlari_buyuk_comprehension(galaksi)

    assert sonuc_map == beklenen
    assert sonuc_comp == beklenen
    assert sonuc_map == sonuc_comp


def test_en_az_iki_baglanti() -> None:
    """En az iki bağlantısı olan gezegenleri iki yolla da test eder."""
    galaksi = veri_yukle()
    beklenen = ["dünya", "centauri", "sirius", "orion"]

    sonuc_filter = en_az_iki_baglanti_filter(galaksi)
    sonuc_comp = en_az_iki_baglanti_comprehension(galaksi)

    assert sonuc_filter == beklenen
    assert sonuc_comp == beklenen
    assert sonuc_filter == sonuc_comp


def test_toplam_baglanti_sayisi() -> None:
    """Toplam bağlantı sayısını iki yolla da (reduce ve sum) test eder."""
    galaksi = veri_yukle()
    beklenen = 10

    sonuc_reduce = toplam_baglanti_reduce(galaksi)
    sonuc_sum = toplam_baglanti_sum(galaksi)

    assert sonuc_reduce == beklenen
    assert sonuc_sum == beklenen
    assert sonuc_reduce == sonuc_sum


def test_yolculuk_ve_hizli_yolculuk_partial() -> None:
    """yolculuk fonksiyonunu ve functools.partial ile türetilen hizli_yolculuk fonksiyonunu test eder."""
    # Standart yolculuk: 30 birim mesafe, varsayılan hız 1 -> 30 süre
    assert yolculuk(30) == 30.0
    assert yolculuk(30, hiz=2) == 15.0

    # hizli_yolculuk: hiz=3 sabitlenmiştir -> 30 / 3 = 10.0
    assert hizli_yolculuk(30) == 10.0
    assert hizli_yolculuk(15) == 5.0
    assert hizli_yolculuk(6) == 2.0

    # Geçersiz hız kontrolü
    with pytest.raises(ValueError):
        yolculuk(10, hiz=0)
    with pytest.raises(ValueError):
        yolculuk(10, hiz=-1)
