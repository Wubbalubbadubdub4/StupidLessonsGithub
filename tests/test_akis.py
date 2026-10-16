# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve Akış Testleri

import inspect
import itertools
from pathlib import Path
import pytest

from uzay_oyunu.akis import (
    fibonacci,
    yakit_gostergesi,
    satirlari_oku,
    ayristir,
    uzun_yolculuklar,
    rota_sayaci,
    rota_sayisi_onbelleksiz,
    zamanlayici,
    tik_tak_programi,
)
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


# --- Görev 1: Fibonacci Testleri ---

def test_fibonacci_next() -> None:
    """next() çağrıları ile Fibonacci serisinin ilk 3 elemanını kontrol eder."""
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice() -> None:
    """itertools.islice ile ilk 12 elemanı alır."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(itertools.islice(fibonacci(), 12)) == beklenen


def test_fibonacci_takewhile() -> None:
    """itertools.takewhile ile 100'den küçük elemanları alır."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(itertools.takewhile(lambda x: x < 100, fibonacci())) == beklenen


def test_fibonacci_tek_kullanimlik() -> None:
    """Üretecin tek kullanımlık olduğunu ve ardışık çağrılarda ilerlediğini gösterir."""
    g = fibonacci()
    ilk = list(itertools.islice(g, 5))
    ikinci = list(itertools.islice(g, 5))

    assert ilk == [0, 1, 1, 2, 3]
    assert ikinci == [5, 8, 13, 21, 34]
    assert ilk != ikinci


# --- Görev 2: Yakıt Göstergesi Testleri ---

def test_yakit_gostergesi_ornek() -> None:
    """Ödev kağıdındaki örnek list(yakit_gostergesi(100, 30)) çıktısını test eder."""
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_stop_iteration() -> None:
    """Yakıt bitince next() çağrısının StopIteration fırlattığını kontrol eder."""
    g = yakit_gostergesi(20, 10)
    assert next(g) == 10
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_yakit_gostergesi_tam_bolunmeyen() -> None:
    """Tüketim tam bölünmediğinde sıfırda durmasını test eder."""
    assert list(yakit_gostergesi(25, 10)) == [15, 5, 0]


def test_yakit_gostergesi_hatali_parametre() -> None:
    """Pozitif olmayan tüketimde ValueError fırlatmalıdır."""
    with pytest.raises(ValueError):
        list(yakit_gostergesi(100, 0))


def test_travel_yakit_bitisi(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """travel() fonksiyonunda yakıt bittiğinde StopIteration yakalanıp kaybetme mesajı verildiğini test eder."""
    from uzay_oyunu import oyun

    mock_galaksi = {
        "gezegenler": ["dünya", "centauri"],
        "baglantilar": {"dünya": ["centauri"], "centauri": ["dünya"]},
        "konum": "dünya",
        "yakit": 10,
    }
    monkeypatch.setattr(oyun, "veri_yukle", lambda: mock_galaksi)

    girdiler = iter(["1", "1", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(girdiler))

    oyun.travel()
    cikti = capsys.readouterr().out
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in cikti


# --- Görev 3: Seyir Defteri Boru Hattı Testleri ---

def test_seyir_defteri_toplam_yakit() -> None:
    """seyir.txt içindeki toplam yakıtın 88 olduğunu doğrular."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"
    toplam = sum(y for _, _, y in ayristir(satirlari_oku(dosya)))
    assert toplam == 88


def test_seyir_defteri_uzun_yolculuklar() -> None:
    """Eşik değeri 10 üzerindeki seyahatlerin hedeflerini doğrular."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"
    kayitlar = ayristir(satirlari_oku(dosya))
    hedefler = [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_generator_tipi() -> None:
    """Boru hattındaki fonksiyonların liste yerine generator döndürdüğünü kontrol eder."""
    dosya = Path(__file__).parent.parent / "veri" / "seyir.txt"

    g1 = satirlari_oku(dosya)
    assert inspect.isgenerator(g1)

    g2 = ayristir(g1)
    assert inspect.isgenerator(g2)

    g3 = uzun_yolculuklar(g2, 10)
    assert inspect.isgenerator(g3)


def test_satirlari_oku_filtreleme(tmp_path: Path) -> None:
    """satirlari_oku fonksiyonunun boşluk ve '#' yorum satırlarını atladığını test eder."""
    dosya = tmp_path / "deneme.txt"
    dosya.write_text("# Yorum\n\ndunya -> mars 10\n   \nmars -> jupiter 20\n", encoding="utf-8")
    assert list(satirlari_oku(dosya)) == ["dunya -> mars 10", "mars -> jupiter 20"]


# --- Görev 4: Önbellekli Rota Sayacı Testleri ---

def test_rota_sayaci_ornek_degerler() -> None:
    """Ödevdeki örnek rota değerlerini kontrol eder: (9, 2185, 16832258606399)."""
    galaksi = veri_yukle()
    say = rota_sayaci(galaksi["baglantilar"])

    assert say("dünya", 3) == 9
    assert say("dünya", 10) == 2185
    assert say("dünya", 40) == 16832258606399


def test_rota_sayaci_cache_calismasi() -> None:
    """Önbelleğe alma ile hit sayısının arttığını kontrol eder."""
    galaksi = veri_yukle()
    say = rota_sayaci(galaksi["baglantilar"])

    say("dünya", 10)
    hits1 = say.cache_info().hits
    assert hits1 > 0

    say("dünya", 10)
    assert say.cache_info().hits == hits1 + 1


def test_rota_sayaci_adim_sifir() -> None:
    """Adım sayısı 0 iken rotanın 1 olduğunu doğrular."""
    galaksi = veri_yukle()
    say = rota_sayaci(galaksi["baglantilar"])
    for g in galaksi["gezegenler"]:
        assert say(g, 0) == 1


def test_rota_sayaci_onbelleksiz_tutarlilik() -> None:
    """Önbellekli ile önbelleksiz sürümün aynı sonucu verdiğini doğrular."""
    galaksi = veri_yukle()
    b = galaksi["baglantilar"]
    say_onb = rota_sayaci(b)

    for adim in range(1, 6):
        assert say_onb("dünya", adim) == rota_sayisi_onbelleksiz(b, "dünya", adim)


# --- Görev 5: İstatistik Fonksiyonları Testleri ---

def test_gezegen_adlari_buyuk() -> None:
    """Gezegen adlarının iki yöntemle de büyük harfe çevrildiğini test eder."""
    galaksi = veri_yukle()
    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]

    assert gezegen_adlari_buyuk_map(galaksi) == beklenen
    assert gezegen_adlari_buyuk_comprehension(galaksi) == beklenen


def test_en_az_iki_baglanti() -> None:
    """En az iki bağlantısı olan gezegenleri iki yöntemle test eder."""
    galaksi = veri_yukle()
    beklenen = ["dünya", "centauri", "sirius", "orion"]

    assert en_az_iki_baglanti_filter(galaksi) == beklenen
    assert en_az_iki_baglanti_comprehension(galaksi) == beklenen


def test_toplam_baglanti_sayisi() -> None:
    """Toplam bağlantı sayısını iki yöntemle (reduce ve sum) test eder."""
    galaksi = veri_yukle()
    assert toplam_baglanti_reduce(galaksi) == 10
    assert toplam_baglanti_sum(galaksi) == 10


def test_hizli_yolculuk_partial() -> None:
    """yolculuk ve hiz=3 partial türevinin doğru çalıştığını test eder."""
    assert yolculuk(30) == 30.0
    assert hizli_yolculuk(30) == 10.0
    assert hizli_yolculuk(15) == 5.0
    with pytest.raises(ValueError):
        yolculuk(10, 0)


# --- Bonus Görevi Testleri ---

def test_zamanlayici_aralik_kontrolu() -> None:
    """Zamanlayıcı aralığı pozitif olmalıdır."""
    with pytest.raises(ValueError):
        next(zamanlayici(0))


def test_tik_tak_programi_calisma(capsys: pytest.CaptureFixture[str]) -> None:
    """tik_tak_programi fonksiyonunun çalıştığını kontrol eder."""
    olaylar = tik_tak_programi(toplam_sure=0.05, yazdir=False)
    assert isinstance(olaylar, list)
