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

# Clean White / Light Theme CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
    }
    
    h1, h2, h3, h4 {
        color: #B45309 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }

    /* Cards / Containers */
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #1F2937 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #4B5563 !important;
        font-weight: 600 !important;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
        color: #FFFFFF !important;
        font-weight: bold !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3F4F6;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        color: #4B5563;
        font-weight: 600;
        border-radius: 6px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #D97706 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Passcode Protection
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

# Safe Data Load & Auto Migration for Missing Columns
def load_data():
    cols = [
        "ID", "Date", "Symbol", "Type", "Entry", "Exit", "SL", "Target", "Quantity", 
        "Brokerage", "Gross_PnL", "Net_PnL", "Risk_Reward", "Strategy", "Tags", 
        "Emotion", "Mistakes", "Notes"
    ]
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            return pd.DataFrame(columns=cols)
        
        # Ensure all columns exist
        for col in cols:
            if col not in df.columns:
                if col == "ID":
                    df["ID"] = range(1, len(df) + 1)
                else:
                    df[col] = ""
                    
        df['Date'] = pd.to_datetime(df['Date'])
        return df[cols]
    else:
        return pd.DataFrame(columns=cols)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

# Header Section
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
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
    m1.metric("Total Realized P&L", f"₹{total_net_pnl:,.2f}")
    m2.metric("Gross P&L", f"₹{total_gross:,.2f}")
    m3.metric("Brokerage & Charges", f"₹{total_charges:,.2f}")
    m4.metric("Win Rate", f"{win_rate:.1f}%")
    m5.metric("Total Trades", total_trades)
    st.divider()

# Navigation Tabs
tab_entry, tab_manage, tab_calendar, tab_analytics, tab_psych, tab_strategy = st.tabs([
    "📊 Trade Log", 
    "🗑️ Delete / Manage Trades",
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
        
        # Strategy selection with Custom Input
        strategy_option = st.selectbox("Strategy Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other (Custom)"])
        if strategy_option == "Other (Custom)":
            strategy = st.text_input("Enter Custom Strategy Name", placeholder="e.g. Scalping, VWAP Reversal")
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
            st.error("⚠️ Fill required fields including strategy name!")

# ==========================================
# 2. MANAGE & DELETE TRADES
# ==========================================
with tab_manage:
    st.subheader("🗑️ Delete Galat / Mistakes Entries")
    if df.empty:
        st.info("No saved trades found in log.")
    else:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
        
        st.divider()
        st.markdown("#### Select Trade to Delete:")
        
        trade_list = [f"ID: {row['ID']} | Date: {pd.to_datetime(row['Date']).strftime('%Y-%m-%d')} | {row['Symbol']} | PnL: ₹{row['Net_PnL']}" for _, row in df.iterrows()]
        selected_trade = st.selectbox("Choose Trade:", trade_list)
        
        if st.button("❌ Delete Selected Trade Entry", use_container_width=True):
            selected_id = int(selected_trade.split("ID: ")[1].split(" |")[0])
            df = df[df["ID"] != selected_id]
            save_data(df)
            st.success("✅ Trade deleted successfully from journal!")
            st.rerun()

# ==========================================
# 3. MONTHLY P&L CALENDAR
# ==========================================
with tab_calendar:
    st.subheader("📅 Daily & Monthly P&L Overview")
    if df.empty:
        st.info("Log trades to view calendar heatmap.")
    else:
        df['DateStr'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        daily_pnl = df.groupby("DateStr")["Net_PnL"].sum().reset_index()
        
        fig_cal = px.bar(
            daily_pnl, 
            x="DateStr", 
            y="Net_PnL", 
            color="Net_PnL", 
            color_continuous_scale=["#EF4444", "#9CA3AF", "#10B981"],
            title="Daily Profit & Loss Bar View"
        )
        st.plotly_chart(fig_cal, use_container_width=True)
        
        st.markdown("### Daily Breakdown Summary Table")
        st.dataframe(daily_pnl.sort_values("DateStr", ascending=False), use_container_width=True)

# ==========================================
# 4. ANALYTICS
# ==========================================
with tab_analytics:
    st.subheader("📈 Performance Metrics")
    if not df.empty:
        df_sorted = df.sort_values("Date").reset_index(drop=True)
        df_sorted['Cum_PnL'] = df_sorted['Net_PnL'].cumsum()
        
        fig_equity = px.line(df_sorted, x="Date", y="Cum_PnL", title="Equity Growth Curve", markers=True)
        fig_equity.update_traces(line_color="#B45309", line_width=3)
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
