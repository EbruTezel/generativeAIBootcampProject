# Banka Kampanyaları Chatbot

Türkiye'deki banka kampanyaları ve kredi faiz oranları hakkında bilgi veren RAG (Retrieval Augmented Generation) tabanlı akıllı sohbet robotu.

## Canlı Demo

**Uygulamaya buradan ulaşabilirsiniz:** [https://chatbot.devarvin.com](https://chatbot.devarvin.com)

> Production ortamında Docker ve Traefik reverse proxy ile SSL sertifikalı olarak yayınlanmaktadır.

## Proje Hakkında

Bu proje, Akbank Generative AI Bootcamp kapsamında geliştirilmiş bir chatbot uygulamasıdır. Kullanıcıların Türkiye'deki bankaların kampanyaları, kredi faiz oranları ve diğer finansal ürünler hakkında doğal dil ile soru sormasını ve anlamlı cevaplar almasını sağlar.

## Özellikler

- RAG (Retrieval Augmented Generation) mimarisi ile doküman tabanlı soru-cevap
- Konuşma belleği ile bağlamsal diyalog yönetimi
- GROQ API ve Llama 3.1 dil modeli entegrasyonu
- FAISS vektör veritabanı ile hızlı benzerlik araması
- HuggingFace embedding modelleri
- Flask tabanlı modern web arayüzü
- PDF dokümanlardan otomatik bilgi çıkarma
- Türkçe dil desteği
- Gerçek zamanlı sohbet deneyimi

## Teknoloji Stack

**Backend:**
- Python 3.9+
- LangChain - RAG pipeline ve LLM entegrasyonu
- GROQ API - Llama 3.1 dil modeli
- FAISS - Vektör veritabanı
- Flask - Web framework
- HuggingFace Transformers - Embedding modelleri
- PyPDF2 - PDF işleme
- ReportLab - PDF oluşturma

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript

## Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- pip paket yöneticisi
- GROQ API anahtarı (ücretsiz hesap oluşturabilirsiniz: https://console.groq.com)

### Adım 1: Projeyi Klonlayın

```bash
git clone <repository-url>
cd generativeAIBootcampProject
```

### Adım 2: Sanal Ortam Oluşturun (Opsiyonel ama Önerilir)

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# veya
.venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Ortam Değişkenlerini Ayarlayın (.env dosyası)

Proje kök dizininde `.env` dosyası oluşturun:

```bash
touch .env
```

`.env` dosyasını açın ve GROQ API anahtarınızı ekleyin:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Adım 5: Veri Dosyalarını Kontrol Edin

Proje, `data/banka_kampanyalari_2025.pdf` dosyasını kullanır. Bu dosya:

**Varsayılan olarak projeyle birlikte gelir.** Chatbot'un çalışması için bu PDF dosyası **gereklidir**.

**İsterseniz PDF'i yeniden oluşturabilirsiniz:**

```bash
python3 create_pdf.py
```

Bu komut, `data/banks_2025.json` dosyasındaki verileri kullanarak `data/banka_kampanyalari_2025.pdf` dosyasını yeniden oluşturur.

**Not:** PDF dosyasını silmeyin veya taşımayın. Chatbot başlatıldığında bu dosya okunur.

## Kullanım

### Chatbot'u Başlatma

```bash
python3 run_chatbot.py
```

Chatbot başlatıldığında şu adımlar otomatik olarak gerçekleşir:
1. PDF dokümanları yüklenir
2. Metin parçalara bölünür (chunking)
3. Embedding modeli yüklenir
4. Vektör veritabanı oluşturulur
5. Konuşma belleği başlatılır
6. Flask web sunucusu başlar

### Web Arayüzüne Erişim

Tarayıcınızda aşağıdaki adresi açın:

```
http://localhost:5001
```

### Konuşma Geçmişini Sıfırlama

Chatbot, konuşma geçmişini bellekte tutar. Yeni bir konuşma başlatmak istediğinizde:
- Web arayüzünde sağ üst köşedeki **"Yeni Konuşma Başlat"** butonuna tıklayın
- Bu işlem konuşma belleğini temizler ve chatbot'u ilk haline döndürür
- Önceki konuşmalar silinir ve bağlam sıfırlanır

## Örnek Kullanım Senaryoları

### Senaryo 1: En Düşük Konut Kredisi Faizi

**Kullanıcı:** Hangi bankanın konut kredisi faiz oranı en düşük?

**Chatbot:** Ziraat Bankası %2.69

---

### Senaryo 2: Kampanya Bilgisi

**Kullanıcı:** İş Bankası'nın kampanyaları neler?

**Chatbot:** İş Bankası'nın konut kredisi kampanyaları şu şekildedir:

- Maaş Avantaj Paketi: 60.000-80.000 TL arası 1.000 TL, 80.000 TL üzeri 1.500 TL + Maximum World kredi kartı hediye. İlk 6 ay tüm bankacılık işlemleri ücretsiz.

---

### Senaryo 3: En Düşük Taşıt Kredisi

**Kullanıcı:** Taşıt kredisi almak istiyorum, en uygun hangisi?

**Chatbot:** Taşıt kredisi için en uygun faiz oranı %2.85 olan Ziraat Bankası'dır.

---

### Senaryo 4: Bağlamsal Soru (İkinci En Düşük)

**Kullanıcı:** Ziraat'ten sonra hangi banka uygun?

**Chatbot:** Ziraat Bankası'ndan sonra en uygun faiz oranı %2.75 olan Akbank'tır.

---

### Senaryo 5: Emekliler İçin Avantajlı Banka

**Kullanıcı:** Emekliler için hangi banka daha avantajlı?

**Chatbot:** Emekliler için en avantajlı banka Ziraat Bankası'dır. Ziraat Bankası, emeklilere özel 350 TL hesap açılış bonusu ve maaş promosyonu sunmaktadır. Ayrıca, emekliler için ek 200 TL bonus verilmektedir.

## Proje Yapısı

```
generativeAIBootcampProject/
├── README.md                          # Proje dokümantasyonu
├── LICENSE                            # Lisans dosyası
├── requirements.txt                   # Python bağımlılıkları
├── create_pdf.py                      # PDF oluşturma scripti
├── run_chatbot.py                     # Uygulama başlatma scripti
├── .env                               # Ortam değişkenleri (oluşturulmalı)
├── data/                              # Veri dosyaları
│   ├── banks_2025.json               # Banka verileri (JSON)
│   ├── banka_kampanyalari_2025.pdf   # Oluşturulan PDF rapor
│   └── fonts/                        # Font dosyaları
│       └── ArialUnicode.ttf
└── src/
    └── python_chatbot/               # Ana chatbot modülü
        ├── __init__.py
        ├── chatbot.py                # RAG chatbot mantığı
        ├── data_loader.py            # PDF okuma modülü
        ├── web_app.py                # Flask web uygulaması
        ├── static/                   # Statik dosyalar
        │   ├── css/
        │   │   └── style.css         # Arayüz stilleri
        │   └── js/
        │       └── main.js           # Frontend JavaScript
        └── templates/                # HTML şablonları
            └── index.html            # Ana sayfa
```

## Nasıl Çalışır?

### RAG (Retrieval Augmented Generation) Mimarisi

1. **Doküman Yükleme:** PDF dosyalarından banka kampanya bilgileri okunur
2. **Chunking:** Metin 2500 karakterlik parçalara bölünür (500 karakter overlap) - Daha büyük chunk'lar daha fazla banka bilgisi içerir
3. **Embedding:** Her parça HuggingFace modeli (sentence-transformers/all-MiniLM-L6-v2) ile vektöre dönüştürülür
4. **Vektör Veritabanı:** FAISS ile indekslenir ve hızlı benzerlik araması için optimize edilir
5. **Sorgu İşleme:** Kullanıcı sorusu aynı embedding modeli ile vektöre çevrilir
6. **Benzerlik Araması:** En alakalı 6 doküman parçası bulunur (k=6) - Tüm bankaları kapsayacak yeterli bilgi
7. **Bağlam Oluşturma:** Bulunan parçalar + konuşma geçmişi birleştirilir
8. **LLM Çağrısı:** GROQ API'ye (Llama 3.1-8B-Instant) context + soru gönderilir
9. **Cevap Üretimi:** Özel optimize edilmiş prompt ile doğal dil cevabı üretilir
10. **Bellek Güncelleme:** ConversationBufferMemory ile konuşma geçmişi kaydedilir

### Konuşma Belleği

Chatbot, önceki konuşmaları `ConversationBufferMemory` ile hafızasında tutar. Bu sayede:
- Kullanıcı "peki", "onun", "o banka" gibi referanslar kullanabilir
- Bağlamsal sorular sorabilir
- Doğal bir diyalog deneyimi yaşar

## Veri Kaynağı

Proje, `data/banks_2025.json` dosyasından 13 bankanın kampanya verilerini kullanır:


### Konuşma Bağlamı Yönetimi

Chatbot, ConversationalRetrievalChain kullanarak konuşma geçmişini yönetir. Prompt template'de chat_history parametresi bulunur ve LLM'e şu talimat verilir:

"Önceki konuşma geçmişini dikkate alarak soruyu yanıtla. Eğer kullanıcı 'onun', 'bunun', 'peki', 'o banka', 'kampanyaları neler' gibi referanslar kullanıyorsa, önceki konuşmaya bakarak hangi bankadan bahsettiğini anla ve SADECE O BANKA hakkında bilgi ver."

Bu sayede kullanıcı:
1. "Hangi bankanın faizi düşük?" sorusunu sorar
2. Chatbot "Ziraat Bankası" diye cevap verir
3. Kullanıcı "Peki kampanyaları neler?" diye sorar
4. Chatbot önceki konuşmayı hatırlayarak SADECE Ziraat Bankası'nın kampanyalarını listeler

### Fallback Mekanizması

GROQ_API_KEY tanımlanmadığında chatbot demo modunda çalışır ve retrieval-temelli basit cevaplar döndürür. Bu sayede proje test edilebilir ve geliştirme ortamında API limitleri tükenmez.

## Sorun Giderme

### Chatbot önceki konuşmaları hatırlıyor 

Eğer chatbot eski konuşmaları hatırlıyor ve yeni bir soru sorduğunuzda önceki bağlamı kullanıyorsa:
- Web arayüzünde **"Yeni Konuşma Başlat"** butonuna tıklayın
- Bu işlem konuşma belleğini tamamen temizler ve yeni bir sohbet başlatır

### PDF yüklenemiyor

- `data/` klasöründe PDF dosyasının bulunduğundan emin olun
- `create_pdf.py` scriptini çalıştırarak PDF'i yeniden oluşturun

### GROQ API hatası

- `.env` dosyasında GROQ_API_KEY'in doğru tanımlandığından emin olun
- API anahtarınızın geçerli olduğunu kontrol edin
- API limitlerini aşmadığınızdan emin olun

### Port 5001 kullanımda

Farklı bir port kullanmak için `src/python_chatbot/web_app.py` dosyasındaki port numarasını değiştirin.


## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## İletişim

Proje Sahibi: Ebru Tezel

## Teşekkürler

- LangChain topluluğu
- GROQ API
- HuggingFace

## Notlar

- Bu proje eğitim/bootcamp amaçlı üretilmiştir
- Gerçek kampanya ve faiz oranları için bankaların resmi web sitelerini ziyaret edin
- Veriler manuel olarak güncellenmelidir
- Finansal kararlar almadan önce mutlaka ilgili banka ile iletişime geçin

