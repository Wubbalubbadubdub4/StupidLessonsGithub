# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 4 – Üreteçler ve functools: Akış ve Boru Hattı Modülü

from collections.abc import Generator, Iterable
import itertools
from pathlib import Path


# ==============================================================================
# Görev 1 – Fibonacci Üreteci (15 puan)
# ==============================================================================

def fibonacci() -> Generator[int, None, None]:
    """Sonsuz Fibonacci sayı dizisi üreten üreteç (generator).

    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89... şeklinde sonsuza kadar devam eder.
    Bellekte tüm listeyi tutmak yerine her adımda bir sonraki değeri tembel (lazy) üretir.

    Yields:
        int: Sıradaki Fibonacci sayısı.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# ==============================================================================
# Görev 2 – Yakıt Göstergesi Üreteci (20 puan)
# ==============================================================================

def yakit_gostergesi(yakit: int, tuketim: int) -> Generator[int, None, None]:
    """Her next() çağrısında yakıtı tuketim kadar azaltıp kalan yakıtı üreten üreteç.

    Yakıt 0'a inince veya altına düşünce 0 üretir ve durur (StopIteration fırlatır).

    Örnek:
    >>> list(yakit_gostergesi(100, 30))
    [70, 40, 10, 0]

    Args:
        yakit: Başlangıçtaki mevcut yakıt miktarı.
        tuketim: Her yolculuk adımında harcanacak yakıt.

    Yields:
        int: Kalan güncel yakıt miktarı (en az 0).

    Raises:
        ValueError: Tüketim sıfır veya negatif verilirse.
    """
    if tuketim <= 0:
        raise ValueError("Tüketim miktarı pozitif bir tam sayı olmalıdır.")

    kalan = yakit
    while kalan > 0:
        kalan = max(0, kalan - tuketim)
        yield kalan


# ==============================================================================
# Görev 3 – Seyir Defteri Boru Hattı (25 puan)
# ==============================================================================

def satirlari_oku(yol: str | Path) -> Generator[str, None, None]:
    """Dosyadaki boş satırları ve '#' ile başlayan yorumları atlayarak temiz satırları üreten üreteç.

    Tüm dosyayı tek seferde belleğe/listeye okumaz, satır satır tembel (lazy) okur.

    Args:
        yol: Okunacak dosya yolu (str veya Path).

    Yields:
        str: Temizlenmiş (strip edilmiş) satır metni.
    """
    dosya_yolu = Path(yol)
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            temiz = satir.strip()
            if temiz and not temiz.startswith("#"):
                yield temiz


def ayristir(satirlar: Iterable[str]) -> Generator[tuple[str, str, int], None, None]:
    """Seyir defteri satırlarını '(kaynak, hedef, yakit)' demetlerine dönüştüren üreteç.

    Beklenen satır formatı: 'dünya -> sirius 12'

    Args:
        satirlar: Satır metinlerini sağlayan yinelenebilir nesne veya üreteç.

    Yields:
        tuple[str, str, int]: (kaynak, hedef, harcanan_yakit) demeti.
    """
    for satir in satirlar:
        if "->" not in satir:
            continue
        kaynak_kisim, hedef_kisim = satir.split("->", 1)
        kaynak = kaynak_kisim.strip()

        hedef_parcalar = hedef_kisim.strip().split()
        if len(hedef_parcalar) >= 2:
            hedef = hedef_parcalar[0]
            yakit = int(hedef_parcalar[1])
            yield (kaynak, hedef, yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Generator[tuple[str, str, int], None, None]:
    """Yakıt tüketimi verilen eşik değerinden kesinlikle büyük olan kayıtları süzen üreteç.

    Boru hattının son halkasıdır; ara listeleme yapmadan kayıtları tembel akıtır.

    Args:
        kayitlar: (kaynak, hedef, yakit) demetlerini sağlayan üreteç.
        esik: Minimum yakıt filtre eşiği.

    Yields:
        tuple[str, str, int]: Yakıtı eşikten büyük olan seyahat demeti.
    """
    for kayit in kayitlar:
        _, _, yakit = kayit
        if yakit > esik:
            yield kayit


