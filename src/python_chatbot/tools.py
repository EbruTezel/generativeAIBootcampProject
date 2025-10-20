"""Chatbot için yardımcı araçlar - Matematiksel karşılaştırmalar için"""

import re
from typing import List, Tuple


def find_min_interest_rate(text: str) -> Tuple[str, float]:
    """
    Metin içinden banka isimlerini ve konut kredisi faiz oranlarını çıkarır,
    en düşük faiz oranına sahip bankayı bulur.

    Args:
        text: Banka bilgilerini içeren metin

    Returns:
        (banka_adı, faiz_oranı) tuple'ı
    """
    # Banka-faiz eşleştirmelerini bul
    banks_data = []

    # Yaygın banka isimleri
    bank_names = [
        "Ziraat Bankası", "İş Bankası", "Garanti BBVA", "Garanti",
        "Yapı Kredi", "Akbank", "VakıfBank", "Halkbank",
        "DenizBank", "QNB Finansbank", "TEB", "İNG"
    ]

    # Her banka için faiz oranını bul
    for bank in bank_names:
        # Banka adından sonra "Konut Kredisi Faizi: %X.XX" pattern'ini ara
        pattern = rf"{bank}.*?Konut Kredisi Faizi:?\s*%?(\d+\.\d+)"
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

        if matches:
            rate = float(matches[0])
            banks_data.append((bank, rate))

    if not banks_data:
        return ("Bilgi bulunamadı", 0.0)

    # En düşük faiz oranını bul
    min_bank = min(banks_data, key=lambda x: x[1])
    return min_bank


def compare_rates(rate1: float, rate2: float) -> str:
    """
    İki faiz oranını karşılaştırır ve açıklama döndürür.

    Args:
        rate1: İlk faiz oranı
        rate2: İkinci faiz oranı

    Returns:
        Karşılaştırma açıklaması
    """
    if rate1 < rate2:
        return f"%{rate1} < %{rate2}, yani %{rate1} daha düşük (daha iyi)"
    elif rate1 > rate2:
        return f"%{rate1} > %{rate2}, yani %{rate1} daha yüksek (daha kötü)"
    else:
        return f"%{rate1} = %{rate2}, yani eşitler"


if __name__ == "__main__":
    # Test
    test_text = """
    Ziraat Bankası
    Konut Kredisi Faizi: %2.69
    
    Akbank
    Konut Kredisi Faizi: %2.75
    
    Garanti BBVA
    Konut Kredisi Faizi: %2.79
    """

    bank, rate = find_min_interest_rate(test_text)
    print(f"En düşük faiz: {bank} - %{rate}")
    print(compare_rates(2.69, 2.75))

