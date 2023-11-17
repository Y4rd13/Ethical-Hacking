import re
import json
import random
import subprocess
import argparse

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
            result = subprocess.check_output(list(args))
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
            result = self._run_command("sudo", "ifconfig", self.interface)
        elif mode == "permanent":
            result = self._run_command("sudo", "ethtool", "-P", self.interface)
        else:
            return None

        return self._extract_mac_details(result) if result else None

    def _generate_random_mac_suffix(self):
        return ":{:02x}:{:02x}:{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def _generate_random_mac(self):
        first_byte = "{:02x}".format(random.randint(0, 255) & 0xFE)
        return ":".join([first_byte] + ["{:02x}".format(random.randint(0, 255)) for _ in range(5)])

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

    def set(self, option, custom_mac=None):
        """
        Set the MAC address of the specified network interface based on the given option.
        
        Options:
        1. Set random vendor MAC of the same kind (same vendor prefix)
        2. Set random vendor MAC of any kind (random vendor prefix)
        3. Set fully random MAC
        4. Set custom MAC (requires custom_mac parameter)
        
        :param option: Integer value representing the MAC setting option (1, 2, 3, or 4).
        :param custom_mac: String representing a custom MAC address for option 4.
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

        elif option == 4:
            if custom_mac and re.match(r"^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$", custom_mac):
                new_mac = custom_mac
            else:
                return None

        else:
            return None

        success = self._set_interface_mac(new_mac)
        return self.show() if success else None

    def parse_arguments():
        parser = argparse.ArgumentParser(description="Change and manage MAC addresses")

        parser.add_argument("-i", "--interface", required=True, help="Specify the network interface to work with.")

        parser.add_argument("-s", "--show", action="store_true", help="Show the current and permanent MAC addresses of the specified interface.")

        parser.add_argument("-r", "--restore", action="store_true", help="Restore the MAC address of the specified interface to its original (permanent) value.")

        parser.add_argument("-set", "--set", type=int, choices=[1, 2, 3, 4], help="Set the MAC address based on the given option: "
                                                                                 "1 - Set a random MAC address with the same vendor prefix as the current MAC. "
                                                                                 "2 - Set a random MAC address with a random vendor prefix. "
                                                                                 "3 - Set a completely random MAC address. "
                                                                                 "4 - Set a custom MAC address (requires the -m option with a valid MAC address).")

        parser.add_argument("-m", "--mac", type=str, help="Custom MAC address to use with option 4 for setting a specific MAC address.")

        return parser.parse_args()


if __name__ == "__main__":
    args = PyMAChanger.parse_arguments()

    pymac = PyMAChanger(args.interface)

    if args.show:
        print(pymac.show())
    elif args.restore:
        pymac.restore()
        print(pymac.show())
        print(f'MAC successfully restored for {args.interface}')
    elif args.set:
        print(pymac.set(option=args.set, custom_mac=args.mac if args.mac else None))