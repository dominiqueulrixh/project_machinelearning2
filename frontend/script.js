let conversationId = null;

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    console.log("Sending message with conversationId:", conversationId);  // Debug-Ausgabe

    const payload = {
        user_id: 'user123',  // Hier kannst du eine dynamische Benutzer-ID setzen
        question: userInput,
        conversation_id: conversationId ? String(conversationId) : null  // Konvertiere conversationId in einen String, falls vorhanden
    };
    console.log("Payload:", JSON.stringify(payload));  // Debug-Ausgabe

    const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Failed to send message:", response.statusText, errorText);  // Debug-Ausgabe
        return;
    }

    const data = await response.json();
    if (conversationId === null) {
        conversationId = data.conversation_id;  // conversation_id wird nur beim ersten Mal gesetzt
    }
    console.log("Received conversationId:", conversationId);  // Debug-Ausgabe

    document.getElementById("chatbox-content").innerHTML += `<p><strong>Mandant:</strong> ${userInput}</p>`;
    document.getElementById("chatbox-content").innerHTML += `<p><strong>Anwalt:</strong> ${data.answer}</p>`;
    document.getElementById("userInput").value = '';
    document.getElementById("chatbox-content").scrollTop = document.getElementById("chatbox-content").scrollHeight;
}

async function loadConversations() {
    clearChat(); // Führe die Funktion clearChat aus, um sicherzustellen, dass ein neuer Chat gestartet wird
}

function clearChat() {
    document.getElementById("chatbox-content").innerHTML = `<p><strong>Anwalt:</strong> Hallo, ich bin dein persönlicher Anwalt und bin spezialisiert auf das Schweizerische Zivilgesetzbuch. Du kannst mich gerne alles darüber fragen.</p>`;  // Setzt den Begrüßungstext
    document.getElementById("userInput").value = '';  // Setzt das Eingabefeld zurück
    conversationId = null;  // Setzt die Konversations-ID zurück
    console.log("Cleared conversationId");  // Debug-Ausgabe
}

window.onload = loadConversations;
