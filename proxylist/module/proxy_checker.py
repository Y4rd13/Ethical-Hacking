import pandas as pd
import requests
from datetime import datetime
from tqdm import tqdm
import argparse

class ProxyChecker:
    def __init__(self, csv_path, timeout=5, test_url="https://www.duckduckgo.com"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.timeout = timeout
        self.test_url = test_url
    
    def check_proxy(self, ip, port, protocol):
        proxies = {
            protocol: f"{protocol}://{ip}:{port}"
        }
        try:
            # Intentamos obtener la página de inicio de Google solo para comprobar la conectividad.
            response = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
            return response.status_code == 200
        except:
            return False
    
    def analyze_proxies(self):
        status_list = []
        updated_at_list = []

        # Usar tqdm para mostrar una barra de progreso
        for index, row in tqdm(self.df.iterrows(), total=self.df.shape[0], desc="Checking proxies"):
            # Tomamos el primer protocolo disponible para la prueba.
            protocol = row['protocols'].split(",")[0].split("(")[1].split(",")[0].split("=")[1]
            ip = row['ip']
            port = row['port']
            is_active = self.check_proxy(ip, port, protocol)

            status_list.append(is_active)
            updated_at_list.append(datetime.now())

        self.df['status'] = status_list
        self.df['updated_at'] = updated_at_list

    def save_to_csv(self, output_csv_path):
        self.df.to_csv(output_csv_path, index=False, encoding="utf-8", sep=",")


def main_args():
    parser = argparse.ArgumentParser(description="A tool to check and analyze proxy status from a CSV file.")
    
    parser.add_argument("--display", action="store_true", help="Display the CSV content.")
    parser.add_argument("--analyze", action="store_true", help="Analyze the proxies to check their status.")
    parser.add_argument("--save", action="store_true", help="Save the analyzed CSV. Use it with --analyze.")
    parser.add_argument("--timeout", "-t", type=int, default=5, help="Set the timeout for testing each proxy. Default is 5 seconds.")
    parser.add_argument("--url", "-u", type=str, default="https://www.duckduckgo.com", help="Set the URL to test the proxy against. Default is https://www.duckduckgo.com.")

    args = parser.parse_args()

    checker = ProxyChecker("proxies-advanced.csv", timeout=args.timeout, test_url=args.url)

    if args.display:
        print(checker.df)

    if args.analyze:
        checker.analyze_proxies()

    if args.save and args.analyze:
        checker.save_to_csv("proxies-advanced-status.csv")