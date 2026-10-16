# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve Akış Testleri

import inspect
import itertools
from pathlib import Path
import types
import pytest
from uzay_oyunu.akis import (
    fibonacci,
    yakit_gostergesi,
    satirlari_oku,
    ayristir,
    uzun_yolculuklar,
)


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


# ==============================================================================
# Görev 2 Testleri – Yakıt Göstergesi Üreteci
# ==============================================================================

def test_yakit_gostergesi_ornek_cikti() -> None:
    """PDF'teki örnek list(yakit_gostergesi(100, 30)) çıktısını test eder."""
    beklenen = [70, 40, 10, 0]
    assert list(yakit_gostergesi(100, 30)) == beklenen


def test_yakit_gostergesi_stop_iteration() -> None:
    """Yakıt tükendiğinde next() çağrısının StopIteration fırlattığını test eder."""
    g = yakit_gostergesi(20, 10)
    assert next(g) == 10
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_yakit_gostergesi_tam_bolunmeyen_tuketim() -> None:
    """Tüketim tam bölünmediğinde yakıtın sıfıra inip durmasını test eder."""
    # 25 -> 15 -> 5 -> 0
    assert list(yakit_gostergesi(25, 10)) == [15, 5, 0]


def test_yakit_gostergesi_hatali_tuketim() -> None:
    """Tüketim sıfır veya negatif verildiğinde ValueError fırlatılmalıdır."""
    with pytest.raises(ValueError):
        list(yakit_gostergesi(100, 0))

    with pytest.raises(ValueError):
        list(yakit_gostergesi(100, -5))


def test_travel_yakit_bitisi(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """travel() fonksiyonunda yakıt bittiğinde StopIteration yakalanıp kaybetme mesajı verildiğini test eder."""
    from uzay_oyunu import oyun

    # Mock galaksi: 10 yakıt ile başlat, tüketim 5 olduğu için 2 adımda yakıt biter, 3. adımda StopIteration fırlatır
    mock_galaksi = {
        "gezegenler": ["dünya", "centauri"],
        "baglantilar": {
            "dünya": ["centauri"],
            "centauri": ["dünya"],
        },
        "konum": "dünya",
        "yakit": 10,
    }
    monkeypatch.setattr(oyun, "veri_yukle", lambda: mock_galaksi)

    # Oyuncu sürekli "1" seçerek gezegenler arasında seyahat eder
    girdiler = iter(["1", "1", "1", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(girdiler))

    oyun.travel()
    cikti = capsys.readouterr().out
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in cikti


# ==============================================================================
# Görev 3 Testleri – Seyir Defteri Boru Hattı
# ==============================================================================

def test_seyir_defteri_toplam_yakit() -> None:
    """PDF'teki toplam yakıt tüketimi örneğini test eder (88)."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"
    toplam = sum(y for _, _, y in ayristir(satirlari_oku(dosya)))
    assert toplam == 88


def test_seyir_defteri_uzun_yolculuklar() -> None:
    """PDF'teki 10 eşiği üzerindeki uzun yolculukların hedeflerini test eder."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"
    kayitlar = ayristir(satirlari_oku(dosya))
    hedefler = [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_tembellik_ve_generator() -> None:
    """Boru hattındaki fonksiyonların bir liste değil, üreteç (generator) döndürdüğünü test eder."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"

    g_satirlar = satirlari_oku(dosya)
    assert inspect.isgenerator(g_satirlar)

    g_kayitlar = ayristir(g_satirlar)
    assert inspect.isgenerator(g_kayitlar)

    g_uzun = uzun_yolculuklar(g_kayitlar, 10)
    assert inspect.isgenerator(g_uzun)


def test_satirlari_oku_yorum_ve_bosluklari_atlar(tmp_path: Path) -> None:
    """satirlari_oku üretecinin '#' ile başlayan yorumları ve boş satırları atladığını test eder."""
    test_dosyasi = tmp_path / "test_seyir.txt"
    test_dosyasi.write_text(
        "# Baslangic yorumu\n\n"
        "dunya -> mars 10\n"
        "   \n"
        "# Ara yorum\n"
        "mars -> jupiter 20\n",
        encoding="utf-8",
    )
    satirlar = list(satirlari_oku(test_dosyasi))
    assert satirlar == ["dunya -> mars 10", "mars -> jupiter 20"]


