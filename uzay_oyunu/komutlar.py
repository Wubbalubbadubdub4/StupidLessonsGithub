# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 5 – Komut Sistemi

from typing import Any, Callable

# Komutları (fonksiyon, aciklama) olarak saklayan merkezi sözlük
KOMUTLAR: dict[str, tuple[Callable[..., Any], str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Fonksiyonu KOMUTLAR sözlüğüne kaydeden dekoratör fabrikası.

    Aynı ad iki kez kullanılırsa ValueError fırlatır.
    Fonksiyonu değiştirmez; (fonksiyon, aciklama) olarak kaydeder.
    """

    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' komutu zaten kayıtlı!")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon  # Fonksiyonu değiştirmeden döndür

    return dekorator


# ---------------------------------------------------------------------------
# Oyun komutları – her biri oyun durumunu (durum sözlüğü) argüman olarak alır
# ---------------------------------------------------------------------------

@komut("yardim", aciklama="komutları listeler")
def yardim_komutu(durum: dict[str, Any]) -> str:
    """Kullanılabilir tüm komutları ve açıklamalarını listeler."""
    satirlar = []
    for isim, (_, aciklama) in sorted(KOMUTLAR.items()):
        satirlar.append(f"{isim:<10}{aciklama}")
    return "\n".join(satirlar)


@komut("envanter", aciklama="eşyalarını gösterir")
def envanter_komutu(durum: dict[str, Any]) -> str:
    """Oyuncunun envanterini gösterir."""
    esyalar = []
    if durum.get("credits"):
        esyalar.append("bol kredi")
    if durum.get("engines"):
        esyalar.append("hiper motor")
    if durum.get("copilot"):
        esyalar.append("yetenekli bir pilot")
    if not esyalar:
        return "Envanterinde hiçbir şey yok."
    return "Sende: " + ", ".join(esyalar)


@komut("harita", aciklama="gidebileceğin gezegenleri gösterir")
def harita_komutu(durum: dict[str, Any]) -> str:
    """Mevcut konumdan gidilebilecek gezegenleri listeler."""
    konum = durum.get("konum", "")
    baglantilar: dict[str, list[str]] = durum.get("baglantilar", {})
    hedefler = baglantilar.get(konum, [])
    if not hedefler:
        return "Hiçbir yere gidemezsin."
    return ", ".join(hedefler)
