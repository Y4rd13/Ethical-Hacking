# Ethical Hacking Projects

## 📖 Table of Contents
<details>
    <summary>Click to expand</summary>

- [Ethical Hacking Projects](#ethical-hacking-projects)
  - [📖 Table of Contents](#-table-of-contents)
- [Checkers for Proxies status and DNS/IP information.](#checkers-for-proxies-status-and-dnsip-information)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Proxy Checker](#proxy-checker)
    - [DNS Checker](#dns-checker)
  - [Note](#note)

</details>

# Checkers for Proxies status and DNS/IP information.

This tool provides functionality to analyze proxies and retrieve DNS/IP information.

## Requirements

- Python 3.x
- Required libraries: `ipinfo`, `dotenv`, and other necessary libraries. Install with `pip install -r requirements.txt` (You'd need to create this file).

## Usage

You can choose between the proxy checker and the DNS checker by using the `--proxy` or `--dns` flags respectively.

### Proxy Checker

To analyze proxies, check their status, and save the results:

```bash
python main.py proxy --analyze -p -mw 50 --save --keep_online --test --protocol "socks5" --format "txt"
```

Arguments:
- `--file, -f`: Path to the CSV file containing the proxies. Default: `./data/static/proxies-advanced.csv`
- `--delimiter, -d`: Delimiter used in the CSV file. Default: `,`
- `--timeout, -t`: Timeout for testing each proxy. Default: 5 seconds.
- `--url, -u`: URL to test the proxy against. Default: `https://www.duckduckgo.com`
- `--test`: Test using `./data/static/proxies-advanced-test.csv`
- `--analyze`: Analyze the proxies to check their status.
- `--parallel, -p`: Use parallel requests to analyze proxies.
- `--max_workers, -mw`: Number of worker threads for parallel requests. Default: 10.
- `--display`: Display the CSV content.
- `--save, -s`: Save the analyzed CSV. Use it with `--analyze`.
- `--format, -fmt`: Output format for the saved file. Options: `csv`, `json`, `txt`. Default: `csv`.
- `--keep_online`: Keep only the proxies with status == True in the saved CSV. Default: True.
- `--protocol, -proto`: Filter proxies by protocol type. Options: `http`, `https`, `socks4`, `socks5`.

### DNS Checker


1. Set the token for ipinfo.io:
```bash
pthon main.py dns --token "{YOUR_TOKEN}"
``` 

2. To retrieve DNS and location information:

```bash
python main.py dns --domain "duckduckgo.com"
```

3. To retrive your own DNS and location information:

```bash
python main.py dns
```

4. To retrieve DNS and location information and save it to a file as json:

```bash
python main.py dns --domain "duckduckgo.com" --save
```

Arguments:
- `--domain, -d`: Domain or IP address to retrieve DNS and location info. Default: None (which retrieves info for the current machine).
- `--token, -t`: IPINFO_TOKEN for accessing ipinfo.io. This will create/update the .env file.
- `--save`: Save the DNS and location info as a JSON file.

## Note

Make sure to have the required environment variables set up, especially if you're using third-party services like ipinfo.io.
