from dash import dcc
from dash import html

def layout(GRAPH_INTERVAL, appColors):
    layout = html.Div(
        [
            # header
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("ISP Network Log", className="app__header__title"),
                        ],
                        className="app__header__desc",
                    ),
                ],
                className="app__header",
            ),

            # graphs
            html.Div(
                [
                    # Network response times; short and long term
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Response time (ms)", className="graph__title")
                                ],
                            ),
                            dcc.Graph(
                                id="response-time-short",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor=appColors["graphBg"],
                                        paper_bgcolor=appColors["graphBg"],
                                    )
                                ),
                            ),
                            dcc.Graph(
                                id="response-time-long",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor=appColors["graphBg"],
                                        paper_bgcolor=appColors["graphBg"],
                                    )
                                ),
                            ),
                            html.Div(
                                [html.Button('Update', id='update-long', n_clicks=0)]
                            ),
                            dcc.Interval(
                                id="update-interval",
                                interval=int(GRAPH_INTERVAL),
                                n_intervals=0,
                            ),
                        ],
                        className="two-thirds column response__time__container",
                    ),
                    html.Div(
                        [
                            # histogram
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Response time Histogram",
                                                className="graph__title",
                                            )
                                        ]
                                    ),
                                    dcc.Graph(
                                        id="response-time-histogram",
                                        figure=dict(
                                            layout=dict(
                                                plot_bgcolor=appColors["graphBg"],
                                                paper_bgcolor=appColors["graphBg"],
                                            )
                                        ),
                                    ),
                                ],
                                className="graph__container first",
                            ),
                            # Network uptime
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Network up-time", className="graph__title"
                                            ),
                                            html.P(
                                                id='uptime-text', className="graph__text"
                                            ),
                                        ]
                                    )
                                    # dcc.Graph(
                                    #     id="uptime-barchart",
                                    #     figure=dict(
                                    #         layout=dict(
                                    #             plot_bgcolor=appColor["graphBg"],
                                    #             paper_bgcolor=appColor["graphBg"],
                                    #         )
                                    #     ),
                                    # ),
                                ],
                                className="graph__container second",
                            ),
                        ],
                        className="one-third column response__time__histogram ",
                    ),
                ],
                className="app__content",
            ),
        ],
        className="app__container",
    )

    return layout