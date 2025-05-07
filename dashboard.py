import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from utils import get_stats, save_to_csv, stats_history, reset_stats
import pandas as pd

external_styles = [
    dbc.themes.FLATLY,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]

app = dash.Dash(__name__, external_stylesheets=external_styles, suppress_callback_exceptions=True)
server = app.server

def build_layout(theme="dark"):
    return dbc.Container([
        dcc.Store(id="theme-store", data=theme),
        dcc.Interval(id="interval", interval=1000, n_intervals=0),

        dbc.Row([
            dbc.Col(html.Img(src="assets/netdash_logo.png", height="50px"), width="auto"),
            dbc.Col(html.H4("NetDash - System & Network Dashboard", className="mt-3")),
            dbc.Col(html.Div(id="datetime-display", className="text-end mt-3", style={"fontSize": "18px"}), width=3),
        ]),

        dbc.Row([
            dbc.Col(dbc.Button("Reset Stats", id="reset-btn", color="danger", className="mb-3 me-2"), width="auto"),
            dbc.Col(dbc.Button("Toggle Theme", id="toggle-theme", color="secondary", className="mb-3"), width="auto")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("CPU Usage"),
                dbc.CardBody(html.H4(id="cpu-value"))
            ], id="cpu-card", inverse=True)),

            dbc.Col(dbc.Card([
                dbc.CardHeader("RAM Usage"),
                dbc.CardBody(html.H4(id="ram-value"))
            ], id="ram-card", inverse=True)),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Network Status"),
                dbc.CardBody(html.H6(id="net-status"))
            ], color="secondary", inverse=True)),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Upload Speed (KB/s)"),
                dbc.CardBody(html.H5(id="upload-value"))
            ], color="info", inverse=True)),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Download Speed (KB/s)"),
                dbc.CardBody(html.H5(id="download-value"))
            ], color="success", inverse=True)),

            dbc.Col(dbc.Card([
                dbc.CardHeader("IP & Interface"),
                dbc.CardBody(html.H6(id="ip-info"))
            ], color="dark", inverse=True)),
        ], className="mb-4"),

        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Live Monitor', value='tab-1'),
            dcc.Tab(label='History', value='tab-2'),
            dcc.Tab(label='About Project', value='tab-3'),
        ]),
        html.Div(id='tabs-content'),

        html.Br(),
        html.A("⬇️ Download CSV", href="/download", download="system_log.csv", target="_blank", className="btn btn-primary")
    ], fluid=True)

app.layout = build_layout()

@app.callback(
    Output("theme-store", "data"),
    [Input("toggle-theme", "n_clicks")],
    [State("theme-store", "data")]
)
def toggle_theme(n, current):
    return "light" if current == "dark" else "dark"

@app.callback(
    Output("cpu-value", "children"),
    Output("ram-value", "children"),
    Output("cpu-card", "color"),
    Output("ram-card", "color"),
    Output("upload-value", "children"),
    Output("download-value", "children"),
    Output("ip-info", "children"),
    Output("net-status", "children"),
    Output("datetime-display", "children"),
    Input("interval", "n_intervals")
)
def update_data(n):
    stats = get_stats()
    stats_history.append(stats)
    if len(stats_history) > 50:
        stats_history.pop(0)

    if n % 30 == 0:
        save_to_csv()

    cpu_color = "danger" if stats["CPU"] > 85 else "success"
    ram_color = "warning" if stats["RAM"] > 85 else "info"
    net_status = "✅ Online" if stats["Online"] else "❌ Offline"

    datetime_display = f"{stats['DateTime'].split(' ')[0]} | {stats['DateTime'].split(' ')[1]}"
    return (f"{stats['CPU']}%", f"{stats['RAM']}%", cpu_color, ram_color,
            f"{stats['Upload']} KB/s", f"{stats['Download']} KB/s",
            f"{stats['Interface']} ({stats['IP']})", net_status,
            datetime_display)

@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == 'tab-1':
        times = [s["Time"] for s in stats_history]
        cpu = [s["CPU"] for s in stats_history]
        ram = [s["RAM"] for s in stats_history]
        upload = [s["Upload"] for s in stats_history]
        download = [s["Download"] for s in stats_history]

        fig = {
            "data": [
                go.Scatter(x=times, y=cpu, name="CPU Usage", mode="lines+markers", line=dict(color='red')),
                go.Scatter(x=times, y=ram, name="RAM Usage", mode="lines+markers", line=dict(color='blue')),
                go.Scatter(x=times, y=upload, name="Upload Speed", mode="lines+markers", line=dict(color='orange')),
                go.Scatter(x=times, y=download, name="Download Speed", mode="lines+markers", line=dict(color='green')),
            ],
            "layout": go.Layout(title="System and Network Usage", xaxis={"title": "Time"}, yaxis={"title": "Usage"}, uirevision=True)
        }
        return dcc.Graph(figure=fig)
    elif tab == 'tab-2':
        df = pd.DataFrame(stats_history)
        return dbc.Table.from_dataframe(df.tail(20), striped=True, bordered=True, hover=True)
    elif tab == 'tab-3':
        return html.Div([
            html.H4("About NetDash", className="mt-3 text-center"),
            html.Hr(),
            html.P("NetDash is a simple, real-time dashboard for monitoring Linux system and network performance.", className="text-center"),
            html.Hr(),
            html.P("Developed by: Hosam", className="text-center"),
            html.P("© 2025", className="text-center")
        ], style={"padding": "15px"})

@app.callback(
    Output("reset-btn", "n_clicks"),
    Input("reset-btn", "n_clicks")
)
def reset(n):
    if n:
        reset_stats()
    return None

@app.server.route("/download")
def download_csv():
    from flask import send_file
    return send_file("system_log.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
