# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Uzay Oyunu Ana Modülü

from typing import Any
from uzay_oyunu.araclar import hamle_sayaci
from uzay_oyunu.galaksi import veri_yukle
from uzay_oyunu.akis import yakit_gostergesi


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Eşyaların durumuna göre envanter durum metnini döndürür.

    Saf fonksiyondur, print etmez, metni döndürür.
    """
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiper motor")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return "Sende: " + ", ".join(esyalar)


def hedef_menusu(hedefler: list[str]) -> str:
    """Gidilebilecek hedefleri numaralandırarak menü olarak döndürür."""
    satirlar = ["Nereye gitmek istersin?"]
    for i, hedef in enumerate(hedefler, 1):
        satirlar.append(f"[{i}] {hedef}")
    return "\n".join(satirlar)


def travel() -> None:
    """Uzay oyunu seyahat fonksiyonu.

    Hedefler sabit listeden değil, galaksi['baglantilar'][planet] üzerinden alınır.
    Hamle sayacı her adımda çağrılır ve oyun bitince toplam hamleyi yazar.
    """
    galaksi = veri_yukle()
    if not galaksi:
        return

    sayac = hamle_sayaci()
    toplam_hamle = 0

    credits = True
    engines = False
    copilot = True

    envanter = envanter_metni(credits, engines, copilot)
    if envanter:
        print(envanter)

    planet = galaksi.get("konum", "dünya")
    baslangic_yakit = galaksi.get("yakit", 100)
    gosterge = yakit_gostergesi(baslangic_yakit, tuketim=5)
    yakit = baslangic_yakit

    while True:
        destinations = galaksi["baglantilar"].get(planet, [])

        if not destinations:
            print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
            break

        print(f"\nŞu anki konum: {planet} | Kalan Yakıt: {yakit}")
        print(hedef_menusu(destinations))

        secim = input("Seçiminiz (Çıkış için q): ")
        if secim.lower() == "q":
            print(f"Oyunu {toplam_hamle} hamlede bitirdin!")
            break

        try:
            index = int(secim) - 1
            if 0 <= index < len(destinations):
                planet = destinations[index]
                try:
                    yakit = next(gosterge)
                except StopIteration:
                    print("Yakıtın bitti, uzayda sürükleniyorsun…")
                    break
                toplam_hamle = sayac()
            else:
                print("Geçersiz seçim!")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")


if __name__ == "__main__":
    travel()
