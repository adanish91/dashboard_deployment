from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

file_path = "C:/Users/danish/Desktop/dashboard_deployment/Accidents.txt"
df = pd.read_csv(file_path, delimiter='|', encoding='ISO-8859-1', low_memory=False)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH, dbc_css])
load_figure_template("MORPH")

min_to_display = list(df["SUBUNIT"].unique())
years_to_display = list(range(df["CAL_YR"].min(), df["CAL_YR"].max()+1, 1))
marks_year = {year: {'label': str(year), 'style': {'font-size': '10px'}} for year in range(df["CAL_YR"].min(), df["CAL_YR"].max()+1)}
marks_mining = {m_type: str(m_type) for m_type in min_to_display}

subunit_options = df['SUBUNIT'].dropna().unique()
degree_injury = df['DEGREE_INJURY'].dropna().unique()
injury_source = df['INJURY_SOURCE'].dropna().unique()
nature_injury = df['NATURE_INJURY'].dropna().unique()
classification = df['CLASSIFICATION'].dropna().unique()
injured_body = df['INJ_BODY_PART'].dropna().unique()
accident_type = df['ACCIDENT_TYPE'].dropna().unique()

mining_type_options = [{'label': 'Mill operations', 'value': 'MILL OPERATION/PREPARATION PLANT'},
                        {'label': 'Surface', 'value': 'STRIP, QUARY, OPEN PIT'},
                        {'label': 'Underground', 'value': 'UNDERGROUND'},
                        {'label': 'Surface at UG', 'value': 'SURFACE AT UNDERGROUND'},
                        {'label': 'Dredge', 'value': 'DREDGE'},
                        {'label': 'Auger', 'value': 'AUGER'},
                        {'label': 'Office workers', 'value': 'OFFICE WORKERS AT MINE SITE'},
                        {'label': 'Other mining', 'value': 'OTHER MINING'},
                        {'label': 'Shops/Yards', 'value': 'INDEPENDENT SHOPS OR YARDS'},
                        {'label': 'Culm/Refuse pile', 'value': 'CULM BANK/REFUSE PILE'}]
coal_metal_options = [{'label': 'Metal', 'value': 'M'},
                      {'label': 'Coal', 'value': 'C'}]

degree_labels = ['Days Restricted Activity Only', 'Days Away From Work Only','No Days Away & No Restricted Activity',
       'Days Away & Restricted Activity', 'Permanent Disability', 'Accidents Only','Occupational Illness', 
        'No Value','Fatality', 'All Other Cases','Injuries Due To Natural Cause','Injuries Involving Non-Employees']

injury_source_labels = ['Metal (pipe, wire, nail)', 'Broken rock/coal/ore/waste','Ladders', 'Barrels/kegs/drums',
       'Nonpowered Handtools', 'Ground', 'Floor/walking surface not UG','Pallets', 'Pulverize mineral (Dust)', 'Motors','Crowbar/pry bar', 'Steps', 'Chute/slide-converyer hoper',
       'Electrical apparatus', 'Boiler/pressure vessel/air hose/ox','Highway ore carrier/large tank', 'Scaffolds/staging',
       'Belt Conveyors', 'Heat (Environment)','Metal covers/guards', 'Kiln prod/Inc build up removal',
       'Mine floor/bottom/footwall', 'Bags', 'Mine Jeep/kersey/jitney','Miscellaneous', 'Rabber/glass/plastic/fiberglass/fab',
       'Underground mining machines', 'Acid/alkali/wet cement','Caving rock/coal/ore/waste', 'Roof (rock) bolts',
       'Post/caps/headers/timber', 'Boxes/crates/cartons','Steel rail', 'Blocking', 'Longwall support/chock',
       'Coal/petrol product', 'Knife', 'Surface mining machines','Wrench', 'Drill steel', 'Cranes/derricks',
       'Conductor/electric/cable', 'Doors/UG ventilation','Axe/hammer/sledge', 'Wood items', 'Animals/insects/birds/reptile',
       'Nonpowered vehicles', 'Stairs/steps outside','Machine-mill/cleaning plant', 'Rail Car surface equipment',
       'Noise', 'Pumps/fans/comp/eng', 'Loose dirt/mud','Mineral items', 'cars/pickup trucks','Powered handtools', 'Bodily motion',
       'Chain/rope/cable', 'Wheel grinder','Machine/welder', 'Transformers/converters', 'Ice','Conveyors', 'Storage tanks & bins', 'Moveable ladders',
       'Forklifts/stackers/tractor', 'Chemicals/chemical compounds','Containers', 'Cement/concrete block', 'Brick/ceramic',
       'Molten metal', 'Power saw', 'Working surface outside','Apparel', 'Dam/locks/ponds/bridges',
       'Building/structure/boat/raft', 'Mine rescue equipment','Drum/puly/sheave-nt conveyor', 'Water', 'Drill percussion/hard rock/jackhammer',
       'Mechanical/hydraulic/air jacks', 'Sand/gravel/shell', 'Rib/side','Wheel-from car/truck', 'Hoisting apparatus',
       'Towers/poles', 'Belts(Not conveyor)', 'Flame/Fire/Smoke','Mechanical power transmission', 'Back/mine roof/hanging wall',
       'Soaps/Detergent/cleaning compound', 'Fixed ladders','Brattice curt/plas/canv', 'Steam', 'Elevators/cages/skips',
       'Shaking/vibrating conveyor', 'Street/road','Hoist/chain block', 'Noxious mine gases',
       'Radiating substance of equip', 'Snow', 'Underground','Railroad ties', 'Wharfs/docks', 'Drill/rotary (Coal drill)',
       'Plants/trees/vegetation', 'Liquids', 'Longwall conveyor','Space hearters', 'Naro g rail cr, meter-UG equipment',
       'Landslide', 'Mine headframe', 'Cold (environment)','Generators', 'Cribbing', 'Impactor/tamper', 'Chisel',
       'Kilns/melt furnace/retort', 'Vehicles','Radioactive ore radiation', 'Explosive direct related to injury',
       'Other heating equipment', 'Methane gas mine/process','Electric hoist', 'Air hoist', 'Coal (processed)','Oxygen deficient atmosphere']
nature_injury_labels = ['Cut/Lacer/Puncture', 'Sprain/Strain/Rupture disc',
       'Scratch/Abrasion', 'Unclassified','Burn/Chemical-fume/compound', 'Hernia;Rupture',
       'Amputation/Encleation', 'Heatstroke/exhausion','Contusion/Bruise/Intact skin', 'Fracture/Chip',
       'Joint/Tendon/Muscle Inflammation', 'Electric arc burn-not contact','Other Injury', 'Crushing', 'Dust in eyes',
       'Multiple Injuries', 'Poisoning, systemic', 'Dislocation','Hearing loss/Impairment', 'Concussion-Brain/Cerebral',
       'Dermatitis/Rash/Skin Inflam', 'Burn/Scald (Heat)','Heart Attach', 'Silicosis', 'Occupational Diseases',
       'Pneumoconiosis/Black lung', 'Electric Shock/Electrocution','Electric Burn-Contact', 'Suffocation/Smoke/Inhalation/Drown',
       'Other Radiation Effect', 'Cerebral Hemorage-Not CCUS','Freezing/Frostbite', 'Contagious/Infectious disease',
       'Asbestosis', 'Other Pnemoconiosis', 'Sunburn', 'Laser Burn','Lung Cancer/Ionizing Radiation']
classification_labels = ['Machinery', 'Handling of Materials', 'Slip/Fall','Handtools(nonpowered)', 'Nonpowered Haulage',
       'Exploding Vessels Under Pressure','Ignition/Explosion (Gas/Dust)','Disorders (Physical Agents)', 'Powered Haulage',
       'Fall of Roof/Back', 'Hoisting', 'Fire','Disorders (Repeated Trauma)', 'Striking/Bumping', 'Electrical',
       'Falling/Sliding/Rolling Materials','Fall of Face/Rib/Pillar/Side/Highwall','Stepping/Kneeling on Object', 'Other',
       'Other Occupational Illnesses', 'Dust Disease of Lungs','Inundation', 'Occupational Skin Diseases',
       'Explosives/Breaking Agents', 'Entrapment', 'Impoundment','Poisoning (Toxic Materials)','Respiratory Conditions (Toxic Agents)']
injured_body_labels = ['Back (Muscles/spine/s-cord/tailbone)', 'Arm','Fingers/thumb', 'Jaw/Chin', 'Knee/Patella',
       'Shoulders (Collarbone/clavicle/scapula)', 'Ankle', 'Neck','Multiple Parts', 'Forearm/Ulnar/Radius',
       'Wrist', 'Chest (Ribs/Breastbone/Chest)','Eye/Optic Nerve/Vision', 'Mouth/Lip/Teeth/Tongue/Throat',
       'No Value Found', 'Ear(s) External','Foot (Not Ankle/Toe)/Tarsus/Metatarsus', 'Elbow','Arm, Multiple parts', 'Head',
       'Hips (Pelvis/Organs/Kidneys/Buttocks)', 'Leg','Nose/Nasal Passages/Sinus/Smell', 'Upper Extremities, Multiple',
       'Hand (Not Wrist or Fingers)', 'Lower Leg/Tibia/Fibula','Body Systems', 'Abdomen/Internal Organs', 'Toe(s)/Phalanges',
       'Brain', 'Lower Extremities, Multiple Parts', 'Face','Face, Multiple Parts', 'Thigh/Femur', 'Upper Arm/Humerus',
       'Ear(s) Internal & Hearing', 'Unclassified','Trunk, Multiple Parts', 'Leg, Multiple Parts',
       'Ear(s) Internal & External', 'Head, Multiple Parts','Lower Extremities', 'Trunk', 'Skull', 'Scalp', '0',
       'Upper Extremities', '6000', 'Body Parts, NEC', '235', '75','100']

accident_type_labels = ['Fall from machine', 'Over-exertion in lifting objects','Caught in, under or between NEC', 'Fall onto or against objects',
       'Fall to the walkway or working surface','Struck by flying object', 'Over-exertion NEC','Struck against stationary object','Struck by... NEC','Absorption of radiations/toxic substances',
       'Over-exertion in wielding/throwing objects', 'Caught in, under/between a moving and a stationary object',
       'Over-exertion in pulling/pushing objects', 'Struck against a moving object', 'Flash burns (welding)','Without injuries','Contact with hot objects/substances','Struck by falling object',
       'Inhalation of radiations/toxic substances','Flash burns (electric)', 'Fall to lower level, NEC',
       'Caught in, under/between running/meshing objects','Contact with heat', 'Struck by powered moving object',
       'Contact with electrical current', 'Bodily reaction, NEC','Struck by rolling or sliding object',
       'Fall from scaffolds, walkways, platforms', 'No Value Found','NEC', 'Fall from ladders', 'Unclassified, insufficient data',
       'Fall from piled material', 'Fall down stairs','Rubbed or abraded','Caught in under/between two or more moving objects',
       'Drowning', '1', 'Fall on save level, NEC', 'Struck by concussion','Fall down raise/shaft/manway',
       'Caught in, under/between collapsing material','Fall from headframe/derrick/tower','Ingestion of radiations/toxic substances','Contact with cold', '0',
       'Contact with cold objects/substances']

def create_figure(data_field, df, date_range, mining_types, values, coal_metal_ind):
    start_date, end_date = date_range
    if (mining_types is None or mining_types == []) and (coal_metal_ind == None or coal_metal_ind == []):
        filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df[data_field].isin(values)
        group_fields = ['CAL_YR', data_field]
        legend_title = data_field.replace("_", " ").title()
    elif (mining_types is None or mining_types == []) or (coal_metal_ind == None or coal_metal_ind == []):
        if (mining_types is None or mining_types == []):
            filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["COAL_METAL_IND"].isin(coal_metal_ind) & df[data_field].isin(values)
            group_fields = ['CAL_YR', 'COAL_METAL_IND', data_field]
            legend_title = data_field.replace("_", " ").title()
        elif (coal_metal_ind == None or coal_metal_ind == []):
            filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["SUBUNIT"].isin(mining_types) & df[data_field].isin(values)
            group_fields = ['CAL_YR', 'SUBUNIT', data_field]
            legend_title = data_field.replace("_", " ").title()
    else:            
        filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["SUBUNIT"].isin(mining_types)& df["COAL_METAL_IND"].isin(coal_metal_ind) & df[data_field].isin(values)
        group_fields = ['CAL_YR', 'SUBUNIT', 'COAL_METAL_IND', data_field]
        legend_title = data_field.replace("_", " ").title()

    data = df[filter_condition]
    dff = data.groupby(group_fields)['NO_INJURIES'].sum().reset_index(name='injuries')

    fig = go.Figure()
    fig.update_layout(
        title=dict(text="TOTAL NUMBER OF INJURIES", font=dict(size=18, family="sans-serif"), x=0.45),
        xaxis=dict(title_text="Years"),
        yaxis=dict(title_text="No of Injuries"),
        legend_title=legend_title,
        legend_title_font=dict(size=12),
        barmode="stack",
        showlegend=True,
        width=920, height=700
    )
    colors = px.colors.qualitative.Plotly
    for i, r in enumerate(dff[data_field].unique()):
        if mining_types is None or mining_types == []:
            plot_df = dff[dff[data_field] == r]
            fig.add_trace(
                go.Bar(x=plot_df.CAL_YR, y=plot_df.injuries,
                       name=r,
                       marker_color=colors[i % len(colors)],
                       hovertemplate='<b>Injuries:</b> %{y} <br>Year: %{x}<br>' + legend_title +': ' + r + '<extra></extra>')
            )
            fig.update_xaxes(tickfont=dict(size=9, family='sans-serif'), type='category')
            fig.update_yaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_layout(legend=dict(font=dict(size=7, family="sans-serif")))
        else:
            plot_df = dff[dff[data_field] == r]
            fig.add_trace(
                go.Bar(x=[plot_df.CAL_YR, plot_df.SUBUNIT], y=plot_df.injuries,
                       name=r,
                       marker_color=colors[i % len(colors)],
                       hovertemplate='<b>Injuries:</b> %{y} <br>Year: %{x}<br>' + legend_title +': ' + r + '<extra></extra>')
            )
            fig.update_xaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_yaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_layout(legend=dict(font=dict(size=7, family="sans-serif")))

    return fig, data

app.layout = dbc.Container([
    dcc.Tabs(
        className="dbc", children=[
        dbc.Tab(label="Health and Safety Analysis", children=[
            html.H1(id="Dataset-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.Div([
                            html.Label("Select Dataset:", style={'font-size': '12px'}),
                            dcc.Dropdown(
                                id='dataset-dropdown',
                                options=[
                                    {'label': 'Accidents', 'value': 'Accidents'},
                                    {'label': 'Inspections', 'value': 'inspections'},
                                    {'label': 'Mines', 'value': 'mines'},
                                    {'label': 'Mines Production', 'value': 'minesprodyearly'},
                                    {'label': 'Noise Samples', 'value': 'inspections'},
                                    {'label': 'Personal Health Samples', 'value': 'inspections'},
                                    {'label': 'Quartz Samples', 'value': 'quartzsamples'},
                                    {'label': 'Violations', 'value': 'violations'},
                                ],
                                style={'width': '100%', 'font-size': '12px'}
                            ),
                        ], style={'padding': '10px'}),
                        html.Div([
                            html.Label("Select Variable", style={'font-size': '12px'}),
                            dcc.Dropdown(
                                id="variable_type_dropdown",
                                style={'font-size': '12px'}
                            ),
                        ], style = {'padding': '10px'}),
                        html.Div(id="subunit_dropdown_container", style={'font-size': '12px','padding': '10px'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Markdown("**Years**", style={'font-size': '12px'}, className="no-bottom-margin"),
                                dcc.RangeSlider(
                                    id="date_slider",
                                    min=df["CAL_YR"].min(),
                                    max=df["CAL_YR"].max(),
                                    step=1,
                                    value=[df["CAL_YR"].min(), df["CAL_YR"].max()],
                                    marks=marks_year,
                                    vertical=True,
                                    className='custom-range-slider'
                                ),
                            ], width=3),
                            html.Br(),
                            dbc.Col([
                                dbc.Col([
                                dcc.Markdown("**Mining Type**", className="no-bottom-margin", style={'font-size': '12px'}),  
                                dcc.Checklist(
                                    id="mining_type_checklist",
                                    options=mining_type_options,
                                    labelStyle={'display': 'block','font-size': '10px'},
                                    className='custom-checklist'
                                ),
                            ], width=7),
                            html.Br(),
                            dbc.Col([
                                dcc.Markdown("**Coal Metal Indicator**", className="no-bottom-margin", style={'font-size': '12px'}),  
                                dcc.Checklist(
                                    id="coal_metal_checklist",
                                    options=coal_metal_options,
                                    labelStyle={'display': 'block','font-size': '10px'},
                                    className='custom-checklist'
                                ),
                            ], width=7)]),
                            
                            
                        ]),
                        html.Button('Submit', id='submit-button', value=1)
                    ])
                ], width=3),
                dbc.Col(dcc.Graph(id="injuries-graph"), width=9)
            ], justify="between"),
            html.Div(
                style={'overflowX': 'auto'},
                children=[
                    dash_table.DataTable(
                        id='data_table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=[],
                        style_table={'minWidth': '100%', 'height': '300px', 'overflowY': 'auto'},
                        filter_action='native',
                        sort_action='native',
                        export_format='csv',
                        style_header={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'lightgrey',
                            'font-family': 'Arial'
                        },
                        style_data={
                            'backgroundColor': 'rgb(80, 80, 80)',
                            'color': 'grey',
                            'font-family': 'Arial'
                        },
                        style_filter={
                            'backgroundColor': 'rgb(90, 90, 90)',
                            'color': 'grey',
                            'font-family': 'Arial'
                        }
                    )
                ]
            )
        ]),
        dbc.Tab(label="AI-based Integrated Models", children=[html.H1(id="ai_models")], style={'display': 'flex'})
    ]),
], style={"width": 1500})

@app.callback(
    Output("geographic-graph", "figure"),
    Output('total_injuries_display', 'children'),
    Output('number_violations', 'children'),
    Output('total_penalty', 'children'),
    Output("submit-button_main", "n_clicks"),
    Input("date_slider_main", "value"),
    Input("submit-button_main", "n_clicks"),
    Input("mining_type_checklist_main", "value"),
    Input("coal_metal_checklist_main", "value")
)

@app.callback(
    Output("variable_type_dropdown", "options"),
    Input('dataset-dropdown', "value")
)

def variable_options(dataset_ind):
    if dataset_ind is None or dataset_ind != 'Accidents':
        options = []
    else:
        options=[{'label': 'Total Injuries', 'value': 'total'},
                {'label': 'Degree of Injury', 'value': 'DEGREE_INJURY'},
                {'label': 'Injured Body Part', 'value': 'INJ_BODY_PART'},
                {'label': 'Injury Source', 'value': 'INJURY_SOURCE'},
                {'label': 'Nature of Injury', 'value': 'NATURE_INJURY'},
                {'label': 'Classification', 'value': 'CLASSIFICATION'},
                {'label': 'Accident Type', 'value': 'ACCIDENT_TYPE'}]
    return options

@app.callback(
    Output("subunit_dropdown_container", "children"),
    Input("variable_type_dropdown", "value"),
)

def data_type(data_type):
    if data_type is None:
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=[])
    elif data_type == 'total':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=[])
    elif data_type == 'DEGREE_INJURY':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options = [{'label': label, 'value': degree} for label, degree in zip(degree_labels, degree_injury)], multi=True)
    elif data_type == 'INJ_BODY_PART':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options = [{'label': label, 'value': body} for label, body in zip(injured_body_labels, injured_body)], multi=True)
    elif data_type == 'INJURY_SOURCE':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options = [{'label': label, 'value': source} for label, source in zip(injury_source_labels, injury_source)], multi=True)
    elif data_type == 'NATURE_INJURY':
        drop_down = dcc.Dropdown(id="dropdown",
                             options = [{'label': label, 'value': nature} for label, nature in zip(nature_injury_labels, nature_injury)], multi=True)
    elif data_type == 'CLASSIFICATION':
        drop_down = dcc.Dropdown(id="dropdown",
                             options = [{'label': label, 'value': classify} for label, classify in zip(classification_labels, classification)], multi=True)
    elif data_type == 'ACCIDENT_TYPE':
        drop_down = dcc.Dropdown(id="dropdown",
                             options = [{'label': label, 'value': accidents} for label, accidents in zip(accident_type_labels, accident_type)], multi=True)
    
    return drop_down

@app.callback(
    Output("injuries-graph", "figure"),
    Output("submit-button", "n_clicks"),
    Output('data_table', 'data'),
    Input('dataset-dropdown', 'value'),
    Input("variable_type_dropdown", "value"),
    Input("dropdown", "value"),
    Input("date_slider", "value"),
    Input("submit-button", "n_clicks"),
    Input("mining_type_checklist", "value"),
    Input("coal_metal_checklist", "value")
)

def update_graph(dataset_ind, data_type, sub_values, date_range, n_clicks, mining_types, coal_metal_ind):
    if dataset_ind is not None:
        file_path = f'C:/Users/danish/Desktop/new_dashboard/datasets/{dataset_ind}.txt'
        df = pd.read_csv(file_path, delimiter='|', encoding='ISO-8859-1', low_memory=False)
    if data_type is None:
        fig = px.line()
        data = []
        return fig, n_clicks, data
    if data_type == 'total':
        if not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            start_date, end_date = date_range
            years_between = [year for year in range(start_date, end_date + 1)]
            if (mining_types == None or mining_types == []) and (coal_metal_ind == None or coal_metal_ind == []):
                data = df[(df["CAL_YR"].between(start_date, end_date))]
                dff = data.groupby(['CAL_YR'])['NO_INJURIES'].sum().reset_index(name='injuries')
                graph_title = "TOTAL NUMBER OF INJURIES"
                fig = px.bar(dff, x="CAL_YR", y="injuries", barmode='group', 
                title=graph_title, 
                color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_layout(
                    title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                    xaxis_title="Year",
                    yaxis_title="Number of Injuries",
                    width=900, height=500)
                fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                fig.update_traces(hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><extra></extra>')               
            elif (mining_types == None or mining_types == []) or (coal_metal_ind == None or coal_metal_ind == []):
                if (mining_types == None or mining_types == []):
                    data = df[(df["CAL_YR"].between(start_date, end_date)) & (df["COAL_METAL_IND"].isin(coal_metal_ind))]
                    dff = data.groupby(['CAL_YR', 'COAL_METAL_IND'])['NO_INJURIES'].sum().reset_index(name='injuries')
                    graph_title = "TOTAL NUMBER OF INJURIES"
                    fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group', 
                    title=graph_title, 
                    color_discrete_sequence=px.colors.qualitative.Plotly)
                    fig.update_layout(
                        title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                        xaxis_title="Year",
                        yaxis_title="Number of Injuries",
                        legend_title="Coal or Metal Mining",
                        showlegend=True,
                        width=900, height=500)
                    fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                    fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                    fig.for_each_trace(
                        lambda trace: trace.update(
                            customdata=dff[dff["COAL_METAL_IND"] == trace.name]["COAL_METAL_IND"],
                            hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><b>Metal or Coal:</b> %{customdata}<extra></extra>'))
                elif (coal_metal_ind == None or coal_metal_ind == []):    
                    data = df[(df["CAL_YR"].between(start_date, end_date)) & (df["SUBUNIT"].isin(mining_types))]
                    dff = data.groupby(['CAL_YR', 'SUBUNIT'])['NO_INJURIES'].sum().reset_index(name='injuries')
                    graph_title = "TOTAL NUMBER OF INJURIES"
                    fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group', 
                    title=graph_title, 
                    color_discrete_sequence=px.colors.qualitative.Plotly)
                    fig.update_layout(
                        title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                        xaxis_title="Year",
                        yaxis_title="Number of Injuries",
                        legend_title="Mining Location",
                        showlegend=True,
                        width=900, height=500)
                    fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                    fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                    fig.for_each_trace(
                        lambda trace: trace.update(
                            customdata=dff[dff["SUBUNIT"] == trace.name]["SUBUNIT"],
                            hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><b>Mining Location:</b> %{customdata}<extra></extra>'))
            else:
                data = df[(df["CAL_YR"].between(start_date, end_date)) & (df["SUBUNIT"].isin(mining_types))& (df["COAL_METAL_IND"].isin(coal_metal_ind))]
                dff = data.groupby(['CAL_YR', 'SUBUNIT', 'COAL_METAL_IND'])['NO_INJURIES'].sum().reset_index(name='injuries')
                graph_title = "TOTAL NUMBER OF INJURIES"
                fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group', 
                title=graph_title, 
                color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_layout(
                    title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                    xaxis_title="Year",
                    yaxis_title="Number of Injuries",
                    legend_title="Mining Location",
                    showlegend=True,
                    width=900, height=500)
                fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                fig.for_each_trace(
                        lambda trace: trace.update(
                            hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><extra></extra>'))
            n_clicks = None
            data = data.to_dict('records')
            return fig, n_clicks, data
    if data_type == 'DEGREE_INJURY':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'INJ_BODY_PART':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'INJURY_SOURCE':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'NATURE_INJURY':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'CLASSIFICATION':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'ACCIDENT_TYPE':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else: 
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data

if __name__ == "__main__":
    app.run_server(port=2000, jupyter_mode='external')