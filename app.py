import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Harshit Terminal | Pro Journal",
    page_icon="👑",
    layout="wide"
)

# Custom CSS for Premium Gold & Matte Black Theme
st.markdown("""
    <style>
    /* Dark Gold Theme Background */
    .stApp {
        background-color: #0A0A0C;
        color: #E2E8F0;
    }
    
    /* Title Styling & Gold Glow */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Cinzel', 'Trebuchet MS', serif;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Metric Values Gold Accent */
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 30px !important;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3);
    }

    div[data-testid="stMetricLabel"] {
        color: #A0AEC0 !important;
    }

    /* Buttons Gold Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #BF953F 0%, #FCF6BA 25%, #B38728 50%, #FBF5B7 75%, #AA771C 100%);
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 12px rgba(212, 175, 55, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.5);
    }

    /* Inputs Style */
    input, select, textarea {
        background-color: #121216 !important;
        color: #FFFFFF !important;
        border: 1px solid #332A15 !important;
        border-radius: 8px !important;
    }

    /* Tabs Styling - Gold Border Active */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #121216;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #262010;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 6px;
        color: #8B949E;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%) !important;
        color: #000000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_innerHTML=True)

# Passcode Protection
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        
    if not st.session_state["password_correct"]:
        st.markdown("<br>", unsafe_allow_innerHTML=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
            st.markdown("<h2 style='text-align: center;'>👑 HARSHIT TRADING TERMINAL</h2>", unsafe_allow_innerHTML=True)
            st.markdown("<p style='text-align: center; color: #A0AEC0;'>GROW • FOCUS • ACHIEVE</p>", unsafe_allow_innerHTML=True)
            
            pwd = st.text_input("🔑 Enter Passcode:", type="password")
            if st.button("Unlock Terminal", use_container_width=True):
                if pwd == "Harshity@9363":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Key")
        return False
    return True

if not check_password():
    st.stop()

FILE_NAME = "harshit_trading_journal.csv"
UPLOADS_DIR = "trade_screenshots"

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Data Load & Init
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        return pd.DataFrame(columns=[
            "Date", "Symbol", "Type", "Entry", "Exit", "SL", "Target", "Quantity", 
            "Brokerage", "Gross_PnL", "Net_PnL", "Risk_Reward", "Strategy", "Tags", 
            "Emotion", "Mistakes", "Notes", "Screenshot"
        ])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# Header Section with Logo
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>HARSHIT'S TRADING TERMINAL</h1>", unsafe_allow_innerHTML=True)
    st.markdown("<p style='color:#D4AF37; margin-top:0; font-size:16px;'>FinanceWithHarshit • Institutional Execution & Journal OS</p>", unsafe_allow_innerHTML=True)

st.markdown("---")

# Navigation Tabs
tab_entry, tab_analytics, tab_psych, tab_calendar, tab_strategy, tab_goals = st.tabs([
    "📊 Trade Log", 
    "📈 Performance Analytics", 
    "🧠 Psychology & Mistakes", 
    "📅 Calendar Review", 
    "🏷️ Strategy Edge", 
    "🎯 Risk & Capital Goals"
])

# ==========================================
# 1. TRADE MANAGEMENT
# ==========================================
with tab_entry:
    st.subheader("📝 Live Execution Logger")
    
    col_input1, col_input2, col_input3 = st.columns([1, 1, 1])
    
    with col_input1:
        trade_date = st.date_input("Trade Date", datetime.today())
        symbol = st.text_input("Symbol / Instrument", placeholder="e.g. NIFTY, BANKNIFTY").upper()
        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=1, value=50, step=1)
        
    with col_input2:
        entry = st.number_input("Entry Price (₹)", min_value=0.0, format="%.2f")
        exit_p = st.number_input("Exit Price (₹)", min_value=0.0, format="%.2f")
        sl = st.number_input("Stop Loss (SL) (₹)", min_value=0.0, format="%.2f")
        target = st.number_input("Target Price (₹)", min_value=0.0, format="%.2f")

    with col_input3:
        brokerage = st.number_input("Brokerage & Charges (₹)", min_value=0.0, value=40.0, step=5.0)
        strategy = st.selectbox("Strategy Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other"])
        tags = st.text_input("Tags", placeholder="Intraday, Scalp, Nifty")
        emotion = st.selectbox("Trading Emotion", ["Confident", "Disciplined", "Fear", "Greed", "FOMO", "Revenge"])
        mistake = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used"])

    notes = st.text_area("Trade Notes / Technical Observations")
    screenshot = st.file_uploader("Upload Chart Screenshot", type=["png", "jpg", "jpeg"])

    if st.button("🚀 Commit Trade To Terminal", use_container_width=True):
        if symbol and entry > 0 and exit_p > 0 and sl > 0:
            if trade_type == "BUY":
                gross_pnl = (exit_p - entry) * quantity
                risk = abs(entry - sl)
                reward = abs(target - entry)
            else:
                gross_pnl = (entry - exit_p) * quantity
                risk = abs(sl - entry)
                reward = abs(entry - target)
                
            net_pnl = gross_pnl - brokerage
            rr_ratio = round(reward / risk, 2) if risk > 0 else 0.0

            img_path = ""
            if screenshot:
                img_path = os.path.join(UPLOADS_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{screenshot.name}")
                with open(img_path, "wb") as f:
                    f.write(screenshot.getbuffer())

            new_trade = pd.DataFrame([{
                "Date": pd.to_datetime(trade_date),
                "Symbol": symbol,
                "Type": trade_type,
                "Entry": entry,
                "Exit": exit_p,
                "SL": sl,
                "Target": target,
                "Quantity": quantity,
                "Brokerage": brokerage,
                "Gross_PnL": gross_pnl,
                "Net_PnL": net_pnl,
                "Risk_Reward": rr_ratio,
                "Strategy": strategy,
                "Tags": tags,
                "Emotion": emotion,
                "Mistakes": mistake,
                "Notes": notes,
                "Screenshot": img_path
            }])

            df = pd.concat([df, new_trade], ignore_index=True)
            save_data(df)
            st.success(f"✅ Trade Recorded! Net P&L: ₹{net_pnl:.2f} | R:R Ratio: 1:{rr_ratio}")
            st.rerun()
        else:
            st.error("⚠️ Fill all required fields!")

# ==========================================
# 2. ANALYTICS
# ==========================================
with tab_analytics:
    st.subheader("📈 Institutional Metrics")
    if df.empty:
        st.info("No trade data logged yet.")
    else:
        df_sorted = df.sort_values("Date").reset_index(drop=True)
        total_trades = len(df_sorted)
        wins = df_sorted[df_sorted["Net_PnL"] > 0]
        losses = df_sorted[df_sorted["Net_PnL"] < 0]
        
        win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0
        tot_win_amt = wins["Net_PnL"].sum()
        tot_loss_amt = abs(losses["Net_PnL"].sum())
        
        profit_factor = round(tot_win_amt / tot_loss_amt, 2) if tot_loss_amt > 0 else tot_win_amt
        avg_win = wins["Net_PnL"].mean() if not wins.empty else 0
        avg_loss = abs(losses["Net_PnL"].mean()) if not losses.empty else 0
        
        expectancy = ((win_rate/100) * avg_win) - (((100 - win_rate)/100) * avg_loss)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Win Rate", f"{win_rate:.1f}%")
        m2.metric("Profit Factor", f"{profit_factor}")
        m3.metric("Expectancy", f"₹{expectancy:.2f}")
        m4.metric("Total Trades", total_trades)

        st.markdown("---")
        df_sorted['Cum_PnL'] = df_sorted['Net_PnL'].cumsum()
        fig_equity = px.line(df_sorted, x="Date", y="Cum_PnL", title="Equity Growth Curve", template="plotly_dark", markers=True)
        fig_equity.update_traces(line_color="#D4AF37", line_width=3)
        st.plotly_chart(fig_equity, use_container_width=True)

# ==========================================
# 3. PSYCHOLOGY
# ==========================================
with tab_psych:
    st.subheader("🧠 Mindset Analytics")
    if not df.empty:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            emo_summary = df.groupby("Emotion")["Net_PnL"].agg(["count", "sum"]).reset_index()
            fig_emo = px.bar(emo_summary, x="Emotion", y="sum", color="Emotion", title="Net P&L by Emotion", template="plotly_dark")
            st.plotly_chart(fig_emo, use_container_width=True)

        with col_p2:
            mistake_summary = df.groupby("Mistakes")["Net_PnL"].agg(["count", "sum"]).reset_index()
            fig_mis = px.pie(mistake_summary, names="Mistakes", values="count", title="Trading Mistakes Breakdown", template="plotly_dark", hole=0.4)
            st.plotly_chart(fig_mis, use_container_width=True)

# ==========================================
# 4. CALENDAR REVIEW
# ==========================================
with tab_calendar:
    st.subheader("📅 Review Heatmap")
    if not df.empty:
        df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
        daily_pnl = df.groupby("DateStr")["Net_PnL"].sum().reset_index()
        fig_cal = px.bar(daily_pnl, x="DateStr", y="Net_PnL", color="Net_PnL", 
                         color_continuous_scale=["#FF3333", "#222222", "#D4AF37"], 
                         title="Daily P&L Heatmap", template="plotly_dark")
        st.plotly_chart(fig_cal, use_container_width=True)

# ==========================================
# 5. STRATEGY EDGE
# ==========================================
with tab_strategy:
    st.subheader("🏷️ Setup Win-Rate & Screenshots")
    if not df.empty:
        strat_df = df.groupby("Strategy").agg(
            Total_Trades=('Net_PnL', 'count'),
            Net_Profit=('Net_PnL', 'sum'),
            Avg_RR=('Risk_Reward', 'mean')
        ).reset_index()
        
        st.dataframe(strat_df, use_container_width=True)
        fig_strat = px.bar(strat_df, x="Strategy", y="Net_Profit", color="Strategy", title="Profitability by Strategy Setup", template="plotly_dark")
        st.plotly_chart(fig_strat, use_container_width=True)

# ==========================================
# 6. GOALS & RISK CAPITAL
# ==========================================
with tab_goals:
    st.subheader("🎯 Goal & Equity Milestones")
    initial_capital = st.number_input("Starting Capital (₹)", value=100000.0, step=5000.0)
    daily_goal = st.number_input("Daily Target Profit (₹)", value=2000.0, step=500.0)
    
    if not df.empty:
        current_pnl = df["Net_PnL"].sum()
        current_cap = initial_capital + current_pnl
        
        g1, g2 = st.columns(2)
        g1.metric("Current Total Equity", f"₹{current_cap:,.2f}", f"₹{current_pnl:,.2f} Net P&L")
        g2.metric("Target Daily P&L", f"₹{daily_goal:,.2f}")
