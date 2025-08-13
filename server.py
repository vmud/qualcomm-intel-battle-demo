#!/usr/bin/env python3
"""
Snapdragon vs Intel Performance Championship Server
Main coordination server for the demo system
"""

import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='dashboard/assets',
            template_folder='dashboard')
app.config['SECRET_KEY'] = 'snapdragon-championship-2025'
CORS(app)

# Initialize SocketIO with WebSocket transport
socketio = SocketIO(app, 
                    cors_allowed_origins="*",
                    async_mode='threading',
                    logger=True,
                    engineio_logger=False)

# Connected devices tracking
connected_devices = {
    'snapdragon': {'connected': False, 'last_seen': None, 'metrics': {}},
    'intel': {'connected': False, 'last_seen': None, 'metrics': {}}
}

# Demo state management
demo_state = {
    'active': False,
    'current_test': None,
    'start_time': None,
    'results': [],
    'commentary': []
}

# Victory messages (professional humor)
VICTORY_MESSAGES = {
    'ai_faster': [
        "Snapdragon completes another masterpiece while Intel contemplates the canvas",
        "45 TOPS vs 11 TOPS - The math speaks for itself",
        "Snapdragon: 'Should I generate another one while we wait?'",
        "AI acceleration: Where NPUs matter more than promises"
    ],
    'battery_efficient': [
        "Snapdragon sips power like fine wine, Intel gulps like it's happy hour",
        "All-day battery vs all-day anxiety",
        "Efficiency: Not just a buzzword for Snapdragon",
        "Power management: Silent victory"
    ],
    'thermal_cool': [
        "Snapdragon maintains zen-like calm while Intel reaches for ice packs",
        "The sound of silence vs the roar of desperation",
        "Laptop on lap: Comfortable vs Concerning",
        "4nm efficiency vs 10nm... enthusiasm"
    ]
}

# Loading messages for entertainment
LOADING_MESSAGES = [
    "Initializing quantum advantage...",
    "Calibrating superiority metrics...",
    "Detecting nearby jet engines... oh wait, that's just Intel's fan",
    "Loading AI capabilities... 45 TOPS located",
    "Engaging silent mode (Snapdragon exclusive feature)...",
    "Preparing thermal warnings for Intel...",
    "Optimizing battery anxiety algorithms...",
    "Summoning the power of 4nm architecture..."
]

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html', config=config)

@app.route('/assets/<path:path>')
def send_assets(path):
    """Serve static assets"""
    return send_from_directory('dashboard/assets', path)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('server_status', {
        'connected': True,
        'devices': connected_devices,
        'demo_state': demo_state,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('device_register')
def handle_device_register(data):
    """Register a device (Snapdragon or Intel laptop)"""
    device_type = data.get('device_type')
    if device_type in connected_devices:
        connected_devices[device_type]['connected'] = True
        connected_devices[device_type]['last_seen'] = datetime.now().isoformat()
        logger.info(f"{device_type} device registered")
        
        # Broadcast device status update
        socketio.emit('device_status', {
            'device': device_type,
            'status': 'connected',
            'timestamp': datetime.now().isoformat()
        })
        
        # Send welcome message
        emit('device_welcome', {
            'message': f"Welcome to the Championship, {config['devices'][device_type]['name']}!",
            'specs': config['devices'][device_type]['specs']
        })

@socketio.on('metrics_update')
def handle_metrics_update(data):
    """Receive metrics update from a device"""
    device_type = data.get('device_type')
    metrics = data.get('metrics')
    
    if device_type in connected_devices:
        connected_devices[device_type]['metrics'] = metrics
        connected_devices[device_type]['last_seen'] = datetime.now().isoformat()
        
        # Broadcast metrics to all clients
        socketio.emit('metrics_broadcast', {
            'device': device_type,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate commentary based on metrics
        commentary = generate_commentary(device_type, metrics)
        if commentary:
            add_commentary(commentary)

@socketio.on('start_demo')
def handle_start_demo(data):
    """Start a demo scenario"""
    scenario = data.get('scenario')
    logger.info(f"Starting demo: {scenario}")
    
    demo_state['active'] = True
    demo_state['current_test'] = scenario
    demo_state['start_time'] = time.time()
    
    # Send loading message for entertainment
    import random
    loading_msg = random.choice(LOADING_MESSAGES)
    
    socketio.emit('demo_started', {
        'scenario': scenario,
        'loading_message': loading_msg,
        'duration': config['demo_scenarios'][scenario]['duration'],
        'timestamp': datetime.now().isoformat()
    })
    
    # Send start command to devices
    socketio.emit('execute_test', {
        'scenario': scenario,
        'config': config['demo_scenarios'][scenario]
    })

@socketio.on('test_complete')
def handle_test_complete(data):
    """Handle test completion from a device"""
    device_type = data.get('device_type')
    result = data.get('result')
    
    logger.info(f"{device_type} completed test: {result}")
    
    # Store result
    demo_state['results'].append({
        'device': device_type,
        'result': result,
        'timestamp': datetime.now().isoformat()
    })
    
    # Check if both devices completed
    if len([r for r in demo_state['results'] 
            if r['timestamp'] > datetime.fromtimestamp(demo_state['start_time']).isoformat()]) >= 2:
        declare_winner()

@socketio.on('stop_demo')
def handle_stop_demo():
    """Stop the current demo"""
    logger.info("Stopping demo")
    demo_state['active'] = False
    demo_state['current_test'] = None
    
    socketio.emit('demo_stopped', {
        'timestamp': datetime.now().isoformat()
    })

def generate_commentary(device_type, metrics):
    """Generate witty commentary based on metrics"""
    commentary_lines = []
    
    # Temperature commentary
    if 'temperature' in metrics:
        temp = metrics['temperature']
        if device_type == 'intel' and temp > 75:
            commentary_lines.append(f"Intel reaching {temp}°C - Thermal throttling imminent")
        elif device_type == 'snapdragon' and temp < 50:
            commentary_lines.append(f"Snapdragon cruising at a cool {temp}°C")
    
    # Battery commentary
    if 'battery' in metrics:
        battery = metrics['battery']
        if device_type == 'intel' and battery['percent'] < 70:
            commentary_lines.append(f"Intel battery already at {battery['percent']}% - Range anxiety activated")
        elif device_type == 'snapdragon' and battery['percent'] > 90:
            commentary_lines.append(f"Snapdragon still at {battery['percent']}% - All-day confidence")
    
    # Fan commentary
    if 'fan_rpm' in metrics:
        rpm = metrics['fan_rpm']
        if device_type == 'intel' and rpm > 3000:
            commentary_lines.append(f"Intel fan at {rpm} RPM - Preparing for takeoff")
        elif device_type == 'snapdragon' and rpm == 0:
            commentary_lines.append("Snapdragon fan status: What fan?")
    
    return commentary_lines

def add_commentary(lines):
    """Add commentary lines to the feed"""
    for line in lines:
        entry = {
            'text': line,
            'timestamp': datetime.now().isoformat(),
            'type': 'auto'
        }
        demo_state['commentary'].append(entry)
        
        # Keep only last 20 commentary lines
        if len(demo_state['commentary']) > 20:
            demo_state['commentary'] = demo_state['commentary'][-20:]
        
        # Broadcast commentary update
        socketio.emit('commentary_update', entry)

def declare_winner():
    """Declare the winner of the current test"""
    test = demo_state['current_test']
    results = demo_state['results']
    
    # Determine winner based on test type
    winner = None
    message = ""
    
    if test == 'ai_showdown':
        # Fastest completion time wins
        snapdragon_time = next((r['result'].get('time') for r in results 
                               if r['device'] == 'snapdragon'), float('inf'))
        intel_time = next((r['result'].get('time') for r in results 
                          if r['device'] == 'intel'), float('inf'))
        
        if snapdragon_time < intel_time:
            winner = 'snapdragon'
            ratio = round(intel_time / snapdragon_time, 1)
            message = f"Snapdragon wins by {ratio}x! " + random.choice(VICTORY_MESSAGES['ai_faster'])
        else:
            winner = 'intel'
            message = "Intel wins! (Please verify test conditions)"
    
    # Broadcast winner
    socketio.emit('winner_declared', {
        'winner': winner,
        'message': message,
        'test': test,
        'timestamp': datetime.now().isoformat()
    })
    
    # Reset for next test
    demo_state['results'] = []

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

def periodic_health_check():
    """Periodic health check for connected devices"""
    while True:
        time.sleep(5)
        for device_type, device_info in connected_devices.items():
            if device_info['connected'] and device_info['last_seen']:
                last_seen = datetime.fromisoformat(device_info['last_seen'])
                if (datetime.now() - last_seen).seconds > 10:
                    device_info['connected'] = False
                    socketio.emit('device_status', {
                        'device': device_type,
                        'status': 'disconnected',
                        'timestamp': datetime.now().isoformat()
                    })

if __name__ == '__main__':
    # Start health check thread
    import threading
    health_thread = threading.Thread(target=periodic_health_check, daemon=True)
    health_thread.start()
    
    # Get server configuration
    server_ip = config['network']['server_ip']
    server_port = config['network']['server_port']
    
    logger.info(f"Starting Performance Championship Server on {server_ip}:{server_port}")
    logger.info("Dashboard will be available at http://{server_ip}:{server_port}")
    
    # Run the server
    socketio.run(app, 
                 host='0.0.0.0',  # Listen on all interfaces
                 port=server_port,
                 debug=True)
