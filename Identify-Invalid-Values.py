import re
import pandas as pd

data = pd.read_csv("./demo_dataset.csv")

# Check for invalid IP addresses
def is_valid_ip(ip):
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip))

invalid_ips = data[~data['source_ip'].astype(str).apply(is_valid_ip)]

# Check for invalid port numbers
def is_valid_port(port):
    try:
        port = int(port)
        return 0 <= port <= 65535
    except ValueError:
        return False

invalid_ports = data[~data['destination_port'].apply(is_valid_port)]

# Check for invalid protocol values
valid_protocols = ['TCP', 'TLS', 'SSH', 'POP3', 'DNS', 'HTTPS', 'SMTP', 'FTP', 'UDP', 'HTTP']
invalid_protocols = data[~data['protocol'].isin(valid_protocols)]

# Check for invalid bytes transferred
def is_valid_bytes(bytes):
    try:
        bytes = int(bytes)
        return bytes >= 0
    except ValueError:
        return False

invalid_bytes = data[~data['bytes_transferred'].apply(is_valid_bytes)]

# Check for invalid threat levels
def is_valid_threat_level(threat_level):
    try:
        threat_level = int(threat_level)
        return 0 <= threat_level <= 2
    except ValueError:
        return False

invalid_threat_levels = data[~data['threat_level'].apply(is_valid_threat_level)]

# Drop invalid entries
data = data.drop(invalid_ips.index, errors='ignore') 
data = data.drop(invalid_ports.index, errors='ignore')
data = data.drop(invalid_protocols.index, errors='ignore')
data = data.drop(invalid_bytes.index, errors='ignore')
data = data.drop(invalid_threat_levels.index, errors='ignore')

print(data.describe(include='all'))
