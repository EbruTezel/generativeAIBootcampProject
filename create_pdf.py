import os
import json
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "banks_2025.json")
OUTPUT_PDF = os.path.join(DATA_DIR, "banka_kampanyalari_2025.pdf")


# Minimal, editable default dataset — lütfen gerçek verilerle güncelleyin.
DEFAULT_BANKS = [
    {
        "isim": "Ziraat Bankası",
        "hesap_bonus": "350 TL (emeklilere özel)",
        "konut_faiz": "%2.69",
        "tasit_faiz": "%2.85",
        "ihtiyac_faiz": "%3.05",
        "kart_benefit": "Maaş emeklisi kartında yıllık aidat yok",
        "notlar": "Kamu çalışanlarına özel ek indirimler olabilir"
    },
    {
        "isim": "İş Bankası",
        "hesap_bonus": "750 TL (kampanya dönemi)",
        "konut_faiz": "%2.85",
        "tasit_faiz": "%2.95",
        "ihtiyac_faiz": "%3.15",
        "kart_benefit": "İlk yıl aidatsız, %5 nakit puan",
        "notlar": "Kampanya tarihleri sınırlıdır"
    },
    {
        "isim": "Garanti BBVA",
        "hesap_bonus": "500 TL",
        "konut_faiz": "%2.79",
        "tasit_faiz": "%2.99",
        "ihtiyac_faiz": "%3.25",
        "kart_benefit": "Yıllık %10 bonus",
        "notlar": "Bazı ürünler şubelere özel olabilir"
    },
    {
        "isim": "Yapı Kredi",
        "hesap_bonus": "400 TL",
        "konut_faiz": "%2.89",
        "tasit_faiz": "%3.05",
        "ihtiyac_faiz": "%3.30",
        "kart_benefit": "World kart ilk yıl bedava",
        "notlar": "Dijital başvurularda ekstra avantaj"
    },
    {
        "isim": "Akbank",
        "hesap_bonus": "600 TL",
        "konut_faiz": "%2.75",
        "tasit_faiz": "%2.92",
        "ihtiyac_faiz": "%3.20",
        "kart_benefit": "Axess'e özel %20 indirim",
        "notlar": "Kampanya sürelerine dikkat edin"
    },
    {
        "isim": "VakıfBank",
        "hesap_bonus": "550 TL + 50 TL mobil bonus",
        "konut_faiz": "%2.82",
        "tasit_faiz": "%2.97",
        "ihtiyac_faiz": "%3.35",
        "kart_benefit": "Maximum World kampanyaları",
        "notlar": "Belirli müşteri segmentlerine özel"
    },
    {
        "isim": "Halkbank",
        "hesap_bonus": "300 TL",
        "konut_faiz": "%2.88",
        "tasit_faiz": "%2.98",
        "ihtiyac_faiz": "%3.22",
        "kart_benefit": "Emekli ve KOBİ destek paketleri",
        "notlar": "KOBİ'lere özel kredi paketleri"
    },
    {
        "isim": "DenizBank",
        "hesap_bonus": "200 TL",
        "konut_faiz": "%2.90",
        "tasit_faiz": "%3.00",
        "ihtiyac_faiz": "%3.25",
        "kart_benefit": "Deniz Bonus uygulamaları",
        "notlar": "Dijital kanallarda avantajlar"
    },
    {
        "isim": "QNB Finansbank",
        "hesap_bonus": "450 TL",
        "konut_faiz": "%2.87",
        "tasit_faiz": "%2.96",
        "ihtiyac_faiz": "%3.18",
        "kart_benefit": "Bonus puan kampanyaları",
        "notlar": "Bireysel bankacılık teklifleri değişken"
    },
    {
        "isim": "TEB",
        "hesap_bonus": "250 TL",
        "konut_faiz": "%2.91",
        "tasit_faiz": "%3.06",
        "ihtiyac_faiz": "%3.28",
        "kart_benefit": "Teb maximum kampanyaları",
        "notlar": "Ödeme kolaylıkları sunuluyor"
    },
    {
        "isim": "ING Türkiye",
        "hesap_bonus": "200 TL",
        "konut_faiz": "%2.93",
        "tasit_faiz": "%3.04",
        "ihtiyac_faiz": "%3.26",
        "kart_benefit": "ING avantajları ve dijital kampanyalar",
        "notlar": "Dijital kanallarda öncelikli teklifler"
    },
    {
        "isim": "Kuveyt Türk (Katılım Bankası)",
        "hesap_bonus": "—",
        "konut_faiz": "Katılım oranına göre değişir",
        "tasit_faiz": "Katılım oranına göre değişir",
        "ihtiyac_faiz": "Katılım oranına göre değişir",
        "kart_benefit": "Katılım bankacılığı ürünleri",
        "notlar": "Faiz yerine kar/zarar paylaşımı modeline göredir"
    },
    {
        "isim": "Türkiye Finans (Katılım Bankası)",
        "hesap_bonus": "—",
        "konut_faiz": "Katılım oranına göre değişir",
        "tasit_faiz": "Katılım oranına göre değişir",
        "ihtiyac_faiz": "Katılım oranına göre değişir",
        "kart_benefit": "Katılım bankacılığı avantajları",
        "notlar": "Katılım bankası ürünleri için ilgili kurallar geçerlidir"
    },
    {
        "isim": "Kuveyt Türk",
        "hesap_bonus": "—",
        "konut_faiz": "%—",
        "tasit_faiz": "%—",
        "ihtiyac_faiz": "%—",
        "kart_benefit": "Katılım bankası ürünleri",
        "notlar": "Detaylar şube/dijital kanallarda kontrol edin"
    },
    {
        "isim": "Şekerbank",
        "hesap_bonus": "150 TL",
        "konut_faiz": "%2.95",
        "tasit_faiz": "%3.10",
        "ihtiyac_faiz": "%3.30",
        "kart_benefit": "Çiftçilere yönelik destek paketleri",
        "notlar": "Tarım desteği olanakları"
    },
    {
        "isim": "Fibabanka",
        "hesap_bonus": "100 TL",
        "konut_faiz": "%2.97",
        "tasit_faiz": "%3.12",
        "ihtiyac_faiz": "%3.35",
        "kart_benefit": "Fiba avantajları",
        "notlar": "Dijital kampanyalar mevcut olabilir"
    },
    {
        "isim": "Alternatif Bank",
        "hesap_bonus": "120 TL",
        "konut_faiz": "%2.99",
        "tasit_faiz": "%3.15",
        "ihtiyac_faiz": "%3.36",
        "kart_benefit": "Alternatif kampanyalar",
        "notlar": "KOBİ ve bireysel ürünlerde fırsatlar"
    },
    {
        "isim": "Odea Bank",
        "hesap_bonus": "—",
        "konut_faiz": "%3.05",
        "tasit_faiz": "%3.20",
        "ihtiyac_faiz": "%3.40",
        "kart_benefit": "Dijital bankacılık avantajları",
        "notlar": "Detaylar için banka ile iletişime geçin"
    },
    {
        "isim": "HSBC Türkiye",
        "hesap_bonus": "—",
        "konut_faiz": "%2.94",
        "tasit_faiz": "%3.10",
        "ihtiyac_faiz": "%3.33",
        "kart_benefit": "Uluslararası avantajlar",
        "notlar": "Yurt dışı işlem avantajları olabilir"
    },
    {
        "isim": "Burgan Bank",
        "hesap_bonus": "—",
        "konut_faiz": "%3.00",
        "tasit_faiz": "%3.18",
        "ihtiyac_faiz": "%3.38",
        "kart_benefit": "Burgan kampanyaları",
        "notlar": "Bireysel ürünlerde farklılıklar olabilir"
    }
]


def ensure_data_file():
    """Ensure the data directory and JSON file exist. If the JSON file is missing, write DEFAULT_BANKS into it for easy editing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_BANKS, f, ensure_ascii=False, indent=2)
            print(f"Oluşturuldu: {DATA_FILE} (dahili varsayılan verilerle). Lütfen gerçek verilerle güncelleyin.")
        except Exception as e:
            print("Data dosyası oluşturulamadı:", e)


def load_banks():
    """Load banks data from JSON if present, otherwise return DEFAULT_BANKS."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return data
            else:
                print("Dikkat: JSON dosyası beklenen formatta değil. Varsayılan veri kullanılacak.")
        except Exception as e:
            print("JSON yüklenirken hata:", e)
    return DEFAULT_BANKS


def register_suitable_font():
    candidates = [
        # macOS common
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        # Linux common
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        # possible local fonts folder in project
        os.path.join(DATA_DIR, "fonts", "DejaVuSans.ttf"),
        os.path.join(DATA_DIR, "fonts", "NotoSans-Regular.ttf"),
        os.path.join(DATA_DIR, "fonts", "Arial.ttf"),
    ]

    # Try explicit candidates first
    for path in candidates:
        if path and os.path.exists(path):
            try:
                font_name = 'CustomFont_' + os.path.splitext(os.path.basename(path))[0]
                if font_name not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont(font_name, path))
                print(f"Kayıtlı font kullanılıyor: {path} -> {font_name}")
                return font_name
            except Exception as e:
                print(f"Font kaydı başarısız ({path}):", e)

    # If none of the explicit candidates exist, scan common directories for .ttf files
    font_dirs = [
        "/Library/Fonts",
        "/System/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
        "/usr/share/fonts/truetype",
        os.path.join(DATA_DIR, "fonts"),
    ]

    for d in font_dirs:
        if not d or not os.path.isdir(d):
            continue
        try:
            for root, _, files in os.walk(d):
                for f in files:
                    if f.lower().endswith('.ttf'):
                        path = os.path.join(root, f)
                        try:
                            font_name = 'CustomFont_' + os.path.splitext(f)[0]
                            if font_name not in pdfmetrics.getRegisteredFontNames():
                                pdfmetrics.registerFont(TTFont(font_name, path))
                            print(f"Bulunan ve kayıt edilen font: {path} -> {font_name}")
                            return font_name
                        except Exception as e:
                            # try next file
                            print(f"Font kaydı yapılamadı ({path}):", e)
        except Exception:
            continue

    # Eğer bulunamadıysa kullanıcıya bilgi ver ve fallback olarak None döndür
    print("UYARI: Yazı tipi bulunamadı. Türkçe karakterler doğru görünmeyebilir.\n"
          "Lütfen bir TTF dosyasını data/fonts/ içine koyun (ör. DejaVuSans.ttf) veya sistem fontlarını kontrol edin.")
    return None


def create_pdf(banks, output_path=OUTPUT_PDF):
    # register font and choose font name
    font_name = register_suitable_font()

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    styles = getSampleStyleSheet()
    story = []

    # Başlık stili
    title_kwargs = {'fontSize': 22, 'alignment': TA_CENTER, 'spaceAfter': 12}
    h_kwargs = {'fontSize': 14, 'textColor': colors.HexColor('#2c5aa0'), 'spaceAfter': 6}
    normal_kwargs = {'fontSize': 11, 'leading': 15}
    small_kwargs = {'fontSize': 9, 'leading': 12, 'textColor': colors.grey}

    # Eğer bir TTF font kaydedildiyse style'lara fontName ekle
    if font_name:
        title_kwargs['fontName'] = font_name
        h_kwargs['fontName'] = font_name
        normal_kwargs['fontName'] = font_name
        small_kwargs['fontName'] = font_name

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], **title_kwargs)
    h_style = ParagraphStyle('Heading', parent=styles['Heading2'], **h_kwargs)
    normal = ParagraphStyle('Normal', parent=styles['Normal'], **normal_kwargs)
    small = ParagraphStyle('Small', parent=styles['Normal'], **small_kwargs)

    # Kapak
    story.append(Paragraph("2025 TÜRKİYE BANKA KAMPANYALARI & KREDİ FAİZ ORANLARI", title_style))
    story.append(Paragraph(f"Oluşturma: {datetime.now().strftime('%d %B %Y %H:%M')}", small))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Bu doküman bilgilendirme amaçlıdır. Güncel ve resmi bilgiler için lütfen bankaların kendi kaynaklarını kontrol ediniz.", normal))
    story.append(Spacer(1, 1 * cm))

    # Özet
    story.append(Paragraph("Kısa Özet", h_style))
    summary_lines = [f"Toplam banka sayısı: <b>{len(banks)}</b>", "Veri kaynağı: data/banks_2025.json (varsa) veya dahili varsayılan veri."]
    for line in summary_lines:
        story.append(Paragraph(line, normal))
    story.append(PageBreak())

    # Her bankayı ayrı bölümde göster
    for banka in banks:
        story.append(Paragraph(banka.get('isim', '---'), h_style))

        rows = [
            ("Hesap Açılış/Bonus", banka.get('hesap_bonus', '—')),
            ("Konut Kredisi Faizi", banka.get('konut_faiz', '—')),
            ("Taşıt Kredisi Faizi", banka.get('tasit_faiz', '—')),
            ("İhtiyaç Kredisi Faizi", banka.get('ihtiyac_faiz', '—')),
            ("Kredi Kartı / Benefit", banka.get('kart_benefit', '—')),
            ("Maaş Kampanyası", banka.get('maas_kampanyasi', '—')),
            ("Gelir Dilimi Avantajları (70K+ TL)", banka.get('gelir_dilimi_avantajlari', '—')),
            ("Diğer Avantajlar", banka.get('diger_avantajlar', '—')),
            ("Notlar", banka.get('notlar', '—')),
        ]

        for label, value in rows:
            story.append(Paragraph(f"<b>{label}:</b> {value}", normal))
            story.append(Spacer(1, 0.15 * cm))

        story.append(Spacer(1, 0.4 * cm))

        # Her banka sonrası sayfa sonu
        story.append(PageBreak())

    # Son sayfa: kaynak ve uyarılar
    story.append(Paragraph("Kaynaklar ve Uyarılar", h_style))
    story.append(Paragraph("Bu doküman eğitim/bootcamp projesi amaçlı üretilmiştir. Gerçek kampanya ve oranlar için bankaların resmi web siteleri ve duyuruları takip edilmelidir.", normal))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Not: Veriler manuel güncellenmelidir.", small))

    # PDF oluştur
    try:
        doc.build(story)
        print(f"✅ PDF başarıyla oluşturuldu: {output_path}")
    except Exception as e:
        print("PDF oluşturulurken hata oluştu:", e)


if __name__ == '__main__':
    ensure_data_file()
    banks = load_banks()
    create_pdf(banks)
