import subprocess
import re
import time
import os

def get_wifi_profiles():
    """Retrieves a list of Wi-Fi profiles and their passwords."""
    netsh_output = subprocess.run(
        ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", netsh_output))
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(
                ["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(
                    ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
                password = re.search(
                    "Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)
    return wifi_list

def display_wifi_profiles(wifi_data):
    """Prints the SSID and password for each Wi-Fi profile."""
    if not wifi_data:
        print("No Wi-Fi profiles found with saved keys.")
        return
    print("--- Wi-Fi Profiles and Passwords ---")
    for profile in wifi_data:
        print(f"SSID: {profile['ssid']}")
        print(f"Password: {profile['password'] if profile['password'] else 'N/A'}")
        print("-" * 30)

def connect_to_wifi(ssid):
    """Attempts to connect to a specified Wi-Fi network."""
    try:
        subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=True, capture_output=True)
        print(f"Successfully connected to '{ssid}'.")
        return True
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        if "There is no such wireless network interface on the system." in error_message:
            print("Error: No wireless network interface found.")
        elif "The specified network name is not available." in error_message:
            print(f"Error: Wi-Fi network '{ssid}' not found.")
        else:
            print(f"Error connecting to '{ssid}': {error_message}")
        return False

def disconnect_wifi():
    """Disconnects from the currently connected Wi-Fi network."""
    try:
        subprocess.run(["netsh", "wlan", "disconnect"], check=True, capture_output=True)
        print("Successfully disconnected from the Wi-Fi network.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error disconnecting from Wi-Fi: {e.stderr.decode()}")
        return False

def get_available_networks():
    """Lists the available Wi-Fi networks."""
    try:
        output = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True).stdout.decode()
        networks = re.findall(r"SSID\s+:\s+(.*)", output)
        if networks:
            print("\n--- Available Wi-Fi Networks ---")
            for network in networks:
                print(network.strip())
            return networks
        else:
            print("No Wi-Fi networks are currently available.")
            return []
    except subprocess.CalledProcessError as e:
        print(f"Error listing available networks: {e.stderr.decode()}")
        return []

def wait_for_connection(timeout=30):
    """Waits for a Wi-Fi connection to be established within a given timeout."""
    print(f"\nWaiting for Wi-Fi connection for {timeout} seconds...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            output = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True).stdout.decode()
            connection_status = re.search(r"State\s+:\s+(.*)", output)
            if connection_status and connection_status.group(1).strip() == "connected":
                print("Successfully connected to a Wi-Fi network.")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error checking connection status: {e.stderr.decode()}")
            return False
        time.sleep(2)
    print("Connection timeout reached.")
    return False

def forget_wifi_profile(ssid):
    """Deletes a specific saved Wi-Fi profile."""
    try:
        subprocess.run(["netsh", "wlan", "delete", f"profile name=\"{ssid}\""], check=True, capture_output=True)
        print(f"Successfully forgot the Wi-Fi profile '{ssid}'.")
        return True
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        if "There is no such wireless network interface on the system." in error_message:
            print("Error: No wireless network interface found.")
        elif f"The profile \"{ssid}\" is not found." in error_message:
            print(f"Error: Wi-Fi profile '{ssid}' not found.")
        else:
            print(f"Error forgetting profile '{ssid}': {error_message}")
        return False

def get_network_details():
    """Retrieves and displays detailed network configuration, including IP, DNS, and potentially gateway."""
    try:
        output = subprocess.run(["ipconfig", "/all"], capture_output=True).stdout.decode()
        print("\n--- Network Configuration ---")

        # Find the active Wi-Fi adapter information
        wifi_adapter_info = None
        adapters = output.split("\n\n")
        for adapter in adapters:
            if "Wireless LAN adapter Wi-Fi" in adapter:
                wifi_adapter_info = adapter
                break

        if wifi_adapter_info:
            print(wifi_adapter_info.strip())
        else:
            print("No active Wi-Fi adapter information found.")

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving network configuration: {e.stderr.decode()}")

def get_dns_servers():
    """Retrieves and displays the DNS servers configured for the active Wi-Fi adapter."""
    try:
        output = subprocess.run(["ipconfig", "/all"], capture_output=True).stdout.decode()
        dns_servers = []
        adapters = output.split("\n\n")
        for adapter in adapters:
            if "Wireless LAN adapter Wi-Fi" in adapter:
                dns_match = re.findall(r"DNS Servers\s+:\s+(.*)", adapter)
                if dns_match:
                    for server in dns_match:
                        dns_servers.extend([s.strip() for s in server.split(',')])
                    break

        if dns_servers:
            print("\n--- DNS Servers (Active Wi-Fi) ---")
            for server in dns_servers:
                print(server)
            return dns_servers
        else:
            print("No DNS server information found for the active Wi-Fi adapter.")
            return []

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving DNS server information: {e.stderr.decode()}")
        return []

def get_isp_information():
    """Attempts to infer the ISP based on the IP address (requires internet connection and might not be accurate)."""
    try:
        import requests
        print("\n--- Attempting to Get ISP Information ---")
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if "org" in data:
            print(f"Likely ISP: {data['org']}")
            return data['org']
        else:
            print("Could not determine ISP information.")
            return None
    except ImportError:
        print("Error: The 'requests' library is not installed. Please install it using 'pip install requests' to attempt ISP lookup.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during ISP lookup: {e}")
        return None

def set_dns_servers(interface_name="Wi-Fi", dns1=None, dns2=None):
    """Sets the DNS servers for a specified network interface."""
    if not dns1:
        print("Error: At least one DNS server address must be provided.")
        return False

    commands = []
    commands.append(f'netsh interface ip set dns name="{interface_name}" source=static address={dns1} primary')
    if dns2:
        commands.append(f'netsh interface ip add dns name="{interface_name}" address={dns2} index=2')

    try:
        for cmd in commands:
            subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully set DNS servers for '{interface_name}'.")
        if dns1:
            print(f"Primary DNS: {dns1}")
        if dns2:
            print(f"Secondary DNS: {dns2}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting DNS servers: {e.stderr.decode()}")
        return False

def restore_default_dns(interface_name="Wi-Fi"):
    """Restores the DNS settings for a specified network interface to DHCP."""
    try:
        cmd = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
        subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully restored default DHCP DNS settings for '{interface_name}'.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error restoring default DNS settings: {e.stderr.decode()}")
        return False

def get_current_connection_ssid():
    """Gets the SSID of the currently connected Wi-Fi network."""
    try:
        output = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True).stdout.decode()
        match = re.search(r"SSID\s+:\s+(.*)", output)
        if match:
            return match.group(1).strip()
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting current connection SSID: {e.stderr.decode()}")
        return None

def block_specific_ssid(ssid_to_block):
    """Attempts to block connections to a specific Wi-Fi SSID (may require administrator privileges)."""
    try:
        cmd = f'netsh wlan add filter permission=block ssid="{ssid_to_block}" networktype=infrastructure'
        subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully added a filter to block connections to '{ssid_to_block}'.")
        # Note: This might require administrator privileges.
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error blocking SSID '{ssid_to_block}': {e.stderr.decode()}")
        print("This operation might require administrator privileges (run the script as administrator).")
        return False

def allow_specific_ssid(ssid_to_allow):
    """Removes a block on a specific Wi-Fi SSID (may require administrator privileges)."""
    try:
        cmd = f'netsh wlan delete filter permission=block ssid="{ssid_to_allow}" networktype=infrastructure'
        subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully removed the block on SSID '{ssid_to_allow}'.")
        # Note: This might require administrator privileges.
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error allowing SSID '{ssid_to_allow}': {e.stderr.decode()}")
        print("This operation might require administrator privileges (run the script as administrator).")
        return False

def get_interface_guid(interface_name="Wi-Fi"):
    """Retrieves the GUID of a specified network interface."""
    try:
        output = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True).stdout.decode()
        match = re.search(r"Interface GUID\s+:\s+(.*)", output)
        if match:
            return match.group(1).strip()
        else:
            print(f"Could not find GUID for interface '{interface_name}'.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting interface GUID: {e.stderr.decode()}")
        return None

def set_mac_address(interface_name="Wi-Fi", new_mac=None):
    """Attempts to set a new MAC address for the specified network interface (may require administrator privileges and might not work on all adapters)."""
    interface_guid = get_interface_guid(interface_name)
    if not interface_guid or not new_mac:
        print("Error: Could not retrieve interface GUID or new MAC address is not provided.")
        return False

    # This method uses PowerShell to change the MAC address.
    powershell_command = f'(Get-NetAdapter -InterfaceGuid "{interface_guid}").MacAddress = "{new_mac}"'

    try:
        subprocess.run(["powershell", "-Command", powershell_command], check=True, capture_output=True)
        print(f"Successfully attempted to set MAC address for '{interface_name}' to '{new_mac}'.")
        # Note: This might require administrator privileges and a reboot to take full effect.
        # Also, not all network adapters allow MAC address changes.
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting MAC address: {e.stderr.decode()}")
        print("This operation might require administrator privileges and might not be supported by your network adapter.")
        return False

def clear_saved_credentials(ssid):
    """Attempts to clear the saved credentials for a specific Wi-Fi network (similar to 'forget')."""
    return forget_wifi_profile(ssid) # Reusing the forget function for simplicity

def enable_wifi_adapter(interface_name="Wi-Fi"):
    """Attempts to enable the specified Wi-Fi adapter (may require administrator privileges)."""
    try:
        cmd = f'netsh interface set interface "{interface_name}" enable'
        subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully enabled the '{interface_name}' adapter.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error enabling adapter '{interface_name}': {e.stderr.decode()}")
        print("This operation might require administrator privileges (run the script as administrator).")
        return False

def disable_wifi_adapter(interface_name="Wi-Fi"):
    """Attempts to disable the specified Wi-Fi adapter (may require administrator privileges)."""
    try:
        cmd = f'netsh interface set interface "{interface_name}" disable'
        subprocess.run(cmd, check=True, shell=True, capture_output=True)
        print(f"Successfully disabled the '{interface_name}' adapter.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error disabling adapter '{interface_name}': {e.stderr.decode()}")
        print("This operation might require administrator privileges (run the script as administrator).")
        return False

if __name__ == "__main__":
    wifi_list = get_wifi_profiles()
    display_wifi_profiles(wifi_list)

    available_networks = get_available_networks()

    current_ssid = get_current_connection_ssid()
    if current_ssid:
        print(f"\nCurrently connected to: {current_ssid}")
    else:
        print("\nNot currently connected to any Wi-Fi network.")

    if wifi_list:
        ssid_to_connect = input("\nEnter the SSID to connect to (leave blank to skip): ").strip()
        if ssid_to_connect:
            connect_successful = connect_to_wifi(ssid_to_connect)
            if connect_successful:
                wait_for_connection()

        disconnect = input("Do you want to disconnect from the current Wi-Fi? (yes/no): ").lower()
        if disconnect == "yes":
            disconnect_wifi()

    if wifi_list:
        ssid_to_forget = input("\nEnter the SSID to forget (leave blank to skip): ").strip()
        if ssid_to_forget:
            forget_wifi_profile(ssid_to_forget)

    get_network_details()
    get_dns_servers()
    get_isp_information()

    set_custom_dns = input("\nDo you want to set custom DNS servers? (yes/no): ").lower
