# Banka Kampanyaları Chatbot

Türkiye'deki banka kampanyaları ve kredi faiz oranları hakkında bilgi veren RAG (Retrieval Augmented Generation) tabanlı akıllı sohbet robotu.

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

### Senaryo 1: Temel Bilgi Sorgulama

**Kullanıcı:** Hangi bankanın konut kredisi faiz oranı en düşük?

**Chatbot:** Türkiye'deki banka kampanyaları arasında en düşük konut kredisi faiz oranına sahip olan bankalar:

Ziraat Bankası:
- Konut Kredisi Faizi: %2.69
- Taşıt Kredisi Faizi: %2.85
- İhtiyaç Kredisi Faizi: %3.05

Akbank:
- Konut Kredisi Faizi: %2.75
- Taşıt Kredisi Faizi: %2.92
- İhtiyaç Kredisi Faizi: %3.20

En düşük konut kredisi faiz oranı Ziraat Bankası'nda %2.69'dur.

---

### Senaryo 2: Bağlamsal Konuşma

**Kullanıcı:** İş Bankası'nın kampanyaları neler?

**Chatbot:** İş Bankası'nın 2025 yılı kampanyaları şunlardır:

İş Bankası:
- Hesap Açılış/Bonus: 750 TL (kampanya dönemi)
- Konut Kredisi Faizi: %2.85
- Taşıt Kredisi Faizi: %2.95
- İhtiyaç Kredisi Faizi: %3.15
- Kredi Kartı / Benefit: İlk yıl aidatsız, %5 nakit puan
- Notlar: Kampanya tarihleri sınırlıdır

**Kullanıcı:** Peki kredi kartı avantajları neler?

**Chatbot:** İş Bankası'nın kredi kartı avantajları:
- İlk yıl aidatsız kullanım
- Her harcamada %5 nakit puan kazanımı
- Kampanya tarihleri sınırlıdır, güncel detaylar için bankaya başvurmanız önerilir

---

### Senaryo 3: Karşılaştırmalı Sorgulama

**Kullanıcı:** Emekliler için hangi banka daha avantajlı?

**Chatbot:** Emekliler için özel kampanyalar sunan bankalar:

Ziraat Bankası:
- Hesap Açılış/Bonus: 350 TL (emeklilere özel)
- Kredi Kartı: Maaş emeklisi kartında yıllık aidat yok
- Notlar: Kamu çalışanlarına özel ek indirimler olabilir

Halkbank:
- Hesap Açılış/Bonus: 300 TL
- Kredi Kartı / Benefit: Emekli ve KOBİ destek paketleri
- Notlar: KOBİ'lere özel kredi paketleri

Emekliler için en avantajlı seçenek Ziraat Bankası'dır.

---

### Senaryo 4: Spesifik Ürün Sorgulama

**Kullanıcı:** Taşıt kredisi almak istiyorum, en uygun faiz hangisinde?

**Chatbot:** Taşıt kredisi faiz oranlarına göre en uygun bankalar:

Ziraat Bankası:
- Taşıt Kredisi Faizi: %2.85

Akbank:
- Taşıt Kredisi Faizi: %2.92

İş Bankası:
- Taşıt Kredisi Faizi: %2.95

En düşük taşıt kredisi faiz oranı Ziraat Bankası'nda %2.85'tir.

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
2. **Chunking:** Metin 1000 karakterlik parçalara bölünür (200 karakter overlap)
3. **Embedding:** Her parça HuggingFace modeli ile vektöre dönüştürülür
4. **Vektör Veritabanı:** FAISS ile indekslenir
5. **Sorgu İşleme:** Kullanıcı sorusu embedding'e çevrilir
6. **Benzerlik Araması:** En alakalı 3 doküman parçası bulunur
7. **Bağlam Oluşturma:** Bulunan parçalar + konuşma geçmişi birleştirilir
8. **LLM Çağrısı:** GROQ API'ye context + soru gönderilir
9. **Cevap Üretimi:** Llama 3.1 modeli doğal dil cevabı üretir
10. **Bellek Güncelleme:** Konuşma geçmişi kaydedilir

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

