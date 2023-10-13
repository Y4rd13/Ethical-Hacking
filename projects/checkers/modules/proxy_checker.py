import pandas as pd
import requests
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class ProxyChecker:
    def __init__(self, csv_path, delimiter=",", timeout=5, test_url="https://www.duckduckgo.com"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path, delimiter=delimiter)
        self.timeout = timeout
        self.test_url = test_url
        self.protocol_list = ["http", "https", "socks4", "socks5"]
        self.results_df = pd.DataFrame()

    def check_proxy(self, ip, port, protocol):
        proxies = {
            protocol: f"{protocol}://{ip}:{port}"
        }
        try:
            response = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
            return response.status_code == 200
        except:
            return False

    def analyze_proxies(self):
        data_to_append = []
        for index, row in tqdm(self.df.iterrows(), total=self.df.shape[0], desc="Checking proxies"):
            protocol = row['protocols'].split(",")[0].split("(")[1].split(",")[0].split("=")[1]
            ip = row['ip']
            port = row['port']
            is_active = self.check_proxy(ip, port, protocol)

            data_to_append.append({
                "ip": ip,
                "port": port,
                "status": is_active,
                "protocol": protocol,
                "updated_at": datetime.now()
            })

        self.results_df = pd.concat([self.results_df, pd.DataFrame(data_to_append)], ignore_index=True)

    def analyze_proxies_parallel(self, max_workers=10):
        """Analyze proxies using parallel requests."""

        def worker(data):
            _, row = data
            protocol = row['protocols'].split(",")[0].split("(")[1].split(",")[0].split("=")[1]
            ip = row['ip']
            port = row['port']
            is_active = self.check_proxy(ip, port, protocol)
            return {
                "ip": ip,
                "port": port,
                "status": is_active,
                "protocol": protocol,
                "updated_at": datetime.now()
            }

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(tqdm(executor.map(worker, self.df.iterrows()), total=self.df.shape[0], desc="Checking proxies in parallel"))

        self.results_df = pd.concat([self.results_df, pd.DataFrame(results)], ignore_index=True)

    def save_output(self, output_path, keep_online=False, filter_protocol=None, file_format="csv"):
        df_to_save = self.results_df.copy()
        if keep_online:
            df_to_save = df_to_save[df_to_save['status'] == True]

        if filter_protocol in self.protocol_list:
            df_to_save = df_to_save[df_to_save['protocol'].str.contains(filter_protocol)]
        
        if file_format == "csv":
            df_to_save.to_csv(output_path, index=False, encoding="utf-8", sep=",")
        elif file_format == "json":
            df_to_save.to_json(output_path, orient="records", lines=True)
        elif file_format == "txt":
            with open(output_path, "w") as f:
                for index, row in df_to_save.iterrows():
                    f.write(f"{row['protocol']}://{row['ip']}:{row['port']}\n")
