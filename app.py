import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Harshit Trading Terminal | Pro OS",
    page_icon="👑",
    layout="wide"
)

# Custom High-Contrast Dark Gold Theme CSS
st.markdown("""
    <style>
    /* Dark Slate / Cyberpunk Gold Styling */
    .stApp {
        background-color: #0c0f14;
        color: #e2e8f0;
    }
    
    h1, h2, h3, h4 {
        color: #f59e0b !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }

    /* Cards / Containers */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
    }

    /* Green and Red PnL styling */
    .profit-text { color: #10b981 !important; font-weight: bold; }
    .loss-text { color: #ef4444 !important; font-weight: bold; }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #161b22;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #2d3748;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        color: #94a3b8;
        font-weight: 600;
        border-radius: 8px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #f59e0b !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Passcode System
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        
    if not st.session_state["password_correct"]:
        st.title("👑 HARSHIT TRADING TERMINAL")
        st.caption("GROW • FOCUS • ACHIEVE")
        
        if os.path.exists("logo.png"):
            st.image("logo.png", width=220)
            
        pwd = st.text_input("🔑 Enter Passcode:", type="password")
        if st.button("Unlock Terminal"):
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

# Load & Save Functions
def load_data():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        return pd.DataFrame(columns=[
            "ID", "Date", "Symbol", "Type", "Entry", "Exit", "SL", "Target", "Quantity", 
            "Brokerage", "Gross_PnL", "Net_PnL", "Risk_Reward", "Strategy", "Tags", 
            "Emotion", "Mistakes", "Notes"
        ])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# Header Section
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)
with col_title:
    st.title("HARSHIT'S TRADING TERMINAL")
    st.caption("FinanceWithHarshit • Institutional Execution & Journal OS")

st.divider()

# ==========================================
# TOP OVERALL P&L METRICS BAR
# ==========================================
if not df.empty:
    total_trades = len(df)
    total_gross = df["Gross_PnL"].sum()
    total_charges = df["Brokerage"].sum()
    total_net_pnl = df["Net_PnL"].sum()
    wins = df[df["Net_PnL"] > 0]
    win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Realized P&L", f"₹{total_net_pnl:,.2f}", delta=f"{'Profit' if total_net_pnl>=0 else 'Loss'}")
    m2.metric("Gross P&L", f"₹{total_gross:,.2f}")
    m3.metric("Brokerage & Charges", f"₹{total_charges:,.2f}")
    m4.metric("Win Rate", f"{win_rate:.1f}%")
    m5.metric("Total Executed Trades", total_trades)
    st.divider()

# Navigation Tabs
tab_entry, tab_manage, tab_calendar, tab_analytics, tab_psych, tab_strategy = st.tabs([
    "📊 Trade Log", 
    "🗑️ Manage & Delete Trades",
    "📅 Monthly P&L Calendar", 
    "📈 Performance Analytics", 
    "🧠 Psychology & Mistakes", 
    "🏷️ Strategy Edge"
])

# ==========================================
# 1. TRADE LOG
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
        
        # Strategy selection with Custom Input!
        strategy_option = st.selectbox("Strategy Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other (Custom)"])
        if strategy_option == "Other (Custom)":
            strategy = st.text_input("Enter Custom Strategy Name", placeholder="e.g. Scalping Setup, VWAP Reversal")
        else:
            strategy = strategy_option

        tags = st.text_input("Tags", placeholder="Intraday, Scalp, Nifty")
        emotion = st.selectbox("Trading Emotion", ["Confident", "Disciplined", "Fear", "Greed", "FOMO", "Revenge"])
        mistake = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used"])

    notes = st.text_area("Trade Notes / Technical Observations")

    if st.button("🚀 Commit Trade To Terminal", use_container_width=True):
        if symbol and entry > 0 and exit_p > 0 and sl > 0 and strategy:
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

            trade_id = int(datetime.now().timestamp())

            new_trade = pd.DataFrame([{
                "ID": trade_id,
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
                "Notes": notes
            }])

            df = pd.concat([df, new_trade], ignore_index=True)
            save_data(df)
            st.success(f"✅ Trade Recorded! Net P&L: ₹{net_pnl:.2f} | R:R Ratio: 1:{rr_ratio}")
            st.rerun()
        else:
            st.error("⚠️ Fill all required fields including strategy name!")

# ==========================================
# 2. MANAGE & DELETE TRADES
# ==========================================
with tab_manage:
    st.subheader("🗑️ Edit / Delete Saved Trades")
    if df.empty:
        st.info("No saved trades found.")
    else:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
        
        st.divider()
        st.markdown("#### Delete A Galat / False Entry")
        
        trade_list = [f"ID: {row['ID']} | Date: {row['Date'].strftime('%Y-%m-%d')} | {row['Symbol']} | PnL: ₹{row['Net_PnL']}" for _, row in df.iterrows()]
        selected_trade = st.selectbox("Select Trade to Delete:", trade_list)
        
        if st.button("❌ Delete Selected Trade", use_container_width=True):
            selected_id = int(selected_trade.split("ID: ")[1].split(" |")[0])
            df = df[df["ID"] != selected_id]
            save_data(df)
            st.success("✅ Selected trade deleted successfully!")
            st.rerun()

# ==========================================
# 3. MONTHLY P&L CALENDAR (ZERODHA STYLE)
# ==========================================
with tab_calendar:
    st.subheader("📅 Zerodha-Style P&L Calendar")
    if df.empty:
        st.info("Log trades to view calendar heatmap.")
    else:
        df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
        daily_pnl = df.groupby("DateStr")["Net_PnL"].sum().reset_index()
        
        fig_cal = px.bar(
            daily_pnl, 
            x="DateStr", 
            y="Net_PnL", 
            color="Net_PnL", 
            color_continuous_scale=["#ef4444", "#1e293b", "#10b981"],
            title="Daily Profit & Loss Bar View"
        )
        st.plotly_chart(fig_cal, use_container_width=True)
        
        # Table view of daily summary
        st.markdown("### Daily Breakdown Summary")
        st.dataframe(daily_pnl.sort_values("DateStr", ascending=False), use_container_width=True)

# ==========================================
# 4. ANALYTICS
# ==========================================
with tab_analytics:
    st.subheader("📈 Performance Metrics")
    if not df.empty:
        df_sorted = df.sort_values("Date").reset_index(drop=True)
        df_sorted['Cum_PnL'] = df_sorted['Net_PnL'].cumsum()
        
        fig_equity = px.line(df_sorted, x="Date", y="Cum_PnL", title="Equity Curve (Growth Chart)", markers=True)
        fig_equity.update_traces(line_color="#f59e0b", line_width=3)
        st.plotly_chart(fig_equity, use_container_width=True)

# ==========================================
# 5. PSYCHOLOGY
# ==========================================
with tab_psych:
    st.subheader("🧠 Emotion & Mistake Breakdown")
    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            emo_df = df.groupby("Emotion")["Net_PnL"].sum().reset_index()
            fig_emo = px.bar(emo_df, x="Emotion", y="Net_PnL", title="PnL by Emotion", color="Net_PnL")
            st.plotly_chart(fig_emo, use_container_width=True)
        with c2:
            mis_df = df.groupby("Mistakes")["Net_PnL"].count().reset_index()
            fig_mis = px.pie(mis_df, names="Mistakes", values="Net_PnL", title="Mistakes Count", hole=0.4)
            st.plotly_chart(fig_mis, use_container_width=True)

# ==========================================
# 6. STRATEGY EDGE
# ==========================================
with tab_strategy:
    st.subheader("🏷️ Strategy Win-Rate & Net Profit")
    if not df.empty:
        strat_summary = df.groupby("Strategy").agg(
            Total_Trades=('Net_PnL', 'count'),
            Net_Profit=('Net_PnL', 'sum'),
            Avg_RR=('Risk_Reward', 'mean')
        ).reset_index()
        
        st.dataframe(strat_summary, use_container_width=True)
        fig_strat = px.bar(strat_summary, x="Strategy", y="Net_Profit", color="Strategy", title="Profitability by Strategy")
        st.plotly_chart(fig_strat, use_container_width=True)
