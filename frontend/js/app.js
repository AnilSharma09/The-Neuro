const API_URL = "http://127.0.0.1:8000";

// --- Upload Logic ---
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const analyzeBtn = document.getElementById('analyze-btn');

if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        fileInput.files = e.dataTransfer.files;
        handleFileSelect();
    });

    analyzeBtn.addEventListener('click', uploadAndAnalyze);
}

function handleFileSelect() {
    const file = fileInput.files[0];
    if (file) {
        document.getElementById('filename').textContent = file.name;
        document.getElementById('file-info').style.display = 'block';
        analyzeBtn.style.display = 'block';
    }
}

async function uploadAndAnalyze() {
    const file = fileInput.files[0];
    if (!file) return;

    // Show loading
    document.getElementById('loader').style.display = 'block';
    document.getElementById('status-text').style.display = 'block';
    analyzeBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Save data to localStorage for Dashboard
        localStorage.setItem('eegAnalysis', JSON.stringify(data));
        
        // Redirect
        window.location.href = 'dashboard.html';

    } catch (error) {
        console.error("Analysis failed", error);
        alert("Analysis failed: " + error.message);
        document.getElementById('loader').style.display = 'none';
        document.getElementById('status-text').style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

// --- Dashboard Logic ---
function renderDashboard() {
    const dataStr = localStorage.getItem('eegAnalysis');
    if (!dataStr) {
        // alert("No analysis data found. Please upload a file.");
        // window.location.href = 'upload.html';
        return;
    }
    
    const data = JSON.parse(dataStr);
    const features = data.features; // {Delta: ..., Theta: ...}
    const prediction = data.prediction;
    const stats = data.signal_stats;

    // Update Text
    document.getElementById('prediction-result').textContent = prediction.disorder;
    document.getElementById('risk-level').textContent = `Risk Level: ${prediction.risk_level}`;
    document.getElementById('confidence-score').textContent = `${(prediction.details[prediction.disorder] || prediction.details['RandomForest'].confidence * 100).toFixed(1)}%`;
    
    if (document.getElementById('stat-mean')) {
        document.getElementById('stat-mean').textContent = stats.mean.toFixed(2) + " µV";
        document.getElementById('stat-std').textContent = stats.std.toFixed(2);
        document.getElementById('stat-max').textContent = stats.max.toFixed(2) + " µV";
    }

    // Chart 1: Waves (Bar)
    const ctxWaves = document.getElementById('wavesChart').getContext('2d');
    new Chart(ctxWaves, {
        type: 'bar',
        data: {
            labels: Object.keys(features),
            datasets: [{
                label: 'Relative Power',
                data: Object.values(features),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)', // Delta
                    'rgba(54, 162, 235, 0.6)', // Theta
                    'rgba(255, 206, 86, 0.6)', // Alpha
                    'rgba(75, 192, 192, 0.6)', // Beta
                    'rgba(153, 102, 255, 0.6)' // Gamma
                ],
                borderColor: 'rgba(255,255,255,0.8)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: 'white' } },
                x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: 'white' } }
            },
            plugins: { legend: { labels: { color: 'white' } } }
        }
    });

    // Chart 2: Probabilities (Pie/Doughnut)
    // Extract probs from prediction.details if available, else just mock or show risk
    // Assuming simple structure for now or extracting from details
    const probs = [];
    const labels = [];
    
    // Logic to show breakdown if available in details
    if (prediction.details) {
         // This is a bit complex as current mock returns one confidence per model.
         // Let's just visualize the features as a Radar chart instead for "Likelihood Breakdown" concept
         // Or simple placeholder. Let's do Radar of bands.
    }
    
    const ctxProbs = document.getElementById('probsChart').getContext('2d');
    new Chart(ctxProbs, {
        type: 'doughnut',
        data: {
            labels: ['Confidence', 'Uncertainty'],
            datasets: [{
                data: [prediction.details['RandomForest'].confidence * 100, 100 - (prediction.details['RandomForest'].confidence * 100)],
                backgroundColor: ['#00B4D8', 'rgba(255,255,255,0.1)'],
                borderWidth: 0
            }]
        },
        options: {
            plugins: { legend: { position: 'bottom', labels: { color: 'white' } } }
        }
    });
}


// --- Chatbot Logic ---
const chatHistory = document.getElementById('chat-history');
const chatInput = document.getElementById('chat-input');

async function sendMessage() {
    if (!chatInput) return;
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    appendMessage(message, 'user');
    chatInput.value = '';

    // Scroll
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        appendMessage(data.response, 'bot');
        
    } catch (error) {
        appendMessage("Error connecting to chatbot service.", 'bot');
    }
    
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    div.innerText = text;
    chatHistory.appendChild(div);
}
