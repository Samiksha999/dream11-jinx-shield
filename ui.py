import streamlit as st 
import requests 
import json 
import os 
st.set_page_config(page_title="Dream11 Jinx Shield", page_icon="???", layout="wide") 
st.title("??? Dream11 'Jinx Shield' Live Chaos & Sentiment Engine") 
st.subheader("Asynchronous Full-Stack Telemetry Pipeline for Customer Engineering Audits") 
col1, col2 = st.columns(2) 
with col1: 
    st.header("Streaming Live Match & Chat Telemetry") 
    if os.path.exists("live_match_feed.json"): 
        with open("live_match_feed.json", "r") as f: feed = json.load(f) 
        for event in reversed(feed): 
            st.markdown(f"**{event['source_feed']} - Ball {event['ball_identifier']}**") 
            st.caption(event['raw_payload']) 
            st.markdown("---") 
    else: st.info("Waiting for live telemetry stream...") 
with col2: 
    st.header("? Live Sentiment Strategy Control Room") 
    if st.button("? Calculate Anti-Jinx Chaos Strategy", type="primary"): 
        with st.spinner("Processing asynchronous pipeline matrices..."): 
            try: 
                response = requests.get("http://127.0.0") 
                if response.status_code == 200: 
                    payload = response.json() 
                    st.metric(label="Pipeline Computation Latency", value=payload.get("pipeline_latency_ms")) 
                    st.caption(f"System Node Status: `{payload.get('engine_status')}`") 
                    data = payload.get("data") 
                    st.markdown("### ?? Public Anxiety & Superstition Context") 
                    st.info(data.get("anxiety_sentiment_context")) 
                    st.markdown("### ?? Anti-Jinx Roster Hedge Strategy") 
                    st.write(data.get("anti_jinx_roster_hedge")) 
                    st.markdown("### ?? Witty Chaos Coach Advisory") 
                    st.success(data.get("chaos_coaching_tip")) 
            except Exception as e: st.error(f"Could not connect to local FastAPI routing node: {e}") 
