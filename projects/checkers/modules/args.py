from .proxy_checker import ProxyChecker
import argparse

def proxy_checker_args():
    parser = argparse.ArgumentParser(description="A tool to check and analyze proxy status from a CSV file.")
    
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


    # Parsear arguments
    args = parser.parse_args()

    # Main
    if args.test:
        args.file = "./data/proxies-advanced-test.csv"

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
            output_path = f"{output_path}.csv"
        elif args.format == "json":
            output_path = f"{output_path}.json"

        elif args.format == "txt":
            output_path = f"{output_path}.txt"

        checker.save_output(output_path, keep_online=args.keep_online, filter_protocol=args.protocol, file_format=args.format)