# Ad Soyad: Alp Dinçoğlu
# Öğrenci Numarası: 20253006040
# Ders: İleri Python Programlama
# Hafta 5 – Dekoratörler

import functools
import time
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Görev 1 – Süre ölçen dekoratör
# ---------------------------------------------------------------------------

def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun çalışma süresini ölçüp 'ad: X.XXXX sn' biçiminde yazdıran dekoratör."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        print(f"{fonksiyon.__name__}: {bitis - baslangic:.4f} sn")
        return sonuc

    return sarmalayici


# ---------------------------------------------------------------------------
# Görev 2 – Çağrı sayacı dekoratör
# ---------------------------------------------------------------------------

def say(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Her çağrıda fonksiyonun 'cagri' niteliğini artıran sayaç dekoratörü."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0  # type: ignore[attr-defined]
    return sarmalayici


# ---------------------------------------------------------------------------
# Görev 3 – Loglayan dekoratör
# ---------------------------------------------------------------------------

def log_cagri(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Her çağrıdan önce adı ve argümanları, sonra dönüş değerini yazdıran dekoratör."""

    @functools.wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        arg_parcalari = [repr(a) for a in args]
        arg_parcalari += [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"-> {fonksiyon.__name__}({', '.join(arg_parcalari)})")
        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {sonuc!r}")
        return sonuc

    return sarmalayici


# ---------------------------------------------------------------------------
# Görev 5 – Argüman alan dekoratör: sinirla(alt, ust)
# ---------------------------------------------------------------------------

def sinirla(alt: float, ust: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Dekore edilen fonksiyonun ilk argümanını [alt, ust] aralığında zorlayan dekoratör fabrikası."""

    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            if not args:
                raise TypeError(f"{fonksiyon.__name__}: en az bir konumsal argüman gerekli")
            deger = args[0]
            if not (alt <= deger <= ust):
                raise ValueError(
                    f"{fonksiyon.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )
            return fonksiyon(*args, **kwargs)

        return sarmalayici

    return dekorator


# ---------------------------------------------------------------------------
# Bonus – Kendi önbellek dekoratörü: hafiza(maxsize=None)
# ---------------------------------------------------------------------------

def hafiza(maxsize: int | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """functools.lru_cache kullanmadan closure tabanlı önbellek dekoratörü.

    maxsize verildiğinde önbellek dolunca en eski girdiyi siler (FIFO).
    """

    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        onbellek: dict[Any, Any] = {}
        siralama: list[Any] = []  # FIFO sırası için anahtar listesi

        @functools.wraps(fonksiyon)
        def sarmalayici(*args: Any) -> Any:
            anahtar = args
            if anahtar in onbellek:
                return onbellek[anahtar]
            sonuc = fonksiyon(*args)
            if maxsize is not None and len(onbellek) >= maxsize:
                en_eski = siralama.pop(0)
                del onbellek[en_eski]
            onbellek[anahtar] = sonuc
            siralama.append(anahtar)
            return sonuc

        sarmalayici.cache = onbellek  # type: ignore[attr-defined]
        return sarmalayici

    return dekorator
