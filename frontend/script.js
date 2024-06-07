let conversationId = null;

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    console.log("Sending message with conversationId:", conversationId); 

    const payload = {
        user_id: 'client',
        question: userInput,
        conversation_id: conversationId ? String(conversationId) : null 
    };

    const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Failed to send message:", response.statusText, errorText); 
        return;
    }

    const data = await response.json();
    if (conversationId === null) {
        conversationId = data.conversation_id; 
    }

    document.getElementById("chatbox-content").innerHTML += `<p><strong>Mandant:</strong> ${userInput}</p>`;
    document.getElementById("chatbox-content").innerHTML += `<p><strong>Boby:</strong> ${data.answer}</p>`;
    document.getElementById("userInput").value = '';
    document.getElementById("chatbox-content").scrollTop = document.getElementById("chatbox-content").scrollHeight;
}

document.addEventListener("DOMContentLoaded", function() {
    var input = document.getElementById("userInput");
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Verhindert das Standardverhalten (falls erforderlich)
            sendMessage();
        }
    });
});

async function loadConversations() {
    clearChat();
}

function clearChat() {
    document.getElementById("chatbox-content").innerHTML = `<p><strong>Boby:</strong> Hallo, ich bin dein persönlicher Anwalt und bin spezialisiert auf das Schweizerische Zivilgesetzbuch. Du kannst mich gerne alles darüber fragen.</p>`;  // Setzt den Begrüßungstext
    document.getElementById("userInput").value = '';
    conversationId = null;  
    console.log("Cleared conversationId");  
}

window.onload = loadConversations;
