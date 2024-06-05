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

    document.getElementById("chatbox").innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    document.getElementById("chatbox").in