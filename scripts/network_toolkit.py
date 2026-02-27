#!/usr/bin/env python3
"""
🌐 BAARLICLAW NETWORK TOOLKIT
Nettverksverktøy og -diagnostikk
"""

import os
import sys
import socket
import subprocess
import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import urllib.request
import urllib.error

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("NetworkToolkit")

@dataclass
class PingResult:
    """Ping test result"""
    host: str
    success: bool
    time_ms: Optional[float]
    packet_loss: float
    error: Optional[str] = None

@dataclass
class PortScanResult:
    """Port scan result"""
    host: str
    port: int
    open: bool
    service: Optional[str] = None

class NetworkTools:
    """Network diagnostic tools"""
    
    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt"
    }
    
    def ping(self, host: str, count: int = 4, timeout: int = 5) -> PingResult:
        """Ping a host"""
        try:
            # Use system ping
            result = subprocess.run(
                ['ping', '-c', str(count), '-W', str(timeout), host],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            if success:
                # Parse output for time
                import re
                times = re.findall(r'time=([\d.]+) ms', result.stdout)
                if times:
                    avg_time = sum(float(t) for t in times) / len(times)
                else:
                    avg_time = None
                
                # Parse packet loss
                loss_match = re.search(r'(\d+)% packet loss', result.stdout)
                packet_loss = float(loss_match.group(1)) if loss_match else 0
                
                return PingResult(host, True, avg_time, packet_loss)
            else:
                return PingResult(host, False, None, 100, "Host unreachable")
                
        except subprocess.TimeoutExpired:
            return PingResult(host, False, None, 100, "Timeout")
        except Exception as e:
            return PingResult(host, False, None, 100, str(e))
    
    def check_port(self, host: str, port: int, timeout: int = 3) -> bool:
        """Check if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, host: str, 
                   ports: Optional[List[int]] = None) -> List[PortScanResult]:
        """Scan ports on a host"""
        ports = ports or list(self.COMMON_PORTS.keys())
        results = []
        
        for port in ports:
            is_open = self.check_port(host, port)
            service = self.COMMON_PORTS.get(port)
            results.append(PortScanResult(host, port, is_open, service))
        
        return results
    
    def get_ip(self, hostname: str) -> Optional[str]:
        """Resolve hostname to IP"""
        try:
            return socket.gethostbyname(hostname)
        except:
            return None
    
    def get_hostname(self, ip: str) -> Optional[str]:
        """Resolve IP to hostname"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
    
    def check_url(self, url: str, timeout: int = 10) -> Dict:
        """Check URL availability"""
        result = {
            "url": url,
            "accessible": False,
            "status_code": None,
            "response_time_ms": None,
            "error": None,
            "headers": {}
        }
        
        try:
            start = time.time()
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                result["response_time_ms"] = (time.time() - start) * 1000
                result["status_code"] = response.getcode()
                result["accessible"] = 200 <= response.getcode() < 400
                result["headers"] = dict(response.headers)
                
        except urllib.error.HTTPError as e:
            result["status_code"] = e.code
            result["error"] = f"HTTP {e.code}"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def speed_test_simple(self) -> Dict:
        """Simple speed test (download from test file)"""
        # Use a small test file
        test_urls = [
            "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        ]
        
        results = []
        for url in test_urls:
            try:
                start = time.time()
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = response.read()
                    elapsed = time.time() - start
                    size_mb = len(data) / (1024 * 1024)
                    speed_mbps = (size_mb * 8) / elapsed
                    
                    results.append({
                        "url": url,
                        "size_mb": round(size_mb, 2),
                        "time_s": round(elapsed, 2),
                        "speed_mbps": round(speed_mbps, 2)
                    })
            except Exception as e:
                results.append({
                    "url": url,
                    "error": str(e)
                })
        
        return {
            "tests": results,
            "average_mbps": round(
                sum(r.get("speed_mbps", 0) for r in results) / 
                len([r for r in results if "speed_mbps" in r]), 2
            ) if results else 0
        }
    
    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_network_info(self) -> Dict:
        """Get network interface info"""
        info = {
            "hostname": socket.gethostname(),
            "local_ip": self.get_local_ip()
        }
        
        # Try to get more info
        try:
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            info["interfaces"] = result.stdout
        except:
            pass
        
        return info
    
    def traceroute(self, host: str, max_hops: int = 30) -> List[Dict]:
        """Simple traceroute"""
        hops = []
        
        for ttl in range(1, max_hops + 1):
            try:
                # Create UDP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
                
                # Send packet
                sock.sendto(b'', (host, 33434))
                
                # Wait for response
                start = time.time()
                sock.recvfrom(512)
                elapsed = (time.time() - start) * 1000
                
                hops.append({
                    "hop": ttl,
                    "host": host,
                    "time_ms": round(elapsed, 2),
                    "reached": True
                })
                break
                
            except socket.timeout:
                hops.append({
                    "hop": ttl,
                    "host": "*",
                    "time_ms": None,
                    "reached": False
                })
            except Exception as e:
                hops.append({
                    "hop": ttl,
                    "host": str(e),
                    "time_ms": None,
                    "reached": False
                })
            finally:
                sock.close()
        
        return hops

class ServiceMonitor:
    """Monitor services and websites"""
    
    def __init__(self):
        self.services: Dict[str, Dict] = {}
        self.history: List[Dict] = []
    
    def add_service(self, name: str, url: str, 
                   check_interval: int = 300):
        """Add a service to monitor"""
        self.services[name] = {
            "url": url,
            "interval": check_interval,
            "last_check": None,
            "status": "unknown",
            "uptime": 100.0
        }
    
    def check_all(self) -> Dict[str, Dict]:
        """Check all services"""
        tools = NetworkTools()
        results = {}
        
        for name, config in self.services.items():
            result = tools.check_url(config["url"])
            
            self.services[name]["last_check"] = time.time()
            self.services[name]["status"] = "up" if result["accessible"] else "down"
            
            results[name] = {
                "status": self.services[name]["status"],
                "response_time": result.get("response_time_ms"),
                "status_code": result.get("status_code")
            }
            
            self.history.append({
                "timestamp": time.time(),
                "service": name,
                **results[name]
            })
        
        return results
    
    def get_uptime_report(self, hours: int = 24) -> Dict:
        """Get uptime report"""
        cutoff = time.time() - (hours * 3600)
        recent = [h for h in self.history if h["timestamp"] > cutoff]
        
        if not recent:
            return {"message": "No data available"}
        
        by_service = {}
        for entry in recent:
            name = entry["service"]
            if name not in by_service:
                by_service[name] = {"up": 0, "down": 0}
            
            if entry["status"] == "up":
                by_service[name]["up"] += 1
            else:
                by_service[name]["down"] += 1
        
        report = {}
        for name, counts in by_service.items():
            total = counts["up"] + counts["down"]
            uptime = (counts["up"] / total * 100) if total > 0 else 0
            report[name] = {
                "uptime_percent": round(uptime, 2),
                "checks": total
            }
        
        return report

# === CONVENIENCE FUNCTIONS ===
def quick_ping(host: str) -> bool:
    """Quick ping test"""
    tools = NetworkTools()
    result = tools.ping(host, count=1)
    return result.success

def check_website(url: str) -> bool:
    """Quick website check"""
    tools = NetworkTools()
    result = tools.check_url(url)
    return result["accessible"]

def scan_common_ports(host: str) -> List[int]:
    """Quick port scan"""
    tools = NetworkTools()
    results = tools.scan_ports(host)
    return [r.port for r in results if r.open]

# === TESTING ===
if __name__ == "__main__":
    print("🌐 BaarliClaw Network Toolkit - Testing")
    print("=" * 50)
    
    tools = NetworkTools()
    
    # Test ping
    print("\n🧪 Testing ping")
    result = tools.ping("google.com", count=2)
    print(f"✅ Ping to {result.host}: {'Success' if result.success else 'Failed'}")
    if result.success:
        print(f"   Time: {result.time_ms:.2f}ms")
        print(f"   Packet loss: {result.packet_loss}%")
    
    # Test IP resolution
    print("\n🧪 Testing IP resolution")
    ip = tools.get_ip("google.com")
    print(f"✅ google.com resolves to: {ip}")
    
    # Test local IP
    print("\n🧪 Testing local IP")
    local_ip = tools.get_local_ip()
    print(f"✅ Local IP: {local_ip}")
    
    # Test URL check
    print("\n🧪 Testing URL check")
    url_result = tools.check_url("https://google.com")
    print(f"✅ google.com: {'Accessible' if url_result['accessible'] else 'Not accessible'}")
    if url_result['accessible']:
        print(f"   Status: {url_result['status_code']}")
        print(f"   Response time: {url_result['response_time_ms']:.2f}ms")
    
    # Test port scan (localhost)
    print("\n🧪 Testing port scan (localhost SSH)")
    ssh_open = tools.check_port("localhost", 22)
    print(f"✅ SSH port 22: {'Open' if ssh_open else 'Closed'}")
    
    print("\n✅ Network Toolkit ready!")
