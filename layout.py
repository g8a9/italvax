import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import requests


LAST_UPDATE_URL = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/last-update-dataset.json"
REPO_URL = "https://github.com/italia/covid19-opendata-vaccini"


def last_update():
    r = json.loads(requests.get(LAST_UPDATE_URL).content)


HEADER = dbc.Row(dbc.Col(html.H1("ItalVax"), className="text-center"))

NOTE = dbc.Row(
    dbc.Col(
        [
            dbc.Alert(
                f"""
                I dati sono forniti dal Commissario straordinario per l'emergenza COVID19
                (Presidenza del Consiglio dei Ministri) e sono disponibili qui: {REPO_URL}.""",
                color="primary",
            ),
            dbc.Alert(
                f"""
                Per comodita' nella visualizzazione di alcuni grafici, i dati
                raccolti per la 
                Provincia Autonoma di Trento e la Provincia Autonoma di Bolzano sono
                stati aggregati sotto l'entita' Trentino Alto Adige.""",
                color="primary",
            ),
        ],
        # className="text-center",
    )
)
