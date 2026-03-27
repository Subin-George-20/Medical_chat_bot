const chat = document.getElementById("chat");

// Temporary memory (no localStorage)
let chatHistory = [];

// Add message
function addMessage(text, className) {
    const wrapper = document.createElement("div");
    wrapper.className = "message " + className;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;

    wrapper.appendChild(bubble);
    chat.appendChild(wrapper);

    chat.scrollTop = chat.scrollHeight;

    chatHistory.push({ role: className, text: text });

    return bubble;
}

// Send message
async function send() {
    const input = document.getElementById("question");
    const question = input.value.trim();

    if (!question) return;

    input.value = "";

    addMessage(question, "user");
    const botBubble = addMessage("", "bot");

    try {
        const response = await fetch("http://127.0.0.1:8000/query-stream", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question,
                history: chatHistory.slice(-10).map(msg => ({
                    role: msg.role === "user" ? "user" : "assistant",
                    content: msg.text
                }))
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let fullResponse = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            fullResponse += chunk;

            botBubble.innerText += chunk;
            chat.scrollTop = chat.scrollHeight;
        }

        chatHistory[chatHistory.length - 1].text = fullResponse;

    } catch (error) {
        botBubble.innerText = "❌ Error: Unable to fetch response";
        console.error(error);
    }
}

// Enter key support
document.getElementById("question")
.addEventListener("keypress", function(e) {
    if (e.key === "Enter") send();
});