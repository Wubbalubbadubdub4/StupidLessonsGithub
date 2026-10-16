# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 3 – Fonksiyonların Birim Testleri

import pytest
from uzay_oyunu.oyun import envanter_metni, hedef_menusu
from uzay_oyunu.kayit import gorev_kaydi
from uzay_oyunu.galaksi import galaksi_kur, veri_yukle
from uzay_oyunu.araclar import hamle_sayaci, en_bagli_gezegenler, sure_olc


# --- Görev 1 Testleri ---

def test_envanter_metni_dolu() -> None:
    """Eşyalar varken beklenen envanter metninin dönmesini test eder."""
    sonuc = envanter_metni(True, False, True)
    assert sonuc == "Sende: bol kredi, yetenekli bir pilot"


def test_envanter_metni_bos() -> None:
    """Hiç eşya yoksa boş metin dönmesini test eder."""
    assert envanter_metni(False, False, False) == ""


def test_envanter_metni_tum_esyalar() -> None:
    """Tüm eşyalar varken tam liste dönmesini test eder."""
    sonuc = envanter_metni(True, True, True)
    assert sonuc == "Sende: bol kredi, hiper motor, yetenekli bir pilot"


def test_hedef_menusu() -> None:
    """Hedeflerin numaralandırılmış liste olarak dönmesini test eder."""
    beklenen = "Nereye gitmek istersin?\n[1] centauri\n[2] sirius"
    assert hedef_menusu(["centauri", "sirius"]) == beklenen


def test_hedef_menusu_tek_hedef() -> None:
    """Tek hedef olduğunda düzgün formatlanmasını test eder."""
    beklenen = "Nereye gitmek istersin?\n[1] orion"
    assert hedef_menusu(["orion"]) == beklenen


# --- Görev 2 Testleri ---

def test_gorev_kaydi(capsys: pytest.CaptureFixture[str]) -> None:
    """Standart parametrelerle görev kaydı çıktısını test eder."""
    gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan",
        "Pilot bul",
        "Hiperdrive al",
        oncelik="yüksek",
        sorumlu="Ayşe",
    )
    captured = capsys.readouterr()
    beklenen = (
        "[YÜKSEK] Kara deliğe atla\n"
        " 1. Kredi kazan\n"
        " 2. Pilot bul\n"
        " 3. Hiperdrive al\n"
        " sorumlu: Ayşe\n"
    )
    assert captured.out == beklenen


def test_gorev_kaydi_unpacking(capsys: pytest.CaptureFixture[str]) -> None:
    """* ve ** açarak çağırma biçimini test eder."""
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ekler = {"sorumlu": "Ayşe"}
    gorev_kaydi("Kara deliğe atla", *adimlar, oncelik="yüksek", **ekler)
    captured = capsys.readouterr()
    beklenen = (
        "[YÜKSEK] Kara deliğe atla\n"
        " 1. Kredi kazan\n"
        " 2. Pilot bul\n"
        " 3. Hiperdrive al\n"
        " sorumlu: Ayşe\n"
    )
    assert captured.out == beklenen


# --- Görev 3 Testleri ---

def test_galaksi_kur_varsayilan_yakit() -> None:
    """Yakıt verilmediğinde varsayılan 50 olmasını test eder."""
    g = galaksi_kur(["mars"], {"mars": []}, "mars")
    assert g["konum"] == "mars"
    assert g["yakit"] == 50


def test_galaksi_kur_gecersiz_baslangic() -> None:
    """Geçersiz başlangıç gezegeninde ValueError fırlatılmasını test eder."""
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "dünya")


def test_veri_yukle() -> None:
    """galaksi.json dosyasından verilerin doğru yüklendiğini test eder."""
    g = veri_yukle()
    assert g["konum"] == "dünya"
    assert g["yakit"] == 100
    assert "sirius" in g["baglantilar"]
    assert g["baglantilar"]["dünya"] == ["centauri", "sirius"]


# --- Görev 5 & Bonus Testleri ---

def test_hamle_sayaci() -> None:
    """Her çağrıda sayacın 1 arttığını ve bağımsız çalıştığını test eder."""
    sayac1 = hamle_sayaci()
    assert sayac1() == 1
    assert sayac1() == 2
    assert sayac1() == 3

    sayac2 = hamle_sayaci()
    assert sayac2() == 1
    assert sayac1() == 4


def test_en_bagli_gezegenler() -> None:
    """Gezegenlerin bağlantı sayısına göre sıralandığını test eder."""
    g = veri_yukle()
    sirali = en_bagli_gezegenler(g)
    beklenen = ["sirius", "centauri", "dünya", "orion", "kara_delik"]
    assert sirali == beklenen


def test_en_bagli_gezegenler_esitlik() -> None:
    """Bağlantı sayısı eşitse alfabetik sıraya bakılmasını test eder."""
    ornek = {
        "baglantilar": {
            "z": ["x"],
            "b": ["x", "y"],
            "a": ["x", "y"],
        }
    }
    assert en_bagli_gezegenler(ornek) == ["a", "b", "z"]


def test_sure_olc(capsys: pytest.CaptureFixture[str]) -> None:
    """Süre ölçen dekoratörün çalıştığını test eder."""
    @sure_olc
    def ornek_hesapla(x: int) -> int:
        return x * x

    assert ornek_hesapla(5) == 25
    captured = capsys.readouterr()
    assert "saniye" in captured.out
