# xaloAC

**Windows Security Research / Information Stealer Analysis**

> **Brand:** xaloAC
> **Author / Developer:** x410m1s0
> **Version:** 5.0
> **Platform:** Windows
> **Language:** Python

---

## ⚠️ Uyarı

Bu repository, Windows üzerinde çalışan information-stealer davranışlarının incelenmesi ve güvenlik araştırması amacıyla hazırlanmıştır.

Kaynak kodu hassas kullanıcı verilerine erişebilen işlevler içerdiğinden yalnızca sahibinin olduğu veya açıkça yetkilendirilmiş test sistemlerinde incelenmelidir.

Yetkisiz sistemlerde kişisel veri, hesap bilgisi, parola, kart bilgisi veya başka hassas verilerin alınması ve aktarılması hukuki sonuçlar doğurabilir.

---

# Proje Hakkında

`xaloac.py`, Windows ortamında çeşitli sistem ve kullanıcı verilerini toplamaya yönelik tek dosyalı bir Python programıdır.

Programın kaynak dosyasında ana sınıf `Stealer` olarak tanımlanmıştır. Program çalışma sırasında bilgisayar adı, kullanıcı adı, IP adresi ve zaman damgası gibi temel bilgileri oluşturur ve çalışma verileri için ayrı bir victim dizini hazırlar.

Program ayrıca isteğe bağlı olarak toplanan sonuçları Discord webhook üzerinden gönderecek bir iletişim mekanizmasına sahiptir.

---

# Özellikler

Kaynak dosyada bulunan ana işlevler:

* Sistem bilgisi toplama
* Harici IP adresini belirleme
* Windows HWID bilgisi alma
* Wi-Fi profil bilgilerini işleme
* Tarayıcı veritabanlarını inceleme
* Browser credential kayıtlarını işleme
* Kredi kartı kayıtlarını işleme
* Browser verilerini ZIP arşivine alma
* Oyun platformu hesap bilgilerini araştırma
* Kullanıcı dizinlerindeki belirli dosya türlerini tarama
* Dosyaları ZIP arşivine alma
* Discord webhook iletişimi
* PowerShell payload oluşturma
* Geçici dosyaları temizleme
* Terminal tabanlı kullanım

---

# Desteklenen Browser'lar

Kaynak kodunda aşağıdaki browser profilleri hedeflenmektedir:

* Google Chrome
* Microsoft Edge
* Brave
* Opera
* Vivaldi

Browser verileri Windows kullanıcı profil dizinlerinden araştırılır. Kaynak kodunda `Login Data`, `Web Data` ve `Cookies` gibi browser veritabanlarıyla çalışıldığı görülmektedir.

---

# Oyun ve Uygulama Araştırması

Program kaynak kodunda çeşitli oyun istemcilerinin yerel yapılandırma dosyaları incelenmektedir.

Desteklenen/araştırılan platformlar arasında:

* Steam
* Epic Games
* Minecraft
* Riot Games
* Ubisoft
* Origin / EA
* Battle.net
* FiveM
* Discord

bulunmaktadır.

Buradaki işlemler ağırlıklı olarak yerel yapılandırma dosyaları ve uygulama verilerinden hesapla ilişkili bilgileri araştırmaya yöneliktir.

---

# Dosya Araştırması

Program belirli kullanıcı klasörlerinde çeşitli dosya uzantılarını araştırır.

Hedeflenen klasörler arasında:

```text
Desktop
Documents
Pictures
Downloads
Videos
```

bulunmaktadır.

Kaynak kodunda doküman, görsel, video, arşiv, kaynak kodu, yapılandırma, veritabanı, sertifika ve benzeri birçok dosya uzantısı tanımlanmıştır.

Dosya işlemlerinde toplam boyut için kaynak kodunda 50 MB sınırı ve tek dosya için 5 MB sınırı kullanılmaktadır.

---

# Çalışma Dizinleri

Program başlatıldığında çalışma dizini altında aşağıdaki klasörleri oluşturur:

```text
output/
victims/
temp/
```

Kaynak kodunda bunlar sırasıyla çıktı, victim verileri ve geçici dosyalar için kullanılmaktadır.

Bir çalışma sonucunda kaynak kodunun gösterdiği çıktı yapısı genel olarak:

```text
victim/
├── system_info.json
├── wifi_passwords.txt
├── passwords.txt
├── credit_cards.txt
├── game_accounts.txt
├── browser_data.zip
└── stolen_files.zip
```

şeklindedir. Dosyaların tamamı her çalışmada oluşmayabilir; ilgili veri bulunmasına bağlıdır.

---

# Sistem Bilgileri

Sistem bilgi toplama bölümünde kaynak kodu aşağıdaki bilgileri kaydetmeye çalışır:

* Computer name
* Windows user
* IP
* Operating system
* Processor
* Architecture
* Hostname
* Timestamp
* HWID
* Last boot time

Sonuç `system_info.json` içerisine yazılır.

---

# Browser Credential İşleme

Kaynak kodunda Windows DPAPI üzerinden browser tarafından korunan bazı değerlerin çözülmesi için:

```python
win32crypt.CryptUnprotectData(...)
```

kullanılmaktadır.

Bu nedenle `pywin32`, programın mevcut kaynak koduyla uyumlu bağımlılıklardan biridir.

---

# Discord İletişimi

Programda Discord webhook desteği bulunmaktadır.

Toplanan sonuçların belirli kategorileri webhook üzerinden HTTP POST istekleriyle gönderilebilir.

Kaynak kodunda aşağıdaki kategoriler için ayrı mesajlar oluşturulmaktadır:

* Sistem bilgileri
* Wi-Fi bilgileri
* Browser parolaları
* Kredi kartı bilgileri
* Oyun bilgileri
* Dosya özeti

Webhook değeri çalışma sırasında kullanıcı tarafından girilmektedir; kaynak dosyada sabit bir Discord tokenı tanımlanmamıştır.

---

# Payload Sistemi

Programda ayrıca bir payload oluşturma bölümü vardır.

Kullanıcının verdiği Discord webhook değeri bir PowerShell payload'ına aktarılır. Payload daha sonra Base64/UTF-16LE formatında encode edilerek PowerShell `EncodedCommand` kullanımına dönüştürülür.

Ana program bu payload'ı `.bat` dosyası olarak oluşturur. Kaynak kodunda bu dosya Windows Update benzeri bir terminal başlığı/metniyle çalıştırılacak şekilde hazırlanmıştır.

---

# Komut Satırı Menüsü

Program başlangıcında üç seçenek sunulur:

```text
[1] Kendi bilgisayarında çalıştır
[2] Kurban için .bat dosyası oluştur
[3] İkisi birden
```

Seçim `main()` fonksiyonunda işlenmektedir.

---

# Gereksinimler

Projenin mevcut kaynak kodu için üçüncü taraf bağımlılıklar:

```text
requests
pywin32
```

olarak özetlenebilir.

`os`, `sys`, `time`, `subprocess`, `socket`, `getpass`, `platform`, `json`, `base64`, `zipfile`, `shutil`, `sqlite3`, `re`, `tempfile`, `datetime` ve `pathlib` Python standart kütüphanesindedir.

Kurulum:

```powershell
python -m pip install -r requirements.txt
```

---

# Projeyi Çalıştırma

Ana program:

```powershell
python xaloac.py
```

olarak çalıştırılır.

Kaynak dosyanın kendi açıklamasında da `python xaloac.py` ana çalışma yöntemi olarak belirtilmiştir.

---

# Proje Yapısı

Repository'nin temel yapısı:

```text
xaloAC/
│
├── xaloac.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

`xaloac.py` ana programdır.

`requirements.txt` Python bağımlılıklarını belirtir.

`README.md` proje dokümantasyonudur.

`LICENSE` lisans bilgisini içerir.

`.gitignore` çalışma sırasında oluşan yerel dosyaların repository'ye eklenmesini engeller.

---

# Teknik Mimari

Ana sınıf:

```text
Stealer
```

Ana çalışma akışı:

```text
main()
  │
  ├── banner()
  │
  ├── kullanıcı seçimi
  │
  └── Stealer
        │
        ├── collect_system_info()
        ├── collect_wifi()
        ├── collect_browsers()
        ├── collect_games()
        ├── collect_files()
        ├── send_to_discord()
        └── cleanup()
```

Bu akış kaynak dosyadaki `run_all()` fonksiyonunda açıkça tanımlanmıştır.

---

# Hata Yönetimi

Kaynak kodunun mevcut sürümünde birçok işlem `try/except` bloklarıyla korunmaktadır.

Bu yaklaşım programın bazı hatalarda çalışmaya devam etmesini sağlarken, bazı hataların ayrıntılı olarak raporlanmamasına da neden olabilir.

Mevcut sürümün davranışını değiştirmemek amacıyla bu README, kaynak kodunda olmayan ek hata yönetimi özellikleri varsaymaz.

---

# Sürüm

```text
xaloAC Stealer v5.0
Windows Complete Edition
```

Kaynak dosyanın banner bölümünde sürüm 5.0 olarak belirtilmiştir.

---

# Marka ve Geliştirici

**Brand / Project Owner**

xaloAC

**Author / Developer**

x410m1s0

---

# Lisans

Bu proje repository içerisindeki `LICENSE` dosyasında belirtilen lisans koşullarına tabidir.

---

# Yasal Kullanım

Bu yazılım yalnızca yetkili güvenlik araştırmaları, kontrollü laboratuvar ortamları ve sahibinin açık izni bulunan sistemlerde kullanılmalıdır.

Başka kişilere ait:

* parolaların,
* hesap bilgilerinin,
* Wi-Fi anahtarlarının,
* ödeme bilgilerinin,
* cookie/session verilerinin,
* kişisel dosyaların

izinsiz şekilde alınması veya aktarılması için kullanılmamalıdır.

Kullanıcı, yazılımı çalıştırdığı ortam ve yaptığı işlemlerden kendisi sorumludur.

---

# xaloAC

**xaloAC**

Security Research & Software

**Author:** x410m1s0

**Version:** 5.0
