import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import calendar
from datetime import datetime, date

# Page Configuration
st.set_page_config(
    page_title="Harshit Trading Terminal | Pro OS",
    page_icon="👑",
    layout="wide"
)

# Clean High-Contrast Light Theme
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #111827; }
    h1, h2, h3, h4 { color: #B45309 !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    
    div[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 800 !important; color: #1F2937 !important; }
    div[data-testid="stMetricLabel"] { color: #4B5563 !important; font-weight: 600 !important; }
    
    .stButton>button {
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
        color: #FFFFFF !important; font-weight: bold !important; border-radius: 8px; border: none; padding: 10px 20px;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #F3F4F6; padding: 8px; border-radius: 10px; border: 1px solid #E5E7EB; }
    .stTabs [data-baseweb="tab"] { height: 42px; color: #4B5563; font-weight: 600; border-radius: 6px; }
    .stTabs [aria-selected="true"] { background-color: #D97706 !important; color: #FFFFFF !important; }
    
    .cal-box-profit { background-color: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; }
    .cal-box-loss { background-color: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; }
    .cal-box-neutral { background-color: #F3F4F6; color: #6B7280; border: 1px solid #E5E7EB; padding: 8px; border-radius: 6px; text-align: center; }
    
    .ai-card { background-color: #FEF3C7; border: 1px solid #FDE68A; padding: 18px; border-radius: 12px; margin-bottom: 20px; }
    .profile-card { background-color: #FFFBEB; border: 1px solid #FDE68A; padding: 18px; border-radius: 12px; margin-top: 25px; }
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
            st.image("logo.png", width=180)
            
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

# Safe Data Loader
def load_data():
    cols = [
        "ID", "Date", "Market", "Symbol", "Type", "Entry", "Exit", "SL", "Target", "Quantity", 
        "Brokerage", "Other_Charges", "Total_Charges", "Gross_PnL", "Net_PnL", 
        "Risk_Reward", "Strategy", "Tags", "Emotion", "Mistakes", "Notes", "Screenshot"
    ]
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            if df.empty:
                return pd.DataFrame(columns=cols)
            
            for col in cols:
                if col not in df.columns:
                    if col == "ID":
                        df["ID"] = range(1, len(df) + 1)
                    elif col in ["Brokerage", "Other_Charges", "Total_Charges", "Gross_PnL", "Net_PnL"]:
                        df[col] = 0.0
                    elif col == "Market":
                        df[col] = "Indian Stocks / F&O"
                    else:
                        df[col] = ""
                        
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            return df[cols]
        except Exception:
            return pd.DataFrame(columns=cols)
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

# TODAY'S MIDNIGHT AUTO-RESET METRICS BANNER
today_date = date.today()
today_str = today_date.strftime("%Y-%m-%d")

if not df.empty:
    df['DateOnly'] = pd.to_datetime(df['Date']).dt.date
    today_df = df[df['DateOnly'] == today_date]
    
    today_gross = float(today_df['Gross_PnL'].sum()) if not today_df.empty else 0.0
    today_charges = float(today_df['Total_Charges'].sum()) if not today_df.empty else 0.0
    today_net = float(today_df['Net_PnL'].sum()) if not today_df.empty else 0.0
    today_trades = len(today_df)
    today_wins = len(today_df[today_df['Net_PnL'] > 0])
    today_winrate = (today_wins / today_trades * 100) if today_trades > 0 else 0.0

    st.markdown(f"### ☀️ Today's Performance Summary ({today_str})")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Today Realized P&L", f"₹{today_net:,.2f}")
    m2.metric("Today Gross P&L", f"₹{today_gross:,.2f}")
    m3.metric("Today Charges", f"₹{today_charges:,.2f}")
    m4.metric("Today Win Rate", f"{today_winrate:.1f}%")
    m5.metric("Today Trades", today_trades)

    MAX_DAILY_LOSS = 2000.0
    if today_net < -MAX_DAILY_LOSS:
        st.error(f"🛑 RISK WARNING: Max Daily Loss Hit (₹{today_net:,.2f}). Stop trading for today!")

st.divider()

# NAVIGATION TABS
tab_entry, tab_calc, tab_ai, tab_analytics, tab_calendar, tab_manage = st.tabs([
    "⚡ Fast Trade Entry", 
    "📐 Position Sizing Calculator",
    "🤖 AI Trade Summariser", 
    "📈 Advanced Analytics (35+)", 
    "📅 Trader's Diary (Calendar)", 
    "🗑️ Manage & Export Data"
])

# ==========================================
# 1. FAST TRADE ENTRY
# ==========================================
with tab_entry:
    st.subheader("📝 Live Execution Logger")
    
    col_input1, col_input2, col_input3 = st.columns([1, 1, 1])
    
    with col_input1:
        trade_date = st.date_input("Trade Date", datetime.today())
        market = st.selectbox("Market Category", ["Indian Stocks / F&O", "Crypto", "Forex", "Commodity"])
        symbol = st.text_input("Symbol / Instrument", placeholder="e.g. NIFTY50, BTCUSDT").upper()
        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        quantity = st.number_input("Quantity / Lot Size", min_value=0.0001, value=75.0, step=1.0)
        
    with col_input2:
        entry = st.number_input("Entry Price (₹/$)", min_value=0.0, format="%.2f")
        exit_p = st.number_input("Exit Price (₹/$)", min_value=0.0, format="%.2f")
        sl = st.number_input("Stop Loss (SL)", min_value=0.0, format="%.2f")
        target = st.number_input("Target Price", min_value=0.0, format="%.2f")

    with col_input3:
        brokerage = st.number_input("Brokerage Charges (₹/$)", min_value=0.0, value=40.0, step=5.0)
        other_charges = st.number_input("Taxes / STT / Exchange (₹/$)", min_value=0.0, value=15.0, step=5.0)
        
        strategy_option = st.selectbox("Strategy Setup", ["15-min Breakout", "EMA Crossover", "Support/Resistance", "Trendline Rejection", "Other (Custom)"])
        if strategy_option == "Other (Custom)":
            strategy = st.text_input("Custom Strategy Name", placeholder="e.g. Scalping, VWAP Reversal")
        else:
            strategy = strategy_option

        tags = st.text_input("Custom Tags", placeholder="Intraday, Scalp, High Volatility")
        emotion = st.selectbox("Trading Emotion", ["Confident", "Disciplined", "Fear", "Greed", "FOMO", "Revenge"])
        mistake = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used"])

    col_notes1, col_notes2 = st.columns([2, 1])
    with col_notes1:
        notes = st.text_area("Trade Notes & Observations")
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
                "Market": market,
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
            st.success(f"✅ Trade Logged! Net P&L: ₹{net_pnl:.2f} | R:R = 1:{rr_ratio}")
            st.rerun()
        else:
            st.error("⚠️ Fill all required fields!")

# ==========================================
# 2. POSITION SIZING CALCULATOR
# ==========================================
with tab_calc:
    st.subheader("📐 Risk Management & Position Sizing Calculator")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        total_capital = st.number_input("Total Capital (₹)", value=100000.0, step=5000.0)
    with col_c2:
        risk_per_trade_pct = st.number_input("Max Risk Per Trade (%)", value=1.0, step=0.5)
    with col_c3:
        entry_price_calc = st.number_input("Planned Entry Price (₹)", value=100.0)
        sl_price_calc = st.number_input("Planned Stop-Loss Price (₹)", value=95.0)

    risk_amount = (total_capital * risk_per_trade_pct) / 100.0
    sl_points = abs(entry_price_calc - sl_price_calc)

    if sl_points > 0:
        recommended_qty = int(risk_amount / sl_points)
        total_trade_val = recommended_qty * entry_price_calc
        
        st.markdown("---")
        st.markdown("### 📊 Recommended Position Size Result:")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Max Cash At Risk", f"₹{risk_amount:,.2f}")
        r2.metric("SL Points", f"₹{sl_points:.2f}")
        r3.metric("Recommended Quantity", f"{recommended_qty} Shares / Qty")
        r4.metric("Total Position Value", f"₹{total_trade_val:,.2f}")

# ==========================================
# 3. AI TRADE ANALYZER (CRASH-PROOF SECURE)
# ==========================================
with tab_ai:
    st.subheader("🤖 AI Auto Insights & Pattern Spotter")
    if df.empty:
        st.info("Log trades first to allow AI pattern analysis.")
    else:
        try:
            tot_tr = len(df)
            wins_df = df[df['Net_PnL'] > 0]
            win_rate = (len(wins_df) / tot_tr) * 100 if tot_tr > 0 else 0
            net_pnl_tot = float(df['Net_PnL'].sum())
            
            # Safe Groupby Checks
            strat_grp = df.groupby('Strategy')['Net_PnL'].sum()
            top_strat = strat_grp.idxmax() if not strat_grp.empty else "N/A"
            
            mis_grp = df.groupby('Mistakes')['Net_PnL'].sum()
            worst_mistake = mis_grp.idxmin() if not mis_grp.empty else "None"
            
            st.markdown(f"""
            <div class="ai-card">
                <h4>💡 AI Trading Performance Insight:</h4>
                <ul>
                    <li><strong>Execution Rate:</strong> Total <b>{tot_tr} trades</b> logged | Win Rate: <b>{win_rate:.1f}%</b> | Realized Net P&L: <b>₹{net_pnl_tot:,.2f}</b>.</li>
                    <li><strong>Top Edge Strategy:</strong> Highest profit strategy is <b>'{top_strat}'</b>. Focus on taking setups aligned with this.</li>
                    <li><strong>Key Leakage Area:</strong> Primary mistake area: <b>'{worst_mistake}'</b>. Focus on eliminating this rule breach.</li>
                    <li><strong>Mindset Guidance:</strong> Always calculate position size before trade entry to keep emotions disciplined.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.info("Log more trades to unlock deeper AI insights!")

# ==========================================
# 4. ADVANCED ANALYTICS (CRASH-PROOF SECURE)
# ==========================================
with tab_analytics:
    st.subheader("📈 Institutional Metrics & Analytics")
    if df.empty:
        st.info("No trade data logged yet.")
    else:
        tot_t = len(df)
        w_df = df[df['Net_PnL'] > 0]
        l_df = df[df['Net_PnL'] < 0]
        
        win_r = (len(w_df)/tot_t)*100 if tot_t > 0 else 0
        tot_w_amt = float(w_df['Net_PnL'].sum()) if not w_df.empty else 0.0
        tot_l_amt = abs(float(l_df['Net_PnL'].sum())) if not l_df.empty else 0.0
        
        profit_factor = round(tot_w_amt/tot_l_amt, 2) if tot_l_amt > 0 else tot_w_amt
        avg_w = float(w_df['Net_PnL'].mean()) if not w_df.empty else 0.0
        avg_l = abs(float(l_df['Net_PnL'].mean())) if not l_df.empty else 0.0
        expectancy = ((win_r/100)*avg_w) - (((100-win_r)/100)*avg_l)

        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("Win Rate", f"{win_r:.1f}%")
        a2.metric("Profit Factor", f"{profit_factor}")
        a3.metric("Expectancy", f"₹{expectancy:.2f}")
        a4.metric("Avg Win", f"₹{avg_w:,.2f}")
        a5.metric("Avg Loss", f"₹{avg_l:,.2f}")

        st.divider()
        df_sorted = df.sort_values("Date").reset_index(drop=True)
        df_sorted['Cum_PnL'] = df_sorted['Net_PnL'].cumsum()
        
        fig_equity = px.line(df_sorted, x="Date", y="Cum_PnL", title="Equity Growth Curve", markers=True)
        fig_equity.update_traces(line_color="#B45309", line_width=3)
        st.plotly_chart(fig_equity, use_container_width=True)

# ==========================================
# 5. TRADER'S DIARY & CALENDAR
# ==========================================
with tab_calendar:
    st.subheader("📅 Trader's Diary Calendar")
    if df.empty:
        st.info("Log trades to view calendar heatmap.")
    else:
        df['Year'] = pd.to_datetime(df['Date']).dt.year
        df['Month'] = pd.to_datetime(df['Date']).dt.month
        df['DateStr'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

        c_yr, c_mo = st.columns(2)
        with c_yr:
            s_yr = st.selectbox("Year:", sorted(df['Year'].unique(), reverse=True))
        with c_mo:
            m_names = [calendar.month_name[i] for i in range(1, 13)]
            s_mo_name = st.selectbox("Month:", m_names, index=datetime.today().month-1)
            s_mo = m_names.index(s_mo_name) + 1

        f_df = df[(df['Year'] == s_yr) & (df['Month'] == s_mo)]
        m_net = float(f_df['Net_PnL'].sum()) if not f_df.empty else 0.0
        
        st.markdown(f"### Net P&L: **₹{m_net:,.2f}** ({s_mo_name} {s_yr})")
        
        cal = calendar.monthcalendar(s_yr, s_mo)
        d_grp = f_df.groupby('DateStr')['Net_PnL'].sum().to_dict() if not f_df.empty else {}

        cols_h = st.columns(7)
        for idx, l in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            cols_h[idx].markdown(f"**{l}**")

        for w in cal:
            cols = st.columns(7)
            for i, d in enumerate(w):
                if d == 0:
                    cols[i].markdown("<div class='cal-box-neutral'>-</div>", unsafe_allow_html=True)
                else:
                    dt_s = f"{s_yr}-{s_mo:02d}-{d:02d}"
                    if dt_s in d_grp:
                        v = d_grp[dt_s]
                        if v > 0:
                            cols[i].markdown(f"<div class='cal-box-profit'>{d}<br>+₹{v:,.0f}</div>", unsafe_allow_html=True)
                        elif v < 0:
                            cols[i].markdown(f"<div class='cal-box-loss'>{d}<br>-₹{abs(v):,.0f}</div>", unsafe_allow_html=True)
                        else:
                            cols[i].markdown(f"<div class='cal-box-neutral'>{d}<br>₹0</div>", unsafe_allow_html=True)
                    else:
                        cols[i].markdown(f"<div class='cal-box-neutral'>{d}</div>", unsafe_allow_html=True)

# ==========================================
# 6. MANAGE & EXPORT DATA
# ==========================================
with tab_manage:
    st.subheader("🗑️ Delete & Export Data")
    if df.empty:
        st.info("No saved trades found in log.")
    else:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
        
        st.divider()
        trade_list = [f"ID: {row['ID']} | Date: {pd.to_datetime(row['Date']).strftime('%Y-%m-%d')} | {row['Symbol']} | PnL: ₹{row['Net_PnL']}" for _, row in df.iterrows()]
        s_trade = st.selectbox("Select Trade to Delete:", trade_list)
        
        c_d, c_e = st.columns(2)
        with c_d:
            if st.button("❌ Delete Trade Entry", use_container_width=True):
                s_id = int(s_trade.split("ID: ")[1].split(" |")[0])
                df = df[df["ID"] != s_id]
                save_data(df)
                st.success("Selected trade entry deleted successfully!")
                st.rerun()
        with c_e:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Journal CSV", data=csv_data, file_name=f"Harshit_Journal_{today_str}.csv", mime="text/csv", use_container_width=True)

# PROFILE FOOTER
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
