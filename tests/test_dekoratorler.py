# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 5 – Dekoratörler Testleri

import functools
import pytest
from functools import lru_cache

from uzay_oyunu.dekoratorler import sure_olc, say, log_cagri, sinirla, hafiza
from uzay_oyunu.komutlar import KOMUTLAR, komut


# ===========================================================================
# Görev 1 – sure_olc testleri
# ===========================================================================

def test_sure_olc_sonuc_degismez() -> None:
    """@sure_olc fonksiyonun sonucunu değiştirmemelidir."""

    @sure_olc
    def topla(a: int, b: int) -> int:
        """İki sayıyı toplar."""
        return a + b

    assert topla(3, 4) == 7


def test_sure_olc_adli_arguman(capsys: pytest.CaptureFixture[str]) -> None:
    """@sure_olc adlı (keyword) argümanlarla çalışmalıdır."""

    @sure_olc
    def carpma(x: int, y: int = 2) -> int:
        """x ile y'yi çarpar."""
        return x * y

    sonuc = carpma(x=5, y=3)
    assert sonuc == 15
    cikti = capsys.readouterr().out
    assert "carpma" in cikti
    assert "sn" in cikti


def test_sure_olc_meta_veri_korunur() -> None:
    """@sure_olc __name__ ve __doc__ niteliklerini korumalıdır (functools.wraps)."""

    @sure_olc
    def orneklem() -> None:
        """Bu bir test fonksiyonudur."""

    assert orneklem.__name__ == "orneklem"
    assert orneklem.__doc__ == "Bu bir test fonksiyonudur."


def test_sure_olc_cikti_format(capsys: pytest.CaptureFixture[str]) -> None:
    """@sure_olc çıktısı 'ad: X.XXXX sn' formatında olmalıdır."""

    @sure_olc
    def bekle() -> int:
        return 42

    bekle()
    cikti = capsys.readouterr().out
    assert "bekle" in cikti
    assert "sn" in cikti


# ===========================================================================
# Görev 2 – say ve dekoratör sırası testleri
# ===========================================================================

def test_say_cagri_sayar() -> None:
    """@say dekoratörü çağrı sayısını doğru artırmalıdır."""

    @say
    def fonk() -> None:
        pass

    assert fonk.cagri == 0
    fonk()
    assert fonk.cagri == 1
    fonk()
    fonk()
    assert fonk.cagri == 3


def test_say_sonuc_korunur() -> None:
    """@say dekoratörü fonksiyon sonucunu değiştirmemelidir."""

    @say
    def ikikat(n: int) -> int:
        return n * 2

    assert ikikat(5) == 10


def test_dekorator_sirasi_sadece_say() -> None:
    """Yalnızca @say ile Fibonacci çağrı sayısı çok yüksektir (fib(20) → 21891)."""

    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib.cagri = 0
    fib(20)
    assert fib.cagri == 21891


def test_dekorator_sirasi_say_ust_lru_cache_alta() -> None:
    """@say üstte, @lru_cache altta → say 39 çağrı sayar (cache hit'leri de sayar)."""

    @say
    @lru_cache(maxsize=None)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    fib.cagri = 0
    fib(20)
    assert fib.cagri == 39


def test_dekorator_sirasi_lru_cache_ust_say_alta() -> None:
    """@lru_cache üstte, @say altta → lru_cache sadece 21 benzersiz çağrıyı say'a iletir."""

    @lru_cache(maxsize=None)
    @say
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib.__wrapped__.cagri >= 0 and fib(n - 1) + fib(n - 2)  # type: ignore

    # Daha temiz yaklaşım:
    @say
    def _fib_ic(n: int) -> int:
        if n < 2:
            return n
        return _fib_onb(n - 1) + _fib_onb(n - 2)

    @lru_cache(maxsize=None)
    def _fib_onb(n: int) -> int:
        return _fib_ic(n)

    _fib_onb(20)
    assert _fib_ic.cagri == 21


# ===========================================================================
# Görev 3 – log_cagri testleri
# ===========================================================================

def test_log_cagri_giris_ciktisi(capsys: pytest.CaptureFixture[str]) -> None:
    """@log_cagri -> ve <- satırlarını yazdırmalıdır."""

    @log_cagri
    def selamla(isim: str) -> str:
        return f"Merhaba {isim}"

    sonuc = selamla("Alp")
    cikti = capsys.readouterr().out
    assert "->" in cikti
    assert "<-" in cikti
    assert "selamla" in cikti
    assert sonuc == "Merhaba Alp"


def test_log_cagri_adli_arguman(capsys: pytest.CaptureFixture[str]) -> None:
    """@log_cagri adlı argümanları da yazdırmalıdır."""

    @log_cagri
    def carp(x: int, y: int = 1) -> int:
        return x * y

    carp(3, y=5)
    cikti = capsys.readouterr().out
    assert "y=5" in cikti


def test_log_cagri_meta_veri(capsys: pytest.CaptureFixture[str]) -> None:
    """@log_cagri functools.wraps ile meta veriyi korumalıdır."""

    @log_cagri
    def deneme() -> None:
        """Deneme fonksiyonu."""

    assert deneme.__name__ == "deneme"
    assert deneme.__doc__ == "Deneme fonksiyonu."


# ===========================================================================
# Görev 4 – Komut sistemi testleri
# ===========================================================================

def test_komut_yardim_kayitli() -> None:
    """'yardim' komutu KOMUTLAR sözlüğünde kayıtlı olmalıdır."""
    assert "yardim" in KOMUTLAR


def test_komut_envanter_kayitli() -> None:
    """'envanter' komutu KOMUTLAR sözlüğünde kayıtlı olmalıdır."""
    assert "envanter" in KOMUTLAR


def test_komut_harita_kayitli() -> None:
    """'harita' komutu KOMUTLAR sözlüğünde kayıtlı olmalıdır."""
    assert "harita" in KOMUTLAR


def test_komut_yardim_ciktisi() -> None:
    """yardim komutu tüm komut adlarını ve açıklamalarını listeler."""
    fonksiyon, _ = KOMUTLAR["yardim"]
    sonuc = fonksiyon({})
    assert "envanter" in sonuc
    assert "harita" in sonuc
    assert "yardim" in sonuc


def test_komut_envanter_dolu() -> None:
    """envanter komutu sahip olunan eşyaları listeler."""
    fonksiyon, _ = KOMUTLAR["envanter"]
    durum = {"credits": True, "engines": False, "copilot": True}
    sonuc = fonksiyon(durum)
    assert "bol kredi" in sonuc
    assert "yetenekli bir pilot" in sonuc
    assert "hiper motor" not in sonuc


def test_komut_envanter_bos() -> None:
    """envanter komutu boş envanter için uygun mesaj döndürür."""
    fonksiyon, _ = KOMUTLAR["envanter"]
    durum = {"credits": False, "engines": False, "copilot": False}
    sonuc = fonksiyon(durum)
    assert "hiçbir şey" in sonuc.lower()


def test_komut_harita_ciktisi() -> None:
    """harita komutu mevcut konumdan gidilebilecek yerleri listeler."""
    fonksiyon, _ = KOMUTLAR["harita"]
    durum = {
        "konum": "dünya",
        "baglantilar": {"dünya": ["centauri", "sirius"]},
    }
    sonuc = fonksiyon(durum)
    assert "centauri" in sonuc
    assert "sirius" in sonuc


def test_komut_cakisma_hatasi() -> None:
    """Aynı ad iki kez kullanılırsa ValueError fırlatmalıdır."""
    with pytest.raises(ValueError, match="zaten kayıtlı"):

        @komut("yardim")
        def sahte_yardim(durum: dict) -> str:
            return ""


def test_komut_fonksiyon_degismez() -> None:
    """Komut dekoratörü orijinal fonksiyonu değiştirmemelidir."""
    fonksiyon, aciklama = KOMUTLAR["harita"]
    assert callable(fonksiyon)
    assert aciklama == "gidebileceğin gezegenleri gösterir"


# ===========================================================================
# Görev 5 – sinirla testleri
# ===========================================================================

@sinirla(0, 100)
def yakit_harca(miktar: int, mevcut: int = 100) -> int:
    """Yakıt harcar; kalan miktarı döndürür."""
    return mevcut - miktar


def test_sinirla_gecerli_deger() -> None:
    """Aralık içindeki değer normal çalışmalıdır."""
    assert yakit_harca(30) == 70


def test_sinirla_alt_sinir() -> None:
    """Alt sınır değeri (0) geçerli olmalıdır."""
    assert yakit_harca(0) == 100


def test_sinirla_ust_sinir() -> None:
    """Üst sınır değeri (100) geçerli olmalıdır."""
    assert yakit_harca(100) == 0


def test_sinirla_aralık_disi_asagi() -> None:
    """Aralık altındaki değer ValueError fırlatmalıdır."""
    with pytest.raises(ValueError, match="0-100 aralığında değil"):
        yakit_harca(-1)


def test_sinirla_aralık_disi_yukari() -> None:
    """Aralık üstündeki değer ValueError fırlatmalıdır."""
    with pytest.raises(ValueError, match="0-100 aralığında değil"):
        yakit_harca(150)


def test_sinirla_meta_veri() -> None:
    """@sinirla functools.wraps ile meta veriyi korumalıdır."""
    assert yakit_harca.__name__ == "yakit_harca"


# ===========================================================================
# Bonus – hafiza testleri
# ===========================================================================

def test_hafiza_sonuc_dogru() -> None:
    """@hafiza önbelleği sonuçları doğru döndürmelidir."""

    @hafiza()
    def kare(n: int) -> int:
        return n * n

    assert kare(5) == 25
    assert kare(5) == 25  # Önbellekten


def test_hafiza_maxsize_eski_girdileri_siler() -> None:
    """maxsize dolunca en eski girdi silinmelidir."""
    cagrı_sayisi = 0

    @hafiza(maxsize=2)
    def hesapla(n: int) -> int:
        nonlocal cagrı_sayisi
        cagrı_sayisi += 1
        return n * 2

    hesapla(1)  # cagrı_sayisi: 1
    hesapla(2)  # cagrı_sayisi: 2 – önbellek dolu
    hesapla(3)  # cagrı_sayisi: 3 – en eski (1) silinir
    hesapla(1)  # cagrı_sayisi: 4 – (1) önbellekte yok, yeniden hesaplanır

    assert cagrı_sayisi == 4


def test_hafiza_lru_cache_ile_tutarli() -> None:
    """@hafiza sonuçları lru_cache ile tutarlı olmalıdır."""

    @hafiza()
    def fib_haf(n: int) -> int:
        if n < 2:
            return n
        return fib_haf(n - 1) + fib_haf(n - 2)

    @lru_cache(maxsize=None)
    def fib_lru(n: int) -> int:
        if n < 2:
            return n
        return fib_lru(n - 1) + fib_lru(n - 2)

    for i in range(20):
        assert fib_haf(i) == fib_lru(i)
