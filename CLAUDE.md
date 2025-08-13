# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a demonstration system designed to showcase Snapdragon X Elite processor superiority over Intel Core Ultra 7 through automated, real-time performance comparisons. The system is specifically designed for Qualcomm training sessions and sales presentations.

## Demo System Architecture

### Core Components
- **Snapdragon Device**: Samsung Galaxy Book4 Edge (Snapdragon X Elite 3.4GHz)
- **Intel Device**: Lenovo Yoga 7i (Intel Core Ultra 7 155U)
- **Presenter Dashboard**: Real-time WebSocket-based control and monitoring system
- **Local Network**: Travel router creating isolated demo environment (192.168.100.x)

### Demo Protocol Structure
The system executes a 10-minute demonstration across three phases:
1. **AI Performance Showdown** (4 minutes) - Stable Diffusion image generation race
2. **Battery Drain Race** (3 minutes) - Power efficiency comparison under load
3. **Thermal Performance** (3 minutes) - Temperature and fan noise monitoring

## Development Commands

Since this repository is in planning phase, actual implementation commands will depend on the technology stack chosen:

### Expected Tech Stack
- **Backend**: Node.js with WebSocket server for device coordination
- **Monitoring**: Python scripts with psutil for system metrics
- **AI Workloads**: Stable Diffusion (optimized builds for both ARM64 and x86)
- **Dashboard**: Web-based interface with real-time visualizations

### Development Setup (When Implemented)
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Start demo system
npm run demo-server      # WebSocket coordination server
python metrics-collector.py  # System monitoring
python ai-benchmark.py   # AI workload execution
```

## Key Design Principles

### Network Architecture
- All devices communicate via local network (192.168.100.x)
- No internet dependency during demonstrations
- WebSocket-based real-time synchronization
- Software-based monitoring (no external hardware meters)

### Visual Presentation
- Branded UI with Intel Blue (#0071c5) vs Snapdragon Red (#e31837)
- Competition-style dashboard with real-time metrics
- Side-by-side laptop positioning for audience visibility
- Automated victory celebrations and progress indicators

### Performance Monitoring
- Battery percentage tracking via system APIs
- CPU/GPU temperature monitoring through software
- NPU utilization comparison (45 TOPS vs 11 TOPS)
- Fan speed detection and thermal throttling alerts

## Demo Constraints & Requirements

### Hardware Limitations
- No external monitors (laptops positioned side-by-side)
- No USB power meters or thermal cameras
- Software-based metrics collection only
- Optional IR thermometer for validation

### Timing Requirements
- Total demo duration: 10 minutes maximum
- Real-time visual feedback essential
- Immediate and obvious performance differences
- Professional presentation quality for executive audiences

## Expected Outcomes

The system should demonstrate clear Snapdragon advantages:
- **AI Performance**: 3-4x faster Stable Diffusion generation
- **Battery Efficiency**: 2-3% vs 5-7% drain during stress tests
- **Thermal Management**: 15-20°C lower operating temperatures
- **User Experience**: Silent operation vs audible Intel fan activation

## Implementation Notes

When developing this system, focus on:
- Legitimate performance comparisons that highlight genuine advantages
- Reliable automation to minimize presenter intervention
- Engaging visual elements that maintain professional credibility
- Robust error handling for live demonstration environments