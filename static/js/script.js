const chatToggle = document.getElementById('chatToggle');
const chatWindow = document.getElementById('chatWindow');
const closeChat = document.getElementById('closeChat');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const sendChat = document.getElementById('sendChat');
const recommendationGrid = document.getElementById('recommendationGrid');
const sportTags = document.querySelectorAll('.sport-tag');

const sportCatalog = {
    cricket: [
        { name: 'Cricket Bat Elite', price: '₹1899' },
        { name: 'Cricket Gloves Pro', price: '₹1399' },
        { name: 'Cricket Pads', price: '₹1299' }
    ],
    football: [
        { name: 'Pro Football Kit', price: '₹2499' },
        { name: 'Football Boots X9', price: '₹3299' },
        { name: 'Football', price: '₹1599' }
    ],
    tennis: [
        { name: 'Tennis Racket Ace', price: '₹4599' },
        { name: 'Tennis Balls', price: '₹799' },
        { name: 'Tennis Grip', price: '₹599' }
    ],
    badminton: [
        { name: 'Badminton Set Prime', price: '₹2199' },
        { name: 'Racket Cover', price: '₹499' },
        { name: 'Shuttlecock Pack', price: '₹699' }
    ],
    boxing: [
        { name: 'Boxing Gloves Titan', price: '₹2699' },
        { name: 'Boxing Head Guard', price: '₹2399' },
        { name: 'Jump Rope', price: '₹799' }
    ],
    gym: [
        { name: 'Power Gym Kit', price: '₹3499' },
        { name: 'Yoga Mat', price: '₹1499' },
        { name: 'Resistance Bands', price: '₹999' }
    ],
    swimming: [
        { name: 'Swim Pro Kit', price: '₹2999' },
        { name: 'Swimming Goggles', price: '₹899' },
        { name: 'Swim Cap', price: '₹499' }
    ]
};

function appendMessage(text, sender = 'bot') {
    const message = document.createElement('div');
    message.className = `message ${sender}`;
    message.textContent = text;
    chatBody.appendChild(message);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function renderRecommendationCards(sport) {
    const items = sportCatalog[sport] || sportCatalog.cricket;
    recommendationGrid.innerHTML = items.map(item => `
        <div class="recommendation-item">
            <h4>${item.name}</h4>
            <p>${item.price}</p>
            <p>Required gear for ${sport.toUpperCase()} training and matches.</p>
        </div>
    `).join('');
}

sportTags.forEach(button => {
    button.addEventListener('click', () => {
        sportTags.forEach(tag => tag.classList.remove('active'));
        button.classList.add('active');
        renderRecommendationCards(button.dataset.sport);
    });
});

renderRecommendationCards('cricket');

chatToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('open');
});

closeChat.addEventListener('click', () => {
    chatWindow.classList.remove('open');
});

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    chatInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        appendMessage(data.reply || 'Sorry, I could not answer that question.', 'bot');

        if (data.recommended && data.recommended.length) {
            const sport = data.recommended[0].sport;
            renderRecommendationCards(sport);
            sportTags.forEach(tag => {
                tag.classList.toggle('active', tag.dataset.sport === sport);
            });
        }
    } catch (error) {
        appendMessage('The chatbot is temporarily unavailable. Please try again later.', 'bot');
    }
}

sendChat.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('quickSportBtn').addEventListener('click', () => {
    chatWindow.classList.add('open');
    chatInput.focus();
    chatInput.placeholder = 'Try: football, cricket, tennis...';
});
