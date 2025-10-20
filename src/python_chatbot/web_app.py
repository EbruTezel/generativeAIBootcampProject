from flask import Flask, render_template, request, jsonify
from .chatbot import BankaChatbot

app = Flask(__name__)

# Bot'u import sırasında başlatma — bunun yerine lazy init kullanacağız
_bot = None
_bot_init_error = None


def get_bot():
    """İlk çağrıda `BankaChatbot` örneğini oluşturur. Hata oluşursa `_bot_init_error` kaydedilir.

    Returns:
        (bot_instance_or_None, error_message_or_None)
    """
    global _bot, _bot_init_error
    if _bot is None and _bot_init_error is None:
        try:
            print("RAG Chatbot başlatılıyor (lazy init)")
            _bot = BankaChatbot()
            print("[OK] Chatbot hazır! Tarayıcınızda http://localhost:5001 adresini açın\n")
        except Exception as e:
            _bot_init_error = str(e)
            print("Chatbot başlatılamadı:", _bot_init_error)
    return _bot, _bot_init_error


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({'response': 'Lütfen bir mesaj yazın'})

    print(f"[?] Kullanıcı sorusu: {user_message}")

    bot, err = get_bot()
    if err:
        # Anlaşılır bir hata mesajı dön
        error_msg = (
            "Chatbot başlatılamadı: " + err + "\n"
            "Lütfen GROQ_API_KEY, bağımlılıklar ve data klasörünü kontrol edin.\n"
            "Eğer sadece önizleme yapmak istiyorsanız, chatbot demo modunda da çalışacaktır (GROQ yoksa demo cevap döner)."
        )
        print(error_msg)
        return jsonify({'response': error_msg})

    try:
        # RAG chatbot'tan cevap al
        bot_response = bot.ask(user_message)
        print(f"[OK] Bot cevabı: {str(bot_response)[:100]}...")
        return jsonify({'response': bot_response})
    except Exception as e:
        error_msg = f"Hata: {str(e)}"
        print(error_msg)
        return jsonify({'response': error_msg})


@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Konuşma geçmişini temizler"""
    bot, err = get_bot()
    if err:
        return jsonify({'success': False, 'message': 'Chatbot başlatılamadı'})

    try:
        # Belleği temizle
        if hasattr(bot, 'memory') and bot.memory:
            bot.memory.clear()
            print("[OK] Konuşma geçmişi temizlendi")
            return jsonify({'success': True, 'message': 'Konuşma geçmişi temizlendi'})
        else:
            return jsonify({'success': False, 'message': 'Bellek bulunamadı'})
    except Exception as e:
        error_msg = f"Bellek temizlenirken hata: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'message': error_msg})


def run_server(debug=False):
    # Debug mode kapalı, otomatik yeniden başlatma yok
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

