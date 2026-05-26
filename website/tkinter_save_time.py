import tkinter as tk
from datetime import datetime
import json
import os

def record_marker(activity, action):
    now = datetime.now().strftime("%Y-%m/%d %H:%M:%S")
    if activity not in markers:
        markers[activity] = {}
    markers[activity][action] = now
    with open('markers.json', 'w') as f:
        json.dump(markers, f, indent=4)
    label_status.config(text=f'{action} for {activity} at {now}')

if __name__ == '__main__':
    markers = {}

    root = tk.Tk()
    root.title('Activity Marker')

    label_status = tk.Label(root, text='Ready')
    label_status.pack()

    for act in ['Activity1', 'Activity2', 'Activity3']:
        frame = tk.Frame(root)
        frame.pack()
        btn_Start = tk.Button(frame, text=f'start_time', command=lambda a=act: record_marker(a, 'Start'))
        btn_Stop = tk.Button(frame, text=f'stop_time', command=lambda a=act: record_marker(a, 'Stop'))

        btn_Start.pack(side='left', padx=5)
        btn_Stop.pack(side='left', padx=5)

    root.mainloop()