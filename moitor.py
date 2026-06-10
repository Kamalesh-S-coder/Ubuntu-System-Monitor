import psutil
import os
import time

# ANSI color codes for the Ubuntu terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def get_color(percentage):
    """Returns a color code based on how high the usage percentage is."""
    if percentage < 60:
        return Colors.GREEN
    elif percentage < 85:
        return Colors.YELLOW
    else:
        return Colors.RED

def format_speed(bytes_per_sec):
    """Converts bytes into human-readable KB/s or MB/s."""
    kb = bytes_per_sec / 1024
    if kb < 1024:
        return f"{kb:.2f} KB/s"
    else:
        mb = kb / 1024
        return f"{mb:.2f} MB/s"

def clear_terminal():
    """Clears the terminal screen."""
    os.system('clear')

def render_dashboard(last_sent, last_recv):
    clear_terminal()
    print("="*40)
    print(" 🖥️  UBUNTU SYSTEM & NETWORK MONITOR")
    print("="*40)
    
    # --- 1. CORE SYSTEM METRICS ---
    # CPU (Checks over a 0.1s interval)
    cpu_usage = psutil.cpu_percent(interval=0.1)
    cpu_color = get_color(cpu_usage)
    print(f"CPU Usage:  {cpu_color}{cpu_usage}%{Colors.RESET}")
    
    # RAM
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024 ** 3)
    ram_total_gb = ram.total / (1024 ** 3)
    ram_color = get_color(ram.percent)
    print(f"RAM Usage:  {ram_color}{ram.percent}%{Colors.RESET} ({ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB)")
    
    # Disk
    disk = psutil.disk_usage('/')
    disk_used_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)
    disk_color = get_color(disk.percent)
    print(f"Disk Usage: {disk_color}{disk.percent}%{Colors.RESET} ({disk_used_gb:.2f} GB / {disk_total_gb:.2f} GB)")
    
    print("-" * 40)
    
    # --- 2. NETWORK METRICS ---
    # Get current cumulative totals
    net_counters = psutil.net_io_counters()
    current_sent = net_counters.bytes_sent
    current_recv = net_counters.bytes_recv
    
    # Calculate speed based on the difference from 2 seconds ago
    # Divided by 2 because our loop sleeps for 2 seconds
    upload_speed = (current_sent - last_sent) / 2
    download_speed = (current_recv - last_recv) / 2
    
    print(f"🚀 Upload:   {format_speed(upload_speed)}")
    print(f"📥 Download: {format_speed(download_speed)}")
    
    print("-" * 40)
    print("Press Ctrl+C to exit.")
    
    # Return the current totals to use as the baseline for the next loop
    return current_sent, current_recv

if __name__ == "__main__":
    try:
        # Initialize baseline network totals before entering the loop
        init_net = psutil.net_io_counters()
        last_sent = init_net.bytes_sent
        last_recv = init_net.bytes_recv
        
        while True:
            # Render dashboard and update the baseline trackers
            last_sent, last_recv = render_dashboard(last_sent, last_recv)
            time.sleep(2)
            
    except KeyboardInterrupt:
        clear_terminal()
        print("System Monitor stopped. Goodbye!")
