import json
from contextlib import contextmanager
from datetime import datetime
import math
import os
import random
import pandas as pd
import streamlit as st
import plotly.graph_objs as go


ACTIVITY_LETTERS = ["A", "B", "C"]
MISSION_PROMPTS = [
    {"accent": "#ff70b8", "soft": "#fff0f7"},
    {"accent": "#00bcd4", "soft": "#e8fbff"},
    {"accent": "#7c5cff", "soft": "#f3eeff"},
]
MYSTERY_STYLES = {
    "A": {"badge": "#ff4fa3", "glow": "rgba(255, 79, 163, 0.18)"},
    "B": {"badge": "#ff9f1c", "glow": "rgba(255, 159, 28, 0.18)"},
    "C": {"badge": "#3d52d5", "glow": "rgba(61, 82, 213, 0.18)"},
}
TIP_EXAMPLES = [
    {"title": "Tall waves", "caption": "Big moves like jumps make tall peaks and deep dips.", "color": "#ff4fa3", "fill": "rgba(255, 79, 163, 0.18)"},
    {"title": "Squiggly waves", "caption": "Fast moves like running or shaking make lots of tiny wiggles.", "color": "#00bcd4", "fill": "rgba(0, 188, 212, 0.18)"},
    {"title": "Calm waves", "caption": "Slow or still poses look flatter and sleepier.", "color": "#7c5cff", "fill": "rgba(124, 92, 255, 0.18)"},
]


def inject_child_friendly_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Capriola&family=DynaPuff:wght@400..700&family=Nunito:wght@600;700;800&display=swap');

        :root {
            --sky: #76d7ff;
            --bubblegum: #ff70b8;
            --sunshine: #ffd166;
            --mint: #66e6b3;
            --grape: #7c5cff;
            --ink: #24335f;
            --card: rgba(255, 255, 255, 0.86);
        }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 12% 18%, rgba(255, 209, 102, 0.35), transparent 22rem),
                radial-gradient(circle at 88% 14%, rgba(255, 112, 184, 0.24), transparent 20rem),
                radial-gradient(circle at 18% 84%, rgba(102, 230, 179, 0.28), transparent 24rem),
                linear-gradient(180deg, #fcfdff 0%, #f3f8ff 48%, #fff7fb 100%);
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2.5rem;
            max-width: 1280px;
        }

        #MainMenu, footer, header { visibility: hidden; }

        p, div, label, span {
            font-family: 'Nunito', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'DynaPuff', cursive !important;
            color: var(--ink) !important;
        }

        .hero-shell {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 1.4rem;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        @media (max-width: 900px) {
            .hero-shell { grid-template-columns: 1fr; }
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2rem 1.8rem;
            border: 3px solid rgba(255, 255, 255, 0.95);
            border-radius: 32px;
            background: linear-gradient(145deg, rgba(255,255,255,0.98), rgba(255,255,255,0.82));
            box-shadow: 0 18px 40px rgba(86, 87, 191, 0.14);
        }

        .hero-card:before {
            content: "";
            position: absolute;
            width: 180px;
            height: 180px;
            right: -50px;
            top: -60px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(255, 209, 102, 0.45), transparent 70%);
        }

        .hero-eyebrow {
            display: inline-block;
            padding: 0.35rem 0.85rem;
            margin-bottom: 0.55rem;
            border-radius: 999px;
            background: #f3eeff;
            color: #7c5cff;
            font-size: 0.85rem;
            font-weight: 900;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0;
            font-family: 'Capriola', cursive;
            font-size: clamp(2.6rem, 6vw, 4.8rem);
            line-height: 1.02;
            color: #3d52d5;
        }

        .hero-subtitle {
            max-width: 34rem;
            margin: 0.85rem 0 0;
            font-size: 1.15rem;
            font-weight: 700;
            color: #536078;
            line-height: 1.55;
        }

        .hero-steps {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1.1rem;
        }

        .hero-step {
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: white;
            border: 2px solid #eadcff;
            font-size: 0.92rem;
            font-weight: 800;
            color: #573fa9;
        }

        .hero-art {
            position: relative;
            min-height: 260px;
            padding: 1rem;
            border-radius: 32px;
            background: linear-gradient(160deg, #fff6bf 0%, #d9f7ff 55%, #ffe3f3 100%);
            border: 3px solid rgba(255,255,255,0.95);
            box-shadow: 0 18px 40px rgba(86, 87, 191, 0.12);
            overflow: hidden;
        }

        .hero-art svg {
            width: 100%;
            height: auto;
            display: block;
        }

        .section-box-anchor {
            display: none;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-box-tips) {
            background: #f0ebff;
            border: 2px solid #d4c4ff !important;
            border-radius: 26px;
            padding: 1.25rem 1.35rem 1.5rem;
            margin: 0.75rem 0 4.5rem;
            box-shadow: 0 10px 28px rgba(124, 92, 255, 0.08);
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-box-record) {
            background: #e8faf4;
            border: 2px solid #b8e8d4 !important;
            border-radius: 26px;
            padding: 1.25rem 1.35rem 1.5rem;
            margin: 1.5rem 0 1.75rem;
            box-shadow: 0 10px 28px rgba(46, 196, 182, 0.08);
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-box-tips) .section-banner,
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-box-record) .section-banner {
            margin-top: 0;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.88);
            border-color: rgba(255, 255, 255, 0.95);
        }

        .section-banner {
            margin: 1.6rem 0 1rem;
            padding: 1rem 1.25rem;
            border-radius: 24px;
            background: white;
            border: 2px solid #eadcff;
            box-shadow: 0 10px 24px rgba(78, 88, 160, 0.08);
        }

        .section-banner h2 {
            margin: 0;
            font-size: 1.85rem;
            color: #3d52d5 !important;
        }

        .section-banner p {
            margin: 0.25rem 0 0;
            font-size: 1rem;
            font-weight: 700;
            color: #536078;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 12px 28px rgba(78, 88, 160, 0.08);
        }

        .mission-card-head {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.35rem;
        }

        .mission-icon {
            width: 3.2rem;
            height: 3.2rem;
            border-radius: 18px;
            display: grid;
            place-items: center;
            font-size: 1.6rem;
            flex-shrink: 0;
        }

        .mission-title {
            margin: 0;
            font-family: 'DynaPuff', cursive;
            font-size: 1.45rem;
            color: #3d52d5;
        }

        .mission-hint {
            margin: 0 0 0.75rem;
            font-weight: 700;
            color: #536078;
            line-height: 1.45;
        }

        .time-chip {
            display: inline-block;
            min-width: 46%;
            margin: 0.15rem 0.15rem 0.05rem 0;
            padding: 0.45rem 0.65rem;
            border-radius: 999px;
            background: #f7f0ff;
            border: 2px solid #eadcff;
            font-size: 0.88rem;
            font-weight: 800;
            color: #573fa9;
        }

        .tips-grid-head {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            margin-bottom: 0.35rem;
        }

        .tips-icon {
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 20px;
            background: linear-gradient(135deg, #fff6bf, #d9f7ff);
            display: grid;
            place-items: center;
            font-size: 1.8rem;
        }

        .example-card {
            padding: 0.35rem 0.15rem 0.15rem;
        }

        .example-head {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.35rem;
        }

        .example-emoji {
            width: 2.4rem;
            height: 2.4rem;
            border-radius: 14px;
            display: grid;
            place-items: center;
            font-size: 1.25rem;
            background: white;
            border: 2px solid #eadcff;
        }

        .example-title {
            margin: 0;
            font-family: 'DynaPuff', cursive;
            font-size: 1.15rem;
            color: #3d52d5;
        }

        .example-caption {
            min-height: 4rem;
            padding: 0.65rem 0.8rem;
            border-radius: 16px;
            background: #faf8ff;
            border: 2px solid #ece6ff;
            color: #536078;
            font-size: 0.92rem;
            font-weight: 700;
            line-height: 1.4;
        }

        .mystery-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.45rem 0.85rem 0.45rem 0.45rem;
            border-radius: 999px;
            background: white;
            border: 2px solid #eadcff;
            margin-bottom: 0.35rem;
        }

        .mystery-badge-dot {
            width: 2.2rem;
            height: 2.2rem;
            border-radius: 999px;
            display: grid;
            place-items: center;
            color: white;
            font-family: 'DynaPuff', cursive;
            font-size: 1.1rem;
            font-weight: 800;
        }

        .plot-title {
            margin: 0;
            font-family: 'DynaPuff', cursive;
            font-size: 1.55rem;
            color: #3d52d5;
        }

        .plot-helper {
            margin: 0.15rem 0 0.75rem;
            font-size: 0.95rem;
            font-weight: 700;
            color: #536078;
        }

        .answer-card {
            padding: 0.75rem 0.9rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #fff6bf, #ffe0f2);
            border: 2px dashed #ff70b8;
            font-size: 1.05rem;
            font-weight: 900;
            text-align: center;
        }

        .action-row {
            margin-top: 0.35rem;
        }

        .stTextInput > div > div > input {
            border: 2px solid #d6cbff;
            border-radius: 16px;
            font-family: 'Nunito', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            padding: 0.7rem 0.95rem;
            background: rgba(255,255,255,0.96);
        }

        .stButton > button {
            border: 0 !important;
            border-radius: 999px !important;
            font-family: 'DynaPuff', cursive !important;
            font-size: 1rem !important;
            font-weight: 800 !important;
            min-height: 2.85rem !important;
            padding: 0.65rem 1rem !important;
            box-shadow: 0 6px 0 rgba(36, 51, 95, 0.12), 0 10px 20px rgba(78, 88, 160, 0.12);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 0 rgba(36, 51, 95, 0.10), 0 14px 24px rgba(78, 88, 160, 0.16);
        }

        .stAlert {
            border-radius: 18px;
            border: 0;
            font-weight: 800;
        }

        .logo-section {
            text-align: center;
            margin: 2rem 0 0;
            padding: 1.2rem;
            background: rgba(255, 255, 255, 0.88);
            border-radius: 24px;
            border: 2px solid #ece6ff;
            box-shadow: 0 10px 24px rgba(78, 88, 160, 0.08);
        }

        .stPlotlyChart {
            border-radius: 20px;
            overflow: hidden;
            background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248, 250, 255, 0.95));
            border: 2px solid #ece6ff;
        }
        </style>
    """, unsafe_allow_html=True)


def render_hero():
    st.markdown("""
        <div class="hero-shell">
            <div class="hero-card">
                <div class="hero-eyebrow">Movesense Motion Lab</div>
                <h1 class="hero-title">Move With Tech!</h1>
                <p class="hero-subtitle">
                    Move, record your wiggles, then become a graph detective and match each mystery wave to the activity that made it.
                </p>
                <div class="hero-steps">
                    <span class="hero-step">1. Record moves</span>
                    <span class="hero-step">2. Save markers</span>
                    <span class="hero-step">3. Guess the graphs</span>
                </div>
            </div>
            <div class="hero-art">
                <svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Motion sensor and movement waves">
                    <defs>
                        <linearGradient id="sensorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#7c5cff"/>
                            <stop offset="100%" stop-color="#3daceb"/>
                        </linearGradient>
                        <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#ff4fa3"/>
                            <stop offset="50%" stop-color="#00bcd4"/>
                            <stop offset="100%" stop-color="#ffd166"/>
                        </linearGradient>
                    </defs>
                    <circle cx="70" cy="48" r="18" fill="#fff6bf"/>
                    <circle cx="360" cy="42" r="14" fill="#ffe0f2"/>
                    <circle cx="340" cy="210" r="22" fill="#d9f7ff"/>
                    <rect x="36" y="48" width="92" height="118" rx="22" fill="url(#sensorGrad)"/>
                    <rect x="52" y="64" width="60" height="44" rx="12" fill="white" opacity="0.92"/>
                    <circle cx="82" cy="132" r="10" fill="#ffd166"/>
                    <path d="M170 170 C 205 70, 245 230, 280 95 S 350 185, 390 120" fill="none" stroke="url(#waveGrad)" stroke-width="8" stroke-linecap="round"/>
                    <path d="M170 198 C 210 150, 250 210, 290 170 S 345 190, 390 176" fill="none" stroke="#7c5cff" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
                    <circle cx="248" cy="72" r="28" fill="#fff" stroke="#ff70b8" stroke-width="4"/>
                    <path d="M236 82 C 244 62, 260 62, 268 82 L 260 92 L 244 92 Z" fill="#ff70b8"/>
                    <rect x="228" y="92" width="40" height="34" rx="10" fill="#00bcd4"/>
                    <rect x="236" y="126" width="10" height="24" rx="5" fill="#3d52d5"/>
                    <rect x="258" y="126" width="10" height="24" rx="5" fill="#3d52d5"/>
                    <circle cx="318" cy="86" r="16" fill="#fff6bf" stroke="#ffd166" stroke-width="3"/>
                    <text x="318" y="92" text-anchor="middle" font-size="18">⭐</text>
                </svg>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_section_banner(title, subtitle):
    st.markdown(f"""
        <div class="section-banner">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


@contextmanager
def section_box(box_class):
    with st.container(border=True):
        st.markdown(f'<div class="section-box-anchor {box_class}"></div>', unsafe_allow_html=True)
        yield


def format_time(value):
    return value if value else "waiting..."


def make_activity_figure(data, activity_name, height):
    style = MYSTERY_STYLES[activity_name]
    color_schemes = {
        "A": {"x": "#ff4fa3", "y": "#00bcd4", "z": "#7c5cff"},
        "B": {"x": "#ff9f1c", "y": "#2ec4b6", "z": "#e71d36"},
        "C": {"x": "#3d52d5", "y": "#06d6a0", "z": "#ffd166"},
    }
    axis_names = {"x": "X wiggle", "y": "Y bounce", "z": "Z zoom"}
    colors = color_schemes[activity_name]
    x_vals = list(range(len(data)))

    fig = go.Figure()
    for axis in ["x", "y", "z"]:
        y_vals = [d[axis] for d in data]
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            name=axis_names[axis],
            line=dict(color=colors[axis], width=4, shape="spline"),
            fill="tozeroy" if axis == "y" else None,
            fillcolor=f"rgba({int(colors[axis][1:3], 16)}, {int(colors[axis][3:5], 16)}, {int(colors[axis][5:7], 16)}, 0.10)" if axis == "y" else None,
            hovertemplate=f"{axis_names[axis]}: %{{y:.2f}}<extra></extra>",
        ))

    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=58, b=42),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0.96)",
        title=dict(
            text=f"Mystery Wave {activity_name}",
            font=dict(size=22, color="#24335f", family="DynaPuff"),
            x=0.02,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#ece6ff",
            borderwidth=1,
            font=dict(size=13),
        ),
        font=dict(size=13, color="#24335f", family="Nunito"),
        hovermode="x unified",
        xaxis=dict(
            title="Time samples",
            gridcolor="rgba(124,92,255,0.10)",
            zeroline=False,
            showline=True,
            linecolor="#ece6ff",
        ),
        yaxis=dict(
            title="Acceleration",
            gridcolor="rgba(124,92,255,0.10)",
            zeroline=True,
            zerolinecolor="rgba(124,92,255,0.18)",
            zerolinewidth=1,
            showline=True,
            linecolor="#ece6ff",
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#ece6ff", width=1),
                fillcolor="rgba(255,255,255,0)",
            )
        ],
    )
    return fig


EXAMPLE_GRAPH_POINTS = 28
EXAMPLE_Y_RANGE = [-3.5, 3.5]


def get_example_wave_values(kind):
    tall_wave_pattern = [0, 3.2, -2.5, 3.5, -3.2, 3.1, -1.8, 1.0]
    if kind == "tall":
        return [tall_wave_pattern[i % len(tall_wave_pattern)] for i in range(EXAMPLE_GRAPH_POINTS)]
    if kind == "squiggly":
        return [
            math.sin(i * 2.9) * 0.95
            + math.sin(i * 5.1) * 0.72
            + math.sin(i * 8.3) * 0.42
            + math.cos(i * 6.4 + 0.6) * 0.38
            for i in range(EXAMPLE_GRAPH_POINTS)
        ]
    return [0.015 * math.sin(i * 0.25) + 0.2 * math.cos(i * 0.9) for i in range(EXAMPLE_GRAPH_POINTS)]


def make_example_figure(title, values, color, fill_color):
    x_vals = list(range(len(values)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=values,
        mode="lines",
        line=dict(color=color, width=4, shape="spline"),
        fill="tozeroy",
        fillcolor=fill_color,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=values,
        mode="markers",
        marker=dict(size=6, color=color, line=dict(color="white", width=1.5)),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=8, r=8, t=42, b=8),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0.96)",
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=16, color="#24335f", family="DynaPuff"),
        ),
        showlegend=False,
        xaxis=dict(visible=False, range=[0, EXAMPLE_GRAPH_POINTS - 1], fixedrange=True),
        yaxis=dict(visible=False, range=EXAMPLE_Y_RANGE, fixedrange=True),
    )
    return fig


def render_graph_detective_tips():
    wave_kinds = ["tall", "squiggly", "calm"]

    with st.container(border=True):
        st.markdown("""
            <div class="tips-grid-head">
                <div class="tips-icon">🕵️</div>
                <div>
                    <p class="mission-title" style="margin:0;">Graph Detective Tips</p>
                    <p class="mission-hint" style="margin:0.15rem 0 0;">
                        Compare these example wave shapes before you record your mystery moves.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        example_cols = st.columns(3)
        for i, (example, kind) in enumerate(zip(TIP_EXAMPLES, wave_kinds)):
            values = get_example_wave_values(kind)
            with example_cols[i]:
                st.markdown(f"""
                    <div class="example-card">
                        <p class="example-title">{example['title']}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(
                    make_example_figure(example["title"], values, example["color"], example["fill"]),
                    use_container_width=True,
                    key=f"example_graph_{i}",
                )
                st.markdown(
                    f"<div class='example-caption'>{example['caption']}</div>",
                    unsafe_allow_html=True,
                )


# ----- Start and stop buttons -----
def start_stop_buttons(markers_path):
    os.makedirs(markers_path, exist_ok=True)

    # Initialize session state for each activity
    for i in range(3):
        if f'start_{i}' not in st.session_state:
            st.session_state[f'start_{i}'] = None
        if f'stop_{i}' not in st.session_state:
            st.session_state[f'stop_{i}'] = None
        if f'activity_type_{i}' not in st.session_state:
            st.session_state[f'activity_type_{i}'] = ""
    
    if 'markers_saved' not in st.session_state:
        st.session_state.markers_saved = False
    
    if 'show_plots' not in st.session_state:
        st.session_state.show_plots = False

    render_hero()

    with section_box("section-box-tips"):
        render_section_banner(
            "1. Learn The Wave Clues",
            "Look at these example graph shapes first — they will help you spot jumps, wiggles, and calm moves later.",
        )
        render_graph_detective_tips()

    with section_box("section-box-record"):
        render_section_banner(
            "2. Record Three Mystery Moves",
            "Type the real activity name, press start, do your move, then press stop. Keep the names secret for the guessing game!",
        )

        activity_cols = st.columns(3)
        for i, col in enumerate(activity_cols):
            mission = MISSION_PROMPTS[i]
            with col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <p class="mission-title" style="border-left: 5px solid {mission['accent']};
                           padding-left: 0.75rem; background: {mission['soft']}; border-radius: 12px;
                           padding: 0.55rem 0.75rem;">
                            Activity {i + 1}
                        </p>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.session_state[f'activity_type_{i}'] = st.text_input(
                        "Select the activity name",
                        value=st.session_state[f'activity_type_{i}'],
                        key=f"type_input_{i}",
                        placeholder="e.g. jumping, dancing, waving",
                    )

                    start_col, stop_col = st.columns(2)
                    with start_col:
                        if st.button("Start", type="secondary", key=f"start_act{i + 1}", use_container_width=True):
                            st.session_state[f'start_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    with stop_col:
                        if st.button("Stop", type="primary", key=f"stop_act{i + 1}", use_container_width=True):
                            st.session_state[f'stop_{i}'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    st.markdown(
                        f"""
                        <span class="time-chip">Start: {format_time(st.session_state[f'start_{i}'])}</span>
                        <span class="time-chip">Stop: {format_time(st.session_state[f'stop_{i}'])}</span>
                        """,
                        unsafe_allow_html=True,
                    )

        col_save, col_gen, col_del = st.columns(3)

        with col_save:
            all_times_set = all(
                st.session_state[f'start_{i}'] is not None and st.session_state[f'stop_{i}'] is not None
                for i in range(3)
            )

            if st.button("Save Moves", type="tertiary", key="save_markers", disabled=not all_times_set, use_container_width=True):
                try:
                    for i in range(3):
                        marker = {
                            "start_time": st.session_state[f'start_{i}'],
                            "stop_time": st.session_state[f'stop_{i}'],
                            "activity_type": st.session_state[f'activity_type_{i}']
                        }
                        marker_file = os.path.join(markers_path, f"activity_{i}_window.json")
                        with open(marker_file, "w") as f:
                            json.dump(marker, f)
                    st.session_state.markers_saved = True
                    st.success("Your mystery moves are saved!")
                except Exception as e:
                    st.error(f"Error saving markers: {str(e)}")

        with col_gen:
            if st.button("Make Mystery Graphs", type="primary", key="gen_plots", disabled=not st.session_state.markers_saved, use_container_width=True):
                st.session_state.show_plots = True
                st.rerun()

        with col_del:
            if st.button("Reset Lab", type="tertiary", key="del_all", help="Delete all markers and plots", use_container_width=True):
                try:
                    for i in range(3):
                        marker_file = os.path.join(markers_path, f"activity_{i}_window.json")
                        if os.path.exists(marker_file):
                            os.remove(marker_file)

                    for key in list(st.session_state.keys()):
                        del st.session_state[key]

                    st.success("The lab is reset and ready for new moves!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting markers: {str(e)}")


# ----- Plot activity data -----
def plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names, markers):
    top_col1, top_col2 = st.columns([1, 1])
    bottom_col = st.container()

    # Initialize session state for guesses and revealed answers if not exists
    if 'guesses' not in st.session_state:
        st.session_state.guesses = {}
    if 'revealed_answers' not in st.session_state:
        st.session_state.revealed_answers = {}

    plot_slots = [top_col1, top_col2, bottom_col]

    for i, data in enumerate(shuffled_activities):
        activity_name = activity_names[i]
        style = MYSTERY_STYLES[activity_name]
        height = 400 if i < 2 else 470

        with plot_slots[i]:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="mystery-badge">
                        <div class="mystery-badge-dot" style="background:{style['badge']}; box-shadow: 0 8px 18px {style['glow']};">
                            {activity_name}
                        </div>
                        <div>
                            <p class="plot-title">Mystery Activity {activity_name}</p>
                        </div>
                    </div>
                    <p class="plot-helper">Look for clues in the wiggly lines, then make your best guess.</p>
                    """,
                    unsafe_allow_html=True,
                )

                plot_col, guess_col = st.columns([3, 1])

                with plot_col:
                    fig = make_activity_figure(data, activity_name, height)
                    st.plotly_chart(fig, use_container_width=True, key=f"plot_{i}")

                with guess_col:
                    guess = st.text_input(
                        f"Your guess for {activity_name}",
                        key=f"guess_{i}",
                        placeholder="What move was it?",
                    )
                    st.session_state.guesses[activity_name] = guess

                    if st.button("🎁 Reveal", key=f"reveal_{i}", help="Show the correct activity type", use_container_width=True):
                        st.session_state.revealed_answers[activity_name] = True

                    if activity_name in st.session_state.revealed_answers:
                        correct_type = markers[shuffled_indices[i]]['activity_type']
                        st.markdown(
                            f"<div class='answer-card'>It was: {correct_type}</div>",
                            unsafe_allow_html=True,
                        )
                        if guess.strip().lower() == correct_type.strip().lower():
                            st.success("Brilliant detective work! 🎉")
                        elif guess.strip():
                            st.error("Not quite — keep investigating! 🔍")
                        else:
                            st.info("Type a guess, then reveal the answer.")


# ----- Load Movesense CLI data -----
def _find_acc_column(columns, axis):
    """Find the accelerometer column for the requested axis (X/Y/Z).

    The Movesense CLI names acceleration columns like ``<device>_Acc_X`` after
    ``unify_notifications`` pivots the data. Whitespace variants (``Acc _X``)
    can also appear depending on pandas' column-flattening, so we accept both.
    """
    suffixes = (f"_Acc_{axis}", f" Acc_{axis}", f"_Acc _{axis}", f" Acc _{axis}")
    for col in columns:
        if isinstance(col, str) and col.endswith(suffixes):
            return col
    return None


def load_data_collection_csv(csv_path):
    """Load the CSV written by the Movesense CLI and return a list of dicts.

    Each entry has the same shape the rest of the app already expects:
    ``{"timestamp": "YYYY-MM-DD HH:MM:SS", "x": float, "y": float, "z": float}``.
    """
    df = pd.read_csv(csv_path)

    x_col = _find_acc_column(df.columns, "X")
    y_col = _find_acc_column(df.columns, "Y")
    z_col = _find_acc_column(df.columns, "Z")

    if x_col is None or y_col is None or z_col is None:
        raise ValueError(
            "Could not find accelerometer X/Y/Z columns in "
            f"{csv_path}. Available columns: {list(df.columns)}"
        )

    df = df.dropna(subset=["timestamp", x_col, y_col, z_col])

    # The CLI stores Unix-epoch floats; convert to the local-time string
    # format the markers use (datetime.now()) so window slicing keeps
    # working unchanged.
    timestamps = [
        datetime.fromtimestamp(float(t)).strftime("%Y-%m-%d %H:%M:%S")
        for t in df["timestamp"]
    ]

    return [
        {"timestamp": ts, "x": float(x), "y": float(y), "z": float(z)}
        for ts, x, y, z in zip(timestamps, df[x_col], df[y_col], df[z_col])
    ]

def get_marker_data(markers_path):
    markers = {}
    # Get marker files (x3) (i.e. start stop times of each activity)
    for act_num in range(3): # 0,1, 2
        marker_file_name = f'activity_{act_num}_window.json'
        marker_file = os.path.join(markers_path, marker_file_name)
        try:
            with open(marker_file) as f:
                markers[act_num] = json.load(f)
        except FileNotFoundError:
            # Return None if any marker file is missing
            return None
        except json.JSONDecodeError:
            # Return None if any marker file has invalid JSON
            return None
    return markers

# ----- Divide activity data -----
def get_activity_data(markers, data):
    activity_data = {0: [], 1: [], 2: []}
    try:
        for act_num in range(3):
            start_time = datetime.strptime(markers[act_num]['start_time'], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(markers[act_num]['stop_time'], "%Y-%m-%d %H:%M:%S")
            for entry in data:
                entry_time = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
                if start_time <= entry_time <= end_time:
                    activity_data[act_num].append(entry)
        return [activity_data[0], activity_data[1], activity_data[2]]
    except (KeyError, ValueError, TypeError):
        # Return None if there's any error processing the data
        return None

# ----- Shuffle the activity data -----
def shuffle_plots(activity_data_list):
    indices = list(range(3))
    random.shuffle(indices)
    return [activity_data_list[i] for i in indices], indices


if __name__ == "__main__":
    st.set_page_config(
        page_title="Move With Tech",
        page_icon="🚀",
        layout="wide",
    )
    

    data_file = (
        '/rds/general/user/cr620/home/GERF/GreatExhibitionRoadFestival/'
        'outputs/data_collection.csv'
    )
    markers_path = '/rds/general/user/cr620/home/GERF/activities/'

    inject_child_friendly_theme()
    start_stop_buttons(markers_path)

    # Only show the plotting section if Generate Plots button was clicked
    if st.session_state.get('show_plots', False):
        try:
            # Get marker data
            markers = get_marker_data(markers_path)
            
            if markers is None:
                st.error("Error: Marker data is missing or invalid. Please make sure all activities have been recorded.")
            else:
                try:
                    data = load_data_collection_csv(data_file)

                    activity_data_list = get_activity_data(markers, data)
                    
                    if activity_data_list is None or any(not activity for activity in activity_data_list):
                        st.error("Error: Could not extract activity data. Make sure the timestamps match with data records.")
                    else:
                        render_section_banner(
                            "3. Guess The Mystery Waves",
                            "Can you match each accelerometer graph to the move that made it?",
                        )
                        
                        # Shuffling of data - only if not already in session state
                        if 'shuffled_activities' not in st.session_state or 'shuffled_indices' not in st.session_state:
                            shuffled_activities, shuffled_indices = shuffle_plots(activity_data_list)
                            st.session_state.shuffled_activities = shuffled_activities
                            st.session_state.shuffled_indices = shuffled_indices
                        else:
                            shuffled_activities = st.session_state.shuffled_activities
                            shuffled_indices = st.session_state.shuffled_indices

                        activity_names = ACTIVITY_LETTERS
                        plot_activity_data_shuffled(shuffled_activities, shuffled_indices, activity_names, markers)

                        # Add Shuffle Again button
                        if st.button("🔀 Shuffle Again", type="primary", help="Mix up the activities"):
                            # Only clear the shuffle-related state, preserve the rest
                            if 'shuffled_activities' in st.session_state:
                                del st.session_state.shuffled_activities
                            if 'shuffled_indices' in st.session_state:
                                del st.session_state.shuffled_indices
                            if 'guesses' in st.session_state:
                                del st.session_state.guesses
                            if 'revealed_answers' in st.session_state:
                                del st.session_state.revealed_answers
                            st.rerun()
                        
                except FileNotFoundError:
                    st.error(
                        f"Error: Could not find data file {data_file}. "
                        "Run the Movesense CLI (or the generator script) "
                        "to produce it."
                    )
                except pd.errors.EmptyDataError:
                    st.error(f"Error: Data file {data_file} is empty.")
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    st.markdown("""
        <div class='logo-section'>
            <h2 style='text-align: center;'>Our Partners</h2>
            <p style='font-weight: 800;'>Big thanks to the teams helping this motion lab happen.</p>
        </div>
    """, unsafe_allow_html=True)
    
    logo_col1, logo_col2, logo_col3 = st.columns(3)
    
    with logo_col1:
        st.image("https://red-stone.com/uploads/images/_siteImagesFullWidthX2/UKDRI_brand_IMAGE_1920x1230-01.jpg", width=200, use_container_width=True)
    
    with logo_col2:
        st.image("https://www.ukri.org/wp-content/uploads/2022/03/ukri-mrc-square-logo.png", width=200, use_container_width=True)
    
    with logo_col3:
        st.image("https://pxl-imperialacuk.terminalfour.net/fit-in/1918x860/filters:upscale()/prod01/channel_3/media/images/banner-left-block-3000X1200/New-Brand-logo-.jpg", width=200, use_container_width=True)