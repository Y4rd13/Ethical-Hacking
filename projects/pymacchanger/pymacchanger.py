import re
import json
import random
import subprocess

class PyMAChanger:
    def __init__(self, interface):
        """
        Initialize the PyMAChanger object with the specified network interface.
        
        :param interface: Name of the network interface to work with.
        """
        with open('./data/oui.json', 'r') as f:
            self.oui_data = json.load(f)

        with open('./data/wireless.list', 'r') as f:
            self.wireless_list_lines = f.readlines()

        self.interface = interface
        self.original_mac = self._get_mac_details()

    def _get_mac_details(self):
        """
        Private method to get the current MAC address of the specified network interface.
        
        :return: Current MAC address of the interface or None if not found.
        """
        try:
            result = subprocess.check_output(["ifconfig", self.interface])
            result = result.decode("utf-8")
            mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result)
            return mac_address_search.group(0) if mac_address_search else None
        except:
            return None

    def get_current_mac(self):
        """
        Get the current MAC address of the specified network interface and its associated manufacturer.
        
        :return: A formatted string displaying the current MAC address and its associated manufacturer.
        """
        current_mac = self._get_mac_details()
        if current_mac:
            oui_part = current_mac.replace(":", "").upper()[:6]
            manufacturer = self.oui_data.get(oui_part, "Unknown Manufacturer").replace("\n", " ")
            return f"Current MAC: {current_mac} ({manufacturer})"
        else:
            return None

    def show(self):
        """
        Show the current MAC address of the specified network interface.
        
        :return: Current MAC address of the interface.
        """
        return self.get_current_mac()

    def restore(self):
        """
        Restore the MAC address of the specified network interface to its original value.
        
        :return: True if successful, False otherwise.
        """
        try:
            subprocess.call(["sudo", "ifconfig", self.interface, "down"])
            subprocess.call(["sudo", "ifconfig", self.interface, "hw", "ether", self.original_mac])
            subprocess.call(["sudo", "ifconfig", self.interface, "up"])
            return True
        except:
            return False

    def set(self, option):
        """
        Set the MAC address of the specified network interface based on the given option.
        
        Options:
        1. Set random vendor MAC of the same kind
        2. Set random vendor MAC of any kind
        3. Set fully random MAC
        
        :param option: Integer value representing the MAC setting option (1, 2, or 3).
        :return: A formatted string displaying the new MAC address and its associated manufacturer.
        """
        manufacturer = None
        
        if option == 1:
            current_mac = self._get_mac_details()
            if current_mac:
                oui_part = current_mac.replace(":", "").upper()[:6]
                new_mac = ":".join([oui_part[i:i+2] for i in range(0, 6, 2)]) + ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                manufacturer = self.oui_data.get(oui_part, "Unknown Manufacturer").replace("\n", " ")

        elif option == 2:
            oui_part = random.choice(list(self.oui_data.keys()))
            new_mac = ":".join([oui_part[i:i+2] for i in range(0, len(oui_part), 2)])
            new_mac += ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            manufacturer = self.oui_data.get(oui_part, "Unknown Manufacturer").replace("\n", " ")

        elif option == 3:
            new_mac = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )

        else:
            return None

        try:
            subprocess.call(["sudo", "ifconfig", self.interface, "down"])
            subprocess.call(["sudo", "ifconfig", self.interface, "hw", "ether", new_mac])
            subprocess.call(["sudo", "ifconfig", self.interface, "up"])
            
            # Format the output as requested
            formatted_output = f"Current MAC: {new_mac} ({manufacturer})"
            return formatted_output
        except:
            return None

pymac = PyMAChanger("eth0")
print(pymac.get_current_mac())
print('----')
print(pymac.set(option=1))