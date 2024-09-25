import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager



def scatter_ranking(df_selected, highlight_user='', crests=None):

    # Flatten the column names in df_selected
    df = df_selected.copy()
    
    # Ensure the correct columns are used for plotting
    score_columns = ['Calcio', 'Personale', 'Tecnologia', 'Economico']
    
    # Extract the relevant columns
    df = df[['Nome', 'Cognome', 'Email'] + score_columns]

    # Identify the user to highlight based on email
    highlight_user_row = df[df['Email'] == highlight_user]
    highlight_name = highlight_user_row['Nome'].values[0] if not highlight_user_row.empty else None
    
    # Prepare an empty DataFrame to store rankings
    ranked_df = df.set_index('Email')[score_columns].rank(ascending=False, method='min', pct=False)
    rank_col = 'Rank'

    # Flatten the DataFrame for plotly to use in long-form
    df_long = df.melt(id_vars=['Nome', 'Cognome', 'Email'], var_name='Metric', value_name='Value')
    ranked_long = ranked_df.melt(var_name='Metric', value_name=rank_col, ignore_index=False)



    # Merge using the correct method
    plot_df = pd.merge(left=df_long, right=ranked_long.reset_index(), 
                       left_on=['Email', 'Metric'], right_on=['Email', 'Metric'])
    
    plot_df['Value'] = plot_df['Value'].astype(int)
    
    # Map metrics to numeric values (1, 2, 3, ...)
    metric_order = {metric: i+1 for i, metric in enumerate(score_columns)}
    plot_df['MetricNumeric'] = plot_df['Metric'].map(metric_order)

    # Compute best and worst values per metric
    best_values = df[score_columns].max()
    worst_values = df[score_columns].min()

    # Add the best and worst values to the DataFrame
    plot_df['Best'] = plot_df['Metric'].map(best_values)
    plot_df['Worst'] = plot_df['Metric'].map(worst_values)

    # Set the marker size and opacity for the highlighted user
    plot_df['MarkerSize'] = np.where(plot_df['Email'] == highlight_user, 20, 10)
    plot_df['Alpha'] = np.where(plot_df['Email'] == highlight_user, 1.0, 0.3)

    # Create scatter plot with vertical noise and different marker sizes for the highlighted user
    fig = go.Figure()

    # Iterate over unique metrics to create separate traces for each metric
    for metric in plot_df['Metric'].unique():
        metric_data = plot_df[plot_df['Metric'] == metric]

        fig.add_trace(go.Scatter(
            x=metric_data[rank_col],
            y=metric_data['MetricNumeric'],
            mode='markers',
            marker=dict(
                size=metric_data['MarkerSize'],
                color=metric_data['MetricNumeric'],
                opacity=metric_data['Alpha']
            ),
            name=metric,
            customdata=metric_data[['Nome', 'Cognome', 'Metric', 'Value', rank_col, 'Best', 'Worst']].values,
            hovertemplate=(
                "<b>%{customdata[0]} %{customdata[1]}</b><br>"  # Name and surname
                "%{customdata[2]}: %{customdata[3]}<br>"  # Metric and value
                "Rank = %{x}<br>"  # Rank
                "Min value = %{customdata[6]}<br>"  # Min value
                "Max value = %{customdata[5]}<br>"  # Max value
                "<extra></extra>"
            )
        ))

    title = 'User Ranking' if not highlight_name else f'User Ranking | {highlight_name}'
    fig.update_layout(
        yaxis=dict(
            tickvals=list(metric_order.values()),
            ticktext=list(metric_order.keys()),
            title=''
        ),
        xaxis=dict(autorange='reversed', showticklabels=False),
        showlegend=False,
        title=title,
        height=125 * len(score_columns) if len(score_columns) > 1 else 300
    )

    # Annotate min, max, and highlighted user's values
    for metric in plot_df['Metric'].unique():
        min_row = plot_df[plot_df['Metric'] == metric].nsmallest(1, 'Value')
        max_row = plot_df[plot_df['Metric'] == metric].nlargest(1, 'Value')
        highlight_row = plot_df[(plot_df['Metric'] == metric) & (plot_df['Email'] == highlight_user)]

        # Min and max annotations
        fig.add_annotation(x=min_row[rank_col].values[0] + 0.2, y=min_row['MetricNumeric'].values[0],
                           text=f"{min_row['Value'].values[0]}", showarrow=False, font=dict(size=12, color="black"))
        fig.add_annotation(x=max_row[rank_col].values[0] - 0.2, y=max_row['MetricNumeric'].values[0],
                           text=f"{max_row['Value'].values[0]}", showarrow=False, font=dict(size=12, color="black"))

        # Highlight user annotation
        if not highlight_row.empty:
            fig.add_annotation(x=highlight_row[rank_col].values[0], y=highlight_row['MetricNumeric'].values[0] + 0.3,
                               text=f"{highlight_row['Value'].values[0]}", showarrow=False, font=dict(size=12))

    return fig


def radar_plot(df_selected, highlight_user='', params=[], mapping=None):

    if mapping:
        labels = [mapping[k] for k in mapping.keys()]
    else:
        labels = params
    

    low = df_selected[params].min(axis=0)
    high = df_selected[params].max(axis=0)

    user_record = df_selected.loc[df_selected['Email'] == highlight_user, :].iloc[0]
    user_data = user_record[params]
    mean_data = df_selected.loc[df_selected['Email'] != highlight_user, params].mean().values

   
    radar = Radar(labels, low, high,
              lower_is_better=[],
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*len(params),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
    
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

    radar.setup_axis(ax=axs['radar'])  # format axis as a radar
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')

    radar1, vertices1 = radar.draw_radar_solid(mean_data, ax=axs['radar'],
                                            kwargs={'facecolor': '#8dbe21',
                                                    'alpha': 0.45,
                                                    'edgecolor': '#216352',
                                                    'lw': 3})

    radar2, vertices2 = radar.draw_radar_solid(user_data, ax=axs['radar'],
                                            kwargs={'facecolor': '#0091a8',
                                                    'alpha': 0.45,
                                                    'edgecolor': '#216352',
                                                    'lw': 3})



    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
            c='#8dbe21', edgecolors='#502a54', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
            c='#0091a8', edgecolors='#216352', marker='o', s=150, zorder=2)
    
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=12, )
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=16, )

    title1_text = axs['title'].text(0.01, 0.65, f"{user_record['Nome']} {user_record['Cognome']}", fontsize=25, 
                                    color='#0091a8',
                                    ha='left', va='center')
    title2_text = axs['title'].text(0.01, 0.25, f"{user_record['Email']}", fontsize=20,
                                ha='left', va='center', color='#0091a8')
    
    title3_text = axs['title'].text(0.99, 0.65, 'Sport Analisi Academy', fontsize=25,
                                ha='right', va='center', color='#8dbe21')
    title4_text = axs['title'].text(0.99, 0.25, 'utente medio', fontsize=20,
                                    ha='right', va='center', color='#8dbe21')

    return fig

def pizza_plot(df_selected, highlight_user='', params=[], mapping={}):

    df = df_selected.copy()

    if mapping:
        labels = [mapping[k] for k in mapping.keys()]
    else:
        labels = params

    

    ranked_df = df.set_index(['Nome', 'Cognome','Email'])[params].rank(ascending=True, pct=True, method='max').reset_index()
    rank_col = 'Rank'

    user_record = ranked_df.loc[ranked_df['Email'] == highlight_user].iloc[0]
    user_values = list(map(int, user_record[params]*100))


    slice_colors = ["#1A78CF"]  + ["#FF9300"]  + ["#D70232"] + ['#8dbe21']
    text_colors = ["#000000"]*len(params) 

    # instantiate PyPizza class
    baker = PyPizza(
        params=labels,                  # list of parameters
        background_color="#ffffff",     # background color
        straight_line_color="#EBEBE9",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        user_values,                          # list of values
        figsize=(6, 6.5),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=11,
            va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )

    # add title
    # fig.text(
    #     0.515, 0.975, f"{user_record['Nome']} {user_record['Cognome']}", size=16,
    #     ha="center", color="#000000"
    # )

    # add subtitle
    fig.text(
        0.515, 0.945,
        f"{user_record['Nome']} {user_record['Cognome']} vs Utenti Sport Analisi Academy",
        size=13,
        ha="center", color="#000000"
    )


    


    return fig