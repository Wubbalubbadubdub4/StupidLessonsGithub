# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Bonus (+10): zamanlayici() Üreteci ve Meşgul Bekleme (Busy Waiting)

from collections.abc import Generator
import time


def zamanlayici(aralik: float) -> Generator[float, None, None]:
    """Belirtilen periyot aralığında (saniye) sinyal üreten sonsuz üreteç.

    Her adımda hedef zaman dolana kadar CPU'yu meşgul ederek bekler (spin-wait)
    ve süre dolduğunda geçen zaman damgasını yield eder.

    Args:
        aralik: Sinyal üretilecek periyot (saniye cinsinden, ör. 2.0 veya 5.0).

    Yields:
        float: Sinyalin tetiklendiği zaman damgası (time.perf_counter()).
    """
    if aralik <= 0:
        raise ValueError("Aralık süresi pozitif olmalıdır.")

    hedef = time.perf_counter() + aralik
    while True:
        # Meşgul bekleme (Busy waiting): CPU boş durmaz, sürekli saati sorgular
        while time.perf_counter() < hedef:
            pass
        yield time.perf_counter()
        hedef += aralik


def tik_tak_programi(
    toplam_sure: float = 10.0, yazdir: bool = True
) -> list[tuple[float, str]]:
    """10 saniye boyunca her 2 saniyede 'tik', her 5 saniyede 'tak' yazdıran program.

    İki bağımsız zamanlayıcı üretecini eşzamanlı (cooperative polling) kontrol eder.

    Args:
        toplam_sure: Programın toplam çalışma süresi (varsayılan 10.0 saniye).
        yazdir: Konsola 'tik'/'tak' çıktısı basılsın mı?

    Returns:
        list[tuple[float, str]]: Kaydedilen olayların (geçen_süre, mesaj) listesi.
    """
    baslangic = time.perf_counter()
    bitis = baslangic + toplam_sure

    sonraki_tik = baslangic + 2.0
    sonraki_tak = baslangic + 5.0

    olaylar: list[tuple[float, str]] = []

    if yazdir:
        print(f"=== Tik-Tak Programı Başlatıldı ({toplam_sure:.1f} saniye) ===")

    while True:
        simdi = time.perf_counter()
        if simdi > bitis:
            break

        gecen = simdi - baslangic

        # 2 saniyede bir 'tik'
        if simdi >= sonraki_tik:
            olaylar.append((round(gecen, 2), "tik"))
            if yazdir:
                print(f"[{gecen:.2f}s] tik")
            sonraki_tik += 2.0

        # 5 saniyede bir 'tak'
        if simdi >= sonraki_tak:
            olaylar.append((round(gecen, 2), "tak"))
            if yazdir:
                print(f"[{gecen:.2f}s] tak")
            sonraki_tak += 5.0

    if yazdir:
        print("=== Süre Doldu, Program Tamamlandı ===")

    return olaylar


# ==============================================================================
# Meşgul Bekleme (Busy Waiting) Nedir ve time.sleep ile Farkı Nelerdir?
# ==============================================================================
#
# 1. Meşgul Bekleme (Busy Waiting / Spinning):
#    - Program bir koşulun (burada sürenin dolması) gerçekleşmesini beklerken
#      bir `while` döngüsü içinde sürekli işlemci saatini sorgular (`pass` / döngü).
#    - Bu süreçte işletim sistemine işlemcinin boş bırakılabileceği bildirilmez.
#    - Sonuç olarak tek bir CPU çekirdeği %100 kullanım oranına (load) ulaşır,
#      gereksiz enerji harcar ve cihazın ısınmasına yol açar.
#
# 2. time.sleep() ile Farkı:
#    - `time.sleep(sure)` fonksiyonu çağrıldığında, Python süreci işletim sistemi
#      çekirdeğine (kernel) sistem çağrısı (syscall) yapar.
#    - İşletim sistemi bu iş parçacığını (thread) 'uyku / bloke' (blocked/sleep)
#      kuyruğuna alır ve CPU'yu tamamen serbest bırakır.
#    - CPU, başka işlemleri yürütmek için kullanılır veya boştaysa uyku durumuna
#      (C-states) geçer; CPU kullanımı %0'a iner.
#    - Süre dolduğunda donanım zamanlayıcı kesmesi (hardware timer interrupt)
#      iş parçacığını uyandırır ve çalışma kaldığı yerden devam eder.
# ==============================================================================

if __name__ == "__main__":
    tik_tak_programi(toplam_sure=10.0, yazdir=True)
