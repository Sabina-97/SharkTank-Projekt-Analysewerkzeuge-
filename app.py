import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Styling und Seiteneinstellungen
sns.set_style("whitegrid")
st.set_page_config(
    page_title="Shark Tank Analyse",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titel und Einleitung
st.title("Analyse der TV-Show Shark Tank U.S.🦈")
st.subheader("\n")
st.subheader("Was ist Shark Tank?")
st.markdown("""
**Shark Tank** ist eine US-amerikanische Reality-TV-Serie, in der Unternehmer*innen ihre Geschäftsidee vor einer Jury, 
bestehend aus Investor*innen, den sogenannten *Sharks*, präsentieren.  
Bei einem erfolgreichen Deal erhalten sie Investitionen für ihr Unternehmen.  
Die Serie wurde **2009** zum ersten Mal ausgestrahlt und umfasst mittlerweile **15 Staffeln**.
""")
st.markdown("\n")
st.subheader("Die Sharks sind:")
st.markdown("""
- **Mark Cuban**: Technologie-Investor & Besitzer des NBA-Teams Dallas Mavericks  
- **Barbara Corcoran**: Immobilienmogulin  
- **Kevin O'Leary**: Unternehmer & Finanz- und Technologieinvestor  
- **Daymond John**: Gründer der Marke FUBU  
- **Lori Greiner**: Erfinderin von QVC (Teleshopping)  
- **Robert Herjavec**: Technologieunternehmer  
- **Gastinvestor*innen**: z. B. Ashton Kutcher oder Gwyneth Paltrow
""")
st.markdown("\n")
st.subheader("Zum Ablauf der Serie:")
st.markdown("""
Unternehmer präsentieren den Sharks ihre Geschäftsidee in Form eines **Pitches**.  
Anschließend wird die **Bewertung des Unternehmens** genannt, welche das Angebot begründet.  
Das Angebot, welches von den Sharks gefordert wird, umfasst:  
- Den **Investitionsbetrag**: Wie viel Geld wird benötigt?  
- Die **abzugebenden Unternehmensanteile**.  

Je nachdem, ob die Sharks in der präsentierten Geschäftsidee Potenzial erkennen, legen sie ein Angebot vor, und es kommt bestenfalls zu einem Deal.
""")
st.markdown("\n")
st.subheader("Warum dieses Thema?")
st.markdown("""
Ich habe dieses Thema gewählt, da ich *Shark Tank* selber seit vielen Jahren schaue und mich die Statistik dazu brennend interessierte.
""")

# Daten laden und cachen
@st.cache_data
def load_data(file_path):
    """Laded Datenset und gibt Datenset zurück."""
    data = pd.read_excel(file_path)
    return data

file_path = 'sharktank_cleaned.xlsx'
data = load_data(file_path)

st.subheader("\n")
# Fragen zur Analyse
st.subheader("Folgende Fragen habe ich mir vor und im Zuge der Erarbeitung gestellt:")
st.markdown("""
1. Wieviele Deals & No-Deals gab es pro Staffel?  
2. In welche Branche wurde am wenigsten und häufigsten investiert?
3. Wie war die Geschlechterverteilung über die gesamten Staffeln hinweg? 
4. Welches Geschlecht hat die meisten Deals und No-Deals erhalten?
5. Haben die geforderten den erhaltenen Deals entsprochen? 
6. Welcher Shark hat die höchste Summe investiert? 
7. Welcher Shark hat sich am häufigsten an Kooperationen beteiligt?
8. Wer hat am meisten bzw. am wenigsten miteinander kooperiert?  
9. Was ist bis dato das erfolgreichste Produkt aller SharkTank Staffeln?  
""")

st.title("\n")
#Beginn Abschnitt Datenset-Beschreibung
st.title("Das Datenset")
st.markdown("""
            Das Datenset stammt von Kaggle und enthält Daten der Staffel 1 bis 14 von Shark Tank.
            Es umfasst 63.750 Werte.
            Im Zuge der Aufbereitung wurden nicht relevante Spalten aus dem Datenset exkludiert.
            """)

st.markdown("\n")
# Datenset-Übersicht
st.subheader("Erste Einblicke in das Datenset")
st.write(data.head())

st.markdown("\n")
# Deskriptive Statistik
st.subheader("Deskriptive Statistik")
desc_stats = data.describe(include='all').T
st.dataframe(desc_stats[['count', 'mean', 'min', 'max', 'std', '25%', '50%', '75%']])

st.markdown("\n")
st.markdown("""
Zusätzlich können folgende Fragen anhand der Daten beantwortet werden:
- Wie vielen Frauen bekamen in der ersten Staffel einen Deal?
- Wie vielen Männer scheiterten in der fünften Staffel mit ihrem Unternehmen der Branche Food & Beverage?
- Welcher von diesen forderte die höchste Investitionssumme?
""")

st.markdown("\n")
# Filteroptionen für Staffel, Branche, Geschlecht und Deal
staffel_options = data['Staffelnummer'].dropna().unique()
selected_staffel = st.multiselect(
    "Wählen Sie Staffel(n):", options=staffel_options, default=staffel_options
)
branche_options = data['Branche'].dropna().unique()
selected_branche = st.multiselect(
    "Wählen Sie Branche(n):", options=branche_options, default=branche_options
)
geschlecht_options = data['Pitcher Geschlecht'].dropna().unique()
selected_geschlecht = st.multiselect(
    "Wählen Sie Geschlecht(er):", options=geschlecht_options, default=geschlecht_options
)
deal_options = data['Deal erhalten'].dropna().unique()
selected_deal = st.multiselect(
    "Wurde ein Deal abgeschlossen?", options=deal_options, default=deal_options
)
filtered_data = data[
    (data['Staffelnummer'].isin(selected_staffel)) &
    (data['Branche'].isin(selected_branche)) &
    (data['Pitcher Geschlecht'].isin(selected_geschlecht)) &
    (data['Deal erhalten'].isin(selected_deal))
    ]

# Interaktive Tabelle
st.subheader("Gefilterte Ergebnisse")
st.dataframe(filtered_data)

# Relevante Spalten für Sharks extrahieren
shark_columns = [
    'Barbara Corcoran Investitionssumme',
    'Mark Cuban Investitionssumme',
    'Lori Greiner Investitionssumme',
    'Robert Herjavec Investitionssumme',
    'Daymond John Investitionssumme',
    'Kevin O Leary Investitionssumme',
    'Gast Investitionssumme'
]
relevant_columns = ['Name des Startups', 'Geforderter Betrag (USD)', 'Erhaltener Betrag (USD)'] + shark_columns
filtered_data = data[relevant_columns]

# Daten umstrukturieren
melted_data = filtered_data.melt(
    id_vars=['Name des Startups', 'Geforderter Betrag (USD)', 'Erhaltener Betrag (USD)'],
    value_vars=shark_columns,
    var_name='Shark',
    value_name='Investitionssumme'
)
melted_data['Shark'] = melted_data['Shark'].str.replace(' Investitionssumme', '')
shark_investments = melted_data.dropna(subset=['Investitionssumme'])


st.title("\n")
# Beginn Abschnitt Visualisierung
st.title("Die Analyse")

# Frage 1: Wieviele Deals & No-Deals gab es pro Staffel?
st.subheader("1. Wieviele Deals & No-Deals gab es pro Staffel?")
deal_counts = data.groupby(['Staffelnummer', 'Deal erhalten']).size().reset_index(name='Anzahl')
deal_counts['Deal erhalten'] = deal_counts['Deal erhalten'].replace({1: 'Deal', 0: 'No-Deal'})

# Plot
fig = px.bar(
    deal_counts,
    x='Staffelnummer',
    y='Anzahl',
    color='Deal erhalten',
    barmode='group',
    labels={'Staffelnummer': 'Staffel', 'Anzahl': 'Anzahl der Pitches'},
    title='Anzahl der Deals und No-Deals pro Staffel'
)
st.plotly_chart(fig, use_container_width=True)

# Frage 2: In welche Branche wurde am wenigsten und häufigsten investiert?
st.subheader("\n")
st.subheader("2. In welche Branche wurde am wenigsten und häufigsten investiert?")
# Ersetzen von 0 in "Deal erhalten" durch 2
data['Deal erhalten'] = data['Deal erhalten'].replace(0, 2)

# Investitionen pro Branche
branche_mit_deals = data[data['Deal erhalten'] == 1]['Branche'].value_counts().reset_index()
branche_mit_deals.columns = ['Branche', 'Anzahl Deals']
branche_ohne_deals = data[data['Deal erhalten'] == 2]['Branche'].value_counts().reset_index()
branche_ohne_deals.columns = ['Branche', 'Anzahl Deals']

# Stacked Bar Chart
fig = px.bar(
    x=branche_mit_deals['Branche'],
    y=branche_mit_deals['Anzahl Deals'],
    text=branche_mit_deals['Anzahl Deals'],
    title="Vergleich der Deals pro Branche",
    labels={'Anzahl Deals': 'Anzahl der Deals'},
)
fig.add_bar(
    x=branche_ohne_deals['Branche'],
    y=branche_ohne_deals['Anzahl Deals'],
    text=branche_ohne_deals['Anzahl Deals'],
    name='Deals ohne Investition'
)
fig.update_layout(
    xaxis_title="Branche",
    yaxis_title="Anzahl der Deals",
    showlegend=True,
    barmode='stack'
)
st.plotly_chart(fig)

# Frage 3: Wie war die Geschlechterverteilung über die gesamten Staffeln hinweg?
st.subheader("\n")
st.subheader("3. Wie war die Geschlechterverteilung über die gesamten Staffeln hinweg?")
# Pitcher Geschlecht und "Deal erhalten"
geschlecht_deal_counts = data.groupby(['Pitcher Geschlecht', 'Deal erhalten']).size().reset_index(name='Anzahl Deals')
geschlecht_deal_counts['Deal erhalten'] = geschlecht_deal_counts['Deal erhalten'].replace({1: 'Deal', 0: 'No-Deal'})

geschlechterverteilung = data['Pitcher Geschlecht'].value_counts().reset_index(name='Anzahl Pitcher')
geschlechterverteilung.columns = ['Geschlecht', 'Anzahl Pitcher']

# Plot
fig_gender_distribution = px.bar(
    geschlechterverteilung,
    x='Geschlecht',
    y='Anzahl Pitcher',
    color='Geschlecht',
    labels={'Anzahl Pitcher': 'Anzahl der Pitcher'},
    title='Geschlechterverteilung der Pitcher'
)
st.plotly_chart(fig_gender_distribution, use_container_width=True)

# Frage 4: Welches Geschlecht hat die meisten Deals und No-Deals erhalten?
st.subheader("\n")
st.subheader("4. Welches Geschlecht hat die meisten Deals und No-Deals erhalten?")
# Pitcher Geschlecht und "Deal erhalten"
geschlecht_deal_counts = data.groupby(['Pitcher Geschlecht', 'Deal erhalten']).size().reset_index(name='Anzahl Deals')

# Umwandlung 1=Deal, 2=No-Deal
geschlecht_deal_counts['Deal erhalten'] = geschlecht_deal_counts['Deal erhalten'].replace({1: 'Deal', 2: 'No-Deal'})

# Plot
fig = px.bar(
    geschlecht_deal_counts,
    x='Pitcher Geschlecht',
    y='Anzahl Deals',
    color='Deal erhalten',
    barmode='group',
    labels={'Pitcher Geschlecht': 'Geschlecht', 'Anzahl Deals': 'Anzahl der Deals'},
    title='Deals und No-Deals pro Geschlecht'
)
st.plotly_chart(fig, use_container_width=True)

# Frage 5: Haben die geforderten den erhaltenen Deals entsprochen?
st.subheader("\n")
st.subheader("5. Haben die geforderten den erhaltenen Deals entsprochen?")
column_options = ['Gebotene Anteile (%)', 'Erhaltene Anteile (%)',
                  'Geforderter Betrag (USD)', 'Geforderte Bewertung (USD)',
                  'Erhaltener Betrag (USD)', 'Bewertung anhand Deal (USD)']
selected_columns = st.multiselect("Wähle um zu vergleichen:", options=column_options, default=column_options)
filtered_data = data[selected_columns].dropna()

# Histogramms
fig = px.histogram(
    data_frame=filtered_data,
    x=selected_columns,
    title="Geforderte vs. erhaltene Deals",
    labels={col: col for col in selected_columns},
    barmode='overlay',
    opacity=0.75,
    marginal='box'
)
st.plotly_chart(fig, use_container_width=True)

# Frage 6: Welcher Shark hat die höchste Summe investiert?
st.subheader("\n")
st.subheader("6. Welcher Shark hat die höchste Summe investiert?")
investment_distribution = shark_investments.groupby('Shark')['Investitionssumme'].sum()

# Diagramm
with st.container():
    fig, ax = plt.subplots(figsize=(4, 4))
    investment_distribution.sort_values(ascending=False).plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Verteilung der Investitionen pro Shark', fontsize=11)
    ax.set_xlabel('Shark', fontsize=8)
    ax.set_ylabel('Investitionssumme (USD)', fontsize=8)

    # Dezimalformat für die y-Achse
    formatter = plt.FuncFormatter(lambda x, _: f'{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis='x', labelsize=9, rotation=90)

    # Layout unabhängig Seitenbreite
    col1, col2, col3 = st.columns([1, 2, 1])  # Spalten definieren
    with col2:  # Diagramm nur in der mittleren, schmalen Spalte
        st.pyplot(fig)

# Frage 7: Welcher Shark hat sich am häufigsten an Kooperationen beteiligt?
st.subheader("\n")
st.subheader("7. Welcher Shark hat sich am häufigsten an Kooperationen beteiligt?")
def main():
    file_path = "shark_cooperation_matrix.xlsx"
    try:
        cooperation_matrix = pd.read_excel(file_path)
    except FileNotFoundError:
        st.error("Die Excel-Datei wurde nicht gefunden. Bitte stelle sicher, dass die Datei 'shark_cooperation_matrix.xlsx' im richtigen Verzeichnis vorhanden ist.")
        return

    sharks = pd.concat([cooperation_matrix['Shark A'], cooperation_matrix['Shark B']]).unique()
    shark_cooperations = {shark: 0 for shark in sharks}
    for _, row in cooperation_matrix.iterrows():
        shark_cooperations[row['Shark A']] += row['Count']
        shark_cooperations[row['Shark B']] += row['Count']

    most_cooperative_shark = max(shark_cooperations, key=shark_cooperations.get)
    most_cooperations = shark_cooperations[most_cooperative_shark]

    # Diagramm
    with st.container():  # Damit das Diagramm nicht an die Breite der Seite angepasst wird
        fig, ax = plt.subplots(figsize=(8, 8))  # Diagrammgröße definieren
        ax.bar(shark_cooperations.keys(), shark_cooperations.values(), color='skyblue', edgecolor='black')
        ax.set_title('Anzahl der Kooperationen pro Shark', fontsize=13)
        ax.set_xlabel('Sharks', fontsize=11)
        ax.set_ylabel('Anzahl der Kooperationen', fontsize=11)
        ax.tick_params(axis='x', labelsize=11, rotation=90)

        # Layout unabhängig Seitenbreite
        col1, col2, col3 = st.columns([1, 2, 1])  # Spalten definieren
        with col2:  # Diagramm nur in der mittleren, schmalen Spalte
            st.pyplot(fig)

# Frage 8: Wer hat am meisten bzw. am wenigsten miteinander kooperiert?
    st.subheader("\n")
    st.subheader("8. Wer hat am meisten bzw. am wenigsten miteinander kooperiert?")
    total_cooperations = cooperation_matrix['Count'].sum()
    st.dataframe(cooperation_matrix, use_container_width=False)

if __name__ == "__main__":
    main()

# Frage 9: Was ist bis dato das erfolgreichste Produkt aller SharkTank Staffeln?
st.subheader("\n")
st.subheader("9. Was ist bis dato das erfolgreichste Produkt aller SharkTank Staffeln?")

# Bilder von ScrubDaddy
image_url1 = "https://miro.medium.com/v2/resize:fit:1400/0*F34FGa5k-ZG-Dh3x"
image_url2 = "https://www.bipa.at/on/demandware.static/-/Sites-catalog/de_AT/v1737030737856/original/376830.png"
col1, col2 = st.columns(2)  # Zwei Spalten
with col1:
    st.image(image_url1, caption="Gründer von ScrubDaddy", width=500)

with col2:
    st.image(image_url2, caption="Produkt ScrubDaddy", width=300)

# SrubDaddy
st.markdown("\n")
st.subheader("Die Erfolgsstory von ScrubDaddy")
st.write(
    """
    **ScrubDaddy – Die Erfolgsstory**

    **1. Was ist ScrubDaddy?**  
    ScrubDaddy ist ein innovativer Spülschwamm, der sich durch sein spezielles Material und Design auszeichnet. 
    Er passt sich je nach Druck an und reinigt effektiv empfindliche oder hartnäckige Oberflächen.

    **2. Wie entstand ScrubDaddy?**  
    Das Unternehmen wurde von Aaron Krause gegründet, der die Idee in der TV-Show *Shark Tank* vorstellte. 
    Mit Unterstützung der Investorin Lori Greiner erhielt ScrubDaddy eine starke Finanzierung und Bekanntheit.

    **3. Der Erfolg nach *Shark Tank*:**  
    Durch die Investition und das große Medieninteresse stieg die Nachfrage enorm. 
    ScrubDaddy etablierte sich weltweit als führendes Reinigungsprodukt und ist heute in großen Einzelhandelsketten 
    wie Walmart und Target erhältlich. Aber auch in Österreich sind die ScrubDaddy Produkte zahlreichen Supermärkten 
    und Drogerieketten zu finden.
    """
)

st.markdown("\n")
file_path = "sharktank_cleaned.xlsx"
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error("Die Excel-Datei wurde nicht gefunden. Bitte stelle sicher, dass die Datei 'sharktank_cleaned.xlsx' im richtigen Verzeichnis vorhanden ist.")
    st.stop()
scrubdaddy_data = df[df["Name des Startups"] == "ScrubDaddy"] # Filtere nach ScrubDaddy im Datensatz

st.markdown("\n")
if not scrubdaddy_data.empty:
    st.write("### Details zum Startup ScrubDaddy anhand Datensatz")
    st.table(scrubdaddy_data)
else:
    st.write("Es wurden keine Informationen zum Startup ScrubDaddy gefunden.")
