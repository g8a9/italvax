import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class ItalyChoropleth:
    def __init__(self, vax_summary, regions):
        self.vax_summary = vax_summary
        self.regions = regions

    def get_figure(self):
        fig = px.choropleth(
            self.vax_summary,
            geojson=self.regions,
            locations="regione",
            color="percentuale_somministrazione",
            # color_continuous_scale="Viridis",
            range_color=(0, 100),
            featureidkey="properties.name",
            projection="mercator",
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig


class ScatterConsegnateSomministrate:
    def __init__(self, vax_summary):
        self.vax_summary = vax_summary

    def get_figure(self):
        fig = px.scatter(
            self.vax_summary,
            x="dosi_consegnate",
            y="dosi_somministrate",
            size="percentuale_somministrazione",
            color="percentuale_somministrazione",
        )
        return fig


class BarBySex:
    def __init__(self, somm_vacc_latest):
        self.somm_vacc_latest = somm_vacc_latest

    def get_figure(self):
        fig = px.bar(
            self.somm_vacc_latest.groupby("area").sum().sort_values("total"),
            y=["sesso_femminile", "sesso_maschile"],
        )
        fig.update_layout(
            legend=dict(yanchor="top", xanchor="left", y=0.99, x=0.01),
            legend_title_text="",
        )
        return fig


class PieSex:
    def __init__(self, somm_vacc_latest):
        self.somm_vacc_latest = somm_vacc_latest

    def get_figure(self):
        return go.Figure(
            data=[
                go.Pie(
                    labels=["Donne", "Uomini"],
                    values=self.somm_vacc_latest[["sesso_femminile", "sesso_maschile"]]
                    .sum()
                    .values,
                )
            ]
        )


class BarByOccupation:
    def __init__(self, somm_vacc_latest):
        self.somm_vacc_latest = somm_vacc_latest

    def get_figure(self):
        fig = px.bar(
            self.somm_vacc_latest.groupby("area").sum().sort_values("total"),
            y=[
                "categoria_operatori_sanitari_sociosanitari",
                "categoria_ospiti_rsa",
                "categoria_personale_non_sanitario",
            ],
        )
        fig.update_layout(
            legend=dict(yanchor="top", xanchor="left", y=0.99, x=0.01),
            legend_title_text="",
        )
        return fig
