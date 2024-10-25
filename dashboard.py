from dash import html, dcc, Dash, callback, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

############################# DATASET ###############################
def load_dataset():
    df = pd.read_csv('obesitydataset.csv')
    return df

df = load_dataset()

############################ THEME CONSTANTS #######################
THEME = {
    'background': '#eeeeee',    # Light background
    'card_bg': '#FFF000',       # White card background
    'primary': '#1E2022',       # Turquoise
    'secondary': '#6C5DD3',     # Purple
    'text': '#1E2022',          # Dark text
    'text_secondary': '#677788', # Secondary text
    'grid': '#E7EAF3',          # Light grid
}

# Color palette matching the image
CHART_COLORS = [
    '#005F5F',  # Dark Teal
    '#4B0082',  # Indigo
    '#0033CC',  # Dark Blue
    '#C72C41',  # Dark Coral
    '#D99A00',  # Dark Gold
    '#A50068',  # Dark Pink
    '#4B3C3D',  # Dark Brown
]


############################ CHART STYLING #################################
def style_figure(fig):
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        font={'family': 'Inter, sans-serif', 'size': 12},
        margin=dict(l=20, r=20, t=90, b=20),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(255,255,255,0)',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter"
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=THEME['grid'],
        showline=True,
        linewidth=1,
        linecolor=THEME['grid'],
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=THEME['grid'],
        showline=True,
        linewidth=1,
        linecolor=THEME['grid'],
        tickfont=dict(size=10)
    )
    return fig

def create_histogram(col_name):
    title = f"Distribution of {ABBREVIATIONS.get(col_name, col_name)}"
    fig = px.histogram(df, x=col_name, color="NObeyesdad", nbins=50,
                      color_discrete_sequence=CHART_COLORS,
                      title=title)
    fig.update_traces(opacity=0.85)
    fig = style_figure(fig)
    fig.update_layout(legend_title_text='Obesity Levels',title={'text': title,'y':0.999,'x':0.5,'xanchor': 'center','yanchor': 'top',
        'font': {'size': 16, 'color': THEME['text'], 'family': 'Inter', 'weight': 'bold'}},
        bargap=0.1
    ).update_xaxes(title_text=col_name.title()).update_yaxes(title_text='Count')
    return fig

def create_box_plot(x_axis, y_axis):
    title = f"{ABBREVIATIONS.get(y_axis, y_axis)} by {ABBREVIATIONS.get(x_axis, x_axis)}"
    fig = px.box(df, x=x_axis, y=y_axis, color="NObeyesdad", 
                 color_discrete_sequence=CHART_COLORS, title=title)
    
    fig = style_figure(fig).update_layout(
        legend_title_text='Obesity Levels', 
        title={'text': title, 'y': 0.999, 'x': 0.5, 'xanchor': 'center', 
               'yanchor': 'top', 'font': {'size': 16, 'color': THEME['text'], 
               'family': 'Inter', 'weight': 'bold'}}
    ).update_xaxes(title_text=x_axis.title()).update_yaxes(title_text=y_axis.title())
    return fig


def create_pie_chart():
    obesity_cnt = df['NObeyesdad'].value_counts().reset_index(name='Count')
    
    fig = (px.pie(obesity_cnt, values='Count', names='NObeyesdad', hole=0.7,
                   color_discrete_sequence=CHART_COLORS, title="Distribution of Obesity Levels")
           .update_traces(textposition='outside', textinfo='label+percent', 
                           hoverinfo='label+value+percent', pull=[0.02] * len(obesity_cnt))
           .update_layout(title={'text': "Distribution of Obesity Levels", 'y': 0.99, 'x': 0.5,
                                 'xanchor': 'center', 'yanchor': 'top', 
                                 'font': {'size': 16, 'color': THEME['text'], 
                                           'family': 'Inter', 'weight': 'bold'}},
                           showlegend=False,
                           margin=dict(t=50, b=50, l=50, r=50)))
    return style_figure(fig)


def create_bar_chart(col_name):
    title = f"Average {ABBREVIATIONS.get(col_name, col_name)} by Obesity Level"
    
    fig = px.histogram(df, x="NObeyesdad", y=col_name, color="NObeyesdad",
                       histfunc="avg", color_discrete_sequence=CHART_COLORS, title=title)
    
    fig = style_figure(fig).update_layout(
        legend_title_text='Obesity Levels', 
        title={'text': title, 'y': 0.999, 'x': 0.5, 'xanchor': 'center', 
               'yanchor': 'top', 'font': {'size': 16, 'color': THEME['text'], 
               'family': 'Inter', 'weight': 'bold'}}
    )
    fig.update_xaxes(title="Obesity Level")  # Ensure x-axis title is in title case
    fig.update_yaxes(title=ABBREVIATIONS.get(col_name, col_name).title())  # y-axis in title case
    return fig

####################### WIDGETS ##########################
def create_dropdown(id, options, value, placeholder):
    return dcc.Dropdown(
        id=id,
        options=options,
        value=value,
        clearable=False,
        placeholder=placeholder,
        className="dropdown-custom",
        style={
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'border': '1px solid #E7EAF3',
            'fontSize': '13px',
            'color': THEME['text']
        }
    )

############################ ABBREVIATION DEFINITIONS #######################
ABBREVIATIONS = {
    'FAVC': 'Frequent Consumption of High Caloric Food',
    'FCVC': 'Frequency of Consumption of Vegetables',
    'NCP': 'Number of Main Meals',
    'CAEC': 'Consumption of Food Between Meals',
    'SMOKE': 'Smoking Habits',
    'CH2O': 'Daily Water Consumption',
    'SCC': 'Calories Consumption Monitoring',
    'FAF': 'Physical Activity Frequency',
    'TUE': 'Time Using Technology Devices',
    'CALC': 'Consumption of Alcohol',
    'MTRANS': 'Transportation Used',
    'NObeyesdad': 'Obesity Level',
    'family_history_with_overweight': 'Family History with Overweight'
}

# Feature lists with descriptions
feature_names = [{"label": f"{ABBREVIATIONS.get(col, col)}", "value": col} 
                 for col in df.columns if col != "NObeyesdad"]

# Split into categorical and numerical while preserving descriptions
categorical = [opt for opt in feature_names 
              if df[opt["value"]].dtype == 'object']
numerical = [opt for opt in feature_names 
            if df[opt["value"]].dtype in ['int64', 'float64']]

####################### LAYOUT #############################
external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
]

app = Dash(__name__, external_stylesheets=external_css)

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Obesity Analysis Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: ''' + THEME['background'] + ''';
                color: ''' + THEME['text'] + ''';
            }
            .dashboard-card {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 2px 5px rgba(140, 152, 164, 0.1);
                padding: 18px;
                margin: 5px;
                margin-left: -18px;
                border: 1px solid #E7EAF3;
                transition: all 0.2s ease;
            }
            .dashboard-card:hover {
                box-shadow: 0 4px 12px rgba(140, 152, 164, 0.15);
            }
            .control-panel {
                background: white;
                padding: 25px;
                border-radius: 2px;
                margin: 10px;
                margin-right: -1px;
                border: 1px solid #E7EAF3;
            }
            .stat-card {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                background: white;
                border: 1px solid #E7EAF3;
            }
            .stat-value {
                font-size: 24px;
                font-weight: 600;
                color: ''' + THEME['primary'] + ''';
            }
            .stat-label {
                font-size: 13px;
                color: ''' + THEME['text_secondary'] + ''';
            }
            .section-title {
                font-size: 14px;
                font-weight: 600;
                color: ''' + THEME['text'] + ''';
                margin-bottom: 10px;
            }
            .abbreviation-item {
                padding: 8px 0;
                border-bottom: 1px solid #E7EAF3;
                font-size: 13px;
            }
            .abbreviation-key {
                color: ''' + THEME['primary'] + ''';
                font-weight: 500;
            }
            .dropdown-custom {
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Create sidebar content
control_panel = html.Div([
    html.H2("Analytics Menu", className="h5 mb-4"),
    
    # Variable controls
    html.Div([
        html.Div("Distribution Analysis", className="section-title"),
        create_dropdown("hist_column", feature_names, "Age", "Select variable"),
    ], className="mb-4"),
    
    html.Div([
        html.Div("Multivariate Analysis", className="section-title"),
        create_dropdown("x_axis", categorical, "Gender", "Select category"),
        create_dropdown("y_axis", numerical, "Weight", "Select measure"),
    ], className="mb-4"),
    
    html.Div([
        html.Div("Average Analysis by Obesity Levels", className="section-title"),
        create_dropdown("avg_drop", numerical, "Age", "Select variable"),
    ], className="mb-4"),
    
    # Abbreviations
    html.Div([
        html.Div("Variable Descriptions", className="section-title mt-4"),
        html.Div([
            html.Div([
                html.Span(key + ": ", className="abbreviation-key"),
                html.Span(value, style={"color": THEME['text_secondary']})
            ], className="abbreviation-item")
            for key, value in ABBREVIATIONS.items()
        ])
    ])
], className="control-panel")

# Main content
main_content = html.Div([
    html.H1("Obesity Analytics Dashboard Using Plotly Dash", 
            className="h3 fw-semibold",
            style={'color': THEME['text']}),
            
    # Charts
    html.Div([
        html.Div([
            dcc.Graph(id="histogram", className="dashboard-card")
        ], className="col-md-6"),
        html.Div([
            dcc.Graph(id="scatter_plot", className="dashboard-card")
        ], className="col-md-6"),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(id="bar_chart", className="dashboard-card")
        ], className="col-md-6"),
        html.Div([
            dcc.Graph(id="pie_chart", figure=create_pie_chart(), className="dashboard-card")
        ], className="col-md-6"),
    ], className="row")
], className="col-md-10 p-3")

# Layout assembly
app.layout = html.Div([
    html.Div([
        html.Div([control_panel], className="col-md-2"),
        main_content
    ], className="row")
], className="container-fluid")

######################## CALLBACKS #######################################
@callback(Output("histogram", "figure"), [Input("hist_column", "value")])
def update_histogram(hist_column):
    return create_histogram(hist_column)

@callback(Output("scatter_plot", "figure"), [Input("x_axis", "value"), Input("y_axis", "value")])
def update_scatter(x_axis, y_axis):
    return create_box_plot(x_axis, y_axis)

@callback(Output("bar_chart", "figure"), [Input("avg_drop", "value")])
def update_bar(avg_drop):
    return create_bar_chart(avg_drop)

################################# RUN APP ##############################
if __name__ == "__main__":
    app.run(debug=True)