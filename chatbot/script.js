document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', function() {
        sendMessage();
    });

    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        } else if (event.key === 'Enter' && event.shiftKey) {
            // Allow the default behavior which adds a new line
        }
    });

    userInput.addEventListener('input', function() {
        // Automatically adjust the height of the textarea
        userInput.style.height = "auto";
        userInput.style.height = userInput.scrollHeight + "px";
    });

    function sendMessage() {
        const userText = userInput.value.trim();
        if (userText !== "") {
            addMessageToChat("You", userText, "user");
            getShampooSenseResponse(userText);
            userInput.value = "";
            userInput.style.height = "auto"; // Reset height to auto
        }
    }

    function addMessageToChat(sender, message, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${marked.parse(message)}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }

    async function getShampooSenseResponse(userText) {
        const apiUrl = "http://127.0.0.1:8060/generate"; // URL of FastAPI server

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: userText
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const shampooSenseResponse = data.response;
            addMessageToChat("Shampoo Sense", shampooSenseResponse, "shampoo-sense");
        } catch (error) {
            console.error('Error:', error);
            addMessageToChat("Shampoo Sense", "Sorry, there was an error processing your request.", "shampoo-sense");
        }
    }
});
