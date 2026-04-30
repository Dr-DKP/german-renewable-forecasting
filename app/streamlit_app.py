"""
Streamlit dashboard for interactive forecast exploration.

Phase 5: Forecast, model info (MLflow run params and metrics),
and About (Project summary, architechture,links).
"""

# Import libraries
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Page config
page = st.sidebar.radio("Navigate", ["Forecast", "Model Info", "About"])

# Page 1: Forecast
if page == "Forecast":
    st.title("Solar Generation Forecast: Germany")
    date = st.date_input("Select forecast date")
    if st.button("Get Forecast"):
        resp = requests.get(f"http://localhost:8000/forecast?date={date}")
        st.session_state["df"] = pd.DataFrame(resp.json()["forecast"])
        st.session_state["df"]["time"] = pd.to_datetime(st.session_state["df"]["time"])
        st.session_state["date"] = date

    if "df" in st.session_state:
        df = st.session_state["df"]
        date = st.session_state["date"]
        actual_resp = requests.get(f"http://localhost:8000/actual?date={date}")
        actual_data = actual_resp.json().get("actual", [])

        # Plot now data
        # Create three columns for top-level stats
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Peak Generation", f"{df['p50_mw'].max():.1f} MW", delta="Expected")
        with col2:
            st.metric("Daily Energy (Est.)", f"{df['p50_mw'].sum():.1f} MWh")
        with col3:
            # Showing the 'width' of our uncertainty band
            uncertainty = (df['p90_mw'] - df['p10_mw']).mean()
            st.metric("Confidence Band", f"±{uncertainty/2:.1f} MW", delta_color="inverse")

        import plotly.graph_objects as go

        fig = go.Figure()

        # P10-P90 Uncertainty Band
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["p90_mw"],
            mode='lines', line=dict(width=0),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["p10_mw"],
            fill='tonexty', # This creates the shaded "band"
            fillcolor='rgba(0, 128, 128, 0.2)', # Teal with alpha
            mode='lines', line=dict(width=0),
            name="Confidence Band (P10-P90)"
        ))

        # P50 Main Forecast Line
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["p50_mw"],
            mode='lines+markers',
            line=dict(color='teal', width=3),
            name="Best Guess (P50)"
        ))
        if actual_data:
            df_actual = pd.DataFrame(actual_data)
            df_actual["time"] = pd.to_datetime(df_actual["time"])
            fig.add_trace(go.Scatter(
                x=df_actual["time"], y=df_actual["actual_mw"],
                mode="lines", name="Actual (SMARD)",
                line=dict(color="black", width=2, dash="dot")
            ))
        fig.update_layout(
            title=f"Probabilistic Solar Forecast — {date}",
            xaxis_title="Time of Day",
            yaxis_title="Solar Power (MW)",
            hovermode="x unified", # Shows all values for a specific hour in one tooltip
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        # plot Physics vs Residual Decomposition
        st.subheader("Physics vs Residual Decomposition")
        df["residual_mw"] = df["p50_mw"] - df["physics_mw"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df["time"], y=df["physics_mw"],
            name="Physics (pvlib clear-sky)",
            marker_color="steelblue"
        ))
        fig2.add_trace(go.Bar(
            x=df["time"], y=df["residual_mw"],
            name="XGBoost residual correction",
            marker_color="coral"
        ))
        fig2.update_layout(
            barmode="stack",
            title="What drives each hour: physics baseline + ML correction",
            xaxis_title="Time of Day",
            yaxis_title="Solar MW",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df)

# Page 2: Model Info
if page == "Model Info":
    # Page title
    st.title("Model Information")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Architecture")
        st.markdown("""
        - **Data:** SMARD + Open-Meteo (2022–2024)
        - **Storage:** TimescaleDB hypertables
        - **Physics:** pvlib Ineichen-Perez clear-sky (R²=0.78)
        - **ML:** XGBoost residual learner (R²=0.92)
        - **UQ:** Quantile regression + split conformal prediction
        - **API:** FastAPI + MLflow model registry
        """)

    with col2:
        st.subheader("Training Metrics")
        metrics = {
            "Metric": ["MAE", "RMSE", "R² (XGBoost)", "P90 Coverage", "CRPS", "Sharpness"],
            "Value":  ["1,534 MW", "3,076 MW", "0.92", "0.869", "514.6 MW", "3,842 MW"],
            "vs Baseline": ["−60%", "−20%", "+18%", "target: 0.90", "vs MAE: −67%", "8% of peak"]
        }
        st.dataframe(pd.DataFrame(metrics), hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("Reliability")
    claimed  = [0.10, 0.50, 0.90]
    observed = [0.036, 0.28, 0.869]
    import plotly.graph_objects as go
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
        line=dict(dash="dash", color="gray"), name="Perfect calibration"))
    fig_r.add_trace(go.Scatter(x=claimed, y=observed, mode="markers+text",
        marker=dict(size=14, color="teal"),
        text=["P10","P50","P90"], textposition="top center", name="Observed"))
    fig_r.update_layout(template="plotly_white",
        xaxis_title="Claimed quantile", yaxis_title="Observed coverage",
        title="Reliability Diagram — P50 miscalibrated (seasonal shift)")
    st.plotly_chart(fig_r, use_container_width=True)


# Page 3: About
if page == "About":
    st.title("About This Project")
    st.markdown("""
A **probabilistic solar generation forecasting system** for the German grid,
built on 3 years of public SMARD and Open-Meteo data.

The core idea: a **physics layer** (pvlib clear-sky irradiance) computes what
solar output would be on a perfect clear day. An **XGBoost residual learner**
then corrects for everything physics cannot see "clouds, aerosols, curtailments".
Forecasts are delivered as **calibrated probability intervals** (P10/P50/P90),
evaluated with CRPS and split conformal prediction.
""")

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Physics baseline R²", "0.78")
    col2.metric("XGBoost R²", "0.92")
    col3.metric("P90 coverage", "0.869")

    st.divider()
    st.subheader("Links")
    st.markdown("""
- [GitHub repository](https://github.com/Dr-DKP/german-renewable-forecasting)
- [SMARD data portal](https://www.smard.de)
- [Open-Meteo API](https://open-meteo.com)
""")

