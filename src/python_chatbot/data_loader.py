import os
from PyPDF2 import PdfReader

class DataLoader:
    """PDF dosyalarını okuyup metin çıkarır"""

    def __init__(self, data_folder="../../data"):
        # Proje kökündeki data/ klasörünü kullan
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_folder = os.path.join(current_dir, data_folder)

    def load_pdf(self, filename):
        filepath = os.path.join(self.data_folder, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"PDF bulunamadı: {filepath}")

        reader = PdfReader(filepath)
        text = ""

        # Tüm sayfaları oku
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    def load_all_pdfs(self):
        all_text = ""

        for filename in os.listdir(self.data_folder):
            if filename.endswith('.pdf'):
                print(f"📄 Okunuyor: {filename}")
                text = self.load_pdf(filename)
                all_text += text + "\n\n"

        return all_text


# Test
if __name__ == "__main__":
    loader = DataLoader()
    content = loader.load_pdf("banka_kampanyalari_2025.pdf")
    print("✅ PDF İçeriği yüklendi:")
    print(content[:500])  # İlk 500 karakter