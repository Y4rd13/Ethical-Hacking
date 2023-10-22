import re
import json
import random
import subprocess

class PyMAChanger:
    def __init__(self, interface):
        self.interface = interface
        self.OUI_DATA, self.WIRELESS_LIST_LINES = self.load_data()

    @staticmethod
    def load_data():
        with open('./data/oui.json', 'r') as f:
            OUI_DATA = json.load(f)
    
        with open('./data/wireless.list', 'r') as f:
            WIRELESS_LIST_LINES = f.readlines()

        return OUI_DATA, WIRELESS_LIST_LINES

    def _run_command(self, *args):
        try:
            result = subprocess.check_output(args)
            return result.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return None

    def _set_interface_mac(self, mac_address):
        try:
            subprocess.call(["sudo", "ifconfig", self.interface, "down"])
            subprocess.call(["sudo", "ifconfig", self.interface, "hw", "ether", mac_address])
            subprocess.call(["sudo", "ifconfig", self.interface, "up"])
            return True
        except Exception as e:
            return False

    def _extract_mac_details(self, raw_output):
        mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", raw_output)
        if mac_address_search:
            mac = mac_address_search.group(0)
            oui_part = mac.replace(":", "").upper()[:6]
            manufacturer_details = self.OUI_DATA.get(oui_part, "Unknown Manufacturer\nUnknown Address").split("\n")
            manufacturer_name = manufacturer_details[0]
            manufacturer_address = " ".join(manufacturer_details[1:]).strip()
            return {
                'mac': mac,
                'vendor': {
                    'name': manufacturer_name,
                    'address': manufacturer_address
                }
            }
        return None

    def _get_mac_details(self, mode="current"):
        if mode == "current":
            result = self._run_command("sudo ifconfig", self.interface)
        elif mode == "permanent":
            result = self._run_command("sudo ethtool", "-P", self.interface)
        else:
            return None

        return self._extract_mac_details(result) if result else None

    def _generate_random_mac_suffix(self):
        return ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def _generate_random_mac(self):
        return ":".join("{:02x}".format(random.randint(0, 255)) for _ in range(6))

    def get_current_mac(self):
        mac_details = self._get_mac_details("current")
        if mac_details:
            current_mac = mac_details['mac']
            manufacturer = f"{mac_details['vendor']['name']} {mac_details['vendor']['address']}"
            return f"Current MAC: {current_mac} ({manufacturer})"
        return None

    def show(self):
        """
        Retrieve the current and permanent MAC addresses for the network interface.
        
        :return: A dictionary containing the current and permanent MAC addresses and their associated manufacturers.
        """
        return {
            'current': self._get_mac_details("current"),
            'permanent': self._get_mac_details("permanent")
        }

    def restore(self):
        """
        Restore the MAC address of the specified network interface to its original (permanent) value.
        
        :return: True if the restoration was successful, False otherwise.
        """
        permanent_details = self._get_mac_details("permanent")
        return self._set_interface_mac(permanent_details['mac']) if permanent_details else False

    def set(self, option):
        """
        Set the MAC address of the specified network interface based on the given option.
        
        Options:
        1. Set random vendor MAC of the same kind (same vendor prefix)
        2. Set random vendor MAC of any kind (random vendor prefix)
        3. Set fully random MAC
        
        :param option: Integer value representing the MAC setting option (1, 2, or 3).
        :return: Dictionary containing the new MAC address and its associated manufacturer or None if an error occurs.
        """
        mac_details = self._get_mac_details("current")
        if not mac_details:
            return None
        current_mac = mac_details['mac']

        if option == 1:
            oui_part = current_mac[:8]
            new_mac = f"{oui_part}{self._generate_random_mac_suffix()}"

        elif option == 2:
            oui_part = random.choice(list(self.OUI_DATA.keys()))
            new_mac = f"{':'.join([oui_part[i:i+2] for i in range(0, 6, 2)])}{self._generate_random_mac_suffix()}"

        elif option == 3:
            new_mac = self._generate_random_mac()

        else:
            return None

        success = self._set_interface_mac(new_mac)
        return self.show() if success else None


pymac = PyMAChanger("eth0")
print('----')
print('SHOW')
print(pymac.show())
print('----')
print('SET')
option = 3
print(f'option: {option}')
print(pymac.set(option))
print('----')
pymac.restore()
print('RESTORE')
print(pymac.show())
print('----')