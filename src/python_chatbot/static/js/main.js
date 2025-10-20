const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function addMessage(text, isUser) {
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user' : 'bot'}`;
    div.innerHTML = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingMessage() {
    const div = document.createElement('div');
    div.className = 'message bot loading';
    div.innerHTML = 'Düşünüyor...';
    div.id = 'loading-message';
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoadingMessage() {
    const loadingMsg = document.getElementById('loading-message');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Kullanıcı mesajını göster
    addMessage(message, true);
    userInput.value = '';

    // Buton ve input'u devre dışı bırak
    sendBtn.disabled = true;
    userInput.disabled = true;

    // Yükleniyor mesajı göster
    addLoadingMessage();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Yükleniyor mesajını kaldır
        removeLoadingMessage();

        // Bot cevabını göster
        addMessage(data.response, false);

    } catch (error) {
        removeLoadingMessage();
        addMessage('Hata: Sunucuya bağlanılamadı. Lütfen tekrar deneyin.', false);
        console.error('Fetch error:', error);
    } finally {
        // Buton ve input'u tekrar aktif et
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

async function resetConversation() {
    if (!confirm('Konuşma geçmişi silinecek. Emin misiniz?')) {
        return;
    }

    resetBtn.disabled = true;

    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (data.success) {
            // Chat kutusunu temizle
            chatBox.innerHTML = '';

            // Hoş geldin mesajını tekrar ekle
            addMessage(`Merhaba!
Banka kampanyaları hakkında size nasıl yardımcı olabilirim?
Örnek sorular:
• Hangi bankada kredi faizi en düşük?
• İş Bankası'nın kampanyaları neler?
• Hesap açarken hangi bankada hediye var?`, false);

            console.log('[OK] Konuşma sıfırlandı');
        } else {
            alert('Konuşma sıfırlanamadı: ' + data.message);
        }
    } catch (error) {
        alert('Hata: Sunucuya bağlanılamadı.');
        console.error('Reset error:', error);
    } finally {
        resetBtn.disabled = false;
    }
}

sendBtn.addEventListener('click', sendMessage);
resetBtn.addEventListener('click', resetConversation);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Sayfa yüklendiğinde input'a focus yap ve hoş geldin mesajını ekle
window.addEventListener('load', () => {
    // Eğer chat kutusu boşsa hoş geldin mesajını ekle
    if (chatBox.children.length === 0) {
        addMessage(`Merhaba!
Banka kampanyaları hakkında size nasıl yardımcı olabilirim?
Örnek sorular:
• Hangi bankada kredi faizi en düşük?
• İş Bankası'nın kampanyaları neler?
• Hesap açarken hangi bankada hediye var?`, false);
    }
    userInput.focus();
});

