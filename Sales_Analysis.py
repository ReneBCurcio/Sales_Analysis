import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

df = pd.read_csv("C:/Users/reneb/OneDrive/Área de Trabalho/Sales_Analysis/dataframelimpo.csv")
optionsDropdownPropaganda = df["Meio de Propaganda"].unique()
optionsDropdownStatus = df["Status de Pagamento"].unique()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    dbc.Col([
        dbc.Card([
            html.H1("Meio de Propaganda"),
            dcc.Dropdown(optionsDropdownPropaganda, "Facebook", id="DropdownPropaganda"),
            html.H1("Status do Pagamento"),
            dcc.Dropdown(optionsDropdownStatus, "Pago", id="DropdownStatus"),
        ])
    ], sm=4),
    dbc.Col([
        dbc.Row([dcc.Graph(id="Grafico1")]),
        dbc.Row([dcc.Graph(id="Grafico2")])
    ], sm=10)
])


@app.callback([Output("Grafico1", "figure"),
               Output("Grafico2", "figure")],
              [Input("DropdownPropaganda", "value"),
               Input("DropdownStatus", "value")])
def fun(MeioPropaganda, StatusPropaganda):
    df_filtrada = df[df["Meio de Propaganda"] == MeioPropaganda]
    df_filtradaStatus = df_filtrada[df_filtrada["Status de Pagamento"] == StatusPropaganda]
    df_ValorPago = df_filtradaStatus.groupby(["Equipe", "Status de Pagamento"])[
        "Valor Pago"].sum().to_frame().reset_index()
    df_tempo = df_filtradaStatus.groupby("Mês")["Duração da chamada"].mean().to_frame().reset_index()

    fig_Equipe = px.bar(df_ValorPago, x="Equipe", y="Valor Pago")
    fig_Chamada = px.line(df_tempo, x="Mês", y="Duração da chamada")
    return fig_Equipe, fig_Chamada


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
