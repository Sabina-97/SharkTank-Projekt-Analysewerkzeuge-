import pandas as pd
import numpy as np
from itertools import combinations
from pathlib import Path

# Klasse zur Verarbeitung der Shark Tank-Daten
class SharkTankProcessor:
    def __init__(self, file_path):
        """
        Initialisiert die Klasse mit dem angegebenen Datei-Pfad.
        Parameters:
        - file_path (str): Der Pfad zur Excel-Datei mit den Shark Tank-Daten.
        """
        self.file_path = Path(file_path).resolve()
        self.sharktank = None

    def load_data(self):
        """
        Lädt das Shark Tank-Datenset aus der angegebenen Excel-Datei.
        Wenn die Datei existiert, wird sie als DataFrame geladen. Falls die Datei
        nicht gefunden wird, wird ein Fehler angezeigt.
        """
        if self.file_path.exists():
            self.sharktank = pd.read_excel(self.file_path)
            print("Data loaded successfully.")
        else:
            print(f"File not found: {self.file_path}")
            print(f"Current working directory: {Path().cwd()}")

    # Datenbereinigung und Spaltenumbenennung
    def clean_data(self, columns_to_drop, rename_columns):
        """
        Bereinigt die Daten, indem irrelevante Spalten entfernt und umbenannt werden.
        Parameters:
        - columns_to_drop (list): Liste der Spalten, die entfernt werden sollen.
        - rename_columns (dict): Wörterbuch, das Spaltennamen umbenennt.
        """
        if self.sharktank is not None:
            self.sharktank = self.sharktank.drop(columns=columns_to_drop, errors='ignore')
            self.sharktank = self.sharktank.rename(columns=rename_columns)
            self.sharktank['Pitcher Bundesstaat'] = self.sharktank['Pitcher Bundesstaat'].fillna('Unbekannt')
            self.sharktank['Pitcher Geschlecht'] = self.sharktank['Pitcher Geschlecht'].fillna('Unbekannt')
            print("Data cleaned and columns renamed successfully.")

    # Ersetze leere Werte mit 'N/A'
    def replace_empty_with_na(self):
        """
        Ersetzt leere Werte in bestimmten Spalten mit 'N/A'.
        """
        specific_columns = [
            'Barbara Corcoran Investitionssumme', 'Barbara Corcoran Kapitalbeteiligung',
            'Mark Cuban Investitionssumme', 'Mark Cuban Kapitalbeteiligung',
            'Lori Greiner Investitionssumme', 'Lori Greiner Kapitalbeteiligung',
            'Robert Herjavec Investitionssumme', 'Robert Herjavec Kapitalbeteiligung',
            'Daymond John Investitionssumme', 'Daymond John Kapitalbeteiligung',
            'Kevin O Leary Investitionssumme', 'Kevin O Leary Kapitalbeteiligung',
            'Gast Investitionssumme', 'Gast Kapitalbeteiligung'
        ]
        for col in specific_columns:
            if col in self.sharktank.columns:
                self.sharktank[col] = self.sharktank[col].replace([np.nan, '', None], 'N/A')
        print("Replaced empty values with 'N/A' in specific columns.")

    # Investitionen und Beteiligungen der Sharks
    def summarize_shark_data(self):
        """
        Diese Methode berechnet die Gesamtsummen der Investitionen und Beteiligungen für die Sharks und Gäste.
        Die Methode erstellt zwei Listen: eine mit den Namen der Sharks und eine weitere mit den Spaltennamen für die Investitionssummen und Kapitalbeteiligungen.
        Anschließend wird für jede Shark und auch für die Gäste die Summe der Investitionen und Beteiligungen berechnet.
        Returns:
            dict: Ein Dictionary, das für jede Shark und die Gäste die Total Investment (USD) und Total Equity (%) enthält.
        """
        sharks = [
            'Barbara Corcoran', 'Mark Cuban', 'Lori Greiner', 'Robert Herjavec',
            'Daymond John', 'Kevin O Leary'
        ]
        investment_cols = [f'{shark} Investitionssumme' for shark in sharks]
        equity_cols = [f'{shark} Kapitalbeteiligung' for shark in sharks]

        for col in investment_cols + equity_cols + ['Gast Investitionssumme', 'Gast Kapitalbeteiligung']:
            if col in self.sharktank.columns:
                self.sharktank[col] = pd.to_numeric(
                    self.sharktank[col].replace('N/A', np.nan), errors='coerce'
                )
        # Gesamtsummen der Investitionen und Beteiligungen für jede Shark
        shark_totals = {
            shark: {
                'Total Investment (USD)': self.sharktank[invest_col].sum(skipna=True),
                'Total Equity (%)': self.sharktank[equity_col].sum(skipna=True)
            }
            for shark, invest_col, equity_col in zip(sharks, investment_cols, equity_cols)
        }
        # Summen für die Gäste
        shark_totals['Guests'] = {
            'Total Investment (USD)': self.sharktank['Gast Investitionssumme'].sum(skipna=True),
            'Total Equity (%)': self.sharktank['Gast Kapitalbeteiligung'].sum(skipna=True)
        }

        return shark_totals

    #Erstellung der Zusammenarbeitsmatrix der Sharks
    def generate_cooperation_matrix(self):
        """
        Diese Methode berechnet die Zusammenarbeit zwischen den Sharks basierend auf den getätigten Investitionen.
        Die Methode iteriert durch jede Zeile des Datenrahmens, ruft eine Hilfsfunktion auf, die die Kombinationen der Sharks in den Investitionen berechnet,
        und speichert diese in einer Liste. Anschließend wird eine Zusammenarbeitsmatrix erstellt, die die Häufigkeiten der gemeinsamen Investitionen zeigt.
        Returns:
            pd.DataFrame: Eine DataFrame-Tabelle, die die Kooperationen zwischen den Sharks und die Anzahl der gemeinsamen Investitionen darstellt.
        """
        def calculate_cooperations(row):
            sharks = [
                'Barbara Corcoran', 'Mark Cuban', 'Lori Greiner', 'Robert Herjavec',
                'Daymond John', 'Kevin O Leary'
            ]
            participants = [shark for shark in sharks if pd.notnull(row[f'{shark} Investitionssumme'])]
            return list(combinations(participants, 2))

        cooperations = []
        for _, row in self.sharktank.iterrows():
            cooperations.extend(calculate_cooperations(row))

        cooperation_counts = pd.DataFrame(cooperations, columns=['Shark A', 'Shark B'])
        cooperation_matrix = cooperation_counts.value_counts().reset_index()
        cooperation_matrix.columns = ['Shark A', 'Shark B', 'Count']
        return cooperation_matrix

    # Speichern der verarbeiteten Daten
    def save_data(self, new_file_name):
        """
        Diese Methode speichert die verarbeiteten Daten in einer Excel-Datei.
        Die Methode überprüft, ob der Datenrahmen `self.sharktank` nicht None ist, und schreibt die Daten in eine Excel-Datei an dem angegebenen Pfad.
        Args:
            new_file_name (str): Der Name der neuen Excel-Datei, in der die Daten gespeichert werden.
        Returns:
            None
        """
        if self.sharktank is not None:
            save_path = Path(new_file_name).resolve()
            self.sharktank.to_excel(save_path, index=False)
            print(f"Data saved successfully to {save_path}.")

# Spalten zu entfernt und umbenannt
columns_to_drop = [
    "Season Start", "Season End", "Episode Number", "Pitch Number", "Original Air Date",
    "Business Description", "Pitchers City", "Pitchers Average Age", "Entrepreneur Names",
    "Company Website", "Multiple Entrepreneurs", "US Viewership",
    "Royality Deal", "Investment Amount Per Shark", "Equity Per Shark", "Royalty Deal", "Loan", "Barbara Corcoran Present", "Mark Cuban Present",
    "Lori Greiner Present", "Robert Herjavec Present", "Daymond John Present",
    "Kevin O Leary Present"
]
rename_columns = {
    "Season Number": "Staffelnummer",
    "Startup Name": "Name des Startups",
    "Industry": "Branche",
    "Pitchers Gender": "Pitcher Geschlecht",
    "Pitchers State": "Pitcher Bundesstaat",
    "Original Ask Amount": "Geforderter Betrag (USD)",
    "Original Offered Equity": "Gebotene Anteile (%)",
    "Valuation Requested": "Geforderte Bewertung (USD)",
    "Got Deal": "Deal erhalten",
    "Total Deal Amount": "Erhaltener Betrag (USD)",
    "Total Deal Equity": "Erhaltene Anteile (%)",
    "Deal Valuation": "Bewertung anhand Deal (USD)",
    "Number of sharks in deal": "Anzahl der Sharks bei Deal",
    "Barbara Corcoran Investment Amount": "Barbara Corcoran Investitionssumme",
    "Barbara Corcoran Investment Equity": "Barbara Corcoran Kapitalbeteiligung",
    "Mark Cuban Investment Amount": "Mark Cuban Investitionssumme",
    "Mark Cuban Investment Equity": "Mark Cuban Kapitalbeteiligung",
    "Lori Greiner Investment Amount": "Lori Greiner Investitionssumme",
    "Lori Greiner Investment Equity": "Lori Greiner Kapitalbeteiligung",
    "Robert Herjavec Investment Amount": "Robert Herjavec Investitionssumme",
    "Robert Herjavec Investment Equity": "Robert Herjavec Kapitalbeteiligung",
    "Daymond John Investment Amount": "Daymond John Investitionssumme",
    "Daymond John Investment Equity": "Daymond John Kapitalbeteiligung",
    "Kevin O Leary Investment Amount": "Kevin O Leary Investitionssumme",
    "Kevin O Leary Investment Equity": "Kevin O Leary Kapitalbeteiligung",
    "Guest Investment Amount": "Gast Investitionssumme",
    "Guest Investment Equity": "Gast Kapitalbeteiligung",
    "Guest Name": "Name des Gastes"
}

file_path = Path('sharktank.xlsx').resolve()

# Bereinigtes File erstellen und Daten laden
processor = SharkTankProcessor(file_path)
processor.load_data()

# Daten bereinigen und Umbenennen
processor.clean_data(columns_to_drop, rename_columns)

# Leerwerte durch NaN ersetzen
processor.replace_empty_with_na()

# Zusammenfassung der Investitionen der Sharks
shark_summary = processor.summarize_shark_data()
cooperation_matrix = processor.generate_cooperation_matrix()

# Bereinigte Daten speichern
processor.save_data('sharktank_cleaned.xlsx')

# Zusammenarbeitsmatrix speichern
cooperation_matrix_path = Path('shark_cooperation_matrix.xlsx').resolve()
cooperation_matrix.to_excel(cooperation_matrix_path, index=False)
print(f"Cooperation matrix saved to {cooperation_matrix_path}.")
