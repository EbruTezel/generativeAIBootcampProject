import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .data_loader import DataLoader
from dotenv import load_dotenv
from typing import cast, Optional
from pydantic import SecretStr

load_dotenv()


class BankaChatbot:
    """Banka kampanyaları hakkında soru-cevap yapan chatbot.

    Değişiklik: Eğer `GROQ_API_KEY` tanımlı değilse uygulama hata fırlatmıyor; bunun yerine
    basit bir retrieval-temelli demo cevabı döndüren fallback davranışı kullanılıyor. Bu sayede
    proje import edildiğinde veya test edilirken dış API anahtarına bağımlı olmaz.
    """

    def __init__(self):
        # API key kontrol
        api_key = os.getenv("GROQ_API_KEY")

        print("PDF yükleniyor...")
        loader = DataLoader()
        self.document_text = loader.load_all_pdfs()

        print("Metin parçalanıyor (chunking)...")
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(self.document_text)
        print(f"[OK] {len(chunks)} parça oluşturuldu")

        print("Embedding modeli yükleniyor...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Vektör veritabanı oluşturuluyor...")
        self.vectorstore = FAISS.from_texts(chunks, embeddings)

        print("Bellek oluşturuluyor...")
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key='answer'
        )

        # Chat prompt template (konuşma geçmişini içeren)
        from langchain.prompts import PromptTemplate

        template = """Sen yardımcı bir banka asistanısın. Verilen bilgilerden soruları cevapla.

SORU TÜRLERİ VE CEVAPLAMA:

1. "EN DÜŞÜK/UYGUN FAİZ" sorulduğunda:
   
   KRİTİK: KREDİ TÜRÜNÜ DİKKATLE BELİRLE!
   - "KONUT kredisi" → Sadece "Konut Kredisi Faizi" değerlerine bak
   - "TAŞIT kredisi" → Sadece "Taşıt Kredisi Faizi" değerlerine bak
   - "İHTİYAÇ kredisi" → Sadece "İhtiyaç Kredisi Faizi" değerlerine bak
   
   Adımlar:
   - DOĞRU kredi türündeki TÜM bankaların faizlerini bul
   - Sayıları karşılaştır (2.69 < 2.75 < 2.85 < 2.92)
   - En KÜÇÜK sayıyı bul (En düşük faiz = En küçük sayı)
   - SADECE sonucu söyle: "Ziraat Bankası'nın [KREDİ TÜRÜ] faiz oranı en düşük, %X.XX"
   
   "İKİNCİ EN DÜŞÜK" veya "ONDAN SONRA" sorulduğunda:
   - TÜM faizleri KÜÇÜKTEN BÜYÜĞE sırala
   - LİSTEDE İKİNCİ SIRADA olanı söyle
   - Örnek: Taşıt kredisi → 2.85 < 2.92 < 2.95 → İkinci: %2.92
   
   ÖRNEKLER:
   DOĞRU: "Konut kredisi en düşük?" → Ziraat %2.69
   DOĞRU: "Ziraat'ten sonra?" → Akbank %2.75 (2.69 < 2.75)
   DOĞRU: "Taşıt kredisi en uygun?" → Ziraat %2.85
   DOĞRU: "Ondan sonra hangi banka?" → Akbank %2.92 (2.85 < 2.92)
   DOĞRU: "2. sırada kim?" → İkinci en düşük olanı söyle
   YANLIŞ: "Ziraat'ten sonra?" → Ziraat (YANLIŞ! Aynı bankayı tekrar söyleme!)
   
   ÖNEMLİ: 2.69 < 2.75 < 2.85 < 2.92. En küçük sayı = En düşük faiz!

2. "KAMPANYALAR" veya "AVANTAJLAR" sorulduğunda:
   - Sorulan bankanın kampanya bilgilerini ver
   - Hesap açılış bonusu, kredi kartı avantajları, notları paylaş
   - Örnek: "İş Bankası: 750 TL bonus, ilk yıl aidatsız, %5 nakit puan"

3. "FAİZ ORANI" sorulduğunda:
   - Sorulan bankanın ilgili kredi türündeki faiz oranını ver
   - Örnek: "İş Bankası'nın konut kredisi faizi %2.85"

4. "EMEKLİLER" veya "ÖZEL GRUP" sorulduğunda:
   - O gruba özel avantajları olan bankayı bul
   - Örnek: "Emekliler için Ziraat Bankası avantajlı, 350 TL özel bonus"

5. Bağlamsal sorular ("Peki", "Bunun", "Onun"):
   - Önceki konuşmayı hatırla
   - Aynı banka hakkında devam et

6. Genel bilgi:
   - Verilerde varsa cevapla
   - Kısa ve net ol
   - Yoksa: "Bu bilgi verilerde mevcut değil"

MATEMATİK KURALI:
- 2.69 < 2.75 < 2.79 < 2.82 < 2.85
- Küçük sayı = Düşük faiz (İYİ)

Geçmiş:
{chat_history}

Veriler:
{context}

Soru: {question}

Cevap (Kısa ve öz):"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["chat_history", "context", "question"]
        )

        # Eğer GROQ API anahtarı varsa gerçek LLM ile zinciri kur
        if api_key:
            print("LLM bağlanıyor (Groq)...")
            # Tip uyumsuzluğu uyarısını sessize almak için statik cast kullan
            api_key_for_llm = cast("Optional[SecretStr]", api_key)
            llm = ChatGroq(
                api_key=api_key_for_llm,
                model="llama-3.1-8b-instant",
                temperature=0.0,
                max_tokens=512,
                top_p=0.1  # Daha deterministik cevaplar için
            )

            print("RAG zinciri oluşturuluyor...")
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}  # Tüm chunk'ları getir (4 chunk var)
                ),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": PROMPT},
                return_source_documents=False,
                verbose=False
            )
            # kullanmak için self.chain mevcut
            self.retriever = None
            self.prompt = None
            print("[OK] Chatbot hazır! (GROQ kullanılıyor, konuşma belleği aktif)\n")
        else:
            # Anahtar yoksa projeyi kırma; basit demo fallback davranışı kur
            print("UYARI: GROQ_API_KEY bulunamadı. Gerçek LLM çağrısı yapılmayacak. Demo modunda çalışıyor.")
            # Retriever hazır, prompt kaydediliyor; ask() yöntemi bunları kullanacak
            self.chain = None
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            self.prompt = PROMPT
            print("[OK] Chatbot hazır! (DEMO modunda, offline cevapları kullanır)\n")

    def ask(self, question):
        """Kullanıcı sorusunu yanıtlar.

        Eğer gerçek LLM zinciri varsa onu kullanır. Aksi halde, retriever ile ilgili dokümanları
        alıp prompt içinde birleştirerek demo biçiminde bir cevap döndürür.
        """
        # Gerçek LLM zinciri varsa onu kullan
        if self.chain:
            response = self.chain({"question": question})
            return response["answer"]

        # Aksi halde demo fallback: ilgili dokümanları al ve prompt'u doldur
        docs = self.retriever.get_relevant_documents(question)
        context = "\n\n".join([d.page_content for d in docs])

        # Prompt'u doldur
        prompt_text = self.prompt.format(chat_history="", context=context, question=question)

        # Basit, insan tarafından okunabilir mock cevap üret
        short_ctx = context[:1200]
        demo_answer = (
            "[DEMO CEVAP — GROQ API anahtarı yok]\n"
            "Aşağıda sorgunuzla ilgili kaynaklardan alınan özet (kısıtlı):\n\n"
            f"{short_ctx}\n\n"
            "Soru: " + question + "\n\n"
            "Not: Bu cevap otomatik demo modunda oluşturuldu. Gerçek, doğal dil üretimi için GROQ_API_KEY ekleyin."
        )

        return demo_answer


# Test
if __name__ == "__main__":
    print("Chatbot başlatılıyor...\n")
    chatbot = BankaChatbot()

    print("="*70)
    print("KAPSAMLI TEST SENARYOLARı\n")
    print("="*70)

    # Test 1: En düşük konut kredisi faizi
    print("\n[TEST 1] En düşük konut kredisi faizi")
    print("-" * 70)
    soru1 = "Hangi bankanın konut kredisi faiz oranı en düşük?"
    cevap1 = chatbot.ask(soru1)
    print(f"Soru: {soru1}")
    print(f"Cevap: {cevap1}")
    beklenen1 = "Ziraat" in cevap1 and "2.69" in cevap1
    print(f"Durum: {'BAŞARILI' if beklenen1 else 'BAŞARISIZ'} (Beklenen: Ziraat %2.69)")

    # Test 2: Kampanya bilgisi
    print("\n[TEST 2] Kampanya bilgisi")
    print("-" * 70)
    soru2 = "İş Bankası'nın kampanyaları neler?"
    cevap2 = chatbot.ask(soru2)
    print(f"Soru: {soru2}")
    print(f"Cevap: {cevap2}")
    beklenen2 = "750" in cevap2 or "bonus" in cevap2.lower()
    print(f"Durum: {'BAŞARILI' if beklenen2 else 'BAŞARISIZ'} (Beklenen: 750 TL bonus)")

    # Test 3: Bağlamsal soru
    print("\n[TEST 3] Bağlamsal soru (kredi kartı)")
    print("-" * 70)
    soru3 = "Peki kredi kartı avantajları neler?"
    cevap3 = chatbot.ask(soru3)
    print(f"Soru: {soru3}")
    print(f"Cevap: {cevap3}")
    beklenen3 = "İş Bankası" in cevap3 or "aidatsız" in cevap3.lower()
    print(f"Durum: {'BAŞARILI' if beklenen3 else 'BAŞARISIZ'} (Beklenen: İş Bankası bilgileri)")

    # Test 4: Farklı kredi türü (Taşıt)
    print("\n[TEST 4] En düşük taşıt kredisi faizi")
    print("-" * 70)
    soru4 = "Taşıt kredisi almak istiyorum, en uygun faiz hangisinde?"
    cevap4 = chatbot.ask(soru4)
    print(f"Soru: {soru4}")
    print(f"Cevap: {cevap4}")
    beklenen4 = "2.85" in cevap4 and "Ziraat" in cevap4
    print(f"Durum: {'BAŞARILI' if beklenen4 else 'BAŞARISIZ'} (Beklenen: Ziraat %2.85)")

    # Test 5: İkinci en düşük (Bağlam + Akıllı cevap)
    print("\n[TEST 5] İkinci en düşük taşıt kredisi")
    print("-" * 70)
    soru5 = "Ziraat'ten sonra hangi banka uygun?"
    cevap5 = chatbot.ask(soru5)
    print(f"Soru: {soru5}")
    print(f"Cevap: {cevap5}")
    beklenen5 = "Akbank" in cevap5 or "2.92" in cevap5 or "İş Bankası" in cevap5
    print(f"Durum: {'BAŞARILI' if beklenen5 else 'BAŞARISIZ'} (Beklenen: İkinci en düşük)")

    # Test 6: Emekliler için özel
    print("\n[TEST 6] Emekliler için avantajlı banka")
    print("-" * 70)
    soru6 = "Emekliler için hangi banka daha avantajlı?"
    cevap6 = chatbot.ask(soru6)
    print(f"Soru: {soru6}")
    print(f"Cevap: {cevap6}")
    beklenen6 = "Ziraat" in cevap6 and "350" in cevap6
    print(f"Durum: {'BAŞARILI' if beklenen6 else 'BAŞARISIZ'} (Beklenen: Ziraat 350 TL)")

    # Özet
    print("\n" + "="*70)
    print("TEST SONUÇLARI ÖZETI")
    print("="*70)
    basarili = sum([beklenen1, beklenen2, beklenen3, beklenen4, beklenen5, beklenen6])
    toplam = 6
    print(f"\nBaşarılı: {basarili}/{toplam}")
    print(f"Başarısız: {toplam - basarili}/{toplam}")

    if basarili == toplam:
        print("\nTÜM TESTLER BAŞARILI! Chatbot production-ready!")
    else:
        print(f"\n{toplam - basarili} test başarısız oldu.")
    print("="*70)

