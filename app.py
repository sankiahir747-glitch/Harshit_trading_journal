import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import calendar
from datetime import datetime, date

# Page Config
st.set_page_config(
    page_title="Harshit Trading Terminal | Pro OS",
    page_icon="👑",
    layout="wide"
)

# Clean Light Theme CSS
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

    /* Metrics Cards */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1F2937 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #4B5563 !important;
        font-weight: 600 !important;
    }

    /* Buttons */
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

    /* Tabs */
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

    /* Calendar Grid Styling */
    .cal-box-profit {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
    }
    .cal-box-loss {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
    }
    .cal-box-neutral {
        background-color: #F3F4F6;
        color: #6B7280;
        border: 1px solid #E5E7EB;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
    }
    .profile-card {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        padding: 18px;
        border-radius: 12px;
        margin-top: 25px;
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
            st.image("logo.png", width=200)
            
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

# Safe Data Load & Auto Migration
def load_data():
    cols = [
        "ID", "Date", "Symbol", "Type", "Entry", "Exit", "SL", "Target", "Quantity", 
        "Brokerage", "Other_Charges", "Total_Charges", "Gross_PnL", "Net_PnL", 
        "Risk_Reward", "Strategy", "Tags", "Emotion", "Mistakes", "Notes", "Screenshot"
    ]
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        if df.empty:
            return pd.DataFrame(columns=cols)
        
        for col in cols:
            if col not in df.columns:
                if col == "ID":
                    df["ID"] = range(1, len(df) + 1)
                elif col in ["Brokerage", "Other_Charges", "Total_Charges"]:
                    df[col] = 0.0
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
        st.image("logo.png", width=95)
with col_title:
    st.title("HARSHIT'S TRADING TERMINAL")
    st.caption("FinanceWithHarshit • Institutional Execution & Journal OS")

st.divider()

# ==========================================
# UPDATE 1: DAILY RESETTING METRICS BANNER (Midnight Auto Reset)
# ==========================================
today_date = date.today()
today_str = today_date.strftime("%Y-%m-%d")

if not df.empty:
    df['DateOnly'] = pd.to_datetime(df['Date']).dt.date
    today_df = df[df['DateOnly'] == today_date]
    
    today_gross = today_df['Gross_PnL'].sum() if not today_df.empty else 0.0
    today_charges = today_df['Total_Charges'].sum() if not today_df.empty else 0.0
    today_net = today_df['Net_PnL'].sum() if not today_df.empty else 0.0
    today_trades = len(today_df)
    today_wins = len(today_df[today_df['Net_PnL'] > 0])
    today_winrate = (today_wins / today_trades * 100) if today_trades > 0 else 0.0

    st.markdown(f"### ☀️ Today's Performance Summary ({today_str})")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Today Realized P&L", f"₹{today_net:,.2f}")
    m2.metric("Today Gross P&L", f"₹{today_gross:,.2f}")
    m3.metric("Today Charges & Brokerage", f"₹{today_charges:,.2f}")
    m4.metric("Today Win Rate", f"{today_winrate:.1f}%")
    m5.metric("Today Trades Logged", today_trades)

    # Risk Warning Rule
    MAX_DAILY_LOSS = 2000.0  # Daily Drawdown Limit
    if today_net < -MAX_DAILY_LOSS:
        st.error(f"🛑 RISK ALERT: Max Daily Drawdown Exceeded (Loss: ₹{today_net:,.2f}). Stop trading for today!")

st.divider()

# Navigation Tabs
tab_entry, tab_manage, tab_calendar, tab_analytics, tab_psych, tab_strategy = st.tabs([
    "📊 Trade Log", 
    "🗑️ Manage & Edit Trades",
    "📅 Trader's Diary (Calendar)", 
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
        symbol = st.text_input("Symbol / Instrument", placeholder="e.g. NIFTY50, BANKNIFTY").upper()
        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=1, value=75, step=1)
        
    with col_input2:
        entry = st.number_input("Entry Price (₹)", min_value=0.0, format="%.2f")
        exit_p = st.number_input("Exit Price (₹)", min_value=0.0, format="%.2f")
        sl = st.number_input("Stop Loss (SL) (₹)", min_value=0.0, format="%.2f")
        target = st.number_input("Target Price (₹)", min_value=0.0, format="%.2f")

    with col_input3:
        brokerage = st.number_input("Brokerage Charges (₹)", min_value=0.0, value=40.0, step=5.0)
        other_charges = st.number_input("Other Charges / STT / Taxes (₹)", min_value=0.0, value=15.0, step=5.0)
        
        strategy_option = st.selectbox("Strategy Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other (Custom)"])
        if strategy_option == "Other (Custom)":
            strategy = st.text_input("Enter Custom Strategy Name", placeholder="e.g. Scalping, Price Action")
        else:
            strategy = strategy_option

        tags = st.text_input("Tags", placeholder="Intraday, Scalp, Nifty")
        emotion = st.selectbox("Trading Emotion", ["Confident", "Disciplined", "Fear", "Greed", "FOMO", "Revenge"])
        mistake = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used"])

    col_notes1, col_notes2 = st.columns([2, 1])
    with col_notes1:
        notes = st.text_area("Trade Notes / Technical Observations")
    with col_notes2:
        chart_file = st.file_uploader("📸 Upload Chart Screenshot", type=["png", "jpg", "jpeg"])

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
                
            total_charges = brokerage + other_charges
            net_pnl = gross_pnl - total_charges
            rr_ratio = round(reward / risk, 2) if risk > 0 else 0.0

            img_path = ""
            if chart_file:
                img_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{chart_file.name}"
                img_path = os.path.join(UPLOADS_DIR, img_filename)
                with open(img_path, "wb") as f:
                    f.write(chart_file.getbuffer())

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
                "Other_Charges": other_charges,
                "Total_Charges": total_charges,
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
# 2. MANAGE & DELETE TRADES
# ==========================================
with tab_manage:
    st.subheader("🗑️ Delete / Manage Logged Entries")
    if df.empty:
        st.info("No saved trades found in log.")
    else:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
        
        st.divider()
        st.markdown("#### Select Trade to Delete:")
        trade_list = [f"ID: {row['ID']} | Date: {pd.to_datetime(row['Date']).strftime('%Y-%m-%d')} | {row['Symbol']} | PnL: ₹{row['Net_PnL']}" for _, row in df.iterrows()]
        selected_trade = st.selectbox("Choose Trade:", trade_list)
        
        col_del, col_exp = st.columns(2)
        with col_del:
            if st.button("❌ Delete Selected Trade", use_container_width=True):
                selected_id = int(selected_trade.split("ID: ")[1].split(" |")[0])
                df = df[df["ID"] != selected_id]
                save_data(df)
                st.success("✅ Trade deleted successfully!")
                st.rerun()
        with col_exp:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Journal to CSV / Excel", data=csv_data, file_name=f"Harshit_Trading_Journal_{today_str}.csv", mime="text/csv", use_container_width=True)

# ==========================================
# UPDATE 2: ZERODHA / SENSIBULL STYLE TRADER'S DIARY & CALENDAR
# ==========================================
with tab_calendar:
    st.subheader("📅 Trader's Diary & Multi-Year P&L Calendar")
    if df.empty:
        st.info("Log trades to view calendar heatmap.")
    else:
        df['Year'] = pd.to_datetime(df['Date']).dt.year
        df['Month'] = pd.to_datetime(df['Date']).dt.month
        df['Day'] = pd.to_datetime(df['Date']).dt.day
        df['DateStr'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

        years_available = sorted(df['Year'].unique(), reverse=True)
        
        c_yr, c_mo = st.columns(2)
        with c_yr:
            selected_year = st.selectbox("Select Year:", years_available, index=0)
        with c_mo:
            months_names = [calendar.month_name[i] for i in range(1, 13)]
            selected_month_name = st.selectbox("Select Month:", months_names, index=datetime.today().month - 1)
            selected_month = months_names.index(selected_month_name) + 1

        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]
        
        # Summary Cards
        monthly_net = filtered_df['Net_PnL'].sum() if not filtered_df.empty else 0.0
        traded_days = filtered_df['DateStr'].nunique() if not filtered_df.empty else 0
        
        daily_grp = filtered_df.groupby('DateStr')['Net_PnL'].sum().reset_index() if not filtered_df.empty else pd.DataFrame(columns=['DateStr', 'Net_PnL'])
        profit_days = len(daily_grp[daily_grp['Net_PnL'] > 0]) if not daily_grp.empty else 0
        loss_days = len(daily_grp[daily_grp['Net_PnL'] < 0]) if not daily_grp.empty else 0

        st.markdown(f"### Net Realised P&L: **₹{monthly_net:,.2f}** for {selected_month_name} {selected_year}")
        
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        m_c1.metric("Traded Days", traded_days)
        m_c2.metric("In-Profit Days", profit_days)
        m_c3.metric("Loss Days", loss_days)
        m_c4.metric("Win-Rate (Days)", f"{(profit_days/traded_days*100):.1f}%" if traded_days > 0 else "0.0%")

        st.divider()

        # Monthly Calendar Grid View
        st.markdown(f"#### 🗓️ Trader's Diary Grid ({selected_month_name} {selected_year})")
        
        cal = calendar.monthcalendar(selected_year, selected_month)
        pnl_map = daily_grp.set_index('DateStr')['Net_PnL'].to_dict() if not daily_grp.empty else {}

        # Days Header
        cols_header = st.columns(7)
        days_label = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, lbl in enumerate(days_label):
            cols_header[idx].markdown(f"**{lbl}**")

        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].markdown("<div class='cal-box-neutral'>-</div>", unsafe_allow_html=True)
                else:
                    curr_date_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
                    if curr_date_str in pnl_map:
                        val = pnl_map[curr_date_str]
                        if val > 0:
                            cols[i].markdown(f"<div class='cal-box-profit'>{day}<br>+₹{val:,.0f}</div>", unsafe_allow_html=True)
                        elif val < 0:
                            cols[i].markdown(f"<div class='cal-box-loss'>{day}<br>-₹{abs(val):,.0f}</div>", unsafe_allow_html=True)
                        else:
                            cols[i].markdown(f"<div class='cal-box-neutral'>{day}<br>₹0</div>", unsafe_allow_html=True)
                    else:
                        cols[i].markdown(f"<div class='cal-box-neutral'>{day}</div>", unsafe_allow_html=True)

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

# ==========================================
# UPDATE 3: TRADER PROFILE & CONTACT FOOTER
# ==========================================
st.markdown("""
    <div class="profile-card">
        <h3>🦁 TRADER IDENTITY & CONTACT DETAILS</h3>
        <p><strong>Name:</strong> HARSHIT YADAV</p>
        <p><strong>Email:</strong> harshity576@gmail.com</p>
        <p><strong>Mobile / WhatsApp:</strong> +91 6393643739</p>
        <p><strong>Instagram:</strong> <a href="https://instagram.com/harshityadu1c_" target="_blank">@harshityadu1c_</a> | 
           <strong>Twitter (X):</strong> <a href="https://twitter.com/harshityadu1c_" target="_blank">@harshityadu1c_</a> | 
           <strong>Snapchat:</strong> harshit-yadu1c</p>
    </div>
""", unsafe_allow_html=True)
