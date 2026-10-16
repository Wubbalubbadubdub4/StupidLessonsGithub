# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve functools

from collections.abc import Generator, Iterable
from functools import lru_cache
import itertools
from pathlib import Path
import time
from typing import Callable


# Görev 1: Sonsuz Fibonacci üreteci
def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreten üreteç (generator)."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Görev 2: Yakıt göstergesi üreteci
def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tüketim kadar azaltıp kalan yakıtı üreten üreteç."""
    if tuketim <= 0:
        raise ValueError("Tüketim miktarı pozitif bir tam sayı olmalıdır.")

    kalan = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan


# Görev 3: Seyir defteri boru hattı üreteçleri
def satirlari_oku(yol: str | Path) -> Generator[str, None, None]:
    """Dosyadaki boş satırları ve '#' ile başlayan yorumları atlayarak temiz satırları okuyan üreteç."""
    dosya_yolu = Path(yol)
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if temiz and not temiz.startswith("#"):
                yield temiz


def ayristir(satirlar: Iterable[str]) -> Generator[tuple[str, str, int], None, None]:
    """Satırları (kaynak, hedef, yakit) demetlerine dönüştüren üreteç."""
    for satir in satirlar:
        if "->" not in satir:
            continue
        kaynak_kisim, hedef_kisim = satir.split("->", 1)
        kaynak = kaynak_kisim.strip()

        parcalar = hedef_kisim.strip().split()
        if len(parcalar) >= 2:
            hedef = parcalar[0]
            yakit = int(parcalar[1])
            yield (kaynak, hedef, yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Generator[tuple[str, str, int], None, None]:
    """Yakıt tüketimi verilen eşikten büyük olan seyahatleri süzen üreteç."""
    for kayit in kayitlar:
        _, _, yakit = kayit
        if yakit > esik:
            yield kayit


# Görev 4: Önbellekli rota sayacı
def rota_sayaci(baglantilar: dict[str, list[str]]) -> Callable[[str, int], int]:
    """Verilen harita üzerinde tam adım uzunluğundaki rota sayısını hesaplayan önbellekli fonksiyonu döndürür."""
    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        if adim < 0:
            return 0
        if adim == 0:
            return 1
        return sum(rota_sayisi(komsu, adim - 1) for komsu in baglantilar.get(gezegen, []))

    return rota_sayisi


def rota_sayisi_onbelleksiz(baglantilar: dict[str, list[str]], gezegen: str, adim: int) -> int:
    """Süre karşılaştırması için önbelleksiz özyinelemeli rota sayısı hesabı."""
    if adim < 0:
        return 0
    if adim == 0:
        return 1
    return sum(rota_sayisi_onbelleksiz(baglantilar, komsu, adim - 1) for komsu in baglantilar.get(gezegen, []))


# Bonus Görevi: zamanlayici üreteci ve meşgul bekleme programı
def zamanlayici(aralik: float) -> Generator[float, None, None]:
    """Belirtilen periyot aralığında (saniye) sinyal üreten meşgul bekleme üreteci."""
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
    """10 saniye boyunca her 2 saniyede 'tik', her 5 saniyede 'tak' yazdıran program."""
    baslangic = time.perf_counter()
    bitis = baslangic + toplam_sure

    sonraki_tik = baslangic + 2.0
    sonraki_tak = baslangic + 5.0

    olaylar: list[tuple[float, str]] = []

    while True:
        simdi = time.perf_counter()
        if simdi > bitis:
            break

        gecen = simdi - baslangic

        if simdi >= sonraki_tik:
            olaylar.append((round(gecen, 2), "tik"))
            if yazdir:
                print(f"[{gecen:.2f}s] tik")
            sonraki_tik += 2.0

        if simdi >= sonraki_tak:
            olaylar.append((round(gecen, 2), "tak"))
            if yazdir:
                print(f"[{gecen:.2f}s] tak")
            sonraki_tak += 5.0

    return olaylar
