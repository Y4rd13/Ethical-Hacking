import socket
import ipinfo
import os
from dotenv import load_dotenv

load_dotenv("projects/checkers/modules/.env")

class DNSInfo:
    def __init__(self, domain=None):
        self.domain = domain
        self.ipinfo_token = os.environ.get('IPINFO_TOKEN')
        if self.ipinfo_token is None:
            raise ValueError("IPINFO_TOKEN is not set. Please provide it using the --token argument.")
        self.ipinfo_handler = ipinfo.getHandler(self.ipinfo_token)

    def get_ip_address(self):
        """Obtiene la dirección IP asociada al dominio."""
        try:
            return socket.gethostbyname(self.domain)
        except socket.gaierror:
            return None

    def get_fqdn(self):
        """Obtiene el nombre de dominio totalmente calificado."""
        return socket.getfqdn(self.domain)

    def get_alias_and_ips(self):
        """Obtiene los alias y las direcciones IP asociadas al dominio."""
        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(self.domain)
            return {
                "hostname": hostname,
                "alias": aliaslist,
                "ip_addresses": ipaddrlist
            }
        except socket.gaierror:
            return None

    def get_name_servers(self):
        """Obtiene los servidores de nombres asociados al dominio."""
        try:
            return socket.getaddrinfo(self.domain, None, socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, socket.AI_CANONNAME)
        except socket.gaierror:
            return None

    def get_own_dns_info(self):
        """Obtiene la información DNS de la propia IP de la máquina."""
        own_hostname = socket.gethostname()
        own_ip = socket.gethostbyname(own_hostname)
        try:
            dns_name, _, _ = socket.gethostbyaddr(own_ip)
            return {
                "hostname": own_hostname,
                "ip": own_ip,
                "dns_name": dns_name
            }
        except socket.herror:
            return {
                "hostname": own_hostname,
                "ip": own_ip,
                "dns_name": None
            }

    def get_location_info(self, ip=None):
        """Obtiene la información de ubicación de la dirección IP proporcionada usando ipinfo.io."""
        return self.ipinfo_handler.getDetails(ip_address=ip).details

def set_ipinfo_token(token):
    """Sets the IPINFO_TOKEN in a .env file."""
    with open(".env", "w") as f:
        f.write(f"IPINFO_TOKEN = \"{token}\"")

if __name__ == "__main__":
    domain_info = DNSInfo("google.com")
    print(domain_info.get_ip_address())
    print(domain_info.get_fqdn())
    print(domain_info.get_alias_and_ips())
    print(domain_info.get_name_servers())

    print('---------------------')
    domain_info = DNSInfo()
    print(domain_info.get_own_dns_info())
    print(domain_info.get_location_info())


    '''
    OUTPUT sample:
    192.0.0.88
    google.com
    {'hostname': 'google.com', 'alias': [], 'ip_addresses': ['192.0.0.88']}
    [(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, 'google.com', ('192.0.0.88', 0))]
    ---------------------
    {'hostname': 'kali', 'ip': '127.0.1.1', 'dns_name': 'kali'}
    {'ip': '176.97.206.182', 'city': 'Amsterdam', 'region': 'North Holland', 'country': 'NL', 'loc': '52.3740,4.8897', 'org': 'AS136787 TEFINCOM S.A.', 'postal': '1012', 'timezone': 'Europe/Amsterdam', 'country_name': 'Netherlands', 'isEU': True, 'country_flag_url': 'https://cdn.ipinfo.io/static/images/countries-flags/NL.svg', 'country_flag': {'emoji': '🇳🇱', 'unicode': 'U+1F1F3 U+1F1F1'}, 'country_currency': {'code': 'EUR', 'symbol': '€'}, 'continent': {'code': 'EU', 'name': 'Europe'}, 'latitude': '52.3740', 'longitude': '4.8897'}
    '''