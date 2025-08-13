# Snapdragon X Elite vs Intel Core Ultra Performance Championship 🏆

A real-time performance demonstration system showcasing Snapdragon X Elite's superiority over Intel Core Ultra 7 processors through automated benchmarks and live monitoring.

## 🎯 Purpose
Designed for Qualcomm training sessions and sales presentations to demonstrate clear performance advantages in:
- AI/ML Performance (45 TOPS vs 11 TOPS)
- Battery Efficiency (2x better performance per watt)
- Thermal Management (Silent operation vs audible fan noise)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Two Windows laptops:
  - Samsung Galaxy Book4 Edge (Snapdragon X Elite)
  - Lenovo Yoga 7i (Intel Core Ultra 7)
- Local network (travel router recommended)

### Installation

1. **Clone the repository on both laptops and presenter device:**
```bash
git clone https://github.com/qualcomm-demo/snapdragon-battle-demo.git
cd snapdragon-battle-demo
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure network settings:**
Edit `config.json` with your device IPs:
```json
{
  "snapdragon_ip": "192.168.100.10",
  "intel_ip": "192.168.100.20",
  "server_ip": "192.168.100.5"
}
```

4. **Start the demo system:**

On the presenter device:
```bash
python server.py
```

On each laptop:
```bash
python agent.py
```

5. **Open the dashboard:**
Navigate to `http://192.168.100.5:5000` in your browser

## 🎮 Demo Scenarios

### 1. AI Performance Showdown (4 minutes)
- Simultaneous Stable Diffusion image generation
- Real-time progress visualization
- Expected: Snapdragon 3-4x faster

### 2. Battery Efficiency Race (3 minutes)
- Intensive workload with battery monitoring
- Live power consumption tracking
- Expected: 2-3% vs 5-7% drain

### 3. Thermal Performance Test (3 minutes)
- Stress test with temperature monitoring
- Fan noise visualization
- Expected: 15-20°C cooler operation

## 🎨 Dashboard Features

- **Live Performance Metrics**: Real-time CPU, GPU, battery, and thermal data
- **Victory Animations**: Celebratory effects when Snapdragon wins
- **Commentary Feed**: Automated witty observations
- **Audience Interaction**: Polls and predictions
- **Professional Mode**: Executive-friendly presentation option

## 📊 Expected Results

| Metric | Snapdragon X Elite | Intel Core Ultra 7 | Advantage |
|--------|-------------------|-------------------|-----------|
| AI Generation | 8-12 seconds | 25-35 seconds | 3-4x faster |
| Battery Drain | 2-3% | 5-7% | 2.5x more efficient |
| Temperature | 45-50°C | 70-85°C | 30°C cooler |
| Fan Noise | Silent | Audible | ∞ quieter |

## 🛠️ Troubleshooting

### Connection Issues
- Ensure all devices are on the same network
- Check Windows Firewall settings
- Verify IP addresses in config.json

### Performance Variations
- Close unnecessary applications
- Ensure both laptops are on AC power for consistent results
- Allow devices to cool between demos

## 📝 Notes

- Demo is designed for 10-minute presentations
- All measurements are software-based (no external hardware required)
- Results are legitimate performance comparisons
- Professional humor is intentional and audience-appropriate

## 🏁 Let the Championship Begin!

*"Where milliseconds matter and fans stay silent"™*

---
*Developed for Qualcomm training and sales enablement*
