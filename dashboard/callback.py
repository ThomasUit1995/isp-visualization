import numpy as np
from dash import html

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh

import time
import api

def register_callbacks(app, appColors, short, long, dtFormat):

    @app.callback(
        Output("response-time-short", "figure"), [Input("update-interval", "n_intervals")]
    )
    def gen_response_time_short(interval):
        """
        Generate the short term (5 minutes) response time graph.

        :params interval: update the graph based on an interval
        """

        # Look at the network for the last 5 minutes
        seconds = 5*60
        dfShort = api.read_file(short, dtFormat).tail(seconds)
        groups = dfShort.groupby(by = "server")
        
        data = []
        for group, df in groups:
            page = ""
            col = ""
            if group == "https://www.google.com":
                page = "google.com"
                col = "#00ff00"
            elif group == "https://www.nu.nl":
                page = "nu.nl"
                col = "#0000ff"
            else:
                page = "None"
                col = "#ff0000"

            traceMarker = dict(
                type = 'scatter',
                x = df['timestamp'],
                y = df['responseTime'],
                mode = "markers",
                name = page,
                marker = dict(color = col),
                hoverinfo="skip",
            )
            data.append(traceMarker)

        traceLine = dict(
            type = 'scatter',
            x = dfShort['timestamp'],
            y = dfShort['responseTime'],
            mode = "lines",
            name = "response time",
            connectgaps = False,
            line = dict(color = "#d5bbfe"),
            hoverinfo="skip",
        )
        data.append(traceLine)

        layout = dict(
            height=325,
            plot_bgcolor=appColors["graphBg"],
            paper_bgcolor=appColors["graphBg"],
            font={"color": "#000"},
            xaxis={
                "showline": True,
                "zeroline": False,
                "fixedrange": True,
                "title": "Time Elapsed (sec)",
            },
            yaxis={
                "range": [
                    min(0, min(dfShort["responseTime"])),
                    max(10, max(dfShort["responseTime"])),
                ],
                "showgrid": True,
                "showline": True,
                "fixedrange": True,
                "zeroline": False,
                "nticks": max(6, round(dfShort["responseTime"].iloc[-1] / 10)),
            },
        )
        return dict(data=data, layout=layout)

    @app.callback(
        Output("response-time-long", "figure"),
        Input("update-long", "n_clicks")
    )
    def gen_response_time_long(n_clicks):
        """
        Generate the long term response time graph.

        :params interval: update the graph based on an interval
        """
        
        dfLong = api.read_file(long, dtFormat)
        groups = dfLong.groupby(by = "server")
        
        data = []
        for group, df in groups:
            page = ""
            col = ""
            if group == "https://www.google.com":
                page = "google.com"
                col = "#00ff00"
            elif group == "https://www.nu.nl":
                page = "nu.nl"
                col = "#0000ff"
            else:
                page = "None"
                col = "#ff0000"

            traceMarker = dict(
                type = 'scatter',
                x = df['timestamp'],
                y = df['responseTime'],
                mode = "markers",
                name = page,
                marker = dict(color = col),
                # hoverinfo="skip",
            )
            data.append(traceMarker)

        traceLine = dict(
            type = 'scatter',
            x = dfLong['timestamp'],
            y = dfLong['responseTime'],
            mode = "lines",
            name = "response time",
            connectgaps = False,
            line = dict(color = appColors["graphLine"]),
            # hoverinfo="skip",
        )
        data.append(traceLine)

        layout = dict(
            height=325,
            plot_bgcolor=appColors["graphBg"],
            paper_bgcolor=appColors["graphBg"],
            font={"color": "#000"},
            xaxis={
                "showline": True,
                "zeroline": False,
                # "fixedrange": True,
                "title": "Time Elapsed (sec)",
            },
            yaxis={
                "range": [
                    min(0, min(dfLong["responseTime"])),
                    max(10, max(dfLong["responseTime"])),
                ],
                "showgrid": True,
                "showline": True,
                # "fixedrange": True,
                "zeroline": False,
                "nticks": max(6, round(dfLong["responseTime"].iloc[-1] / 20)),
            },
        )
        return dict(data=data, layout=layout)

    @app.callback(
        Output("response-time-histogram", "figure"),
        [Input("update-interval", "n_intervals")],
        [State("response-time-short", "figure")],
    )
    def gen_reponse_time_histogram(interval, networkShortFigure):
        """
        Genererate the response time histogram graph.

        :params interval: upadte the graph based on an interval
        :params networkShortFigure: current wind speed graph
        """

        responseTime = []

        try:
            # Check to see whether wind-speed has been plotted yet
            if networkShortFigure is not None:
                dfShort = api.read_file(short, dtFormat).tail(300)
                responseTime = list(dfShort['responseTime'])
                binList = np.histogram(
                    responseTime,
                    bins=range(int(round(min(responseTime))), int(round(max(responseTime)))),
                )
        except Exception as error:
            raise PreventUpdate

        avg = float(sum(responseTime)) / len(responseTime)
        median = np.median(responseTime)

        pdfRayleigh = rayleigh.pdf(
            binList[1], loc=(avg) * 0.55, scale=(binList[1][-1] - binList[1][0]) / 3
        )

        yVal = (pdfRayleigh * max(binList[0]) * 20,)
        yMax = max(yVal[0])
        binMax = max(binList[0])

        trace = dict(
            type="bar",
            x=binList[1],
            y=binList[0],
            marker={"color": appColors["graphCol"]},
            showlegend=False,
            hoverinfo="x+y",
        )

        tracesScatter = [
            {"line_dash": "dash", "line_color": "#cf4768", "name": "Average"},
            {"line_dash": "dot", "line_color": "#6847cf", "name": "Median"},
        ]

        dataScatter = [
            dict(
                type="scatter",
                x=[binList[int(len(binList) / 2)]],
                y=[0],
                mode="lines",
                line={"dash": traces["line_dash"], "color": traces["line_color"]},
                marker={"opacity": 0.3},
                visible=True,
                name=traces["name"],
            )
            for traces in tracesScatter
        ]

        trace3 = dict(
            type="scatter",
            mode="lines",
            line={"color": appColors["graphLine"]},
            y=yVal[0],
            x=binList[1][: len(binList[1])],
            name="Rayleigh Fit",
        )
        layout = dict(
            height=350,
            plot_bgcolor=appColors["graphBg"],
            paper_bgcolor=appColors["graphBg"],
            font={"color": "#000"},
            xaxis={
                "title": "Avg Response time (ms)",
                "showgrid": False,
                "showline": False,
                "fixedrange": True,
            },
            yaxis={
                "showgrid": False,
                "showline": False,
                "zeroline": False,
                "title": "Number of Samples",
                "fixedrange": True,
            },
            autosize=True,
            bargap=0.01,
            bargroupgap=0,
            hovermode="closest",
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "xanchor": "center",
                "y": 1,
                "x": 0.5,
            },
            shapes=[
                {
                    "xref": "x",
                    "yref": "y",
                    "y1": int(max(binMax, yMax)) + 0.5,
                    "y0": 0,
                    "x0": avg,
                    "x1": avg,
                    "type": "line",
                    "line": {"dash": "dash", "color": "#cf4768", "width": 2},
                },
                {
                    "xref": "x",
                    "yref": "y",
                    "y1": int(max(binMax, yMax)) + 0.5,
                    "y0": 0,
                    "x0": median,
                    "x1": median,
                    "type": "line",
                    "line": {"dash": "dot", "color": "#6847cf", "width": 2},
                },
            ],
        )
        return dict(data=[trace, dataScatter[0], dataScatter[1], trace3], layout=layout)

    @app.callback(
        Output('uptime-text', 'children'),
        Input("update-interval", "n_intervals")
    )
    
    def update_output(interval):
        dfLong = api.read_file(long, dtFormat)
        counts = dfLong['server'].value_counts(normalize=True)
        google = round(counts['https://www.google.com']*100,1)
        nu = round(counts['https://www.nu.nl']*100,1)
        both = round((counts['https://www.google.com'] + counts['https://www.nu.nl'])*100,1)
        # none = round(counts['none']*100,1)

        secondsInDay = 60*60*24
        df24h = dfLong.tail(secondsInDay)
        noneSeconds = df24h['reachable'].value_counts()[False]
        if noneSeconds >= 3600:
            downTime = time.strftime('%Hh %Mm %Ss', time.gmtime(noneSeconds))
        elif noneSeconds >= 60:
            downTime = time.strftime('%Mm %Ss', time.gmtime(noneSeconds))
        else:
            downTime = time.strftime('%Ss', time.gmtime(noneSeconds))

        outputList = [f'Running up-time: {both}%', html.Br(), f'nu.nl {nu}% - google.com {google}%', html.Br(), html.Br(), f'Total downtime last 24 hours: {downTime}']

        return outputList
    
    
    # @app.callback(
    #     Output("uptime-barchart", "figure"), [Input("update-interval", "n_intervals")]
    # )
    # def gen_network_uptime(interval):
    #     """
    #     Generate the network uptime barchart graph.

    #     :params interval: update the graph based on an interval
    #     """

    #     dfLong = api.read_file(long, dtFormat)
    #     counts = dfLong['server'].value_counts(normalize=True)
    #     google = round(counts['https://www.google.com']*100,1)
    #     nu = round(counts['https://www.nu.nl']*100,1)
    #     # both = round((counts['https://www.google.com'] + counts['https://www.nu.nl'])*100,1)
    #     none = round(counts['none']*100,1)

    #     xvals = [nu, google, none]
    #     # x = [both, none]
    #     yval = "uptime"
    #     colors = ["#33dbff", "#63ff33", "#ff4233"]

    #     data = []
    #     for i in range(0, len(xvals)):
    #         trace = dict(
    #             type = "bar",
    #             x=[xvals[i]],
    #             y=[yval],
    #             orientation="h",
    #             marker = dict(
    #                 color = colors[i],
    #                 line=dict(color='rgb(248, 248, 249)', width=1)
    #             )
    #         )
    #         data.append(trace)
        
    #     # print(data)
        
    #     layout = dict(
    #         xaxis=dict(
    #             showgrid=False,
    #             showline=False,
    #             showticklabels=False,
    #             zeroline=False,
    #             domain=[0.15, 1]
    #             ),
    #         yaxis=dict(
    #             showgrid=False,
    #             showline=False,
    #             showticklabels=False,
    #             zeroline=False,
    #         ),
    #         barmode='stack',
    #         paper_bgcolor='rgb(248, 248, 255)',
    #         plot_bgcolor='rgb(248, 248, 255)',
    #         margin=dict(l=120, r=10, t=140, b=80),
    #         showlegend=False,
    #     )
    #     return dict(data=data, layout=layout)