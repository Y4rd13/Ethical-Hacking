import re
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
        self.clients_df = pd.read_csv(self.csv_path, skiprows=start_index_clients_df, on_bad_lines='skip')
        self.clients_df.columns = [col.strip() for col in self.clients_df.columns]

    def save_as_csv(self, path_ap_df="airo-access_points.csv", path_clients_df="airo-clients.csv"):
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

        Returns
        -------
        DataFrame
            A DataFrame containing the top 'n' most vulnerable access points.
        """
        if self.ap_df is None:
            raise ValueError("Access Points DataFrame is not available. Process the CSV file first.")

        vulnerables = self.ap_df.copy()

        client_count = self.clients_df['BSSID'].value_counts()
        vulnerables['Client_Count'] = vulnerables['BSSID'].map(client_count).fillna(0)
        

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
        vulnerables['Vulnerability_Score'] += vulnerables['Privacy'].apply(lambda x: 2 if 'WPA' in x and not 'WPA2' in x and not 'WPA3' in x else 1)
        vulnerables['Vulnerability_Score'] += vulnerables['Privacy'].apply(lambda x: 3 if 'OPN' in x else 0)
        vulnerables['Vulnerability_Score'] += vulnerables['Power'].apply(lambda x: 1 if x > -50 else 0)
        max_ivs = vulnerables['# IV'].max()
        vulnerables['Vulnerability_Score'] += vulnerables['# IV'].apply(lambda x: (x / max_ivs) * 2 if max_ivs > 0 else 0)

        # Assign vulnerability level based on Vulnerability_Score
        max_score = vulnerables['Vulnerability_Score'].max()
        bins = [0, max_score*0.1, max_score*0.3, max_score*0.5, max_score*0.7, max_score*0.9, max_score, max_score*2]
        labels = ['Zero', 'Lowest', 'Low', 'Medium', 'High', 'Highest', 'Critical']
        vulnerables['Vulnerability_level'] = pd.cut(vulnerables['Vulnerability_Score'], bins=bins, labels=labels, include_lowest=True)

        # Sort by vulnerability score from highest to lowest
        top_vulnerables = vulnerables.sort_values(by='Vulnerability_Score', ascending=False).head(top_n)

        # Save to CSV if required
        if save_to_csv:
            top_vulnerables.to_csv('airo-vulnerable_access_points.csv', index=False)

        return top_vulnerables

    # def get_related_clients(self, top_vulnerables):
    #     """
    #     Obtener clientes relacionados con los puntos de acceso vulnerables más destacados.

    #     Parámetros
    #     ----------
    #     top_vulnerables : DataFrame
    #         DataFrame que contiene los puntos de acceso vulnerables más destacados.

    #     Devuelve
    #     -------
    #     DataFrame
    #         Un DataFrame que contiene los clientes relacionados con los puntos de acceso vulnerables más destacados.
    #     """
    #     if self.clients_df is None:
    #         raise ValueError("El DataFrame de clientes no está disponible. Procesa primero el archivo CSV.")

    #     # Asegurarse de que los BSSID de top_vulnerables estén en un formato que pueda ser comparado correctamente
    #     bssids_vulnerables = set(top_vulnerables['BSSID'].dropna())

    #     # Filtrar clientes basándose en los BSSID presentes en los AP vulnerables
    #     related_clients = self.clients_df[self.clients_df['BSSID'].apply(lambda x: x in bssids_vulnerables)]

    #     # Agregar un conteo de clientes para cada BSSID
    #     related_clients['Client_Count'] = related_clients.groupby('BSSID')['Station MAC'].transform('count')

    #     return related_clients

# Using the class
csv_path = "airodump_sample-01.csv"  # Replace with the path to your CSV file
handler = AirodumpHandler(csv_path)

# Process CSV
handler.process_csv()

# Display Dataframes AP and clients
handler.display_dataframes()

# Save the dataframes as CSV or JSON if desired
#handler.save_as_csv('access_points.csv', 'clients.csv')
# handler.save_as_json('access_points.json', 'clients.json')

# Top vulnerables AP
top_vulnerables = handler.top_n_vulnerables(top_n=10, client_n=1, exclude_protocol=['OPN', 'WPA'], essid_key=True, exclude_bssid=['B0:EC:DD:71:BB:48'], exclude_essid=['iphone'], save_to_csv=True)

print(f'\nTop vulnerable AP')
print(top_vulnerables)