/**
 * Main Application JavaScript for Performance Championship Dashboard
 */

// Global variables
let socket = null;
let connectedDevices = {
    snapdragon: false,
    intel: false
};
let currentTest = null;
let professionalMode = false;
let performanceChart = null;

// Loading messages for entertainment
const LOADING_MESSAGES = [
    "Initializing quantum advantage...",
    "Calibrating superiority metrics...",
    "Detecting nearby jet engines... oh wait, that's just Intel's fan",
    "Loading AI capabilities... 45 TOPS located",
    "Engaging silent mode (Snapdragon exclusive feature)...",
    "Preparing thermal warnings for Intel...",
    "Optimizing battery anxiety algorithms...",
    "Summoning the power of 4nm architecture..."
];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Performance Championship 2025 Initializing...');
    
    // Initialize loading screen
    initializeLoadingScreen();
    
    // Initialize Socket.IO connection
    initializeSocket();
    
    // Initialize UI event handlers
    initializeUIHandlers();
    
    // Initialize performance chart
    initializeChart();
    
    // Start loading sequence
    setTimeout(() => {
        hideLoadingScreen();
    }, 3000);
});

// Initialize loading screen
function initializeLoadingScreen() {
    const loadingMessage = document.getElementById('loadingMessage');
    let messageIndex = 0;
    
    // Rotate loading messages
    setInterval(() => {
        if (document.getElementById('loadingScreen').style.display !== 'none') {
            loadingMessage.textContent = LOADING_MESSAGES[messageIndex];
            messageIndex = (messageIndex + 1) % LOADING_MESSAGES.length;
        }
    }, 2000);
}

// Hide loading screen and show main dashboard
function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loadingScreen');
    const mainDashboard = document.getElementById('mainDashboard');
    
    loadingScreen.style.opacity = '0';
    setTimeout(() => {
        loadingScreen.style.display = 'none';
        mainDashboard.style.display = 'block';
        mainDashboard.style.opacity = '0';
        
        setTimeout(() => {
            mainDashboard.style.opacity = '1';
        }, 100);
    }, 500);
}

// Initialize Socket.IO connection
function initializeSocket() {
    // Connect to server
    socket = io('http://localhost:5000', {
        transports: ['websocket', 'polling']
    });
    
    // Connection event handlers
    socket.on('connect', () => {
        console.log('✅ Connected to Championship Server');
        addCommentary('SYSTEM', 'Connected to Championship Server');
    });
    
    socket.on('disconnect', () => {
        console.log('❌ Disconnected from Championship Server');
        addCommentary('SYSTEM', 'Disconnected from Championship Server');
        updateDeviceStatus('snapdragon', false);
        updateDeviceStatus('intel', false);
    });
    
    // Device status updates
    socket.on('device_status', (data) => {
        console.log('Device status update:', data);
        updateDeviceStatus(data.device, data.status === 'connected');
    });
    
    // Metrics updates
    socket.on('metrics_broadcast', (data) => {
        updateDeviceMetrics(data.device, data.metrics);
    });
    
    // Demo events
    socket.on('demo_started', (data) => {
        console.log('Demo started:', data);
        currentTest = data.scenario;
        addCommentary('DEMO', `Starting ${data.scenario} test - ${data.loading_message}`);
        disableScenarioButtons(true);
    });
    
    socket.on('demo_stopped', (data) => {
        console.log('Demo stopped');
        currentTest = null;
        disableScenarioButtons(false);
    });
    
    // Test progress updates
    socket.on('test_progress', (data) => {
        console.log('Test progress:', data);
        if (data.progress % 25 === 0) {
            addCommentary(data.device_type.toUpperCase(), 
                `Progress: ${data.progress}% (Step ${data.step}/${data.total_steps})`);
        }
    });
    
    // Commentary updates
    socket.on('commentary_update', (data) => {
        addCommentary(data.type || 'AUTO', data.text);
    });
    
    // Winner declaration
    socket.on('winner_declared', (data) => {
        console.log('Winner declared:', data);
        showVictoryModal(data.winner, data.message);
        disableScenarioButtons(false);
    });
}

// Initialize UI event handlers
function initializeUIHandlers() {
    // Professional mode toggle
    document.getElementById('btnProfessionalMode').addEventListener('click', () => {
        professionalMode = !professionalMode;
        document.body.classList.toggle('professional-mode', professionalMode);
        
        const btn = document.getElementById('btnProfessionalMode');
        if (professionalMode) {
            btn.innerHTML = '<i class="fas fa-party-horn"></i> Fun Mode';
            addCommentary('SYSTEM', 'Professional mode activated - Humor circuits disabled');
        } else {
            btn.innerHTML = '<i class="fas fa-briefcase"></i> Professional Mode';
            addCommentary('SYSTEM', 'Fun mode activated - Sarcasm levels restored');
        }
    });
    
    // Scenario buttons
    document.querySelectorAll('.btn-scenario').forEach(btn => {
        btn.addEventListener('click', function() {
            const scenario = this.dataset.scenario;
            startDemo(scenario);
        });
    });
}

// Update device connection status
function updateDeviceStatus(device, connected) {
    connectedDevices[device] = connected;
    
    const statusElement = document.getElementById(`${device}Status`);
    if (statusElement) {
        const icon = statusElement.querySelector('i');
        const text = statusElement.querySelector('.status-text');
        
        if (connected) {
            icon.className = 'fas fa-circle text-success';
            text.textContent = device === 'snapdragon' ? 'Ready to Dominate' : 'Warming Up';
        } else {
            icon.className = 'fas fa-circle text-danger';
            text.textContent = 'Disconnected';
        }
    }
    
    // Update device card animation
    const card = document.querySelector(`.${device}-card`);
    if (card) {
        card.classList.toggle('active', connected);
    }
}

// Update device metrics
function updateDeviceMetrics(device, metrics) {
    // CPU
    if (metrics.cpu) {
        const cpuElement = document.getElementById(`${device}Cpu`);
        if (cpuElement) {
            cpuElement.textContent = `${Math.round(metrics.cpu.percent)}%`;
            cpuElement.classList.add('metric-update');
            setTimeout(() => cpuElement.classList.remove('metric-update'), 500);
        }
    }
    
    // Battery
    if (metrics.battery) {
        const batteryElement = document.getElementById(`${device}Battery`);
        if (batteryElement) {
            batteryElement.textContent = `${Math.round(metrics.battery.percent)}%`;
            
            // Update battery icon based on level
            const batteryIcon = batteryElement.parentElement.querySelector('.metric-icon i');
            if (batteryIcon) {
                const percent = metrics.battery.percent;
                if (percent > 75) {
                    batteryIcon.className = 'fas fa-battery-full';
                } else if (percent > 50) {
                    batteryIcon.className = 'fas fa-battery-three-quarters';
                } else if (percent > 25) {
                    batteryIcon.className = 'fas fa-battery-half';
                } else if (percent > 10) {
                    batteryIcon.className = 'fas fa-battery-quarter';
                } else {
                    batteryIcon.className = 'fas fa-battery-empty battery-draining';
                }
            }
        }
    }
    
    // Temperature
    if (metrics.temperature !== undefined) {
        const tempElement = document.getElementById(`${device}Temp`);
        if (tempElement) {
            const temp = Math.round(metrics.temperature);
            tempElement.textContent = `${temp}°C`;
            
            // Add heat warning if temperature is high
            if (temp > 70) {
                tempElement.classList.add('heat-warning');
            } else {
                tempElement.classList.remove('heat-warning');
            }
        }
    }
    
    // Fan speed
    if (metrics.fan_rpm !== undefined) {
        const fanElement = document.getElementById(`${device}Fan`);
        if (fanElement) {
            const rpm = metrics.fan_rpm;
            
            if (rpm === 0) {
                fanElement.textContent = 'Silent';
                fanElement.parentElement.querySelector('.metric-icon i').className = 'fas fa-fan';
            } else {
                fanElement.textContent = `${rpm} RPM`;
                fanElement.parentElement.querySelector('.metric-icon i').className = 'fas fa-fan fa-spin';
                
                // Adjust spin speed based on RPM
                const icon = fanElement.parentElement.querySelector('.metric-icon i');
                if (rpm > 3000) {
                    icon.style.animationDuration = '0.5s';
                } else if (rpm > 2000) {
                    icon.style.animationDuration = '1s';
                } else {
                    icon.style.animationDuration = '2s';
                }
            }
        }
    }
    
    // Update chart
    if (performanceChart) {
        updateChart(device, metrics);
    }
}

// Add commentary entry
function addCommentary(type, text) {
    const feed = document.getElementById('commentaryFeed');
    
    const entry = document.createElement('div');
    entry.className = 'commentary-entry commentary-new';
    
    const time = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    
    entry.innerHTML = `
        <span class="commentary-time">${type}</span>
        <span class="commentary-text">${text}</span>
    `;
    
    feed.appendChild(entry);
    
    // Auto-scroll to bottom
    feed.scrollTop = feed.scrollHeight;
    
    // Remove animation class after animation completes
    setTimeout(() => {
        entry.classList.remove('commentary-new');
    }, 500);
    
    // Limit to 50 entries
    while (feed.children.length > 50) {
        feed.removeChild(feed.firstChild);
    }
}

// Start demo scenario
function startDemo(scenario) {
    if (!connectedDevices.snapdragon || !connectedDevices.intel) {
        alert('Both devices must be connected to start a demo!');
        return;
    }
    
    console.log('Starting demo:', scenario);
    socket.emit('start_demo', { scenario: scenario });
    
    // Add dramatic commentary
    let message = '';
    switch(scenario) {
        case 'ai_showdown':
            message = 'AI Performance Showdown initiated! 45 TOPS vs 11 TOPS - The math is clear, but let\'s watch anyway...';
            break;
        case 'battery_race':
            message = 'Battery Efficiency Race started! Place your bets on who reaches for the charger first...';
            break;
        case 'thermal_test':
            message = 'Thermal Performance Test engaged! One stays cool, one becomes a space heater...';
            break;
    }
    addCommentary('ARENA', message);
}

// Disable/enable scenario buttons
function disableScenarioButtons(disabled) {
    document.querySelectorAll('.btn-scenario').forEach(btn => {
        btn.disabled = disabled;
        if (disabled) {
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        } else {
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        }
    });
}

// Show victory modal
function showVictoryModal(winner, message) {
    const modal = new bootstrap.Modal(document.getElementById('victoryModal'));
    
    document.getElementById('victoryDevice').textContent = 
        winner === 'snapdragon' ? 'Snapdragon X Elite' : 'Intel Core Ultra 7';
    
    document.getElementById('victoryMessage').textContent = message;
    
    // Trigger confetti if Snapdragon wins
    if (winner === 'snapdragon' && typeof confetti !== 'undefined') {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#e31837', '#ffd700', '#ffffff']
        });
    }
    
    modal.show();
}

// Initialize performance chart
function initializeChart() {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;
    
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Snapdragon CPU',
                    data: [],
                    borderColor: '#e31837',
                    backgroundColor: 'rgba(227, 24, 55, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Intel CPU',
                    data: [],
                    borderColor: '#0071c5',
                    backgroundColor: 'rgba(0, 113, 197, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#b4b9c4'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#b4b9c4'
                    },
                    grid: {
                        color: '#2a3142'
                    }
                },
                x: {
                    ticks: {
                        color: '#b4b9c4'
                    },
                    grid: {
                        color: '#2a3142'
                    }
                }
            }
        }
    });
}

// Update chart with new data
function updateChart(device, metrics) {
    if (!performanceChart || !metrics.cpu) return;
    
    const datasetIndex = device === 'snapdragon' ? 0 : 1;
    const dataset = performanceChart.data.datasets[datasetIndex];
    
    // Add timestamp if needed
    if (performanceChart.data.labels.length === 0 || 
        performanceChart.data.labels.length < dataset.data.length + 1) {
        const time = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        });
        performanceChart.data.labels.push(time);
    }
    
    // Add data point
    dataset.data.push(metrics.cpu.percent);
    
    // Keep only last 20 points
    if (dataset.data.length > 20) {
        dataset.data.shift();
        if (performanceChart.data.labels.length > 20) {
            performanceChart.data.labels.shift();
        }
    }
    
    performanceChart.update('none'); // Update without animation for smooth real-time updates
}

// Export for debugging
window.championshipDebug = {
    socket,
    connectedDevices,
    currentTest,
    professionalMode
};
