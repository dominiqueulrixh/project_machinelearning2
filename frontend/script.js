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

    const chatboxContent = document.getElementById("chatbox-content");
    chatboxContent.innerHTML += `<p><strong>Client:</strong> ${userInput}</p>`;
    chatboxContent.innerHTML += `<p><strong>Boby:</strong> ${data.answer}</p>`;
    document.getElementById("userInput").value = '';

    chatbox.scrollTop = chatbox.scrollHeight;
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
    const chatboxContent = document.getElementById("chatbox-content");
    chatboxContent.innerHTML = `<p><strong>Boby:</strong> Hello Client! I'm Boby, your witty lawyer, always ready to assist you with the Swiss Civil Code!
    Ask me anything you want to know – from "When do you come of age in Switzerland?" to any other curious question that's on your mind.
    So, go ahead, shoot your questions, and I'm ready to solve your legal puzzles.</p>`;
    document.getElementById("userInput").value = '';
    conversationId = null;  
    console.log("Cleared conversationId");  
}

window.onload = loadConversations;
