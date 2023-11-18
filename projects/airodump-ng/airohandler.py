import re
import json
import argparse
import pandas as pd

class AirodumpHandler:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.ap_df = None  # Access Points DataFrame
        self.clients_df = None  # Clients DataFrame

    def process_csv(self):
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Find start indexes for each section
        start_index_clients_df = None
        for i, line in enumerate(lines):
            if 'Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs' in line:
                start_index_clients_df = i
                break

        if start_index_clients_df is None:
            raise ValueError("Section for the clients dataframe not found.")

        self.ap_df = pd.read_csv(self.csv_path, skiprows=1, nrows=start_index_clients_df - 2, on_bad_lines='skip')
        self.ap_df.columns = [col.strip() for col in self.ap_df.columns]
        self.ap_df['BSSID'] = self.ap_df['BSSID'].apply(lambda x: x.strip())

        self.clients_df = pd.read_csv(self.csv_path, skiprows=start_index_clients_df, on_bad_lines='skip')
        self.clients_df.columns = [col.strip() for col in self.clients_df.columns]
        self.clients_df['BSSID'] = self.clients_df['BSSID'].apply(lambda x: x.strip())
        # print(self.ap_df['BSSID'].to_list())
        # print(self.clients_df['BSSID'].to_list())

    def save_as_csv(self, path_ap_df="./output/airo-access_points.csv", path_clients_df="./output/airo-clients.csv"):
        if self.ap_df is not None and self.clients_df is not None:
            self.ap_df.to_csv(path_ap_df, index=False)
            self.clients_df.to_csv(path_clients_df, index=False)
        else:
            raise ValueError("You must process the CSV file first.")

    def save_as_json(self, path_ap_df, path_clients_df):
        if self.ap_df is not None and self.clients_df is not None:
            self.ap_df.to_json(path_ap_df, orient='records', lines=True)
            self.clients_df.to_json(path_clients_df, orient='records', lines=True)
        else:
            raise ValueError("You must process the CSV file first.")

    def display_dataframes(self):
        if self.ap_df is not None:
            print("Access Points DataFrame:\n", self.ap_df.head())
        else:
            print("Access Points DataFrame is not available.")
        
        if self.clients_df is not None:
            print("Clients DataFrame:\n", self.clients_df.head())
        else:
            print("Clients DataFrame is not available.")

    def top_n_vulnerables(self, top_n=5, save_to_csv=False, exclude_protocol=[], essid_key=False, exclude_bssid=[], exclude_essid=[], client_n=None):
        """
        Identify the top 'n' most vulnerable access points based on various criteria.

        Parameters
        ----------
        top_n : int
            Number of top vulnerable access points to return.
        save_to_csv : bool
            If True, saves the result to a CSV file.
        exclude_protocol : list
            List of encryption protocols to exclude.
        essid_key : bool
            If True, only includes networks with a non-empty ESSID.
        exclude_bssid : list
            List of BSSIDs to exclude.
        exclude_essid : list
            List of regular expressions to exclude specific ESSIDs.
        client_n : int or None
            Minimum number of clients required for an access point to be considered.

        Returns
        -------
        DataFrame
            A DataFrame containing the top 'n' most vulnerable access points.
        """
        if self.ap_df is None or self.clients_df is None:
            raise ValueError("DataFrames are not available. Process the CSV file first.")

        # Filter by common BSSIDs
        df_ap_filtered, df_cli_filtered = self.filter_by_common_bssid()

        # Count the number of clients associated with each BSSID
        client_count = df_cli_filtered['BSSID'].value_counts()
        df_ap_filtered['Client_Count'] = df_ap_filtered['BSSID'].map(client_count).fillna(0)

        # Filter APs with at least client_n clients if client_n is not None
        if client_n is not None:
            df_ap_filtered = df_ap_filtered[df_ap_filtered['Client_Count'] >= client_n]

        # Apply additional filters to the filtered AP DataFrame
        vulnerables = df_ap_filtered.copy()

        # Exclude specific protocols using exact match
        for protocol in exclude_protocol:
            regex_pattern = r'\b' + protocol + r'\b'  # Using word boundaries to match the whole word
            vulnerables = vulnerables[~vulnerables['Privacy'].str.contains(regex_pattern, regex=True)]

        # Include only networks with ESSID if essid_key is True
        if essid_key:
            vulnerables = vulnerables[vulnerables['ESSID'].str.strip() != '']

        # Exclude specific BSSIDs
        vulnerables = vulnerables[~vulnerables['BSSID'].isin(exclude_bssid)]

        # Ensure ESSID is a string and Exclude ESSIDs based on regular expressions
        vulnerables['ESSID'] = vulnerables['ESSID'].astype(str)
        for pattern in exclude_essid:
            vulnerables = vulnerables[~vulnerables['ESSID'].str.contains(pattern, flags=re.IGNORECASE, regex=True, na=False)]

        # Assign a vulnerability score
        vulnerables['Vulnerability_Score'] = 0
        vulnerables['Vulnerability_Score'] += vulnerables.apply(self.score_privacy_cipher, axis=1)
        vulnerables['Vulnerability_Score'] += vulnerables['Power'].apply(self.score_power)
        vulnerables['Vulnerability_Score'] += vulnerables.apply(self.score_visibility_duration, axis=1)
        vulnerables['Vulnerability_Score'] += vulnerables['Speed'].apply(self.score_speed)
        vulnerables['Vulnerability_Score'] += vulnerables.apply(self.score_iv_beacons, axis=1)
        vulnerables['Vulnerability_Score'] += vulnerables.apply(self.score_essid_key, axis=1)

        # Assign vulnerability level based on Vulnerability_Score
        max_score = vulnerables['Vulnerability_Score'].max()
        bins = [0, max_score*0.1, max_score*0.2, max_score*0.4, max_score*0.6, max_score*0.8, max_score, max_score*1.2]
        labels = ['Zero', 'Very Low', 'Low', 'Medium', 'High', 'Very High', 'Critical']
        vulnerables['Vulnerability_level'] = pd.cut(vulnerables['Vulnerability_Score'], bins=bins, labels=labels, include_lowest=True)

        # Sort by vulnerability score from highest to lowest
        top_vulnerables = vulnerables.sort_values(by='Vulnerability_Score', ascending=False)

        if top_n:
            top_vulnerables = top_vulnerables.head(top_n)

        # Save to CSV if required
        if save_to_csv:
            top_vulnerables.to_csv('output/airo-vulnerable_access_points.csv', index=False)

        return top_vulnerables

    def filter_by_common_bssid(self):
        """
        Filters the access point and client dataframes based on common BSSIDs.

        :return: Two filtered DataFrames, one for access points and one for clients.
        """
        df_ap = self.ap_df
        df_cli = self.clients_df

        # Filter the client dataframe to exclude those not associated with a BSSID
        df_cli_filtered = df_cli[df_cli['BSSID'] != '(not associated)']

        # Find common BSSIDs between access points and clients
        common_bssids = set(df_ap['BSSID']).intersection(set(df_cli_filtered['BSSID']))

        # Filter the dataframes based on common BSSIDs
        df_ap_filtered = df_ap[df_ap['BSSID'].isin(common_bssids)]
        df_cli_filtered = df_cli_filtered[df_cli_filtered['BSSID'].isin(common_bssids)]

        return df_ap_filtered, df_cli_filtered

    @staticmethod
    def score_privacy_cipher(row):
        privacy_score = 0
        if 'WEP' in row['Privacy']:
            privacy_score = 10
        elif 'WPA' in row['Privacy']:
            if 'WPA2' not in row['Privacy']:
                privacy_score = 7
            else:
                privacy_score = 5
        elif 'OPN' in row['Privacy']:
            privacy_score = 10
        if 'CCMP' in row['Cipher']:
            privacy_score -= 2
        elif 'TKIP' in row['Cipher']:
            privacy_score -= 1
        if 'PSK' in row['Authentication']:
            privacy_score += 1
        return max(privacy_score, 0)

    @staticmethod
    def score_power(power):
        if power > -50:
            return 4
        elif power > -70:
            return 2
        else:
            return 1

    @staticmethod
    def score_visibility_duration(row):
        first_seen = pd.to_datetime(row['First time seen'])
        last_seen = pd.to_datetime(row['Last time seen'])
        duration = (last_seen - first_seen).total_seconds()
        return min(duration / 3600, 5)  # Máximo 5 puntos por duración

    @staticmethod
    def score_speed(speed):
        if speed <= 54:  # 802.11g o inferior
            return 4
        elif speed <= 150:  # 802.11n
            return 2
        else:  # Velocidades más altas
            return 1

    @staticmethod
    def score_iv_beacons(row):
        iv_score = min(row['# IV'] / 1000, 5)  # Máximo 5 puntos
        beacon_score = min(row['# beacons'] / 1000, 3)  # Máximo 3 puntos
        return iv_score + beacon_score

    @staticmethod
    def score_essid_key(row):
        essid_score = 0
        common_essids = ['default', 'linksys', 'netgear', 'dlink', 'tplink']
        if any(essid in row['ESSID'].lower() for essid in common_essids):
            essid_score += 3
        if row['Key'] == '':
            essid_score += 2
        return essid_score

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Process and analyze Airodump CSV data.")
        parser.add_argument("--csv_path", help="Path to the Airodump CSV file. Only required without --start.")
        parser.add_argument("-s", "--show", action="store_true", help="Display the top rows of the Access Points and Clients DataFrames.")
        parser.add_argument("--save", choices=['csv', 'json'], help="Save the processed data in either CSV or JSON format. Saved in output as airo-client.csv and airo-access_points.csv")
        parser.add_argument("-t", "--top_n", type=int, default=5, help="Display the top N most vulnerable access points.")
        parser.add_argument("-ep", "--exclude_protocol", nargs='*', default=[], help="List of encryption protocols to exclude.")
        parser.add_argument("-ek", "--essid_key", action="store_true", help="Include only networks with a non-empty ESSID.")
        parser.add_argument("-eb", "--exclude_bssid", nargs='*', default=[], help="List of BSSIDs to exclude.")
        parser.add_argument("-ee", "--exclude_essid", nargs='*', default=[], help="List of regular expressions to exclude specific ESSIDs.")
        parser.add_argument("-cn", "--client_n", type=int, help="Minimum number of clients required for an access point to be considered.")
        parser.add_argument("--start", action="store_true", help="Start AirodumpHandler from config.json configuration file.")

        return parser.parse_args()


if __name__ == "__main__":
    args = AirodumpHandler.parse_arguments()

    if args.start:
        with open("./config.json", 'r') as file:
            config = json.load(file)

            csv_path = config['csv_path']
    else:
        csv_path = args.csv_path


    handler = AirodumpHandler(csv_path)
    handler.process_csv()

    if args.show:
        handler.display_dataframes()

    if args.save == 'csv':
        handler.save_as_csv()
    elif args.save == 'json':
        handler.save_as_json()

    if args.top_n:
        top_vulnerables = handler.top_n_vulnerables(top_n=args.top_n,
                                                    client_n=args.client_n,
                                                    exclude_protocol=args.exclude_protocol,
                                                    essid_key=args.essid_key,
                                                    exclude_bssid=args.exclude_bssid,
                                                    exclude_essid=args.exclude_essid)
        print(f'\nTop {args.top_n} Vulnerable Access Points:\n', top_vulnerables)
    
    if args.start:
        top_vulnerables = handler.top_n_vulnerables(top_n=config.get('top_n', 5),
                        save_to_csv=config.get('save_to_csv', False),
                        exclude_protocol=config.get('exclude_protocol', []),
                        essid_key=config.get('essid_key', False),
                        exclude_bssid=config.get('exclude_bssid', []),
                        exclude_essid=config.get('exclude_essid', []),
                        client_n=config.get('client_n', None))
        print(f'\nTop {args.top_n} Vulnerable Access Points:\n', top_vulnerables)