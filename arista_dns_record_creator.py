import pexpect
import re
import ipaddress

# Configuration
DEVICE_IPS = ["172.31.1.11", "172.31.1.12"]  # Replace with your list of Arista device IPs
USERNAME = "admin"                          # Replace with your username
PASSWORD = "password"                       # Replace with your password
DOMAIN = "example.com"                     # Replace with your domain
OUTPUT_FILE = "dns_records.txt"            # Output file name

def connect_to_device(ip, username, password):
    """Connect to the Arista device via SSH and return the session."""
    ssh_cmd = f"ssh {username}@{ip}"
    session = pexpect.spawn(ssh_cmd, timeout=30)
    session.expect("password:")
    session.sendline(password)
    session.expect(r"#")
    return session

def get_hostname(session):
    """Retrieve the hostname from the device."""
    session.sendline("show hostname")
    session.expect(r"#")
    output = session.before.decode("utf-8")
    hostname_match = re.search(r"Hostname: (\S+)", output)
    if hostname_match:
        return hostname_match.group(1)
    return "unknown"

def get_interfaces(session):
    """Scrape detailed interface IP and VRF information from the device."""
    session.sendline("terminal length 0")
    session.expect(r"#")
    session.sendline("show ip interface")
    session.expect(r"#")
    output = session.before.decode("utf-8")
    return output

def parse_interfaces(output):
    """Parse the 'show ip interface' output and extract interface, IP, and VRF data."""
    interfaces = []
    lines = output.splitlines()
    current_interface = None
    current_vrf = None
    ip_pattern = r"Internet address is (\d+\.\d+\.\d+\.\d+(/\d+)?)"
    vrf_pattern = r"VPN Routing/Forwarding \"(\S+)\""

    for line in lines:
        # Skip command echoes
        if line.strip().startswith("terminal length") or line.strip().startswith("show ip interface"):
            continue
        # Detect interface name (lines not starting with a space)
        if line.strip() and not line.startswith(" "):
            if current_interface and "ip" in locals():  # Save previous interface if it had an IP
                interfaces.append((current_interface, ip, current_vrf))
            current_interface = line.split()[0]
            current_vrf = None  # Reset VRF for new interface
        # Extract VRF if present
        vrf_match = re.search(vrf_pattern, line)
        if vrf_match:
            current_vrf = vrf_match.group(1)
        # Extract IP address
        ip_match = re.search(ip_pattern, line)
        if ip_match and current_interface:
            ip = ip_match.group(1).split("/")[0]  # Remove subnet mask
            if ip != "unassigned":
                # Don’t append yet; wait for next interface or end
                pass  # IP is stored in `ip` variable

    # Append the last interface if it has an IP
    if current_interface and "ip" in locals():
        interfaces.append((current_interface, ip, current_vrf))

    return interfaces

def generate_dns_name(interface, vrf, hostname, domain):
    """Generate the DNS name for rDNS based on interface type and VRF."""
    interface = interface.lower()
    if interface.startswith("ethernet"):
        eth_num = re.sub(r"ethernet(\d+(/\d+)?)", r"\1", interface)
        eth_num = eth_num.replace("/", "-")
        base_name = f"eth{eth_num}"
    elif interface.startswith("vlan"):
        vlan_num = re.sub(r"vlan(\d+)", r"\1", interface)
        base_name = f"vlan{vlan_num}"
    elif interface.startswith("port-channel"):
        pc_num = re.sub(r"port-channel(\d+)", r"\1", interface)
        base_name = f"pc{pc_num}"
    elif interface.startswith("management"):
        ma_num = re.sub(r"management(\d+)", r"\1", interface)
        base_name = f"ma{ma_num}"
    else:
        base_name = interface

    # Append VRF if present and not "default"
    if vrf and vrf.lower() != "default":
        return f"{base_name}-{vrf}.{hostname}.{domain}"
    return f"{base_name}.{hostname}.{domain}"

def generate_records(interfaces, hostname, domain):
    """Generate A and rDNS records."""
    a_records = []
    rdns_records = []

    for interface, ip, vrf in interfaces:
        # A record: create one for each IP with the same hostname
        a_records.append(f"{hostname}.{domain} IN A {ip}")
        # rDNS record: include interface and VRF
        dns_name = generate_dns_name(interface, vrf, hostname, domain)
        try:
            ip_obj = ipaddress.ip_address(ip)
            reverse_ptr = ip_obj.reverse_pointer
            rdns_records.append(f"{reverse_ptr} IN PTR {dns_name}")
        except ValueError:
            print(f"Skipping invalid IP: {ip}")
    return a_records, rdns_records

def save_to_file(a_records, rdns_records, filename):
    """Save records to a text file."""
    with open(filename, "w") as f:
        f.write("### A Records ###\n")
        for record in a_records:
            f.write(f"{record}\n")
        f.write("\n### rDNS Records ###\n")
        for record in rdns_records:
            f.write(f"{record}\n")
    print(f"DNS records saved to {filename}")

def main():
    all_a_records = []
    all_rdns_records = []

    for device_ip in DEVICE_IPS:
        print(f"Connecting to {device_ip}...")
        try:
            session = connect_to_device(device_ip, USERNAME, PASSWORD)

            hostname = get_hostname(session)
            print(f"Hostname: {hostname}")

            interface_output = get_interfaces(session)
            print("Raw interface output:")
            print(interface_output)
            interfaces = parse_interfaces(interface_output)
            print(f"Found {len(interfaces)} interfaces with IPs")

            a_records, rdns_records = generate_records(interfaces, hostname, DOMAIN)
            all_a_records.extend(a_records)
            all_rdns_records.extend(rdns_records)

            session.sendline("exit")
            session.close()
        except pexpect.ExceptionPexpect as e:
            print(f"Failed to process {device_ip}: {e}")

    # Save all records after processing all devices
    if all_a_records or all_rdns_records:
        save_to_file(all_a_records, all_rdns_records, OUTPUT_FILE)
    else:
        print("No records generated.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
