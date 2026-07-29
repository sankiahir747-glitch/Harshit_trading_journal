import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Harshit's Trading Journal & OS",
    page_icon="📈",
    layout="wide"
)

# Passcode Protection
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        
    if not st.session_state["password_correct"]:
        st.title("🔒 Harshit Trading Terminal - Secure Access")
        pwd = st.text_input("🔑 Passcode daalein access karne ke liye:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == "Harshit123":  # Aapka Password
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Galat Passcode!")
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

st.title("📈 Harshit's Trading Terminal & Journal")
st.markdown("---")

# Navigation Tabs
tab_entry, tab_analytics, tab_psych, tab_calendar, tab_strategy, tab_goals = st.tabs([
    "1️⃣ Trade Management", 
    "2️⃣ Advanced Analytics", 
    "3️⃣ Psychology & Mistakes", 
    "4️⃣ Review & Calendar", 
    "5️⃣ Strategy & Setups", 
    "6️⃣ Goals & Risk Capital"
])

# ==========================================
# 1. TRADE MANAGEMENT (LOGGING & AUTO-CALC)
# ==========================================
with tab_entry:
    st.header("📝 Auto Trade Logging Terminal")
    
    col_input1, col_input2, col_input3 = st.columns([1, 1, 1])
    
    with col_input1:
        trade_date = st.date_input("Trade Date", datetime.today())
        symbol = st.text_input("Symbol / Instrument", placeholder="e.g. NIFTY, BANKNIFTY, AAPL").upper()
        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=1, value=50, step=1)
        
    with col_input2:
        entry = st.number_input("Entry Price (₹)", min_value=0.0, format="%.2f")
        exit_p = st.number_input("Exit Price (₹)", min_value=0.0, format="%.2f")
        sl = st.number_input("Stop Loss (SL) (₹)", min_value=0.0, format="%.2f")
        target = st.number_input("Target Price (₹)", min_value=0.0, format="%.2f")

    with col_input3:
        brokerage = st.number_input("Brokerage & Charges (₹)", min_value=0.0, value=40.0, step=5.0)
        strategy = st.selectbox("Strategy / Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other"])
        tags = st.text_input("Custom Tags (comma separated)", placeholder="Intraday, Scalp, Nifty")
        emotion = st.selectbox("Trading Emotion", ["Confident", "Disciplined", "Fear", "Greed", "FOMO", "Revenge"])
        mistake = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used"])

    notes = st.text_area("Trade Notes / Technical Observations")
    screenshot = st.file_uploader("Upload Chart Screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if st.button("🚀 Record Trade To Journal", use_container_width=True):
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
            st.success(f"Trade Recorded! Net P&L: ₹{net_pnl:.2f} | R:R Ratio: 1:{rr_ratio}")
            st.rerun()
        else:
            st.error("Kripya saare zaroori fields (Symbol, Entry, Exit, SL) sahi bharein!")

# ==========================================
# 2. ANALYTICS & INSTITUTIONAL METRICS
# ==========================================
with tab_analytics:
    st.header("📊 Performance & Risk Metrics")
    if df.empty:
        st.info("Abhi tak koi trades data nahi hai. Tab 1 se trades enter karein.")
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
        
        df_sorted['Win'] = df_sorted['Net_PnL'] > 0
        streaks = (df_sorted['Win'] != df_sorted['Win'].shift()).cumsum()
        streak_counts = df_sorted.groupby(streaks)['Win'].agg(['first', 'count'])
        
        max_win_streak = streak_counts[streak_counts['first'] == True]['count'].max() if True in streak_counts['first'].values else 0
        max_loss_streak = streak_counts[streak_counts['first'] == False]['count'].max() if False in streak_counts['first'].values else 0

        df_sorted['Cum_PnL'] = df_sorted['Net_PnL'].cumsum()
        df_sorted['Peak'] = df_sorted['Cum_PnL'].cummax()
        df_sorted['Drawdown'] = df_sorted['Cum_PnL'] - df_sorted['Peak']
        max_drawdown = df_sorted['Drawdown'].min()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Win Rate", f"{win_rate:.1f}%")
        m2.metric("Profit Factor", f"{profit_factor}")
        m3.metric("Trade Expectancy", f"₹{expectancy:.2f} /trade")
        m4.metric("Max Drawdown", f"₹{max_drawdown:.2f}")

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Avg Win Amount", f"₹{avg_win:.2f}")
        m6.metric("Avg Loss Amount", f"₹{avg_loss:.2f}")
        m7.metric("Max Win Streak", f"{max_win_streak} Trades")
        m8.metric("Max Loss Streak", f"{max_loss_streak} Trades")

        st.markdown("---")
        st.subheader("📈 Cumulative Equity Curve & Drawdown")
        
        fig_equity = px.line(df_sorted, x="Date", y="Cum_PnL", title="Capital Growth Curve (Net P&L)", markers=True)
        st.plotly_chart(fig_equity, use_container_width=True)

# ==========================================
# 3. PSYCHOLOGY & MISTAKES TRACKER
# ==========================================
with tab_psych:
    st.header("🧠 Behavioral & Mindset Breakdown")
    if not df.empty:
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.subheader("Impact of Emotions on P&L")
            emo_summary = df.groupby("Emotion")["Net_PnL"].agg(["count", "sum"]).reset_index()
            fig_emo = px.bar(emo_summary, x="Emotion", y="sum", color="Emotion", title="Net P&L by Emotional State", text_auto=True)
            st.plotly_chart(fig_emo, use_container_width=True)

        with col_p2:
            st.subheader("Cost of Trading Mistakes")
            mistake_summary = df.groupby("Mistakes")["Net_PnL"].agg(["count", "sum"]).reset_index()
            fig_mis = px.pie(mistake_summary, names="Mistakes", values="count", title="Mistake Frequency Distribution", hole=0.4)
            st.plotly_chart(fig_mis, use_container_width=True)

# ==========================================
# 4. REVIEW & TRADING CALENDAR
# ==========================================
with tab_calendar:
    st.header("📅 Daily, Weekly & Monthly Reviews")
    if not df.empty:
        df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
        df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        review_type = st.radio("Select View", ["Daily Heatmap View", "Monthly Summary"], horizontal=True)
        
        if review_type == "Daily Heatmap View":
            daily_pnl = df.groupby("DateStr")["Net_PnL"].sum().reset_index()
            fig_cal = px.bar(daily_pnl, x="DateStr", y="Net_PnL", color="Net_PnL", 
                             color_continuous_scale=["red", "gray", "green"], 
                             title="Daily Net P&L Review Calendar")
            st.plotly_chart(fig_cal, use_container_width=True)
        else:
            monthly_pnl = df.groupby("YearMonth")["Net_PnL"].sum().reset_index()
            st.dataframe(monthly_pnl, use_container_width=True)

# ==========================================
# 5. STRATEGY & SETUP TRACKING
# ==========================================
with tab_strategy:
    st.header("🏷️ Strategy-wise Edge Analysis")
    if not df.empty:
        strat_df = df.groupby("Strategy").agg(
            Total_Trades=('Net_PnL', 'count'),
            Net_Profit=('Net_PnL', 'sum'),
            Avg_RR=('Risk_Reward', 'mean')
        ).reset_index()
        
        st.dataframe(strat_df, use_container_width=True)
        
        fig_strat = px.bar(strat_df, x="Strategy", y="Net_Profit", color="Strategy", title="Profitability by Strategy Setup")
        st.plotly_chart(fig_strat, use_container_width=True)
        
        st.subheader("🖼️ Setup Screenshot Review Log")
        trades_with_img = df[df["Screenshot"] != ""]
        if not trades_with_img.empty:
            for _, row in trades_with_img.iterrows():
                with st.expander(f"Trade: {row['Symbol']} | Date: {row['DateStr']} | Setup: {row['Strategy']}"):
                    st.write(f"**Notes:** {row['Notes']}")
                    if os.path.exists(row['Screenshot']):
                        st.image(Image.open(row['Screenshot']), caption="Chart Setup Screenshot", width=600)

# ==========================================
# 6. GOALS & CAPITAL RISK TRACKER
# ==========================================
with tab_goals:
    st.header("🎯 Goal Tracking & Capital Growth")
    initial_capital = st.number_input("Starting Capital (₹)", value=100000.0, step=5000.0)
    daily_goal = st.number_input("Daily Target Profit (₹)", value=2000.0, step=500.0)
    
    if not df.empty:
        current_pnl = df["Net_PnL"].sum()
        current_cap = initial_capital + current_pnl
        today_str = datetime.today().strftime('%Y-%m-%d')
        today_pnl = df[df['Date'].dt.strftime('%Y-%m-%d') == today_str]["Net_PnL"].sum()
        
        g1, g2, g3 = st.columns(3)
        g1.metric("Current Total Capital", f"₹{current_cap:,.2f}", f"₹{current_pnl:,.2f} Total P&L")
        g2.metric("Today's Progress", f"₹{today_pnl:,.2f}", f"Goal: ₹{daily_goal:,.2f}")
        
        progress = min(max(today_pnl / daily_goal, 0.0), 1.0) if daily_goal > 0 else 0.0
        st.progress(progress)
        st.caption(f"Aapne aaj ke daily goal ka {progress*100:.1f}% achieve kar liya hai.")
