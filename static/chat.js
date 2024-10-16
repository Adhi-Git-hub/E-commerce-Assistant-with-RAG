async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === "") return;

    const chatLog = document.getElementById('chat-log');
    chatLog.innerHTML += `<div class="user-message">You: ${userInput}</div>`;

    document.getElementById('userInput').value = '';  // Clear input field

    // Send query to Flask backend
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
    });

    const data = await response.json();
    chatLog.innerHTML += `<div class="bot-message">Bot: ${data.response}</div>`;
    chatLog.scrollTop = chatLog.scrollHeight;  // Scroll to the bottom
}
