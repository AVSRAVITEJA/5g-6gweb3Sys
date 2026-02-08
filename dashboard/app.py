import streamlit as st
import pandas as pd
import time
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Network Slicing Dashboard",
    layout="wide"
)

st.title("📡 AI-Driven Network Slicing with Blockchain Logging")
st.caption("Real-time visualization of ESP32-driven network state, AI decisions, and on-chain logging")

# -------------------- BACKEND CONFIG --------------------
BACKEND_URL = "http://127.0.0.1:5001/latest"
REFRESH_INTERVAL = 2  # seconds

# -------------------- SESSION STATE --------------------
if "data" not in st.session_state:
    st.session_state.data = []

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# -------------------- DATA FETCH --------------------
current_time = time.time()

if current_time - st.session_state.last_update > REFRESH_INTERVAL:
    try:
        response = requests.get(BACKEND_URL, timeout=2)

        if response.status_code == 200:
            payload = response.json()

            # Backend returns this when ESP32 hasn't sent data yet
            if "status" not in payload:
                st.session_state.data.append(payload)

    except Exception:
        st.warning("⚠️ Backend not reachable")

    st.session_state.last_update = current_time
    st.rerun()

# -------------------- DATAFRAME --------------------
df = pd.DataFrame(st.session_state.data)

# -------------------- DASHBOARD --------------------
if not df.empty:
    col1, col2, col3 = st.columns(3)

    col1.metric("📶 Avg Latency (ms)", round(df["latency_ms"].mean(), 2))
    col2.metric("📉 Avg Packet Loss (%)", round(df["packet_loss"].mean(), 2))
    col3.metric("👥 Active Users", int(df["active_users"].iloc[-1]))

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Bandwidth Allocation Over Time")
        st.line_chart(df["bandwidth_allocated"])

    with col_right:
        st.subheader("🚦 Traffic Context Distribution")
        st.bar_chart(df["traffic_type"].value_counts())

    st.subheader("📈 Network Metrics Timeline")
    st.line_chart(df[["latency_ms", "packet_loss", "congestion_level"]])

    st.subheader("🔗 Recent Blockchain Logged Decisions")
    st.dataframe(
        df[[
            "timestamp",
            "decision",
            "bandwidth_allocated",
            "tx_hash"
        ]].tail(10),
        use_container_width=True
    )

else:
    st.info("⏳ Waiting for ESP32 data via backend...")
