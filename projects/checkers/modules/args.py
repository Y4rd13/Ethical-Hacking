from .proxy_checker import ProxyChecker
from .dns_checker import DNSInfo, set_ipinfo_token
import json
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
    parser.add_argument("--file", "-f", type=str, default="./data/static/proxies-advanced.csv", help="Path to the CSV file containing the proxies. Default: './data/static/proxies-advanced.csv'.")
    parser.add_argument("--delimiter", "-d", type=str, default=",", help="Delimiter used in the CSV file. Default: ','.")
    parser.add_argument("--timeout", "-t", type=int, default=5, help="Timeout for testing each proxy. Default: 5 seconds.")
    parser.add_argument("--url", "-u", type=str, default="https://www.duckduckgo.com", help="URL to test the proxy against. Default: 'https://www.duckduckgo.com'.")
    parser.add_argument("--test", action="store_true", help="Test using './data/static/proxies-advanced-test.csv'.")

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
    parser.add_argument("--save", action="store_true", help="Save the DNS and location info as a JSON file.")

def run_proxy(args):
    # Main logic for proxy checker

    if args.test:
        args.file = "./data/static/proxies-advanced-test.csv"

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
        output_path = "./data/output/proxy-checker-output"
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
        print('IPINFO_TOKEN set successfully.')
        
    else:
        dns_info = DNSInfo(args.domain if args.domain else "duckduckgo.com")
        if args.domain:
            output_data = {
                "domain": args.domain,
                "info":{
                    "ip_address": dns_info.get_ip_address(),
                    "fqdn": dns_info.get_fqdn(),
                    "alias_and_ips": dns_info.get_alias_and_ips(),
                    "name_servers": dns_info.get_name_servers(),
                    "location": dns_info.get_location_info()
                }
            }
        else:
            output_data = {
                "domain": args.domain,
                "info":{
                    "own_dns": dns_info.get_own_dns_info(),
                    "location": dns_info.get_location_info()
                }
            }

        # Display the information
        for key, value in output_data.items():
            print(f"{key}: {value}")
            print("-" * 50)

        # Save to JSON if --save is set
        if args.save:
            output_path = f"./data/output/dns_info_{args.domain if args.domain else 'own'}.json"
            with open(output_path, 'w') as json_file:
                json.dump(output_data, json_file, indent=4)
            print(f"Saved DNS and Location Info to {output_path}")