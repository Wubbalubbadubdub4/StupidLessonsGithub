# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Bonus Testleri: zamanlayici() ve Tik-Tak Programı

import time
import pytest
from uzay_oyunu.bonus import zamanlayici, tik_tak_programi


def test_zamanlayici_aralik_hatasi() -> None:
    """Aralık süresi sıfır veya negatif verildiğinde ValueError fırlatılmalıdır."""
    with pytest.raises(ValueError):
        next(zamanlayici(0))
    with pytest.raises(ValueError):
        next(zamanlayici(-1))


def test_zamanlayici_calisma() -> None:
    """zamanlayici üretecinin küçük bir aralıkta (0.01s) doğru çalıştığını test eder."""
    g = zamanlayici(0.01)
    t0 = time.perf_counter()
    t1 = next(g)
    assert t1 > t0
    assert (t1 - t0) >= 0.009  # En az 0.01 saniye civarı geçmiş olmalıdır


def test_tik_tak_programi_kisa_calisma(capsys: pytest.CaptureFixture[str]) -> None:
    """tik_tak_programi fonksiyonunun başarıyla tamamlandığını ve çıktı ürettiğini test eder."""
    # Testlerin hızlı koşması için 0.05 saniyelik mikro süreyle çağırıyoruz
    olaylar = tik_tak_programi(toplam_sure=0.05, yazdir=True)
    cikti = capsys.readouterr().out
    assert "Tik-Tak Programı Başlatıldı" in cikti
    assert "Süre Doldu, Program Tamamlandı" in cikti
    assert isinstance(olaylar, list)
