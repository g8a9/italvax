import dash
import dash_core_components as dcc
from dash_core_components import Graph
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_bootstrap_components import Row, Col, Card

import plotly.express as px
import pandas as pd
import json
from charts import *
from layout import *


# Data retrieval and preprocessing

VACCINI_SUMMARY_URL = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv"
SOMM_VACC_LATEST = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"
REGION_CODE_NAME = {
    "ABR": "abruzzo",
    "BAS": "basilicata",
    "CAL": "calabria",
    "CAM": "campania",
    "EMR": "emilia-romagna",
    "FVG": "friuli venezia giulia",
    "LAZ": "lazio",
    "LIG": "liguria",
    "LOM": "lombardia",
    "MAR": "marche",
    "MOL": "molise",
    "PAB": "provincia autonoma di bolzano",
    "PAT": "provincia autonoma di trento",
    "PIE": "piemonte",
    "PUG": "puglia",
    "SAR": "sardegna",
    "SIC": "sicilia",
    "TOS": "toscana",
    "UMB": "umbria",
    "VDA": "valle d'aosta",
    "VEN": "veneto",
    "TRA": "trentino-alto adige/sudtirol",
}

# Retrieve data from open repository
# Credit: TODO
vax_summary = pd.read_csv(VACCINI_SUMMARY_URL)
vax_summary["regione"] = vax_summary.area.apply(lambda x: REGION_CODE_NAME[x])

somm_vacc_latest = pd.read_csv(SOMM_VACC_LATEST)
somm_vacc_latest["total"] = (
    somm_vacc_latest.sesso_maschile + somm_vacc_latest.sesso_femminile
)

# build trentino aldo adige's data summing data from
# - Provincia Autonoma di Trento
# - Provincia Autonoma di Bolzano
pat = vax_summary[vax_summary.area == "PAT"]
pab = vax_summary[vax_summary.area == "PAB"]
tra = {
    "area": "TRA",
    "dosi_somministrate": pat.dosi_somministrate.values[0]
    + pab.dosi_somministrate.values[0],
    "dosi_consegnate": pat.dosi_consegnate.values[0] + pab.dosi_consegnate.values[0],
    "percentuale_somministrazione": 100
    * (pat.dosi_somministrate.values[0] + pab.dosi_somministrate.values[0])
    / (pat.dosi_consegnate.values[0] + pab.dosi_consegnate.values[0]),
    "ultimo_aggiornamento": pat.ultimo_aggiornamento.values[0],
    "regione": "trentino-alto adige/sudtirol",
}
vax_summary = vax_summary.append(tra, ignore_index=True)

# Load region borders from GeoJSON
# Credit: TODO
with open("italy-regions.json") as fp:
    regions = json.load(fp)
names = [f["properties"]["name"] for f in regions["features"]]

# Figures

ic = ItalyChoropleth(vax_summary, regions)
scs = ScatterConsegnateSomministrate(vax_summary)
bbs = BarBySex(somm_vacc_latest)
pbs = PieSex(somm_vacc_latest)
bbo = BarByOccupation(somm_vacc_latest)

# DASH APP

app = dash.Dash(
    __name__,
    title="ItalVax",
    update_title="Loading...",
    external_stylesheets=[dbc.themes.LUMEN],
)


app.layout = dbc.Container(
    [
        HEADER,
        Row(
            Col(Graph(id="italy-choropleth", figure=ic.get_figure())),
        ),
        Row(
            Col(Graph(id="scatter-consegnate-somministrate2", figure=scs.get_figure()))
        ),
        Row(
            [
                Col(Graph(id="bar-by-sex", figure=bbs.get_figure()), width=8),
                Col(Graph(id="pie-by-sex", figure=pbs.get_figure()), width=4),
            ]
        ),
        Row([Col(Graph(id="bar-by-occupation", figure=bbo.get_figure()))]),
        NOTE,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)