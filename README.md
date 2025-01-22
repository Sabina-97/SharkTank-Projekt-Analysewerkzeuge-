# Analyse von Investitionsdaten aus der TV-Show Shark Tank U.S.

## Projektbeschreibung

Shark Tank U.S. ist eine Reality-TV-Show, in der Unternehmer ihre Ideen und Geschäftsmodelle prominenten Investoren, den sogenannten „Sharks“, vorstellen. Ziel der Show ist es, einen Deal zu erzielen, bei dem die Sharks in das vorgestellte Unternehmen investieren. 

## Ziel des Projekts

Ziel dieses Projekts ist es, mit Hilfe von statistischen und analytischen Werkzeugen mögliche Muster in den Investitionen und Entscheidungen der Sharks zu erkennen.

Die folgenden Fragen wurden erarbeitet:
1. Wieviele Deals & No-Deals gab es pro Staffel?  
2. In welche Branche wurde am wenigsten und häufigsten investiert?
3. Wie war die Geschlechterverteilung über die gesamten Staffeln hinweg? 
4. Welches Geschlecht hat die meisten Deals und No-Deals erhalten?
5. Haben die geforderten den erhaltenen Deals entsprochen? 
6. Welcher Shark hat die höchste Summe investiert? 
7. Welcher Shark hat sich am häufigsten an Kooperationen beteiligt?
8. Wer hat am meisten bzw. am wenigsten miteinander kooperiert?  
9. Was ist bis dato das erfolgreichste Produkt aller SharkTank Staffeln?  

## Verwendete Pakete

- python==3.12.8
- pandas==2.2.3
- numpy==2.2.1
- streamlit==1.41.1
- seaborn==0.13.2
- matplotlib==3.10.0
- plotly==5.24.1
- openpyxl==3.1.5

## Datenquellen

Die folgenden Daten werden für die Analyse verwendet:
- SharkTank Dataset von Kaggle (https://www.kaggle.com/datasets/arpitsinghaiml/shark-tank-u-s-seasons-1-14?select=Shark+tank.xlsx)

## Beschreibung des Datensatzes

Das Datenset stammt von Kaggle und enthält Daten der Staffel 1 bis 14 von Shark Tank.
Es umfasst 1275 Zeilen, 50 Spalten und etwas über 63.750 Werte.

Zur besseren Auswertung wurde der Datensatz bereinigt.
Die zentralen Spalten sind:
- Staffelnummer
- Name des Startups
- Branche
- Pitcher Geschlecht
- Pitcher Bundesstaat
- Geforderter Betrag (USD)
- Gebotene Anteile (%)
- Geforderte Bewertung (USD)
- Deal erhalten (Ja/Nein)
- Erhaltener Betrag (USD)
- Erhaltene Anteile (%)
- Bewertung anhand Deal (USD)
- Anzahl der Sharks bei Deal
- Barbara Corcoran Investitionssumme
- Barbara Corcoran Kapitalbeteiligung
- Mark Cuban Investitionssumme
- Mark Cuban Kapitalbeteiligung
- Lori Greiner Investitionssumme
- Lori Greiner Kapitalbeteiligung
- Robert Herjavec Investitionssumme
- Robert Herjavec Kapitalbeteiligung
- Daymond John Investitionssumme
- Daymond John Kapitalbeteiligung
- Kevin O Leary Investitionssumme
- Kevin O Leary Kapitalbeteiligung
- Gast Investitionssumme
- Gast Kapitalbeteiligung
- Name des Gastes

## Methodik

Für die Analyse werden die folgenden Schritte durchgeführt:
1. Bereinigung der Daten
2. Explorative Datenanalyse
3. Visualisierung der Ergebnisse

## Verarbeitungsschritte

1. Verarbeitung und Analyse von Shark Tank-Daten  
   1.1. Initialisierung  
   1.2. Daten laden  
   1.3. Datenbereinigung und Umbenennung  
   1.4. Ersetzen von leeren Werten  
   1.5. Zusammenfassung der Investitionen der Sharks  
   1.6. Erstellung der Zusammenarbeit-Matrix  
   1.7. Speichern der verarbeiteten Daten  

2. Datenvisualisierung von Shark Tank-Daten  
   2.1 Seitenlayout und Design  
   2.2 Daten laden  
   2.3 Einleitung und Ziel der Analyse  
   2.4 Fragen zur Analyse  
   2.5 Datenset-Beschreibung  
   2.6 Grundlegende Datenanalyse  
   2.7 Daten filtern  
   2.8 Interaktive Datenanzeige  
   2.9 Relevante Daten für Sharks  
   2.10 Visualisierungen erstellen  
   2.11 Diagramme und Vergleiche  
   2.12 Erfolggeschichte von SharkTank  

