// API Configuration
const API_BASE_URL = "http://localhost:8000/api";
let chatHistory = JSON.parse(localStorage.getItem("chatHistory") || "[]");
let isGenerating = false;

// DOM Elements
const chatContainer = document.getElementById("chatContainer");
const promptInput = document.getElementById("promptInput");
const styleSelect = document.getElementById("styleSelect");
const sendBtn = document.querySelector(".send-btn");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    renderHistory();
});

function renderHistory() {
    const recentDiv = document.getElementById("recentHistory");
    const allDiv = document.getElementById("allHistory");

    if (!recentDiv || !allDiv) return;

    recentDiv.innerHTML = "";
    allDiv.innerHTML = "";

    chatHistory.slice(0, 5).forEach((item, index) => {
        recentDiv.appendChild(createHistoryItem(item, index));
    });

    chatHistory.slice(5).forEach((item, index) => {
        allDiv.appendChild(createHistoryItem(item, index + 5));
    });
}

function createHistoryItem(text, index) {
    const div = document.createElement("div");
    div.className = "history-item";
    const shortText = text.length > 30 ? text.substring(0, 30) + "..." : text;
    div.innerHTML = `
        <div class="history-text" onclick="loadHistoryPrompt('${escapeHtml(text).replace(/'/g, "\\'")}')">${escapeHtml(shortText)}</div>
        <div class="delete-btn" onclick="deleteHistoryItem(${index})">🗑</div>
    `;
    return div;
}

function addToHistory(prompt) {
    if (!chatHistory.includes(prompt)) {
        chatHistory.unshift(prompt);
        if (chatHistory.length > 50) chatHistory.pop();
        localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
        renderHistory();
    }
}

function deleteHistoryItem(index) {
    chatHistory.splice(index, 1);
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    renderHistory();
}

function loadHistoryPrompt(prompt) {
    promptInput.value = prompt;
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function searchHistory(query) {
    const items = document.querySelectorAll(".history-item");
    items.forEach((item) => {
        const text = item
            .querySelector(".history-text")
            .textContent.toLowerCase();
        item.style.display = text.includes(query.toLowerCase())
            ? "flex"
            : "none";
    });
}

function startNewChat() {
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">🎨</div>
            <h2>Welcome to ViralGen AI</h2>
            <p>Describe your advertisement idea and let AI create stunning visuals & copy</p>
            <div class="example-prompts">
                <div class="example-prompt" onclick="setExample('Luxury watch for professionals, gold and black design')">⌚ Luxury watch for professionals</div>
                <div class="example-prompt" onclick="setExample('Eco-friendly water bottle, active lifestyle, nature')">💧 Eco-friendly water bottle</div>
                <div class="example-prompt" onclick="setExample('Modern sneakers with LED lights, futuristic design')">👟 Modern sneakers with LED</div>
                <div class="example-prompt" onclick="setExample('Coffee shop promotion, cozy atmosphere, morning vibe')">☕ Coffee shop promotion</div>
            </div>
        </div>
    `;
    promptInput.value = "";
    showToast("New conversation started");
}

function setExample(text) {
    promptInput.value = text;
    sendPrompt();
}

function handleKeyPress(event) {
    if (event.key === "Enter" && !isGenerating) {
        sendPrompt();
    }
}

function addUserMessage(prompt) {
    // Remove welcome message if exists
    const welcomeMsg = document.querySelector(".welcome-message");
    if (welcomeMsg) welcomeMsg.remove();

    const messageDiv = document.createElement("div");
    messageDiv.className = "message";
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="user-message">${escapeHtml(prompt)}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.id = "typingIndicator";
    typingDiv.className = "message";
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) indicator.remove();
}

function addBotResponse(
    imageUrl,
    marketingCopy,
    enhancedPrompt,
    originalPrompt,
) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message";
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="image-card">
                <img src="${imageUrl}" class="generated-image" alt="Generated advertisement" onclick="openImageModal('${imageUrl}')">
                <div class="image-actions">
                    <button class="download-btn" onclick="downloadImage('${imageUrl}')">📥 Download Image</button>
                    <button class="copy-btn" onclick="copyToClipboard('${escapeHtml(marketingCopy).replace(/'/g, "\\'")}')">📋 Copy Text</button>
                </div>
            </div>
            <div class="copy-card">
                <h4>📝 AI Generated Copy</h4>
                <div class="copy-content">${escapeHtml(marketingCopy).replace(/\n/g, "<br>")}</div>
            </div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function downloadImage(url) {
    const link = document.createElement("a");
    link.href = url;
    link.download = `viralgen_ad_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("Image downloaded!");
}

function copyToClipboard(text) {
    navigator.clipboard
        .writeText(text)
        .then(() => {
            showToast("Marketing copy copied to clipboard!");
        })
        .catch(() => {
            showToast("Failed to copy text");
        });
}

function openImageModal(url) {
    
    const modal = document.createElement("div");
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        cursor: pointer;
    `;
    modal.innerHTML = `<img src="${url}" style="max-width: 90%; max-height: 90%; border-radius: 8px;">`;
    modal.onclick = () => modal.remove();
    document.body.appendChild(modal);
}

function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

async function sendPrompt() {
    const prompt = promptInput.value.trim();

    if (!prompt || isGenerating) return;

    const style = styleSelect.value;

    
    addUserMessage(prompt);
    promptInput.value = "";
    addTypingIndicator();
    isGenerating = true;
    sendBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt: prompt, style: style }),
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.success && data.image_url) {
            addBotResponse(
                data.image_url,
                data.marketing_copy,
                data.enhanced_prompt,
                prompt,
            );
            addToHistory(prompt);
        } else {
            addErrorMessage(
                data.error || "Failed to generate content. Please try again.",
            );
        }
    } catch (error) {
        removeTypingIndicator();
        addErrorMessage(
            "Network error. Please check if the backend server is running.",
        );
        console.error("Error:", error);
    } finally {
        isGenerating = false;
        sendBtn.disabled = false;
    }
}

function addErrorMessage(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "message";
    errorDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div style="background: rgba(239, 68, 68, 0.9); padding: 12px 20px; border-radius: 18px; color: white;">
                ⚠️ ${escapeHtml(message)}
            </div>
        </div>
    `;
    chatContainer.appendChild(errorDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
