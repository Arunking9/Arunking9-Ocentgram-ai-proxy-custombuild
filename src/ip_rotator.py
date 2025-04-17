import subprocess
import time
import random
import os
from src import printcolors as pc

class IPRotator:
    def __init__(self):
        self.enabled = False
        self.rotation_interval = 300  # 5 minutes default
        self.last_rotation = 0
        self._load_config()
    
    def _load_config(self):
        """Load IP rotation configuration"""
        config_path = os.path.join("config", "ip_config.ini")
        if os.path.exists(config_path):
            import configparser
            config = configparser.ConfigParser()
            config.read(config_path)
            self.enabled = config.getboolean("IP", "enabled", fallback=False)
            self.rotation_interval = config.getint("IP", "rotation_interval", fallback=300)
    
    def rotate_ip(self):
        """Rotate the IP address using various methods"""
        if not self.enabled:
            return False
        
        current_time = time.time()
        if current_time - self.last_rotation < self.rotation_interval:
            return False
        
        try:
            # Try different methods to change IP
            methods = [
                self._rotate_via_tor,
                self._rotate_via_vpn,
                self._rotate_via_proxy
            ]
            
            # Shuffle methods to try them in random order
            random.shuffle(methods)
            
            for method in methods:
                if method():
                    self.last_rotation = current_time
                    pc.printout("IP address successfully rotated\n", pc.GREEN)
                    return True
            
            pc.printout("Failed to rotate IP address\n", pc.RED)
            return False
            
        except Exception as e:
            pc.printout(f"Error rotating IP: {str(e)}\n", pc.RED)
            return False
    
    def _rotate_via_tor(self):
        """Rotate IP using Tor"""
        try:
            # Check if Tor is installed
            subprocess.run(["which", "tor"], check=True, capture_output=True)
            
            # Restart Tor service
            subprocess.run(["sudo", "systemctl", "restart", "tor"], check=True)
            time.sleep(5)  # Wait for Tor to restart
            
            # Configure system to use Tor
            subprocess.run(["sudo", "ip", "route", "add", "default", "via", "127.0.0.1", "dev", "lo"], check=True)
            return True
        except:
            return False
    
    def _rotate_via_vpn(self):
        """Rotate IP using VPN"""
        try:
            # Check if OpenVPN is installed
            subprocess.run(["which", "openvpn"], check=True, capture_output=True)
            
            # Get list of VPN configs
            vpn_configs = subprocess.run(["ls", "/etc/openvpn/*.ovpn"], capture_output=True, text=True)
            if not vpn_configs.stdout:
                return False
            
            # Select random VPN config
            configs = vpn_configs.stdout.split()
            random_config = random.choice(configs)
            
            # Connect to VPN
            subprocess.run(["sudo", "openvpn", "--config", random_config, "--daemon"], check=True)
            time.sleep(10)  # Wait for VPN connection
            return True
        except:
            return False
    
    def _rotate_via_proxy(self):
        """Rotate IP using proxy"""
        try:
            # Check if proxy is configured
            proxy_config = os.path.join("config", "proxy_config.ini")
            if not os.path.exists(proxy_config):
                return False
            
            import configparser
            config = configparser.ConfigParser()
            config.read(proxy_config)
            
            if "Proxy" not in config:
                return False
            
            # Set system proxy
            proxy = config["Proxy"]["address"]
            subprocess.run(["export", f"http_proxy={proxy}"], check=True)
            subprocess.run(["export", f"https_proxy={proxy}"], check=True)
            return True
        except:
            return False 