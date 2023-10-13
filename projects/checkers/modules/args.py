from .proxy_checker import ProxyChecker
from .dns_checker import DNSInfo, set_ipinfo_token
from dotenv import load_dotenv
import argparse
load_dotenv()

def main_arguments():
    parser = argparse.ArgumentParser(description="Checkers for Proxies status and DNS/IP information.")
    subparsers = parser.add_subparsers(dest="mode")

    # Proxy subparser
    proxy_parser = subparsers.add_parser("proxy", help="Run proxy checker.")
    proxy_checker_args(proxy_parser)

    # DNS subparser
    dns_parser = subparsers.add_parser("dns", help="Run DNS checker.")
    dns_checker_args(dns_parser)

    args = parser.parse_args()

    if args.mode == "proxy":
        run_proxy(args)
    elif args.mode == "dns":
        run_dns(args)

def proxy_checker_args(parser):
    # File and basic options
    parser.add_argument("--file", "-f", type=str, default="./data/proxies-advanced.csv", help="Path to the CSV file containing the proxies. Default: './data/proxies-advanced.csv'.")
    parser.add_argument("--delimiter", "-d", type=str, default=",", help="Delimiter used in the CSV file. Default: ','.")
    parser.add_argument("--timeout", "-t", type=int, default=5, help="Timeout for testing each proxy. Default: 5 seconds.")
    parser.add_argument("--url", "-u", type=str, default="https://www.duckduckgo.com", help="URL to test the proxy against. Default: 'https://www.duckduckgo.com'.")
    parser.add_argument("--test", action="store_true", help="Test using './data/proxies-advanced-test.csv'.")

    # Analysis options
    parser.add_argument("--analyze", action="store_true", help="Analyze the proxies to check their status.")
    parser.add_argument("--parallel", "-p", action="store_true", help="Use parallel requests to analyze proxies. Default: False.")
    parser.add_argument("--max_workers", "-mw", type=int, default=10, help="Number of worker threads for parallel requests. Effective only if --parallel is set. Default: 10.")

    # Output and display options
    parser.add_argument("--display", action="store_true", help="Display the CSV content.")
    parser.add_argument("--save", "-s", action="store_true", help="Save the analyzed CSV. Use it with --analyze.")
    parser.add_argument("--format", "-fmt", type=str, default="csv", choices=["csv", "json", "txt"], help="Output format for the saved file. Options: 'csv' or 'json'. Default: 'csv'.")
    parser.add_argument("--keep_online", action="store_true", default=True, help="Keep only the proxies with status == True in the saved CSV. Use it with --save and --analyze. Default: True.")
    parser.add_argument("--protocol", "-proto", type=str, choices=["http", "https", "socks4", "socks5"], help="Filter proxies by protocol type. Options: 'http', 'https', 'socks4', or 'socks5'. If not set, all protocols are used.")

def dns_checker_args(parser):
    parser.add_argument("--domain", "-d", type=str, default=None, help="Domain or IP address to retrieve DNS and location info. Default: None, which retrieves info for the current machine.")
    parser.add_argument("--token", "-t", type=str, default=None, help="IPINFO_TOKEN for accessing ipinfo.io. This will create/update the .env file.")

def run_proxy(args):
    # Main logic for proxy checker
    checker = ProxyChecker(args.file, delimiter=args.delimiter, timeout=args.timeout, test_url=args.url)

    if args.display:
        print("-" * 50)
        print("--- DISPLAYING CSV CONTENT ---")
        print(checker.df)
        print("-" * 50)

    if args.analyze:
        if args.parallel:
            checker.analyze_proxies_parallel(max_workers=args.max_workers)
        else:
            checker.analyze_proxies()

    if args.save and args.analyze:
        output_path = "./data/proxy-checker-output"
        if args.format == "csv":
            output_path += ".csv"
        elif args.format == "json":
            output_path += ".json"
        elif args.format == "txt":
            output_path += ".txt"

        checker.save_output(output_path, keep_online=args.keep_online, filter_protocol=args.protocol, file_format=args.format)

def run_dns(args):
    # Main logic for DNS checker
    if args.token:
        set_ipinfo_token(args.token)
        load_dotenv()  # Reload environment variable

    dns_info = DNSInfo(args.domain if args.domain else "google.com")

    if args.domain:
        print("DNS and Location Info for:", args.domain)
        print("-" * 50)
        print("IP Address:", dns_info.get_ip_address())
        print("FQDN:", dns_info.get_fqdn())
        print("Alias and IPs:", dns_info.get_alias_and_ips())
        print("Name Servers:", dns_info.get_name_servers())
        print("Location Info:", dns_info.get_location_info())
        print("-" * 50)
    else:
        print("DNS and Location Info for own machine:")
        print("-" * 50)
        print("Own DNS Info:", dns_info.get_own_dns_info())
        print("Location Info:", dns_info.get_location_info())
        print("-" * 50)