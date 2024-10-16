document.getElementById('send-btn').addEventListener('click', async function () {
    // Get the user input
    const userInput = document.getElementById('user-input').value;
    document.getElementById('user-input').value = "";

    // If input is not empty
    if (userInput.trim() !== "") {
        // Create a new message div for the user
        const newUserMessage = document.createElement('div');
        newUserMessage.classList.add('message', 'user-message');

        // Create a paragraph element and set its text to the user input
        const userMessageText = document.createElement('p');
        userMessageText.textContent = userInput;

        // Append the paragraph to the user message div
        newUserMessage.appendChild(userMessageText);

        // Append the user message div to the chat box
        const chatBox = document.getElementById('chat-box');
        chatBox.appendChild(newUserMessage);

        // Disable the input box and send button while the bot is typing
        document.getElementById('user-input').disabled = true;
        document.getElementById('send-btn').disabled = true;

        // Create a new message div for the bot
        const newBotMessage = document.createElement('div');
        newBotMessage.classList.add('message', 'bot-message');

        // Create a paragraph element for the bot's response
        const botMessageText = document.createElement('p');
        newBotMessage.appendChild(botMessageText);

        // Append the bot message div to the chat box
        chatBox.appendChild(newBotMessage);

        try {
            const response = await fetch('/chat/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: userInput })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let done = false;

            while (!done) {
                const { value, done: streamDone } = await reader.read();
                done = streamDone;
                if (value) {
                    let chunk = decoder.decode(value, { stream: true });
                    // Define the pattern to match a number followed by a period
                    let pattern = /(\d+)\./g;

                    // Replace the number followed by a period with a newline, the same number, and a period
        
                    chunk = chunk.replace(pattern, '\n$1.');

                    // Replace newlines with <br> tags to format the output correctly in HTML
                    botMessageText.innerHTML += chunk.replace(/\n/g, '<br>');

                }
            }
            // const data = await response.json();
            // botMessageText.textContent = data.response;
        }
        catch (error) {
            console.error('Error:', error);
            botMessageText.innerHTML = '<p>An error occurred while processing your request.</p>';
        }

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
        
        document.getElementById('user-input').disabled = false;
        document.getElementById('send-btn').disabled = false;
        chunk = botMessageText.innerHTML
        chunk = chunk.replace(/([a-zA-Z\s\d\-\(\)]+:)/g, '<strong>$1</strong>');

        // Replace newlines with <br> tags to format the output correctly in HTML
        botMessageText.innerHTML = chunk;
        // Clear the input field
    }
});


document.getElementById('user-input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default form submission (if in a form)
        document.getElementById('send-btn').click(); // Trigger the send button click
    }
});


// Function to clear all messages and add a default bot message
function clearConversations() {
    const chatBox = document.getElementById('chat-box');

    // Clear all content inside chat-box
    chatBox.innerHTML = '';

    // Add a default bot message
    const defaultMessage = document.createElement('div');
    defaultMessage.className = 'message bot-message';
    defaultMessage.innerHTML = '<p>Hello! How can I help you today?</p>';

    chatBox.appendChild(defaultMessage);
}

// Add event listener to the "Clear Conversations" button
document.addEventListener('DOMContentLoaded', () => {
    const clearButton = document.querySelector('.sidebar-footer button');
    clearButton.addEventListener('click', clearConversations);
});
