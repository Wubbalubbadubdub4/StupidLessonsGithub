# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 3 – Görev 2: Esnek parametreler (*adimlar, oncelik, **ekler)

from typing import Any


def gorev_kaydi(baslik: str, *adimlar: str, oncelik: str = "normal", **ekler: Any) -> str:
    """Görev adımlarını ve ek bilgileri ekrana yazdırır ve metni döndürür.

    'oncelik' parametresi varsayılan 'normal'dir ve anahtar kelime argümanı olarak verilebilir.
    """
    satirlar = [f"[{oncelik.upper()}] {baslik}"]

    for i, adim in enumerate(adimlar, 1):
        satirlar.append(f" {i}. {adim}")

    for anahtar, deger in ekler.items():
        satirlar.append(f" {anahtar}: {deger}")

    metin = "\n".join(satirlar)
    print(metin)
    return metin


if __name__ == "__main__":
    gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan",
        "Pilot bul",
        "Hiperdrive al",
        oncelik="yüksek",
        sorumlu="Ayşe",
    )
