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
# def start_stop_buttons(markers_path):
#     # Initialize session state for each activity
#     for i in range(3):
#         if f'start_{i}' not in st.session_state:
#             st.session_state[f'start_{i}'] = None
#         if f'stop_{i}' not in st.session_state:
#             st.session_state[f'stop_{i}'] = None
#         if f'activity_type_{i}' not in st.session_state:
#             st.session_state[f'activity_type_{i}'] = ""

#     st.title("Activity Marker Recorder")

#     for i in range(3):
#         st.subheader(f"Activity {i+1}")
#         # Add activity type input
#         st.session_state[f'activity_type_{i}'] = st.text_input(
#             f"Type of Activity {i+1}",
#             value=st.session_state[f'activity_type_{i}'],
#             key=f"type_input_{i}"
#         )
        
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button(f"Start Activity {i+1}"):
#                 st.session_state[f'start_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         with col2:
#             if st.button(f"Stop Activity {i+1}"):
#                 st.session_state[f'stop_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         st.write(f"Start: {st.session_state[f'start_{i}']}")
#         st.write(f"Stop: {st.session_state[f'stop_{i}']}")

#     # Save markers to file
#     if st.button("Save Markers"):
#         for i in range(3):
#             marker = {
#                 "start_time": st.session_state[f'start_{i}'],
#                 "stop_time": st.session_state[f'stop_{i}'],
#                 "activity_type": st.session_state[f'activity_type_{i}']
#             }
#             marker_file = os.path.join(markers_path, f"activity_{i}_window.json")
#             with open(marker_file, "w") as f:
#                 json.dump(marker, f)
#         st.success("Markers saved!")

def start_stop_buttons(markers_path):
    # Initialize session state for each activity
    for i in range(3):
        if f'start_{i}' not in st.session_state:
            st.session_state[f'start_{i}'] = None
        if f'stop_{i}' not in st.session_state:
            st.session_state[f'stop_{i}'] = None
        if f'activity_type_{i}' not in st.session_state:
            st.session_state[f'activity_type_{i}'] = ""

    st.title("Activity Marker Recorder")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Place activity controls in the first three grid spaces
    with col1:
        st.subheader("Activity 1")
        st.session_state['activity_type_0'] = st.text_input(
            "Type of Activity 1",
            value=st.session_state['activity_type_0'],
            key="type_input_0"
        )
        if st.button("Start Activity 1"):
            st.session_state['start_0'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if st.button("Stop Activity 1"):
            st.session_state['stop_0'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Start: {st.session_state['start_0']}")
        st.write(f"Stop: {st.session_state['stop_0']}")

    with col2:
        st.subheader("Activity 2")
        st.session_state['activity_type_1'] = st.text_input(
            "Type of Activity 2",
            value=st.session_state['activity_type_1'],
            key="type_input_1"
        )
        if st.button("Start Activity 2"):
            st.session_state['start_1'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if st.button("Stop Activity 2"):
            st.session_state['stop_1'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Start: {st.session_state['start_1']}")
        st.write(f"Stop: {st.session_state['stop_1']}")

    with col3:
        st.subheader("Activity 3")
        st.session_state['activity_type_2'] = st.text_input(
            "Type of Activity 3",
            value=st.session_state['activity_type_2'],
            key="type_input_2"
        )
        if st.button("Start Activity 3"):
            st.session_state['start_2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if st.button("Stop Activity 3"):
            st.session_state['stop_2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Start: {st.session_state['start_2']}")
        st.write(f"Stop: {st.session_state['stop_2']}")

    # Add animation in the fourth grid space
    with col4:
        st.subheader("Activity Demonstration")
        
        # Option 1: Upload a video file
        video_file = st.file_uploader("Upload a demonstration video", type=['mp4', 'mov', 'avi'])
        if video_file is not None:
            st.video(video_file)
        
        # Option 2: Use a video from a URL
        # st.video("https://www.youtube.com/watch?v=your_video_id")
        
        # Option 3: Use a local video file
        # video_path = "path/to/your/video.mp4"
        # if os.path.exists(video_path):
        #     st.video(video_path)

    # Save markers to file
    if st.button("Save Markers"):
        for i in range(3):
            marker = {
                "start_time": st.session_state[f'start_{i}'],
                "stop_time": st.session_state[f'stop_{i}'],
                "activity_type": st.session_state[f'activity_type_{i}']
            }
            marker_file = os.path.join(markers_path, f"activity_{i}_window.json")
            with open(marker_file, "w") as f:
                json.dump(marker, f)
        st.success("Markers saved!")

def plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names, markers):
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

    # Define color schemes for each activity
    color_schemes = {
        'A': {'x': '#1f77b4', 'y': '#ff7f0e', 'z': '#2ca02c'},  # Blue, Orange, Green
        'B': {'x': '#d62728', 'y': '#9467bd', 'z': '#8c564b'},  # Red, Purple, Brown
        'C': {'x': '#e377c2', 'y': '#7f7f7f', 'z': '#bcbd22'}   # Pink, Gray, Yellow
    }

    # Initialize session state for guesses and revealed answers if not exists
    if 'guesses' not in st.session_state:
        st.session_state.guesses = {}
    if 'revealed_answers' not in st.session_state:
        st.session_state.revealed_answers = {}

    # Plot the first two activities in the top row
    for i, data in enumerate(shuffled_activities[:2]):
        with top_col1 if i == 0 else top_col2:
            st.subheader(f'Activity {activity_names[i]}')
            
            # Create columns for plot and reveal button
            plot_col, button_col = st.columns([4, 1])
            
            with plot_col:
                fig = go.Figure()
                x_vals = [d['x'] for d in data]
                y_vals = [d['y'] for d in data]
                z_vals = [d['z'] for d in data]
                
                # Use color scheme for this activity
                colors = color_schemes[activity_names[i]]
                fig.add_trace(go.Scatter(y=x_vals, mode='lines', name='X', line=dict(color=colors['x'])))
                fig.add_trace(go.Scatter(y=y_vals, mode='lines', name='Y', line=dict(color=colors['y'])))
                fig.add_trace(go.Scatter(y=z_vals, mode='lines', name='Z', line=dict(color=colors['z'])))
                
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
            
            with button_col:
                if st.button("Reveal Answer", key=f"reveal_{i}"):
                    st.session_state.revealed_answers[activity_names[i]] = True
            
            # Add guess input
            guess = st.text_input(f"Guess the activity type for Activity {activity_names[i]}", 
                                key=f"guess_{i}")
            st.session_state.guesses[activity_names[i]] = guess
            
            # Show answer if revealed
            if activity_names[i] in st.session_state.revealed_answers:
                correct_type = markers[shuffled_indices[i]]['activity_type']
                st.write(f"Correct answer: {correct_type}")
                if guess.lower() == correct_type.lower():
                    st.success("Your guess was correct! 🎉")
                else:
                    st.error("Your guess was incorrect!")

    # Plot the third activity in the bottom row
    with bottom_col:
        st.subheader(f'Activity {activity_names[2]}')
        
        # Create columns for plot and reveal button
        plot_col, button_col = st.columns([4, 1])
        
        with plot_col:
            fig = go.Figure()
            x_vals = [d['x'] for d in shuffled_activities[2]]
            y_vals = [d['y'] for d in shuffled_activities[2]]
            z_vals = [d['z'] for d in shuffled_activities[2]]
            
            # Use color scheme for the third activity
            colors = color_schemes[activity_names[2]]
            fig.add_trace(go.Scatter(y=x_vals, mode='lines', name='X', line=dict(color=colors['x'])))
            fig.add_trace(go.Scatter(y=y_vals, mode='lines', name='Y', line=dict(color=colors['y'])))
            fig.add_trace(go.Scatter(y=z_vals, mode='lines', name='Z', line=dict(color=colors['z'])))
            
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
        
        with button_col:
            if st.button("Reveal Answer", key="reveal_2"):
                st.session_state.revealed_answers[activity_names[2]] = True
        
        # Add guess input for third activity
        guess = st.text_input(f"Guess the activity type for Activity {activity_names[2]}", 
                            key=f"guess_2")
        st.session_state.guesses[activity_names[2]] = guess
        
        # Show answer if revealed
        if activity_names[2] in st.session_state.revealed_answers:
            correct_type = markers[shuffled_indices[2]]['activity_type']
            st.write(f"Correct answer: {correct_type}")
            if guess.lower() == correct_type.lower():
                st.success("Your guess was correct! 🎉")
            else:
                st.error("Your guess was incorrect!")

    
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


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    data_path = '/rds/general/user/cr620/home/GERF/fitbitaccapp/data/'
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

    # shuffling of data - only if not already in session state
    st.title('Guess the activity')
    st.write('Below are the accelerometer plots for three activities. Can you guess which is which?')
    

    if 'shuffled_activities' not in st.session_state or 'shuffled_indices' not in st.session_state:
        shuffled_activities, shuffled_indices = shuffle_plots(activity_data_list)
        st.session_state.shuffled_activities = shuffled_activities
        st.session_state.shuffled_indices = shuffled_indices
    else:
        shuffled_activities = st.session_state.shuffled_activities
        shuffled_indices = st.session_state.shuffled_indices

    activity_names = ['A', 'B', 'C']

    plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names, markers)


    if st.button("Shuffle Again"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # to run the app: "streamlit run filter_data_flip_plots.py"



    # increase font size, make reveal button bigger -- BIG LETTERS
    # increase width of plot lines
    # add more text colors, and font type - basically all children friendly
    # add UKDRI , mrc and imperial logos



    # do a 2x2 grid, plot C should be in 0,1 - on 1,1 do a congrats! you passed  kinda thing