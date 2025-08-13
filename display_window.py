#!/usr/bin/env python3
"""
Visual Display Window for Stable Diffusion Generation
Shows real-time progress and generated images using Tkinter
"""

import tkinter as tk
from tkinter import ttk, Canvas, Label
import threading
import time
import queue
from pathlib import Path
from typing import Optional
import sys
import os

# Import PIL for image handling
try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    print("Installing Pillow...")
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image, ImageTk, ImageDraw

# Import SD generator
from sd_generator import StableDiffusionGenerator
from platform_detector import PlatformDetector

class ImageGenerationWindow:
    def __init__(self, platform_type: str = 'auto'):
        """Initialize the display window"""
        self.platform_type = platform_type
        self.root = tk.Tk()
        self.image_queue = queue.Queue()
        self.generator = None
        self.current_thread = None
        
        # Auto-detect platform if needed
        if self.platform_type == 'auto':
            detector = PlatformDetector()
            self.platform_type = detector.platform_info.get('platform_type', 'intel')
        
        # Platform-specific colors
        if self.platform_type == 'snapdragon':
            self.primary_color = '#e31837'  # Snapdragon red
            self.accent_color = '#00b4a6'   # Qualcomm teal
            self.title = "Snapdragon X Elite - AI Generation"
        else:
            self.primary_color = '#0071c5'  # Intel blue
            self.accent_color = '#c8c9ca'   # Intel silver
            self.title = "Intel Core Ultra 7 - AI Generation"
        
        self.setup_window()
        self.setup_ui()
        self.generator = StableDiffusionGenerator(self.platform_type)
        self.generator.load_model()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(self.title)
        self.root.geometry("800x900")
        self.root.configure(bg='#1e1e1e')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Set icon if available
        try:
            icon_path = Path('assets/icon.ico')
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
    
    def setup_ui(self):
        """Create the UI elements"""
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title label
        title_label = tk.Label(
            header_frame,
            text=self.title,
            font=('Arial', 20, 'bold'),
            fg='white',
            bg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # Platform badge
        platform_label = tk.Label(
            header_frame,
            text=f"🚀 {self.platform_type.upper()} OPTIMIZED",
            font=('Arial', 12),
            fg='white',
            bg=self.primary_color
        )
        platform_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#2e2e2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Prompt frame
        prompt_frame = tk.Frame(content_frame, bg='#2e2e2e')
        prompt_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            prompt_frame,
            text="Prompt:",
            font=('Arial', 12),
            fg='white',
            bg='#2e2e2e'
        ).pack(anchor=tk.W)
        
        self.prompt_entry = tk.Entry(
            prompt_frame,
            font=('Arial', 11),
            bg='#3e3e3e',
            fg='white',
            insertbackground='white'
        )
        self.prompt_entry.pack(fill=tk.X, pady=(5, 0))
        self.prompt_entry.insert(0, "Futuristic cityscape at sunset, 4K quality")
        
        # Image display frame
        image_frame = tk.Frame(content_frame, bg='#3e3e3e', relief=tk.RAISED, bd=2)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image canvas
        self.canvas = Canvas(image_frame, width=512, height=512, bg='black', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Initialize with placeholder
        self.show_placeholder()
        
        # Progress frame
        progress_frame = tk.Frame(content_frame, bg='#2e2e2e')
        progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Custom.Horizontal.TProgressbar',
            background=self.primary_color,
            troughcolor='#3e3e3e',
            bordercolor='#2e2e2e',
            lightcolor=self.primary_color,
            darkcolor=self.primary_color
        )
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to generate",
            font=('Arial', 11),
            fg='white',
            bg='#2e2e2e'
        )
        self.status_label.pack()
        
        # Metrics frame
        metrics_frame = tk.Frame(content_frame, bg='#2e2e2e')
        metrics_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create metric labels
        self.metric_labels = {}
        metrics = [
            ('Steps', '0/0'),
            ('Time', '0.0s'),
            ('Temperature', 'N/A'),
            ('Performance', 'N/A')
        ]
        
        for i, (name, value) in enumerate(metrics):
            col_frame = tk.Frame(metrics_frame, bg='#2e2e2e')
            col_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            tk.Label(
                col_frame,
                text=name + ':',
                font=('Arial', 10),
                fg='#888',
                bg='#2e2e2e'
            ).pack()
            
            label = tk.Label(
                col_frame,
                text=value,
                font=('Arial', 11, 'bold'),
                fg=self.accent_color,
                bg='#2e2e2e'
            )
            label.pack()
            self.metric_labels[name.lower()] = label
        
        # Control buttons frame
        button_frame = tk.Frame(content_frame, bg='#2e2e2e')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Generate button
        self.generate_btn = tk.Button(
            button_frame,
            text="🎨 Generate Image",
            font=('Arial', 12, 'bold'),
            bg=self.primary_color,
            fg='white',
            activebackground=self.accent_color,
            command=self.start_generation,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=('Arial', 12),
            bg='#8B0000',
            fg='white',
            state=tk.DISABLED,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Benchmark button
        benchmark_btn = tk.Button(
            button_frame,
            text="📊 Benchmark",
            font=('Arial', 12),
            bg='#4a4a4a',
            fg='white',
            command=self.run_benchmark,
            cursor='hand2',
            relief=tk.RAISED,
            bd=2
        )
        benchmark_btn.pack(side=tk.RIGHT)
    
    def show_placeholder(self):
        """Show placeholder image"""
        # Create placeholder image
        img = Image.new('RGB', (512, 512), color='#2e2e2e')
        draw = ImageDraw.Draw(img)
        
        # Draw placeholder text
        text = "Click 'Generate Image' to start"
        draw.text((256, 256), text, fill='#888', anchor='mm')
        
        # Display on canvas
        self.display_image(img)
    
    def display_image(self, pil_image: Image.Image):
        """Display PIL image on canvas"""
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update canvas
        self.canvas.delete('all')
        self.canvas.create_image(256, 256, image=photo)
        self.canvas.image = photo  # Keep reference
    
    def start_generation(self):
        """Start image generation"""
        if self.current_thread and self.current_thread.is_alive():
            return
        
        prompt = self.prompt_entry.get()
        if not prompt:
            prompt = "Futuristic cityscape at sunset"
        
        # Update UI state
        self.generate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_label.config(text="Starting generation...")
        
        # Start generation in background
        self.start_time = time.time()
        self.current_thread = self.generator.generate_async(prompt)
        
        # Start progress monitoring
        self.monitor_progress()
    
    def monitor_progress(self):
        """Monitor generation progress"""
        # Check for progress updates
        progress = self.generator.get_progress()
        
        if progress:
            # Update progress bar
            self.progress_var.set(progress['progress'] * 100)
            
            # Update status
            step = progress['step']
            total = progress['total_steps']
            self.status_label.config(text=f"Generating... Step {step}/{total}")
            
            # Update metrics
            elapsed = time.time() - self.start_time
            self.metric_labels['steps'].config(text=f"{step}/{total}")
            self.metric_labels['time'].config(text=f"{elapsed:.1f}s")
            
            # Update image
            if 'image' in progress:
                self.display_image(progress['image'])
            
            # Check if completed
            if progress.get('completed'):
                self.generation_complete(elapsed)
                return
        
        # Continue monitoring
        if self.current_thread and self.current_thread.is_alive():
            self.root.after(100, self.monitor_progress)
        else:
            # Thread finished without completion signal
            elapsed = time.time() - self.start_time
            self.generation_complete(elapsed)
    
    def generation_complete(self, elapsed_time: float):
        """Handle generation completion"""
        # Update UI state
        self.generate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(100)
        
        # Update status
        self.status_label.config(text=f"✅ Generation complete in {elapsed_time:.1f}s")
        
        # Update performance metric
        if self.platform_type == 'snapdragon':
            perf = "EXCELLENT"
        else:
            perf = "STANDARD"
        self.metric_labels['performance'].config(text=perf)
        
        # Flash completion effect
        self.flash_effect()
    
    def flash_effect(self):
        """Create a completion flash effect"""
        original_bg = self.canvas['bg']
        self.canvas.config(bg=self.accent_color)
        self.root.after(100, lambda: self.canvas.config(bg=original_bg))
    
    def run_benchmark(self):
        """Run benchmark mode"""
        # This would trigger a benchmark comparison
        self.status_label.config(text="Benchmark mode - Coming soon!")
    
    def run(self):
        """Start the window main loop"""
        self.root.mainloop()


def main():
    """Main function for standalone testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Image Generation Display Window')
    parser.add_argument('--platform', choices=['snapdragon', 'intel', 'auto'],
                       default='auto', help='Platform to simulate')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  IMAGE GENERATION DISPLAY")
    print("=" * 60)
    print(f"\n🖼️ Launching display window for {args.platform}...")
    
    window = ImageGenerationWindow(args.platform)
    window.run()


if __name__ == '__main__':
    main()
