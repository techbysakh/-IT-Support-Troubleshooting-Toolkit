import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import platform
import psutil
import platform
import speedtest
# Check Internet Connection
def check_network():
    try:
        # Ping google DNS to check internet connectivity
        if platform.system().lower() == "windows":
            # Windows command to ping
            subprocess.check_call(["ping", "8.8.8.8", "-n", "1"], stdout=subprocess.DEVNULL)
        else:
            # Linux/Mac command to ping
            subprocess.check_call(["ping", "8.8.8.8", "-c", "1"], stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Main App Window
root = tk.Tk()
root.title("IT Support Troubleshooting Toolkit")
root.geometry("400x400")
root.config(bg="#f0f0f0")

# Title
title = tk.Label(root, text="🛠 IT Support Toolkit", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title.pack(pady=20)

# Buttons and their placeholder actions
def check_reset_network():
    # Check if the device is connected to the internet
    if check_network():
        messagebox.showinfo("Check & Reset Network", "You are connected to the internet!")
    else:
        messagebox.showwarning("Check & Reset Network", "No internet connection found. Please check your network settings.")

def test_speed():
    st = speedtest.Speedtest()
    
    # Get best server
    st.get_best_server()
    
    # Perform download and upload tests
    download_speed = st.download() / 1_000_000  # Convert from bits/s to Mbit/s
    upload_speed = st.upload() / 1_000_000      # Convert from bits/s to Mbit/s
    
    # Get ping
    ping = st.results.ping
    
    # Display results in the message box
    messagebox.showinfo("Internet Speed", f"Download speed: {download_speed:.2f} Mbps\n"
                                         f"Upload speed: {upload_speed:.2f} Mbps\n"
                                         f"Ping: {ping} ms")

def show_sys_info():
    # Get system information
    system_info = {
        "OS": platform.system() + " " + platform.version(),
        # Fix RAM issue by getting it in GB with proper conversions
        "RAM": f"Total: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB | Available: {psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
    }

    # Get storage details (correctly calculating total and available space on all mounted drives)
    partitions = psutil.disk_partitions()
    storage_info = ""
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_info += f"{partition.device} - Total: {usage.total / (1024 ** 3):.2f} GB | Available: {usage.free / (1024 ** 3):.2f} GB\n"

    # Add storage info to the system info
    system_info["Storage"] = storage_info

    # Get GPU info (updated method)
    try:
        gpus = subprocess.check_output("nvidia-smi --list-gpus", shell=True).decode("utf-8").strip().split("\n")
        if not gpus or "NVIDIA" not in gpus[0]:
            gpus = subprocess.check_output("lspci | grep VGA", shell=True).decode("utf-8").strip().split("\n")
        
        gpu_info = "\n".join([f"GPU {i+1}: {gpu}" for i, gpu in enumerate(gpus)])
    except Exception as e:
        gpu_info = "No GPU info available."

    # Create a string to display
    info_str = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
    
    # Add GPU info to the string
    info_str += f"\n\n{gpu_info}"

    # Show in message box
    messagebox.showinfo("System Info", info_str)


def detect_drivers():
    system_type = platform.system()

    if system_type == "Windows":
        message = detect_drivers_windows()
    elif system_type == "Linux":
        message = detect_drivers_linux()
    else:
        message = "Driver detection not supported on this OS."

    # Show the result in a messagebox
    messagebox.showinfo("Outdated Drivers", message)
def detect_drivers_windows():
    try:
        # Get installed drivers using wmic
        drivers = subprocess.check_output("wmic sysdriver get caption,description", shell=True).decode("utf-8").strip().split("\n")
        outdated_drivers = []

        # Placeholder for specific driver check (expand this logic for actual version checks)
        for driver in drivers:
            if "NVIDIA" in driver or "AMD" in driver:
                outdated_drivers.append(driver)

        # Example logic to update NVIDIA drivers using winget (Windows Package Manager)
        if "NVIDIA" in str(outdated_drivers):
            outdated_drivers.append("Run 'winget upgrade NVIDIA' to update your NVIDIA drivers.")
        
        if outdated_drivers:
            message = "Outdated or specific drivers found:\n" + "\n".join(outdated_drivers)
        else:
            message = "All drivers are up to date!"

    except subprocess.CalledProcessError as e:
        message = f"Error detecting drivers: {e}"

    return message

def detect_drivers_linux():
    try:
        # Check for outdated drivers using apt
        outdated_packages = subprocess.check_output("apt list --upgradable", shell=True).decode("utf-8").strip()

        outdated_drivers = []
        if "nvidia" in outdated_packages.lower():
            outdated_drivers.append("Outdated GPU drivers detected. You can update using the following command:\n'apt-get install --only-upgrade nvidia-driver'")

        if not outdated_drivers:
            message = "No outdated drivers found!"
        else:
            message = "Outdated drivers:\n" + "\n".join(outdated_drivers)

    except subprocess.CalledProcessError as e:
        message = f"Error detecting drivers: {e}"

    return message  
def clear_temp_files():
    system_type = platform.system()

    if system_type == "Windows":
        temp_folder = "C:\\Windows\\Temp"
        try:
            subprocess.run(f"del /q {temp_folder}\\*", shell=True)
            subprocess.run(f"rmdir /s /q {temp_folder}", shell=True)
            messagebox.showinfo("Clear Temp Files", "Temporary files cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear temporary files: {str(e)}")
    
    elif system_type == "Linux":
        temp_folder = "/tmp"
        try:
            subprocess.run(f"rm -rf {temp_folder}/*", shell=True)
            messagebox.showinfo("Clear Temp Files", "Temporary files cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear temporary files: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Temporary file clearing is not supported on this OS.")

def clear_browser_cache():
    system_type = platform.system()

    if system_type == "Windows":
        # Example for Chrome (Adjust as needed for other browsers)
        chrome_cache = "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"
        try:
            subprocess.run(f"del /q {chrome_cache}\\*", shell=True)
            messagebox.showinfo("Clear Browser Cache", "Browser cache cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear browser cache: {str(e)}")
    
    elif system_type == "Linux":
        # Example for Chrome (Adjust as needed for other browsers)
        chrome_cache = "~/.cache/google-chrome/Default/Cache"
        try:
            subprocess.run(f"rm -rf {chrome_cache}/*", shell=True)
            messagebox.showinfo("Clear Browser Cache", "Browser cache cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear browser cache: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Browser cache clearing is not supported on this OS.")


def check_disk_space():
    system_type = platform.system()
    
    if system_type == "Windows":
        try:
            # Get disk usage with 'wmic logicaldisk'
            disk_usage = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True).decode("utf-8")
            messagebox.showinfo("Disk Space", f"Disk space info:\n{disk_usage}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get disk space info: {str(e)}")
    
    elif system_type == "Linux":
        try:
            disk_usage = subprocess.check_output("df -h", shell=True).decode("utf-8")
            messagebox.showinfo("Disk Space", f"Disk space info:\n{disk_usage}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get disk space info: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Disk space checking is not supported on this OS.")


def check_disk_space():
    system_type = platform.system()
    
    if system_type == "Windows":
        try:
            # Get disk usage with 'wmic logicaldisk'
            disk_usage = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True).decode("utf-8")
            messagebox.showinfo("Disk Space", f"Disk space info:\n{disk_usage}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get disk space info: {str(e)}")
    
    elif system_type == "Linux":
        try:
            disk_usage = subprocess.check_output("df -h", shell=True).decode("utf-8")
            messagebox.showinfo("Disk Space", f"Disk space info:\n{disk_usage}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get disk space info: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Disk space checking is not supported on this OS.")


def system_cleanup():
    system_type = platform.system()

    if system_type == "Windows":
        try:
            subprocess.run("cleanmgr /sagerun:1", shell=True)
            messagebox.showinfo("System Cleanup", "System cleanup completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to perform system cleanup: {str(e)}")
    
    elif system_type == "Linux":
        try:
            subprocess.run("sudo apt-get clean", shell=True)
            subprocess.run("sudo apt-get autoremove", shell=True)
            messagebox.showinfo("System Cleanup", "System cleanup completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to perform system cleanup: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "System cleanup is not supported on this OS.")

# Port descriptions (simplified)
PORT_DESCRIPTIONS = {
    22: "SSH (Secure Shell) - Remote login",
    80: "HTTP - Web traffic",
    443: "HTTPS - Secure web traffic",
    21: "FTP - File transfer",
    53: "DNS - Domain Name System",
    25: "SMTP - Email sending",
    110: "POP3 - Email retrieval",
    143: "IMAP - Email retrieval",
    3306: "MySQL - Database",
    3389: "RDP - Remote Desktop",
}

# Function to get open ports (with descriptions)
def get_open_ports():
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        # Filtering only the listening ports
        if conn.status == 'LISTEN':
            port = conn.laddr.port
            # Get the description for the port or use a generic message
            description = PORT_DESCRIPTIONS.get(port, "Unknown service")
            open_ports.append(f"Port {port}: {description}")
    return open_ports

# Function to check system-level open ports
def check_system_open_ports():
    system_type = platform.system()
    ports_info = ""

    if system_type == "Windows":
        try:
            ports_info = subprocess.check_output("netstat -an", shell=True).decode("utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check open ports: {str(e)}")
    
    elif system_type == "Linux":
        try:
            ports_info = subprocess.check_output("ss -tuln", shell=True).decode("utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check open ports: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Open ports checking is not supported on this OS.")
    
    return ports_info

# Unified function to display both open ports with descriptions and system-level ports
def show_open_ports():
    open_ports = get_open_ports()
    system_ports = check_system_open_ports()

    if not open_ports and not system_ports:
        messagebox.showinfo("Open Ports", "No open ports found.")
        return

    # Create a new window to show open ports
    ports_window = tk.Toplevel(root)
    ports_window.title("Open Ports")
    ports_window.geometry("600x400")

    # Add a scrollable Text widget
    scroll_text = scrolledtext.ScrolledText(ports_window, width=80, height=20, wrap=tk.WORD)
    scroll_text.pack(padx=10, pady=10)

    # Insert description-based open ports into the scrollable text
    scroll_text.insert(tk.END, "Open Ports with Descriptions:\n")
    for port_info in open_ports:
        scroll_text.insert(tk.END, port_info + "\n")

    scroll_text.insert(tk.END, "\nSystem-Level Open Ports:\n")
    scroll_text.insert(tk.END, system_ports)

    # Disable editing
    scroll_text.config(state=tk.DISABLED)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def check_software_updates():
    system_type = platform.system()

    if system_type == "Windows":
        try:
            subprocess.run("powershell -Command \"Get-WindowsUpdate\"", shell=True)
            messagebox.showinfo("Software Updates", "Check for available updates.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check software updates: {str(e)}")
    
    elif system_type == "Linux":
        try:
            updates = subprocess.check_output("apt list --upgradable", shell=True).decode("utf-8")
            messagebox.showinfo("Software Updates", f"Available updates:\n{updates}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check software updates: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Software update check is not supported on this OS.")

def toggle_firewall():
    system_type = platform.system()

    if system_type == "Windows":
        try:
            # Check if the firewall is enabled
            firewall_status = subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode("utf-8")
            if "State ON" in firewall_status:
                # Disable firewall
                subprocess.run("netsh advfirewall set allprofiles state off", shell=True)
                messagebox.showinfo("Firewall Status", "Firewall has been disabled.")
            else:
                # Enable firewall
                subprocess.run("netsh advfirewall set allprofiles state on", shell=True)
                messagebox.showinfo("Firewall Status", "Firewall has been enabled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle firewall: {str(e)}")
    
    elif system_type == "Linux":
        try:
            # Check if UFW is active
            ufw_status = subprocess.check_output("ufw status", shell=True).decode("utf-8")
            if "Status: active" in ufw_status:
                # Disable UFW
                subprocess.run("sudo ufw disable", shell=True)
                messagebox.showinfo("Firewall Status", "Firewall has been disabled.")
            else:
                # Enable UFW
                subprocess.run("sudo ufw enable", shell=True)
                messagebox.showinfo("Firewall Status", "Firewall has been enabled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle firewall: {str(e)}")
    else:
        messagebox.showwarning("Unsupported OS", "Firewall toggle is not supported on this OS.")


# Buttons UI
btn_style = {"width": 30, "padx": 5, "pady": 5, "bg": "#e0e0e0"}

tk.Button(root, text="✅ Check & Reset Network", command=check_reset_network, **btn_style).pack(pady=5)
tk.Button(root, text="🚀 Test Internet Speed", command=test_speed, **btn_style).pack(pady=5)
tk.Button(root, text="🖥 Show System Info", command=show_sys_info, **btn_style).pack(pady=5)
tk.Button(root, text="🔍 Detect Outdated Drivers", command=detect_drivers, **btn_style).pack(pady=5)
tk.Button(root, text="🧹 Clear Temp Files", command=clear_temp_files, **btn_style).pack(pady=5)
tk.Button(root, text="🧼 Clear Browser Cache", command=clear_browser_cache, **btn_style).pack(pady=5)
tk.Button(root, text="💾 Check Disk Space", command=check_disk_space, **btn_style).pack(pady=5)
tk.Button(root, text="🛠 System Cleanup", command=system_cleanup, **btn_style).pack(pady=5)
ports_button = tk.Button(root, text="🔍Show Open Ports", command=show_open_ports, **btn_style )
ports_button.pack(pady=5)
tk.Button(root, text="🔄 Check Software Updates", command=check_software_updates, **btn_style).pack(pady=5)
tk.Button(root, text="🔒 Toggle Firewall", command=toggle_firewall, **btn_style).pack(pady=5)
tk.Button(root, text="❌ Exit", command=root.quit, fg="red", **btn_style).pack(pady=20)

root.mainloop()
