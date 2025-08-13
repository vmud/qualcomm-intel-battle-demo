<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapdragon vs Intel - Live Demo Control Center</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: relative;
        }

        /* Header */
        .header {
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            color: white;
            position: relative;
            z-index: 10;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        .subtitle {
            font-size: 1.2em;
            color: #ffd700;
            margin-top: 10px;
        }

        /* Main Arena */
        .battle-arena {
            display: flex;
            flex: 1;
            padding: 20px;
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
        }

        /* Machine Panels */
        .machine-panel {
            flex: 1;
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            position: relative;
            transition: all 0.3s ease;
            overflow: hidden;
        }

        .machine-panel:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        }

        /* Snapdragon Panel Styling */
        .snapdragon-panel {
            background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
            border: 3px solid #00ff00;
        }

        .snapdragon-panel::before {
            content: '✓ SUPERIOR';
            position: absolute;
            top: 10px;
            right: 10px;
            background: #00ff00;
            color: #000;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 12px;
            animation: blink 2s infinite;
        }

        /* Intel Panel Styling */
        .intel-panel {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);
            border: 3px solid #ff4444;
        }

        .intel-panel.overheating::after {
            content: '🔥 THERMAL THROTTLING 🔥';
            position: absolute;
            top: 10px;
            right: 10px;
            background: red;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            animation: blink 0.5s infinite;
        }

        @keyframes blink {
            50% { opacity: 0.5; }
        }

        /* Machine Headers */
        .machine-header {
            text-align: center;
            margin-bottom: 20px;
            position: relative;
        }

        .machine-logo {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .snapdragon-panel .machine-logo {
            color: #004d00;
            text-shadow: 0 0 10px rgba(0,255,0,0.5);
        }

        .intel-panel .machine-logo {
            color: #0071c5;
            text-shadow: 0 0 10px rgba(255,0,0,0.3);
        }

        .machine-model {
            font-size: 1.2em;
            color: #333;
            margin: 5px 0;
        }

        .npu-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
        }

        .snapdragon-panel .npu-badge {
            background: #00ff00;
            color: #000;
        }

        .intel-panel .npu-badge {
            background: #ff9999;
            color: #000;
        }

        /* Status Display */
        .status-display {
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            font-family: 'Courier New', monospace;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 8px;
            background: rgba(255,255,255,0.7);
            border-radius: 5px;
            transition: all 0.3s;
        }

        .metric:hover {
            background: rgba(255,255,255,0.9);
            transform: translateX(5px);
        }

        .metric-label {
            font-weight: 600;
            color: #333;
        }

        .metric-value {
            font-weight: bold;
        }

        .snapdragon-panel .metric-value {
            color: #00aa00;
        }

        .intel-panel .metric-value {
            color: #ff4444;
        }

        /* Performance Bar */
        .performance-bar {
            width: 100%;
            height: 35px;
            background: #ddd;
            border-radius: 20px;
            overflow: hidden;
            margin: 15px 0;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }

        .performance-fill {
            height: 100%;
            transition: width 1s ease-out;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        .snapdragon-panel .performance-fill {
            background: linear-gradient(90deg, #00ff00, #00aa00);
        }

        .intel-panel .performance-fill {
            background: linear-gradient(90deg, #ff9999, #ff4444);
        }

        /* Demo Buttons */
        .demo-buttons {
            display: grid;
            gap: 12px;
            margin-top: 20px;
        }

        .demo-btn {
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
            color: white;
        }

        .demo-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }

        .demo-btn:active {
            transform: scale(0.95);
        }

        .demo-btn.running {
            animation: pulse 1s infinite;
        }

        .demo-btn.completed::after {
            content: '✓';
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
        }

        .wake-btn { background: linear-gradient(135deg, #667eea, #764ba2); }
        .thermal-btn { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .ai-btn { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .sd-btn { background: linear-gradient(135deg, #43e97b, #38f9d7); }
        .battery-btn { background: linear-gradient(135deg, #fa709a, #fee140); }

        /* Control Center */
        .control-center {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.9);
            padding: 20px;
            border-radius: 20px;
            display: flex;
            gap: 15px;
            z-index: 1000;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .master-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }

        .master-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 20px rgba(255,255,255,0.3);
        }

        .start-all {
            background: linear-gradient(135deg, #00ff00, #00aa00);
        }

        .stop-all {
            background: linear-gradient(135deg, #ff0000, #aa0000);
        }

        .mock-intel {
            background: linear-gradient(135deg, #ff6b6b, #ff3333);
        }

        /* Commentary Box */
        .commentary {
            position: fixed;
            top: 120px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.95);
            padding: 20px 40px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            display: none;
            z-index: 2000;
            max-width: 80%;
            text-align: center;
            animation: slideDown 0.5s;
        }

        @keyframes slideDown {
            from { 
                transform: translateX(-50%) translateY(-100px); 
                opacity: 0; 
            }
            to { 
                transform: translateX(-50%) translateY(0); 
                opacity: 1; 
            }
        }

        /* Connection Status */
        .connection-status {
            position: absolute;
            top: 10px;
            left: 10px;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
        }

        .status-connected {
            background: #00ff00;
            color: #000;
        }

        .status-disconnected {
            background: #ff0000;
            color: #fff;
        }

        /* Loading Spinner */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Emoji Rain */
        .emoji-rain {
            position: fixed;
            top: -50px;
            font-size: 2em;
            z-index: 1500;
            animation: fall 3s linear forwards;
        }

        @keyframes fall {
            to { 
                transform: translateY(calc(100vh + 100px)); 
            }
        }

        /* Network Error Banner */
        .error-banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff0000;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            display: none;
            z-index: 3000;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .battle-arena {
                flex-direction: column;
            }
            
            .control-center {
                flex-direction: column;
                bottom: 10px;
                width: 90%;
            }
        }
    </style>
</head>
<body>
    <!-- Error Banner -->
    <div class="error-banner" id="errorBanner">
        Network connection lost. Please check connections.
    </div>

    <!-- Header -->
    <div class="header">
        <h1>⚡ SNAPDRAGON vs INTEL BATTLE ARENA ⚡</h1>
        <p class="subtitle">Live Performance Comparison Dashboard</p>
    </div>

    <!-- Battle Arena -->
    <div class="battle-arena">
        <!-- Snapdragon Panel -->
        <div class="machine-panel snapdragon-panel" id="snapdragon-panel">
            <div class="connection-status status-disconnected" id="snap-connection">
                CONNECTING...
            </div>
            
            <div class="machine-header">
                <div class="machine-logo">SNAPDRAGON</div>
                <div class="machine-model">Galaxy Book4 Edge</div>
                <div class="npu-badge">45 TOPS NPU 🚀</div>
            </div>

            <div class="status-display">
                <div class="metric">
                    <span class="metric-label">CPU Usage:</span>
                    <span class="metric-value" id="snap-cpu">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">NPU Active:</span>
                    <span class="metric-value" id="snap-npu">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Temperature:</span>
                    <span class="metric-value" id="snap-temp">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Battery:</span>
                    <span class="metric-value" id="snap-battery">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Power Draw:</span>
                    <span class="metric-value" id="snap-power">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Fan Speed:</span>
                    <span class="metric-value" id="snap-fan">Silent 🤫</span>
                </div>
            </div>

            <div class="performance-bar">
                <div class="performance-fill" id="snap-perf" style="width: 0%">
                    <span id="snap-perf-text">-- Efficiency</span>
                </div>
            </div>

            <div class="demo-buttons">
                <button class="demo-btn wake-btn" onclick="runDemo('wake', 'snapdragon', this)">
                    ⏰ Instant Wake Test
                </button>
                <button class="demo-btn thermal-btn" onclick="runDemo('thermal', 'snapdragon', this)">
                    ❄️ Thermal Test (Cool)
                </button>
                <button class="demo-btn ai-btn" onclick="runDemo('ai', 'snapdragon', this)">
                    🧠 AI Workload (NPU)
                </button>
                <button class="demo-btn sd-btn" onclick="runDemo('sd', 'snapdragon', this)">
                    🎨 Stable Diffusion
                </button>
                <button class="demo-btn battery-btn" onclick="runDemo('battery', 'snapdragon', this)">
                    🔋 Battery Efficiency
                </button>
            </div>
        </div>

        <!-- Intel Panel -->
        <div class="machine-panel intel-panel" id="intel-panel">
            <div class="connection-status status-disconnected" id="intel-connection">
                CONNECTING...
            </div>
            
            <div class="machine-header">
                <div class="machine-logo">INTEL</div>
                <div class="machine-model">Lenovo Yoga 7i</div>
                <div class="npu-badge">11 TOPS NPU 🐌</div>
            </div>

            <div class="status-display">
                <div class="metric">
                    <span class="metric-label">CPU Usage:</span>
                    <span class="metric-value" id="intel-cpu">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">NPU Active:</span>
                    <span class="metric-value" id="intel-npu">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Temperature:</span>
                    <span class="metric-value" id="intel-temp">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Battery:</span>
                    <span class="metric-value" id="intel-battery">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Power Draw:</span>
                    <span class="metric-value" id="intel-power">--</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Fan Speed:</span>
                    <span class="metric-value" id="intel-fan">Spinning 💨</span>
                </div>
            </div>

            <div class="performance-bar">
                <div class="performance-fill" id="intel-perf" style="width: 0%">
                    <span id="intel-perf-text">-- Efficiency</span>
                </div>
            </div>

            <div class="demo-buttons">
                <button class="demo-btn wake-btn" onclick="runDemo('wake', 'intel', this)">
                    😴 Slow Wake Test
                </button>
                <button class="demo-btn thermal-btn" onclick="runDemo('thermal', 'intel', this)">
                    🔥 Thermal Test (Hot)
                </button>
                <button class="demo-btn ai-btn" onclick="runDemo('ai', 'intel', this)">
                    🐢 AI Workload (CPU)
                </button>
                <button class="demo-btn sd-btn" onclick="runDemo('sd', 'intel', this)">
                    ⏳ Slow Diffusion
                </button>
                <button class="demo-btn battery-btn" onclick="runDemo('battery', 'intel', this)">
                    💀 Battery Drain
                </button>
            </div>
        </div>
    </div>

    <!-- Control Center -->
    <div class="control-center">
        <button class="master-btn start-all" onclick="startBattle()">
            🚀 START BATTLE
        </button>
        <button class="master-btn stop-all" onclick="stopAll()">
            🛑 STOP ALL
        </button>
        <button class="master-btn mock-intel" onclick="mockIntel()">
            😂 MOCK INTEL
        </button>
    </div>

    <!-- Commentary Box -->
    <div class="commentary" id="commentary"></div>

    <script>
        // Configuration
        const config = {
            snapdragonIP: '192.168.1.102',
            intelIP: '192.168.1.101',
            wsPort: 8080,
            reconnectDelay: 3000,
            updateInterval: 2000
        };

        // WebSocket connections
        let snapdragonWS = null;
        let intelWS = null;
        let reconnectTimers = {};

        // Connection status
        let connectionStatus = {
            snapdragon: false,
            intel: false
        };

        // Initialize connections
        function initConnections() {
            connectToMachine('snapdragon', config.snapdragonIP);
            connectToMachine('intel', config.intelIP);
        }

        // Connect to a machine
        function connectToMachine(machine, ip) {
            console.log(`Connecting to ${machine} at ${ip}:${config.wsPort}...`);
            
            const ws = new WebSocket(`ws://${ip}:${config.wsPort}`);
            
            ws.onopen = () => {
                console.log(`Connected to ${machine}`);
                connectionStatus[machine] = true;
                updateConnectionStatus(machine, true);
                
                // Clear reconnect timer
                if (reconnectTimers[machine]) {
                    clearTimeout(reconnectTimers[machine]);
                }
            };
            
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    updateMetrics(machine, data);
                } catch (error) {
                    console.error(`Error parsing data from ${machine}:`, error);
                }
            };
            
            ws.onerror = (error) => {
                console.error(`WebSocket error for ${machine}:`, error);
                updateConnectionStatus(machine, false);
            };
            
            ws.onclose = () => {
                console.log(`Disconnected from ${machine}`);
                connectionStatus[machine] = false;
                updateConnectionStatus(machine, false);
                
                // Attempt reconnection
                reconnectTimers[machine] = setTimeout(() => {
                    connectToMachine(machine, ip);
                }, config.reconnectDelay);
            };
            
            // Store WebSocket reference
            if (machine === 'snapdragon') {
                snapdragonWS = ws;
            } else {
                intelWS = ws;
            }
        }

        // Update connection status display
        function updateConnectionStatus(machine, connected) {
            const element = document.getElementById(`${machine === 'snapdragon' ? 'snap' : 'intel'}-connection`);
            if (connected) {
                element.textContent = 'CONNECTED';
                element.className = 'connection-status status-connected';
            } else {
                element.textContent = 'DISCONNECTED';
                element.className = 'connection-status status-disconnected';
            }
            
            // Show error banner if both disconnected
            if (!connectionStatus.snapdragon && !connectionStatus.intel) {
                document.getElementById('errorBanner').style.display = 'block';
            } else {
                document.getElementById('errorBanner').style.display = 'none';
            }
        }

        // Update metrics display
        function updateMetrics(machine, data) {
            const prefix = machine === 'snapdragon' ? 'snap' : 'intel';
            
            // Update CPU
            const cpuElement = document.getElementById(`${prefix}-cpu`);
            if (data.cpu) {
                cpuElement.textContent = `${data.cpu.usage || 0}%`;
            }
            
            // Update NPU
            const npuElement = document.getElementById(`${prefix}-npu`);
            if (data.npu) {
                const npuText = data.npu.usage !== undefined ? 
                    `${data.npu.usage}% / ${data.npu.maxTOPS || 0} TOPS` : 
                    'Inactive';
                npuElement.textContent = npuText;
            }
            
            // Update Temperature
            const tempElement = document.getElementById(`${prefix}-temp`);
            if (data.temperature) {
                const temp = data.temperature.current || 0;
                tempElement.textContent = `${temp}°C`;
                
                // Add overheating class to Intel if hot
                if (machine === 'intel' && temp > 80) {
                    document.getElementById('intel-panel').classList.add('overheating');
                } else {
                    document.getElementById('intel-panel').classList.remove('overheating');
                }
            }
            
            // Update Battery
            const batteryElement = document.getElementById(`${prefix}-battery`);
            if (data.battery) {
                batteryElement.textContent = `${data.battery.level || 0}%`;
            }
            
            // Update Power Draw
            const powerElement = document.getElementById(`${prefix}-power`);
            if (data.battery) {
                powerElement.textContent = `${data.battery.powerDraw || 0}W`;
            }
            
            // Update Fan
            const fanElement = document.getElementById(`${prefix}-fan`);
            if (data.fan) {
                fanElement.textContent = data.fan.noiseLevel || data.fan.speed || 'Unknown';
            }
            
            // Update Performance Score
            const perfBar = document.getElementById(`${prefix}-perf`);
            const perfText = document.getElementById(`${prefix}-perf-text`);
            if (data.performance) {
                const score = data.performance.score || 0;
                perfBar.style.width = `${score}%`;
                perfText.textContent = `${score}% Efficiency`;
            }
        }

        // Run demo on specific machine
        function runDemo(demoType, machine, button) {
            const ws = machine === 'snapdragon' ? snapdragonWS : intelWS;
            
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                showCommentary(`❌ ${machine} is not connected!`);
                return;
            }
            
            // Send demo command
            ws.send(JSON.stringify({
                command: 'run_demo',
                demo: demoType
            }));
            
            // Update button state
            button.classList.add('running');
            
            // Show commentary
            const comments = {
                wake: {
                    snapdragon: "⚡ Snapdragon waking instantly...",
                    intel: "😴 Intel slowly waking up..."
                },
                thermal: {
                    snapdragon: "❄️ Snapdragon staying cool under pressure!",
                    intel: "🔥 Intel heating up rapidly!"
                },
                ai: {
                    snapdragon: "🧠 45 TOPS NPU crushing AI workload!",
                    intel: "🐌 11 TOPS struggling with AI..."
                },
                sd: {
                    snapdragon: "🎨 Snapdragon generating images at lightning speed!",
                    intel: "⏳ Intel crawling through image generation..."
                },
                battery: {
                    snapdragon: "🔋 Snapdragon sipping power efficiently!",
                    intel: "💀 Intel draining battery rapidly!"
                }
            };
            
            showCommentary(comments[demoType][machine]);
            
            // Simulate completion
            setTimeout(() => {
                button.classList.remove('running');
                button.classList.add('completed');
                
                if (machine === 'snapdragon') {
                    createEmojiRain('✅');
                } else {
                    createEmojiRain('🐢');
                }
            }, machine === 'snapdragon' ? 3000 : 10000);
        }

        // Start all demos (battle mode)
        function startBattle() {
            showCommentary("🎯 LET THE BATTLE BEGIN!");
            
            const demos = ['wake', 'thermal', 'ai', 'sd', 'battery'];
            let index = 0;
            
            function runNext() {
                if (index < demos.length) {
                    const demo = demos[index];
                    
                    // Run on both machines
                    const snapBtn = document.querySelector(`.snapdragon-panel .${demo}-btn`);
                    const intelBtn = document.querySelector(`.intel-panel .${demo}-btn`);
                    
                    if (snapBtn) runDemo(demo, 'snapdragon', snapBtn);
                    if (intelBtn) runDemo(demo, 'intel', intelBtn);
                    
                    index++;
                    setTimeout(runNext, 12000); // 12 seconds between demos
                } else {
                    // Show winner
                    setTimeout(() => {
                        showCommentary("🏆 SNAPDRAGON WINS DECISIVELY! 🏆");
                        createEmojiRain('🎉');
                        createEmojiRain('🏆');
                        createEmojiRain('💚');
                    }, 3000);
                }
            }
            
            runNext();
        }

        // Stop all demos
        function stopAll() {
            if (snapdragonWS && snapdragonWS.readyState === WebSocket.OPEN) {
                snapdragonWS.send(JSON.stringify({ command: 'stop_all' }));
            }
            
            if (intelWS && intelWS.readyState === WebSocket.OPEN) {
                intelWS.send(JSON.stringify({ command: 'stop_all' }));
            }
            
            showCommentary("All demos stopped. Intel needed a break anyway... 😅");
            
            // Reset all buttons
            document.querySelectorAll('.demo-btn').forEach(btn => {
                btn.classList.remove('running', 'completed');
            });
        }

        // Mock Intel function
        const intelJokes = [
            "Intel: 'Wait, you have HOW many TOPS?' 😱",
            "Intel's NPU called in sick today 🤒",
            "Intel: 'Is it hot in here or is it just me?' 🔥",
            "Breaking: Intel fan achieves liftoff 🚁",
            "Intel: 'I'm not slow, I'm energy... consuming' ⚡",
            "Intel asking Snapdragon for cooling tips 🧊",
            "Intel: '11 TOPS is plenty!' *nervous sweating* 💦",
            "Plot twist: Intel's battery gauge is just a countdown timer ⏰",
            "Intel: 'My thermal throttling is a feature!' 🌡️",
            "Intel considering career change to space heater 🔥"
        ];

        function mockIntel() {
            const joke = intelJokes[Math.floor(Math.random() * intelJokes.length)];
            showCommentary(joke);
            
            // Make Intel panel shake
            const intelPanel = document.getElementById('intel-panel');
            intelPanel.style.animation = 'shake 0.5s';
            setTimeout(() => {
                intelPanel.style.animation = '';
            }, 500);
            
            // Add some fire emojis
            createEmojiRain('🔥');
        }

        // Show commentary
        function showCommentary(text) {
            const commentary = document.getElementById('commentary');
            commentary.textContent = text;
            commentary.style.display = 'block';
            
            setTimeout(() => {
                commentary.style.display = 'none';
            }, 5000);
        }

        // Create emoji rain effect
        function createEmojiRain(emoji) {
            for (let i = 0; i < 10; i++) {
                setTimeout(() => {
                    const emojiEl = document.createElement('div');
                    emojiEl.className = 'emoji-rain';
                    emojiEl.textContent = emoji;
                    emojiEl.style.left = Math.random() * window.innerWidth + 'px';
                    document.body.appendChild(emojiEl);
                    
                    setTimeout(() => {
                        emojiEl.remove();
                    }, 3000);
                }, i * 200);
            }
        }

        // Add shake animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
        `;
        document.head.appendChild(style);

        // Fallback for local testing (simulated data)
        function simulateMetrics() {
            // Only simulate if not connected
            if (!connectionStatus.snapdragon) {
                updateMetrics('snapdragon', {
                    cpu: { usage: 15 + Math.random() * 10 },
                    npu: { usage: 60 + Math.random() * 20, maxTOPS: 45 },
                    temperature: { current: 42 + Math.random() * 5 },
                    battery: { level: 95 + Math.random() * 3, powerDraw: 10 + Math.random() * 3 },
                    fan: { noiseLevel: 'Silent' },
                    performance: { score: 90 + Math.random() * 10 }
                });
            }
            
            if (!connectionStatus.intel) {
                updateMetrics('intel', {
                    cpu: { usage: 45 + Math.random() * 30 },
                    npu: { usage: 5 + Math.random() * 6, maxTOPS: 11 },
                    temperature: { current: 70 + Math.random() * 15 },
                    battery: { level: 65 + Math.random() * 10, powerDraw: 28 + Math.random() * 10 },
                    fan: { noiseLevel: 'Loud' },
                    performance: { score: 35 + Math.random() * 15 }
                });
            }
        }

        // Initialize on page load
        window.addEventListener('load', () => {
            console.log('Dashboard initializing...');
            
            // Try to connect to machines
            initConnections();
            
            // Start simulation for testing (remove in production)
            setInterval(simulateMetrics, 2000);
            
            // Welcome message
            setTimeout(() => {
                showCommentary("Welcome to the AI Performance Battle Arena! 🎮");
            }, 1000);
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'b' || e.key === 'B') {
                startBattle();
            } else if (e.key === 's' || e.key === 'S') {
                stopAll();
            } else if (e.key === 'm' || e.key === 'M') {
                mockIntel();
            }
        });
    </script>
</body>
</html>