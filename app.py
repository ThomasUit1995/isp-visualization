import os
import dash
from numpy.lib.function_base import _append_dispatcher

from dashboard.layout import layout
from dashboard.callback import register_callbacks
# import scraper

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

dtFormat = '%Y-%m-%d %H:%M:%S'
short = 'data/short.txt'
long = 'data/long.txt'

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)
server = app.server
app.title = "ISP Network Dashboard"
appColors = {"graphBg": "#f9f9f9", "graphCol": "#aef168", "graphLine": "bdbdbd"}

app.layout = layout(GRAPH_INTERVAL, appColors)
register_callbacks(app, appColors, short, long, dtFormat)

if __name__ == "__main__":
    app.run_server(debug=True)