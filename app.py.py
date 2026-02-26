import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION & "OBSIDIAN" STYLING
# ==========================================
st.set_page_config(
    page_title="Deriv Pulse | AI Risk Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DERIV "OBSIDIAN" THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* BASE THEME */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 70%);
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    /* REMOVE STREAMLIT PADDING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* CUSTOM CARDS (Glassmorphism) */
    .obsidian-card {
        background: rgba(22, 22, 22, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* NEON TEXT STYLES */
    .neon-text-red {
        color: #ff444f;
        text-shadow: 0 0 10px rgba(255, 68, 79, 0.4);
        font-family: 'JetBrains Mono', monospace;
    }
    .neon-text-green {
        color: #00ff88;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* KPI BOXES */
    .kpi-box {
        text-align: center;
    }
    .kpi-label {
        color: #888;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* PULSE ANIMATION */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }
    .live-dot {
        height: 12px;
        width: 12px;
        background-color: #00ff88;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse-green 2s infinite;
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #ff444f 0%, #d62d38 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border-radius: 6px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 68, 79, 0.4);
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE (Logic Preserved)
# ==========================================
class TradeGenerator:
    @staticmethod
    def generate_narrative_arc():
        trades = []
        base_time = datetime.now() - timedelta(minutes=100)
        
        # Session A: Disciplined
        for i in range(20):
            base_time += timedelta(minutes=np.random.randint(3, 8))
            trades.append({
                "Trade_ID": f"T-{1000+i}", "Asset": np.random.choice(["EUR/USD", "Vol_100", "Gold"]),
                "Outcome": np.random.choice(["Win", "Loss"], p=[0.55, 0.45]),
                "Stake_Size": np.round(np.random.uniform(10, 15), 2),
                "Timestamp": base_time, "Session": "Disciplined"
            })
            
        # Session B: The Tilt
        current_stake = 20.0
        for i in range(20, 35):
            base_time += timedelta(seconds=np.random.randint(30, 90))
            outcome = np.random.choice(["Win", "Loss"], p=[0.2, 0.8])
            if trades[-1]["Outcome"] == "Loss": current_stake *= np.random.uniform(1.5, 3.0)
            else: current_stake = max(20.0, current_stake * 0.8)
            current_stake = min(current_stake, 2000.0) 
            trades.append({
                "Trade_ID": f"T-{1000+i}", "Asset": "Vol_100",
                "Outcome": outcome, "Stake_Size": np.round(current_stake, 2),
                "Timestamp": base_time, "Session": "Tilt"
            })

        # Session C: Recovery
        base_time += timedelta(minutes=20) 
        for i in range(35, 50):
            base_time += timedelta(minutes=np.random.randint(4, 10))
            trades.append({
                "Trade_ID": f"T-{1000+i}", "Asset": np.random.choice(["EUR/USD", "Vol_100"]),
                "Outcome": np.random.choice(["Win", "Loss"], p=[0.6, 0.4]),
                "Stake_Size": np.round(np.random.uniform(10, 12), 2),
                "Timestamp": base_time, "Session": "Recovery"
            })
            
        return pd.DataFrame(trades)

    @staticmethod
    def inject_scenario(scenario_type="Tilt"):
        """Injects specific test scenarios for demo purposes."""
        base_time = datetime.now()
        trades = []
        
        if scenario_type == "Tilt":
            # Scenario: User loses, then doubles down repeatedly (Martingale)
            trades.append({"Trade_ID": "SIM-1", "Asset": "Vol_100", "Outcome": "Loss", "Stake_Size": 10.0, "Timestamp": base_time, "Session": "Sim_Tilt"})
            trades.append({"Trade_ID": "SIM-2", "Asset": "Vol_100", "Outcome": "Loss", "Stake_Size": 25.0, "Timestamp": base_time + timedelta(minutes=1), "Session": "Sim_Tilt"})
            trades.append({"Trade_ID": "SIM-3", "Asset": "Vol_100", "Outcome": "Loss", "Stake_Size": 60.0, "Timestamp": base_time + timedelta(minutes=2), "Session": "Sim_Tilt"})
            trades.append({"Trade_ID": "SIM-4", "Asset": "Vol_100", "Outcome": "Loss", "Stake_Size": 150.0, "Timestamp": base_time + timedelta(minutes=3), "Session": "Sim_Tilt"})
            
        elif scenario_type == "Recovery":
             # Scenario: User stabilizes after a loss
            trades.append({"Trade_ID": "SIM-1", "Asset": "EUR/USD", "Outcome": "Loss", "Stake_Size": 20.0, "Timestamp": base_time, "Session": "Sim_Rec"})
            trades.append({"Trade_ID": "SIM-2", "Asset": "EUR/USD", "Outcome": "Win", "Stake_Size": 20.0, "Timestamp": base_time + timedelta(minutes=5), "Session": "Sim_Rec"})
            trades.append({"Trade_ID": "SIM-3", "Asset": "EUR/USD", "Outcome": "Win", "Stake_Size": 20.0, "Timestamp": base_time + timedelta(minutes=10), "Session": "Sim_Rec"})
            
        return pd.DataFrame(trades)

# ==========================================
# 3. ANALYTICS ENGINE (Logic Preserved)
# ==========================================
class RiskEngine:
    @staticmethod
    def analyze(df):
        df = df.copy()
        df['Tilt_Detected'] = False
        df['Volatility_Ratio'] = 0.0
        df['Risk_Penalty'] = 0.0
        tilt_events = []
        df = df.sort_values(by='Timestamp').reset_index(drop=True)
        
        for i in range(1, len(df)):
            prev = df.iloc[i-1]
            curr = df.iloc[i]
            time_delta = (curr['Timestamp'] - prev['Timestamp']).total_seconds() / 60.0
            
            # Tilt Logic
            if (prev['Outcome'] == 'Loss' and time_delta < 5 and curr['Stake_Size'] >= 2.0 * prev['Stake_Size']):
                df.at[i, 'Tilt_Detected'] = True
                df.at[i, 'Risk_Penalty'] = 20.0
                tilt_events.append(i)

        # Volatility
        rolling_std = df['Stake_Size'].rolling(window=5).std()
        rolling_mean = df['Stake_Size'].rolling(window=5).mean().replace(0, 1)
        df['Volatility_Ratio'] = rolling_std / rolling_mean
        df.loc[df['Volatility_Ratio'] > 2.5, 'Risk_Penalty'] += 15.0
        return df, tilt_events

    @staticmethod
    def calculate_pulse_score(df):
        base_score = 100.0
        now = df['Timestamp'].max()
        total_penalty = 0.0
        for idx, row in df.iterrows():
            if row['Risk_Penalty'] > 0:
                mins_ago = (now - row['Timestamp']).total_seconds() / 60.0
                weight = np.exp(-0.02 * mins_ago)
                total_penalty += row['Risk_Penalty'] * weight
        return int(max(0.0, base_score - total_penalty))

# ==========================================
# 4. OBSIDIAN UI RENDERER
# ==========================================
def main():
    # --- Data Processing ---
    if 'data' not in st.session_state: st.session_state.data = TradeGenerator.generate_narrative_arc()
    df_raw = st.session_state.data
    df_analyzed, tilt_indices = RiskEngine.analyze(df_raw)
    score = RiskEngine.calculate_pulse_score(df_analyzed)
    volatility = df_analyzed['Volatility_Ratio'].iloc[-1] if len(df_analyzed) > 0 else 0
    tilt_count = len(tilt_indices)

    # --- Header ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("DERIV PULSE")
        st.caption("AI-POWERED BEHAVIORAL RISK SYSTEM // V.1.0.4")
    with c2:
        st.markdown('<div style="text-align: right; padding-top: 15px;"><span class="live-dot"></span><span style="font-family: monospace; color: #00ff88;">SYSTEM ONLINE</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPI HERO SECTION (Custom HTML) ---
    k1, k2, k3 = st.columns(3)
    
    # Pulse Score Logic
    score_color = "neon-text-green" if score > 70 else ("#ffa700" if score > 40 else "neon-text-red")
    
    with k1:
        st.markdown(f"""
        <div class="obsidian-card kpi-box">
            <div class="kpi-label">PSYCHOLOGICAL PULSE</div>
            <div class="kpi-value {score_color}">{score}</div>
            <div style="font-size: 0.8rem; color: #555; margin-top: 5px;">TARGET: >85</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        vol_color = "neon-text-red" if volatility > 2.5 else "neon-text-green"
        st.markdown(f"""
        <div class="obsidian-card kpi-box">
            <div class="kpi-label">VOLATILITY RATIO</div>
            <div class="kpi-value {vol_color}">{volatility:.2f}x</div>
            <div style="font-size: 0.8rem; color: #555; margin-top: 5px;">THRESHOLD: 2.50x</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        tilt_display = f'<span class="neon-text-red">{tilt_count}</span>' if tilt_count > 0 else '<span class="neon-text-green">0</span>'
        st.markdown(f"""
        <div class="obsidian-card kpi-box">
            <div class="kpi-label">REVENGE EVENTS</div>
            <div class="kpi-value">{tilt_display}</div>
            <div style="font-size: 0.8rem; color: #555; margin-top: 5px;">DETECTED IN SESSION</div>
        </div>
        """, unsafe_allow_html=True)

    # --- MAIN CHART (Pro Trading View) ---
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown('<div class="obsidian-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Live Stake Analysis")
        
        colors = df_analyzed['Outcome'].map({'Win': '#00ff88', 'Loss': '#ff444f'})
        fig = go.Figure()
        
        # Area Chart for Stake Size
        fig.add_trace(go.Scatter(
            x=df_analyzed['Timestamp'], y=df_analyzed['Stake_Size'],
            fill='tozeroy', mode='lines+markers',
            line=dict(color='#2E93fA', width=2),
            marker=dict(color=colors, size=6, line=dict(width=1, color='white')),
            name='Stake Size'
        ))
        
        # Tilt Annotations
        for idx in tilt_indices:
            row = df_analyzed.iloc[idx]
            fig.add_annotation(
                x=row['Timestamp'], y=row['Stake_Size'],
                text="TILT", showarrow=True, arrowhead=1,
                arrowcolor="#ff444f", bgcolor="#1a1a1a", bordercolor="#ff444f",
                font=dict(color="#ff444f", size=10)
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SIDEBAR: LIVE COACHING CHAT ---
    with col_side:
        st.markdown('<div class="obsidian-card" style="height: 500px; display: flex; flex-direction: column;">', unsafe_allow_html=True)
        st.subheader("💬 AI Performance Coach")
        
        # Initialize Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "I'm monitoring your trade flow. Current Pulse Score is " + str(score) + ". How can I help?"}
            ]
            
        # Display Chat History (Scrollable container)
        chat_container = st.container(height=300)
        with chat_container:
            for msg in st.session_state.messages:
                # Style the chat bubbles to match the Dark Theme
                if msg["role"] == "assistant":
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #00ff88;">
                        <small style="color: #00ff88; font-weight: bold;">DERIV AI</small><br>
                        {msg["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(46, 147, 250, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 8px; text-align: right; border-right: 3px solid #2E93fA;">
                        {msg["content"]}
                    </div>
                    """, unsafe_allow_html=True)

        # Chat Logic (Simulated "RAG" - Retrieval Augmented Generation)
        if prompt := st.chat_input("Ask about your performance..."):
            # 1. User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                st.markdown(f"""<div style="background: rgba(46, 147, 250, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 8px; text-align: right; border-right: 3px solid #2E93fA;">{prompt}</div>""", unsafe_allow_html=True)

            # 2. AI Logic (Context Aware)
            response = ""
            p_lower = prompt.lower()
            
            # --- CONTEXT AWARENESS ENGINE ---
            if "score" in p_lower or "low" in p_lower:
                if score < 50:
                    response = f"Your score dropped to **{score}** because I detected **{tilt_count} revenge trades** in the last session. You doubled your stake immediately after losses."
                else:
                    response = f"Your score is a healthy **{score}**. You are maintaining consistent stake sizing. Keep it up."
            
            elif "tilt" in p_lower or "revenge" in p_lower:
                if tilt_count > 0:
                    last_tilt = df_analyzed[df_analyzed['Tilt_Detected']==True].iloc[-1]
                    response = f"Yes, I flagged a critical event at **{last_tilt['Timestamp'].strftime('%H:%M')}**. You bet **${last_tilt['Stake_Size']}** immediately after a loss. This fits the 'Martingale' risk pattern."
                else:
                    response = "I haven't detected any Tilt patterns in this session. You are trading with discipline."
            
            elif "advice" in p_lower or "do" in p_lower:
                if volatility > 2.5:
                    response = "My advice: **Stop trading for 15 minutes.** Your volatility ratio is critically high. Walk away before you give back your profits."
                else:
                    response = "You are in the zone. My advice is to maintain your current position sizing of around $10-$15."
            
            else:
                response = f"I am analyzing your live data points. Currently tracking volatility at {volatility:.2f}x and {tilt_count} risk events."

            # 3. AI Reply
            time.sleep(0.5) # Fake "Thinking" latency
            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_container:
                 st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #00ff88;">
                        <small style="color: #00ff88; font-weight: bold;">DERIV AI</small><br>
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Force refresh to keep UI snappy
            # st.rerun() 

        # Lock Button (Moved to bottom of sidebar)
        if score < 40:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔒 EMERGENCY LOCK"):
                st.session_state['locked'] = True
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- COOL DOWN OVERLAY ---
    if st.session_state.get('locked', False):
        st.markdown("""
        <div style="background: rgba(255, 68, 79, 0.1); border: 1px solid #ff444f; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
            <h2 style="color: #ff444f; margin:0;">🚫 TERMINAL LOCKED</h2>
            <p style="color: #ccc;">Cortisol Reset in Progress. Step away.</p>
            <h1 style="font-family: monospace; font-size: 3rem;">14:59</h1>
        </div>
        """, unsafe_allow_html=True)

    # --- SIDEBAR: SIMULATION & DEBUGGING ---
    with st.sidebar:
        # LOGO INTEGRATION
        st.image("logo.jpg", output_format="JPG")
        st.markdown("### 🛠️ Simulation Mode")
        with st.expander("Control Panel", expanded=True):
            st.caption("Inject scenarios to demonstrate AI Analysis.")
            
            # Scenario Buttons
            if st.button("🔥 FORCE TILT (Revenge)"):
                st.session_state.data = TradeGenerator.inject_scenario("Tilt")
                st.session_state.messages = [{"role": "assistant", "content": "⚠️ ALERT: I've detected a high-risk martingale pattern. You are doubling stakes after losses. STOP."}]
                st.rerun()
            
            if st.button("🧘 FORCE RECOVERY"):
                st.session_state.data = TradeGenerator.inject_scenario("Recovery")
                st.session_state.messages = [{"role": "assistant", "content": "Good job stabilizing. Your stake sizing is consistent again."}]
                st.rerun()

            st.divider()
            
            # Manual Injection
            st.markdown("**Manual Trade Injection**")
            m_outcome = st.selectbox("Outcome", ["Win", "Loss"], key="m_out")
            m_stake = st.number_input("Stake ($)", 1.0, 1000.0, 10.0, key="m_stk")
            
            if st.button("➕ Add Single Trade"):
                last_time = st.session_state.data['Timestamp'].max() if not st.session_state.data.empty else datetime.now()
                new_trade = pd.DataFrame([{
                    "Trade_ID": f"MAN-{len(st.session_state.data)}",
                    "Asset": "Manual_Input",
                    "Outcome": m_outcome,
                    "Stake_Size": m_stake,
                    "Timestamp": last_time + timedelta(minutes=2),
                    "Session": "Manual"
                }])
                st.session_state.data = pd.concat([st.session_state.data, new_trade], ignore_index=True)
                st.rerun()
                
            if st.button("🔄 Reset to Random Stream"):
                del st.session_state.data
                st.session_state.messages = []
                st.rerun()

    # --- RAW DATA ---
    with st.expander("Show Forensic Log"):
        st.dataframe(df_analyzed, use_container_width=True)

if __name__ == "__main__":
    main()