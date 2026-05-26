import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import streamlit as st
import plotly.graph_objs as go



# ----- Start and stop buttons -----
def start_stop_buttons(markers_path):
    # Initialize session state for each activity
    for i in range(3):
        if f'start_{i}' not in st.session_state:
            st.session_state[f'start_{i}'] = None
        if f'stop_{i}' not in st.session_state:
            st.session_state[f'stop_{i}'] = None

    st.title("Activity Marker Recorder")

    for i in range(3):
        st.subheader(f"Activity {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Start Activity {i+1}"):
                st.session_state[f'start_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with col2:
            if st.button(f"Stop Activity {i+1}"):
                st.session_state[f'stop_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Start: {st.session_state[f'start_{i}']}")
        st.write(f"Stop: {st.session_state[f'stop_{i}']}")

    # Save markers to file
    if st.button("Save Markers"):
        for i in range(3):
            marker = {
                "start_time": st.session_state[f'start_{i}'],
                "stop_time": st.session_state[f'stop_{i}']
            }
            marker_file = os.path.join(markers_path, f"activity_{i}_window.json")
            with open(marker_file, "w") as f:
                json.dump(marker, f)
        st.success("Markers saved!")

# ----- Load json data -----
def get_todays_date(data_path):
    # Get today's date in YYYY-MM-DD format
    date = datetime.now().strftime("%Y-%m-%d")
    file_name = f'{data_path}/{date}_accelerometer.json'
    return file_name

def get_marker_data(markers_path):
    markers = {}
    # Get marker files (x3) (i.e. start stop times of each activity)
    for act_num in range(3): # 0,1, 2
        marker_file_name = f'activity_{act_num}_window.json'
        marker_file = os.path.join(markers_path, marker_file_name)
        with open(marker_file) as f:
            markers[act_num] = json.load(f)
    return markers

# ----- Divide activity data -----
def get_activity_data(markers, data):
    activity_data = {0: [], 1: [], 2: []}
    for act_num in range(3):
        start_time = datetime.strptime(markers[act_num]['start_time'], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(markers[act_num]['stop_time'], "%Y-%m-%d %H:%M:%S")
        for entry in data:
            entry_time = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
            if start_time <= entry_time <= end_time:
                activity_data[act_num].append(entry)
    return [activity_data[0], activity_data[1], activity_data[2]]


# ----- Shuffle the activity data -----
def shuffle_plots(activity_data_list):
    indices = list(range(3))
    random.shuffle(indices)
    return [activity_data_list[i] for i in indices], indices


# ----- Plot the shuffled activity data -----
def plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names):
    # Set page to wide mode
    # st.set_page_config(layout="wide")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .stPlotlyChart {
            width: 100%;
            height: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create a 2x2 grid layout
    top_col1, top_col2 = st.columns([1, 1])
    bottom_col = st.container()

    # Plot the first two activities in the top row
    for i, data in enumerate(shuffled_activities[:2]):
        with top_col1 if i == 0 else top_col2:
            st.subheader(f'Activity {activity_names[i]}')
            fig = go.Figure()
            x_vals = [d['x'] for d in data]
            y_vals = [d['y'] for d in data]
            z_vals = [d['z'] for d in data]
            fig.add_trace(go.Scatter(y=x_vals, mode='lines', name='X'))
            fig.add_trace(go.Scatter(y=y_vals, mode='lines', name='Y'))
            fig.add_trace(go.Scatter(y=z_vals, mode='lines', name='Z'))
            
            # Update layout for top plots
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            st.plotly_chart(fig, use_container_width=True, key=f"plot_{i}")

    # Plot the third activity in the bottom row
    with bottom_col:
        st.subheader(f'Activity {activity_names[2]}')
        fig = go.Figure()
        x_vals = [d['x'] for d in shuffled_activities[2]]
        y_vals = [d['y'] for d in shuffled_activities[2]]
        z_vals = [d['z'] for d in shuffled_activities[2]]
        fig.add_trace(go.Scatter(y=x_vals, mode='lines', name='X'))
        fig.add_trace(go.Scatter(y=y_vals, mode='lines', name='Y'))
        fig.add_trace(go.Scatter(y=z_vals, mode='lines', name='Z'))
        
        # Update layout for bottom plot
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        st.plotly_chart(fig, use_container_width=True, key="plot_2")

    if st.button('Reveal answers'):
        st.write(f'the correct mapping was:')
        for i, idx in enumerate(shuffled_indices):
            st.write(f'Activity {activity_names[i]}: Original Activity {idx+1}')

if __name__ == "__main__":
    st.set_page_config(layout="wide")  # Add this at the start of your main script

    data_path = '/rds/general/user/cr620/home/GERF/fitbitaccapp/data/' # ------------------------- CHANGE THIS
    markers_path = '/rds/general/user/cr620/home/GERF/activities/'

    start_stop_buttons(markers_path)

    # get marker data
    markers = get_marker_data(markers_path)

    # get activity data   
    data_file_name = get_todays_date(data_path)
    data_file = os.path.join(data_path, data_file_name)
    with open(data_file) as f:
        data = json.load(f)
    activity_data_list = get_activity_data(markers, data)

    # shuffling of data
    st.title('Guess the activity')
    st.write('Below are the accelerometer plots for three activities. Can you guess which is which?')
    shuffled_activities, shuffled_indices = shuffle_plots(activity_data_list)
    activity_names = ['A', 'B', 'C']

    # plot the shuffled activity data
    plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names) 


    # to run the app: "streamlit run filter_data.py"
    