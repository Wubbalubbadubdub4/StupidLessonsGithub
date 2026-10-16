# İleri Python Programlama - Hafta 3: Değişken Kapsamı (Scope) ve Tuzaklar Raporu

**Öğrenci Adı Soyadı:** Alp Dinçoğlu  
**Öğrenci Numarası:** 20253006040  
**Ders:** İleri Python Programlama  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Murat Emeç  
**Dönem:** 2026–2027 Güz  

---

## 1. Giriş ve Python'da LEGB Kuralı

Python'da bir değişkene erişilmek istendiğinde, Python ad alanlarını (namespaces) **LEGB** sırasıyla arar:
1. **L (Local):** Fonksiyonun kendi yerel kapsamı.
2. **E (Enclosing):** İç içe geçmiş fonksiyonlarda dıştaki (kapsayan) fonksiyonun kapsamı.
3. **G (Global):** Modül düzeyinde tanımlanmış değişkenler.
4. **B (Built-in):** Python'ın yerleşik fonksiyon ve sabitleri (`len`, `range`, `print` vb.).

---

## 2. Dersteki Kapsam Örnekleri

### Örnek 1: Yerel (Local) ve Global Değişken Gölgeleme (Shadowing)

```python
x = 10

def f():
    x = 20
    print("Fonksiyon içi x:", x)

f()
print("Fonksiyon dışı x:", x)
```

- **Tahminim:** Fonksiyon çağrıldığında 20 basar, sonrasında global x değeri değişmeyeceği için fonksiyon dışında 10 basar.
- **Gerçek Sonuç:**
  ```text
  Fonksiyon içi x: 20
  Fonksiyon dışı x: 10
  ```
- **Nedeni:**  
  Python'da fonksiyon içerisinde bir değişkene atama yapıldığında (`x = 20`), Python bu değişkeni fonksiyonun **yerel (local)** kapsamında yeni bir değişken olarak tanımlar. Bu yerel `x`, global `x`'i gölgeler (shadowing). Fonksiyon tamamlandığında yerel ad alanı bellekten temizlenir. Modül düzeyindeki global `x` değişkeni hiçbir şekilde etkilenmez ve değeri `10` kalır.

---

### Örnek 2: UnboundLocalError Tuzağı

```python
sayac = 0

def arttir():
    sayac += 1
    print(sayac)

arttir()
```

- **Tahminim:** Dışarıdaki `sayac` okunmaya çalışılır ancak fonksiyon içinde atama olduğu için Python bunu yerel kabul eder ve henüz değer atanmadığından `UnboundLocalError` hatası verir.
- **Gerçek Sonuç:**
  ```text
  UnboundLocalError: cannot access local variable 'sayac' where it is not associated with a value
  ```
- **Nedeni ve Detaylı Açıklama:**  
  1. **Derleme Aşaması (Bytecode Generation):** Python fonksiyon gövdesinde atama (`sayac = sayac + 1`) gördüğü için `sayac` adını baştan yerel (local) olarak işaretler.
  2. **Çalışma Aşaması (Runtime):** Sağ taraftaki `sayac + 1` ifadesi değerlendirilirken yerel ad alanında henüz tanımlı bir değer bulunamadığından `UnboundLocalError` hatası fırlatılır.
  3. **Çözüm:** `global` anahtar kelimesi yerine parametre aktarımı veya iç içe fonksiyonlarda `nonlocal` kullanmaktır.

---

### Örnek 3: Kapsayan Alan (Enclosing Scope), Closure ve `nonlocal`

```python
def dis():
    mesaj = "merhaba"
    def ic():
        nonlocal mesaj
        mesaj = "dünya"
    ic()
    print("Dış fonksiyon mesajı:", mesaj)

dis()
```

- **Tahminim:** `nonlocal` kullanıldığı için iç fonksiyon dış fonksiyonun yerel değişkenini değiştirebilir ve "dünya" basar.
- **Gerçek Sonuç:**
  ```text
  Dış fonksiyon mesajı: dünya
  ```
- **Nedeni:**  
  `nonlocal` anahtar kelimesi, değişkenin en yakın kapsayan fonksiyona (enclosing scope) ait olduğunu bildirir ve yeni bir yerel değişken açılmasını önleyerek dış değişkenin doğrudan güncellenmesini sağlar.

---

## 3. Varsayılan Argüman Tuzağı (Mutable Default Argument)

### Problem:
```python
def yakit_ekle(miktar, depo=[]):
    depo.append(miktar)
    return depo
```
Python'da varsayılan argümanlar (`depo=[]`) fonksiyon çağrılırken değil, fonksiyon tanımlandığı an bellekte bir defa oluşturulur. Ardışık çağrılarda aynı liste nesnesi paylaşıldığı için çağrılar birbirini kirletir.

### Çözüm (None Kalıbı):
```python
def yakit_ekle(miktar: int, depo: list | None = None) -> list:
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo
```
`None` değişmez (immutable) olduğu için her çağrıda `depo is None` koşuluyla o çağrıya özel yeni bir liste başlatılır.
