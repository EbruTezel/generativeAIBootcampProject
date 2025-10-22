import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .data_loader import DataLoader
from dotenv import load_dotenv

load_dotenv()


class BankaChatbot:
    """Banka kampanyaları hakkında soru-cevap yapan chatbot."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        print("PDF yükleniyor...")
        loader = DataLoader()
        self.document_text = loader.load_all_pdfs()

        print("Metin parçalanıyor...")
        text_splitter = CharacterTextSplitter(
            chunk_size=5000,  # Daha büyük chunk = tüm bankalar tek chunk'ta
            chunk_overlap=800
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

        from langchain.prompts import PromptTemplate

        # OPTİMİZE EDİLMİŞ PROMPT - Matematiksel hesaplama GEREKTİRMEZ
        template = """Sen profesyonel bir banka danışmanısın.

KURALLAR:
1. Soruyu TEKRAR ETME
2. Direkt cevap ver
3. Verilen listeyi OLDUĞU GİBİ kullan

EN DÜŞÜK FAİZ:
- Kredi türünü belirle (konut/taşıt/ihtiyaç)
- Verilen bilgide o türdeki EN KÜÇÜK RAKAMLI bankayı söyle
- Örnek: "Ziraat Bankası %2.69"

"SONRA/SONRAKİ/ONDAN SONRA" SORULDUĞUNDA:
- KRİTİK: Geçmişe bak! Hangi bankaları söyledin?
- Söylediğin bankaları LİSTELE (zihninde)
- Verilen bilgide o türdeki bankaları KÜÇÜKTEN BÜYÜĞE sırala
- Daha önce SÖYLEMEDİĞİN bir SONRAKİ bankayı seç
- ASLA aynı bankayı tekrar söyleme!
- Örnek: Ziraat %2.85 söyledim → Akbank %2.92 söyledim → Şimdi İş Bankası %2.95 söylemeliyim

KAMPANYA:
- Bankanın avantajlarını listele

KARŞILAŞTIRMA:
- 2-3 bankayı yan yana göster

---
Geçmiş:
{chat_history}

Bilgiler:
{context}

Soru: {question}

Cevap:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["chat_history", "context", "question"]
        )

        if api_key:
            print("LLM bağlanıyor (Groq)...")
            llm = ChatGroq(
                api_key=api_key,
                model="llama-3.1-8b-instant",
                temperature=0.0,
                max_tokens=512
            )

            print("RAG zinciri oluşturuluyor...")
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 10}  # Daha fazla chunk getir
                ),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": PROMPT},
                return_source_documents=False,
                verbose=False
            )
            self.retriever = None
            self.prompt = None
            print("[OK] Chatbot hazır!\n")
        else:
            print("UYARI: GROQ_API_KEY bulunamadı. Demo modunda çalışıyor.")
            self.chain = None
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            self.prompt = PROMPT
            print("[OK] Chatbot hazır! (DEMO modu)\n")

    def ask(self, question):
        """Kullanıcı sorusunu yanıtlar."""
        if self.chain:
            response = self.chain({"question": question})
            return response["answer"]

        docs = self.retriever.get_relevant_documents(question)
        context = "\n\n".join([d.page_content for d in docs])
        short_ctx = context[:1200]
        demo_answer = (
            "[DEMO CEVAP - GROQ API anahtarı yok]\n"
            f"{short_ctx}\n\n"
            f"Soru: {question}\n\n"
            "Not: Gerçek cevap için GROQ_API_KEY ekleyin."
        )
        return demo_answer


# Test
if __name__ == "__main__":
    print("Chatbot başlatılıyor...\n")
    chatbot = BankaChatbot()

    print("="*70)
    print("TEST SENARYOLARİ\n")
    print("="*70)

    # Test 1: En düşük konut kredisi
    print("\n[TEST 1] En düşük konut kredisi faizi")
    print("-" * 70)
    soru1 = "Hangi bankanın konut kredisi faiz oranı en düşük?"
    cevap1 = chatbot.ask(soru1)
    print(f"Soru: {soru1}")
    print(f"Cevap: {cevap1}")
    beklenen1 = "Ziraat" in cevap1 and "2.69" in cevap1
    print(f"Durum: {'BAŞARILI ✓' if beklenen1 else 'BAŞARISIZ ✗'}")

    # Test 2: Kampanya
    print("\n[TEST 2] Kampanya bilgisi")
    print("-" * 70)
    soru2 = "İş Bankası'nın kampanyaları neler?"
    cevap2 = chatbot.ask(soru2)
    print(f"Soru: {soru2}")
    print(f"Cevap: {cevap2}")
    beklenen2 = "750" in cevap2 or "bonus" in cevap2.lower()
    print(f"Durum: {'BAŞARILI ✓' if beklenen2 else 'BAŞARISIZ ✗'}")

    # Test 3: Taşıt kredisi
    print("\n[TEST 3] En düşük taşıt kredisi")
    print("-" * 70)
    soru3 = "Taşıt kredisi almak istiyorum, en uygun hangisi?"
    cevap3 = chatbot.ask(soru3)
    print(f"Soru: {soru3}")
    print(f"Cevap: {cevap3}")
    beklenen3 = "2.85" in cevap3 or "Ziraat" in cevap3
    print(f"Durum: {'BAŞARILI ✓' if beklenen3 else 'BAŞARISIZ ✗'}")

    # Test 4: İkinci en düşük
    print("\n[TEST 4] İkinci en düşük taşıt kredisi")
    print("-" * 70)
    soru4 = "Ziraat'ten sonra hangi banka uygun?"
    cevap4 = chatbot.ask(soru4)
    print(f"Soru: {soru4}")
    print(f"Cevap: {cevap4}")
    print(f"Durum: Kontrol edilmeli")

    # Test 5: Emekliler
    print("\n[TEST 5] Emekliler için avantajlı banka")
    print("-" * 70)
    soru5 = "Emekliler için hangi banka daha avantajlı?"
    cevap5 = chatbot.ask(soru5)
    print(f"Soru: {soru5}")
    print(f"Cevap: {cevap5}")
    beklenen5 = "Ziraat" in cevap5 and "350" in cevap5
    print(f"Durum: {'BAŞARILI ✓' if beklenen5 else 'BAŞARISIZ ✗'}")

    print("\n" + "="*70)
    print("TEST TAMAMLANDI")
    print("="*70)

