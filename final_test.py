#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/ebrutezel/Desktop/projects/generativeAIBootcampProject')

print("Chatbot başlatılıyor...\n")
from src.python_chatbot.chatbot import BankaChatbot

chatbot = BankaChatbot()

print("\n" + "="*70)
print("KRİTİK TEST: Hangi bankanın konut kredisi faiz oranı en düşük?")
print("="*70)

soru = "Hangi bankanın konut kredisi faiz oranı en düşük?"
print(f"\n👤 Soru: {soru}")
cevap = chatbot.ask(soru)
print(f"\n🤖 Cevap: {cevap}")

print("\n" + "="*70)
print("SONUÇ ANALİZİ")
print("="*70)

if "Ziraat" in cevap and "2.69" in cevap:
    print("\n✅ BAŞARILI! Doğru cevap verdi:")
    print("   Ziraat Bankası - %2.69 (EN DÜŞÜK)")
    print("\n🎉 SORUN ÇÖZÜLDÜ!")
elif "Akbank" in cevap:
    print("\n❌ BAŞARISIZ! Hala yanlış cevap veriyor:")
    print("   Akbank - %2.75 (YANLIŞ! En düşük DEĞİL)")
    print("\n   Doğru cevap: Ziraat Bankası - %2.69")
    print("\n⚠️  LLM matematik konusunda zorluk yaşıyor.")
    print("   Alternatif çözümler:")
    print("   1. Daha güçlü bir model kullan (GPT-4, Claude)")
    print("   2. Few-shot prompting ekle")
    print("   3. ReAct ajanı ile araç kullanımı ekle")
else:
    print("\n⚠️  BELİRSİZ CEVAP")
    print(f"   Aldığımız cevap: {cevap[:200]}")

