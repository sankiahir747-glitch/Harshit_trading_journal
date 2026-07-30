import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import calendar
from datetime import datetime, date, time
import pytz
import yfinance as yf
import feedparser

# Page Config
st.set_page_config(
    page_title="Harshit Trading Terminal | Institutional OS",
    page_icon="👑",
    layout="wide"
)

# AUTOMATIC FAST AUTO-REFRESH (Every 3 Seconds)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=3000, key="live_market_tick_stream")
except Exception:
    pass

# ULTRA-CLEAN LIGHT THEME WITH LIVE BLINKING DOT ANIMATION
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF !important;
        background-image: 
            radial-gradient(rgba(217, 119, 6, 0.04) 1.5px, transparent 0),
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" opacity="0.03"><path d="M20 10v40m10-30v20m20-30v50m10-40v30m20-20v30" stroke="%23D97706" stroke-width="2" fill="none"/></svg>');
        background-size: 30px 30px, 180px 180px;
        color: #111827 !important;
    }
    
    .live-status-container {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
    }
    
    .dot-live {
        height: 10px;
        width: 10px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #10B981;
        animation: blinker 1.2s linear infinite;
    }

    .dot-closed {
        height: 10px;
        width: 10px;
        background-color: #EF4444;
        border-radius: 50%;
        display: inline-block;
    }

    @keyframes blinker {
        50% { opacity: 0.2; }
    }

    .quote-banner {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 5px solid #D97706;
        padding: 10px 18px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .quote-text {
        font-size: 14px;
        font-weight: 700;
        color: #B45309 !important;
        font-style: italic;
    }

    h1, h2, h3, h4 {
        color: #B45309 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
    }

    p, span, label, div {
        color: #1F2937 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #4B5563 !important;
        font-weight: 700 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3F4F6 !important;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #D1D5DB !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        color: #374151 !important;
        font-weight: 700 !important;
        border-radius: 6px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #D97706 !important;
        color: #FFFFFF !important;
    }

    .cal-box-profit {
        background-color: #DCFCE7 !important;
        color: #15803D !important;
        border: 1px solid #86EFAC !important;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
    }
    .cal-box-loss {
        background-color: #FEE2E2 !important;
        color: #B91C1C !important;
        border: 1px solid #FCA5A5 !important;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
    }
    .cal-box-neutral {
        background-color: #F3F4F6 !important;
        color: #6B7280 !important;
        border: 1px solid #E5E7EB !important;
        padding: 8px;
        border-radius: 6px;
        text-align: center;
    }

    .profile-card-dedicated {
        background-color: #FFFBEB !important;
        border: 2px solid #D97706 !important;
        padding: 25px;
        border-radius: 15px;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Passcode Protection
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        
    if not st.session_state["password_correct"]:
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if os.path.exists("logo.png"):
                st.image("logo.png", width=180)
            st.title("👑 HARSHIT TRADING TERMINAL")
            st.caption("GROW • FOCUS • ACHIEVE")
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

def get_financial_year(dt):
    if pd.isna(dt):
        return "Unknown"
    year = dt.year
    month = dt.month
    if month >= 4:
        return f"FY {year}-{str(year+1)[-2:]}"
    else:
        return f"FY {year-1}-{str(year)[-2:]}"

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
            df['FY'] = df['Date'].apply(get_financial_year)
            return df
        except Exception:
            return pd.DataFrame(columns=cols)
    else:
        return pd.DataFrame(columns=cols)

def save_data(df):
    save_cols = [c for c in df.columns if c != 'FY']
    df[save_cols].to_csv(FILE_NAME, index=False)

df = load_data()

# Header Section
col_logo, col_title, col_status = st.columns([1, 4, 2])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=90)

with col_title:
    st.title("HARSHIT'S TRADING TERMINAL")
    st.caption("FinanceWithHarshit • Institutional Execution & Journal OS")

# LIVE / CLOSED STATUS & TIME LOGIC
with col_status:
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    current_time_str = now_ist.strftime("%I:%M:%S %p").lower()
    
    is_weekday = now_ist.weekday() < 5
    m_open = time(9, 15)
    m_close = time(15, 30)
    curr_t = now_ist.time()
    
    is_market_open = is_weekday and (m_open <= curr_t <= m_close)
    
    if is_market_open:
        status_html = f"""
            <div style="text-align: right; margin-top: 10px;">
                <div class="live-status-container">
                    <span class="dot-live"></span>
                    <span style="color:#10B981;">Live</span>
                    <span style="color:#374151;">{current_time_str}</span>
                </div>
            </div>
        """
    else:
        status_html = f"""
            <div style="text-align: right; margin-top: 10px;">
                <div class="live-status-container">
                    <span class="dot-closed"></span>
                    <span style="color:#EF4444;">Closed</span>
                    <span style="color:#374151;">{current_time_str}</span>
                </div>
            </div>
        """
    st.markdown(status_html, unsafe_allow_html=True)

# SAFE REAL-TIME DERIVATIVE INDEX TICKER STREAMING
@st.cache_data(ttl=3)
def fetch_realtime_pure_indices():
    indices = {
        "NIFTY 50": "^NSEI", 
        "BANKNIFTY": "^NSEBANK", 
        "SENSEX": "^BSESN", 
        "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
        "MIDCAP NIFTY": "^NSEMDCP50",
        "BSE BANKEX": "BSE-BANK.BO",
        "NIFTY IT": "^CNXIT",
        "INDIA VIX": "^INDIAVIX"
    }
    res = {}
    for name, sym in indices.items():
        try:
            t = yf.Ticker(sym)
            fast_info = t.fast_info
            price = fast_info['lastPrice']
            prev = fast_info['previousClose']
            chg = price - prev
            pct = (chg / prev) * 100
            res[name] = (price, chg, pct)
        except Exception:
            res[name] = (0.0, 0.0, 0.0)
    return res

live_ticks = fetch_realtime_pure_indices()

# Display Indices Cleanly in 2 Rows of 4
if live_ticks:
    items = list(live_ticks.items())
    
    # Row 1 (First 4 Indices)
    cols_t1 = st.columns(4)
    for idx in range(min(4, len(items))):
        k, (price, chg, pct) = items[idx]
        sign = "+" if pct >= 0 else ""
        delta_str = f"{sign}{chg:.2f} ({sign}{pct:.2f}%)" if price > 0 else "Offline"
        cols_t1[idx].metric(k, f"₹{price:,.2f}" if price > 0 else "Fetch...", delta_str)
        
    # Row 2 (Next 4 Indices)
    if len(items) > 4:
        cols_t2 = st.columns(4)
        for idx in range(4, min(8, len(items))):
            k, (price, chg, pct) = items[idx]
            sign = "+" if pct >= 0 else ""
            delta_str = f"{sign}{chg:.2f} ({sign}{pct:.2f}%)" if price > 0 else "Offline"
            cols_t2[idx - 4].metric(k, f"₹{price:,.2f}" if price > 0 else "Fetch...", delta_str)

st.markdown("""
    <div class="quote-banner">
        <span class="quote-text">📈 TRADER RULE: "Trust the Process. Protect your capital first, profits will follow." 🐂📊</span>
    </div>
""", unsafe_allow_html=True)

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

# TABS NAVIGATION
tab_entry, tab_calc, tab_strategy, tab_components, tab_sector, tab_news, tab_calendar, tab_manage, tab_profile = st.tabs([
    "⚡ Fast Trade Entry", 
    "📐 Position Sizing Calculator",
    "🎯 Strategy Edge & Accuracy",
    "🏛️ Index Heavyweights",
    "📊 Sector Flow & FII/DII",
    "📰 News & Global Impact",
    "📅 Trader's Diary (Calendar)", 
    "🗑️ Manage & Export Data",
    "👤 Trader Profile"
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
        symbol_raw = st.text_input("Symbol / Instrument", placeholder="e.g. RELIANCE, NIFTY50, BTCUSD").upper()
        
        live_price_val = 0.0
        if symbol_raw:
            try:
                sym_lookup = symbol_raw + ".NS" if market == "Indian Stocks / F&O" and not symbol_raw.endswith(".NS") else symbol_raw
                t_ticker = yf.Ticker(sym_lookup)
                live_price_val = t_ticker.fast_info['lastPrice']
                st.info(f"📡 Real-Time Live Price ({sym_lookup}): **₹{live_price_val:,.2f}**")
            except Exception:
                pass

        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        quantity = st.number_input("Quantity / Lot Size", min_value=0.0001, value=75.0, step=1.0)
        
    with col_input2:
        default_entry = float(live_price_val) if live_price_val > 0 else 0.0
        entry = st.number_input("Entry Price (₹/$)", min_value=0.0, value=default_entry, format="%.2f")
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
        
        mistake_option = st.selectbox("Mistake Logged", ["None", "Early Exit", "Over-leveraged", "Chased Price", "Moved SL", "No SL Used", "Other (Custom Mistake)"])
        if mistake_option == "Other (Custom Mistake)":
            mistake = st.text_input("Enter Custom Mistake", placeholder="e.g. Traded during high news event")
        else:
            mistake = mistake_option

    col_notes1, col_notes2 = st.columns([2, 1])
    with col_notes1:
        notes = st.text_area("Trade Notes & Observations")
    with col_notes2:
        chart_file = st.file_uploader("📸 Upload Chart Screenshot", type=["png", "jpg", "jpeg"])

    if st.button("🚀 Commit Trade To Terminal", use_container_width=True):
        if symbol_raw and entry > 0 and exit_p > 0 and sl > 0 and strategy:
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
                "Symbol": symbol_raw,
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
# 3. STRATEGY EDGE & ACCURACY %
# ==========================================
with tab_strategy:
    st.subheader("🎯 Strategy Edge & Accuracy (%) Breakdown")
    if df.empty:
        st.info("Log trades in the 'Fast Trade Entry' tab to start generating strategy accuracy metrics.")
    else:
        strat_stats = []
        for strat, group in df.groupby('Strategy'):
            total_t = len(group)
            wins = len(group[group['Net_PnL'] > 0])
            losses = len(group[group['Net_PnL'] < 0])
            accuracy = (wins / total_t) * 100 if total_t > 0 else 0.0
            net_profit = float(group['Net_PnL'].sum())
            avg_rr = float(group['Risk_Reward'].mean()) if not group.empty else 0.0

            strat_stats.append({
                "Strategy": strat,
                "Total Trades": total_t,
                "Wins": wins,
                "Losses": losses,
                "Accuracy (%)": round(accuracy, 2),
                "Net Realized P&L (₹)": round(net_profit, 2),
                "Avg Risk:Reward": round(avg_rr, 2)
            })

        strat_df = pd.DataFrame(strat_stats).sort_values(by="Accuracy (%)", ascending=False)
        st.dataframe(strat_df, use_container_width=True)

        st.divider()
        st.markdown("#### 📊 Strategy Accuracy Chart")
        fig_strat_acc = px.bar(
            strat_df, 
            x="Strategy", 
            y="Accuracy (%)", 
            color="Accuracy (%)",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            title="Strategy Win-Rate Accuracy (%)"
        )
        st.plotly_chart(fig_strat_acc, use_container_width=True)

# ==========================================
# 4. INDEX HEAVYWEIGHTS
# ==========================================
with tab_components:
    st.subheader("🏛️ Major Index Heavyweights & Technical Trend Screener")
    
    idx_choice = st.radio("Select Index Components:", ["Nifty 50 Heavyweights", "BankNifty Heavyweights", "Sensex Top Stocks"], horizontal=True)
    
    components_map = {
        "Nifty 50 Heavyweights": {
            "RELIANCE": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC BANK": "HDFCBANK.NS", 
            "ICICI BANK": "ICICIBANK.NS", "INFOSYS": "INFY.NS", "BHARTI AIRTEL": "BHARTIARTL.NS",
            "ITC": "ITC.NS", "STATE BANK OF INDIA": "SBIN.NS", "L&T": "LT.NS", "AXIS BANK": "AXISBANK.NS"
        },
        "BankNifty Heavyweights": {
            "HDFC BANK": "HDFCBANK.NS", "ICICI BANK": "ICICIBANK.NS", "STATE BANK OF INDIA": "SBIN.NS",
            "AXIS BANK": "AXISBANK.NS", "KOTAK BANK": "KOTAKBANK.NS", "INDUSIND BANK": "INDUSINDBK.NS",
            "FEDERAL BANK": "FEDERALBNK.NS", "BANK OF BARODA": "BANKBARODA.NS", "PNB": "PNB.NS"
        },
        "Sensex Top Stocks": {
            "RELIANCE": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC BANK": "HDFCBANK.NS",
            "ICICI BANK": "ICICIBANK.NS", "INFOSYS": "INFY.NS", "HINDUSTAN UNILEVER": "HINDUNILVR.NS",
            "BHARTI AIRTEL": "BHARTIARTL.NS", "ITC": "ITC.NS", "BAJAJ FINANCE": "BAJFINANCE.NS"
        }
    }
    
    selected_dict = components_map[idx_choice]
    comp_list = []
    
    for name, sym in selected_dict.items():
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="1mo")
            if len(hist) >= 5:
                cp = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                pct = ((cp - prev)/prev)*100
                
                sma_20 = hist['Close'].mean()
                if cp > sma_20 * 1.02:
                    signal = "Strong Bullish 🟢🟢"
                elif cp > sma_20:
                    signal = "Bullish Medium 🟢"
                elif cp < sma_20 * 0.98:
                    signal = "Strong Bearish 🔴🔴"
                else:
                    signal = "Bearish Medium 🔴"
                    
                comp_list.append({"Stock Name": name, "Ticker": sym, "Price (₹)": round(cp, 2), "Change (%)": round(pct, 2), "Technical Trend": signal})
        except Exception:
            pass
            
    if comp_list:
        comp_df = pd.DataFrame(comp_list)
        st.dataframe(comp_df, use_container_width=True)
        
        st.divider()
        st.markdown("#### 📈 Quick Interactive Technical Chart Viewer")
        selected_stock_name = st.selectbox("Select Stock to View Technical History:", list(selected_dict.keys()))
        selected_stock_ticker = selected_dict[selected_stock_name]
        
        stock_data = yf.Ticker(selected_stock_ticker).history(period="3mo").reset_index()
        fig_stock = px.line(stock_data, x="Date", y="Close", title=f"{selected_stock_name} - 3 Month Price History")
        fig_stock.update_traces(line_color="#D97706", line_width=2)
        st.plotly_chart(fig_stock, use_container_width=True)

# ==========================================
# 5. SECTOR PERFORMANCE
# ==========================================
with tab_sector:
    st.subheader("📊 Sector Performance & FII / DII Daily Activity Tracker")
    
    st.markdown("#### 🏦 Sectoral Heatmap")
    sec_symbols = {
        "IT": "^CNXIT",
        "AUTOMOBILE": "^CNXAUTO",
        "Nifty Oil & Gas": "NIFTY_OIL_AND_GAS.NS",
        "PHARMA": "^CNXPHARMA",
        "PSU Bank": "^CNXPSUBANK",
        "METALS": "^CNXMETAL",
        "PVT Bank": "NIFTY_PVT_BANK.NS",
        "Bank Nifty": "^NSEBANK",
        "CONSTRUCTION": "NIFTY_CONSTRUCT.NS"
    }
    
    sec_data = []
    for name, sym in sec_symbols.items():
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            cp = fi['lastPrice']
            prev = fi['previousClose']
            chg_pct = ((cp - prev)/prev)*100
            sec_data.append({"Sector": name, "Price": round(cp, 2), "Change (%)": round(chg_pct, 2)})
        except Exception:
            pass
            
    if sec_data:
        sec_df = pd.DataFrame(sec_data).sort_values("Change (%)", ascending=True)
        
        c_sec1, c_sec2 = st.columns([2, 1])
        with c_sec1:
            fig_sec = px.bar(
                sec_df, 
                y="Sector", 
                x="Change (%)", 
                orientation='h',
                color="Change (%)", 
                color_continuous_scale=["#EF4444", "#10B981"], 
                title="Sector Performance (% Change)"
            )
            st.plotly_chart(fig_sec, use_container_width=True)
            
        with c_sec2:
            st.markdown("#### Constituent Stocks Snapshot")
            st.dataframe(sec_df.reset_index(drop=True), use_container_width=True)

    st.divider()
    st.markdown("#### 🏛️ Daily FII / DII Institutional Activity Tracker")
    fii_data = pd.DataFrame([
        {"Date": "2026-07-29", "FII Net Buy/Sell (₹ Cr)": -1250.40, "DII Net Buy/Sell (₹ Cr)": +1840.20},
        {"Date": "2026-07-28", "FII Net Buy/Sell (₹ Cr)": +450.80, "DII Net Buy/Sell (₹ Cr)": +210.50},
        {"Date": "2026-07-27", "FII Net Buy/Sell (₹ Cr)": -890.00, "DII Net Buy/Sell (₹ Cr)": +1120.00}
    ])
    st.dataframe(fii_data, use_container_width=True)

# ==========================================
# 6. NEWS
# ==========================================
with tab_news:
    st.subheader("📰 Live Market News, Crypto/Forex & Global Impact Matrix")
    
    news_cat = st.radio("Select News Channel:", ["🇮🇳 Indian Stock Market", "🪙 Crypto & 💵 Forex Feeds", "🌍 Global Events & Nifty Impact Framework"], horizontal=True)
    st.divider()
    
    if news_cat == "🇮🇳 Indian Stock Market":
        try:
            feed = feedparser.parse("https://news.google.com/rss/search?q=Indian+Stock+Market+Nifty+Sensex&hl=en-IN&gl=IN&ceid=IN:en")
            for entry in feed.entries[:8]:
                st.markdown(f"🔹 **[{entry.title}]({entry.link})**")
                st.caption(f"Published: {entry.published}")
                st.divider()
        except Exception:
            st.info("Live Indian market feeds loading...")

    elif news_cat == "🪙 Crypto & 💵 Forex Feeds":
        try:
            feed_c = feedparser.parse("https://news.google.com/rss/search?q=Crypto+Bitcoin+Forex+USDINR&hl=en-IN&gl=IN&ceid=IN:en")
            for entry in feed_c.entries[:8]:
                st.markdown(f"🪙 **[{entry.title}]({entry.link})**")
                st.caption(f"Published: {entry.published}")
                st.divider()
        except Exception:
            st.info("Live Crypto/Forex feeds loading...")

    elif news_cat == "🌍 Global Events & Nifty Impact Framework":
        st.markdown("### 📊 Global Event Impact Matrix on Indian Market")
        
        c_i1, c_i2, c_i3 = st.columns(3)
        with c_i1:
            st.markdown("""
            <div style="background-color:#FFFBEB; border:1px solid #FDE68A; padding:15px; border-radius:8px;">
                <h4>🇺🇸 US Fed Interest Rates</h4>
                <p><b>Rate Cut:</b> Bullish 🟢 for Nifty (FII Inflow increases)</p>
                <p><b>Rate Hike:</b> Bearish 🔴 for Nifty (FII Outflow to US Bonds)</p>
            </div>
            """, unsafe_allow_html=True)
        with c_i2:
            st.markdown("""
            <div style="background-color:#FFFBEB; border:1px solid #FDE68A; padding:15px; border-radius:8px;">
                <h4>🛢️ Brent Crude Oil Prices</h4>
                <p><b>Crude Down (< $75):</b> Bullish 🟢 for Rupee & Nifty</p>
                <p><b>Crude Up (> $85):</b> Bearish 🔴 (Increases India's Inflation)</p>
            </div>
            """, unsafe_allow_html=True)
        with c_i3:
            st.markdown("""
            <div style="background-color:#FFFBEB; border:1px solid #FDE68A; padding:15px; border-radius:8px;">
                <h4>💵 US Dollar Index (DXY)</h4>
                <p><b>DXY Falling:</b> Bullish 🟢 for Indian Emerging Market</p>
                <p><b>DXY Rising (> 105):</b> Bearish 🔴 Pressure on Nifty</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 🌐 Latest Global Macro News Feeds")
        try:
            feed_g = feedparser.parse("https://news.google.com/rss/search?q=US+Fed+Inflation+Global+Economy+Stock+Market&hl=en-IN&gl=IN&ceid=IN:en")
            for entry in feed_g.entries[:6]:
                st.markdown(f"🌐 **[{entry.title}]({entry.link})**")
                st.caption(f"Published: {entry.published}")
                st.divider()
        except Exception:
            st.info("Global Macro news loading...")

# ==========================================
# 7. TRADER'S DIARY
# ==========================================
with tab_calendar:
    st.subheader("📅 Trader's Diary & Dynamic Financial Year Report")
    
    generated_fys = [f"FY {y}-{str(y+1)[-2:]}" for y in range(2020, 2031)]
    
    c_fy, c_mo = st.columns(2)
    with c_fy:
        selected_fy = st.selectbox("Select Financial Year (FY):", generated_fys, index=6)
        
    fy_df = df[df['FY'] == selected_fy] if not df.empty else pd.DataFrame()
    fy_net = float(fy_df['Net_PnL'].sum()) if not fy_df.empty else 0.0
    fy_gross = float(fy_df['Gross_PnL'].sum()) if not fy_df.empty else 0.0
    fy_charges = float(fy_df['Total_Charges'].sum()) if not fy_df.empty else 0.0
    fy_trades = len(fy_df)

    st.markdown(f"### 🏢 **{selected_fy} Financial Summary**")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric(f"Total Net P&L ({selected_fy})", f"₹{fy_net:,.2f}")
    f2.metric("Gross P&L", f"₹{fy_gross:,.2f}")
    f3.metric("Total Charges Paid", f"₹{fy_charges:,.2f}")
    f4.metric("Total FY Trades", fy_trades)

    st.divider()

    with c_mo:
        m_names = [calendar.month_name[i] for i in range(1, 13)]
        s_mo_name = st.selectbox("Select Month for Grid View:", m_names, index=datetime.today().month-1)
        s_mo = m_names.index(s_mo_name) + 1

    if not fy_df.empty:
        fy_df['Year'] = pd.to_datetime(fy_df['Date']).dt.year
        fy_df['Month'] = pd.to_datetime(fy_df['Date']).dt.month
        fy_df['DateStr'] = pd.to_datetime(fy_df['Date']).dt.strftime('%Y-%m-%d')
        f_df = fy_df[fy_df['Month'] == s_mo]
    else:
        f_df = pd.DataFrame()

    m_net = float(f_df['Net_PnL'].sum()) if not f_df.empty else 0.0
    st.markdown(f"#### Monthly Realized Net P&L: **₹{m_net:,.2f}** ({s_mo_name})")
    
    start_yr = int(selected_fy.split(" ")[1].split("-")[0])
    cal_yr = start_yr if s_mo >= 4 else start_yr + 1

    cal = calendar.monthcalendar(cal_yr, s_mo)
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
                dt_s = f"{cal_yr}-{s_mo:02d}-{d:02d}"
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
# 8. MANAGE & EXPORT
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

# ==========================================
# 9. PROFILE
# ==========================================
with tab_profile:
    st.subheader("👤 Trader Profile & Terminal Creator Info")
    
    st.markdown("""
        <div class="profile-card-dedicated">
            <h2>🦁 TRADER IDENTITY & DEVELOPER BRANDING</h2>
            <hr>
            <p style="font-size: 16px;"><strong>💻 Website Made By:</strong> HARSHIT YADAV</p>
            <p style="font-size: 16px;"><strong>✉️ Email Contact:</strong> harshity576@gmail.com</p>
            <p style="font-size: 16px;"><strong>📱 Phone / WhatsApp:</strong> +91 6393643739</p>
            <p style="font-size: 16px;"><strong>📸 Social Media Handles:</strong></p>
            <ul>
                <li><strong>Instagram:</strong> <a href="https://instagram.com/harshityadu1c_" target="_blank" style="color: #B45309;">@harshityadu1c_</a></li>
                <li><strong>Twitter (X):</strong> <a href="https://twitter.com/harshityadu1c_" target="_blank" style="color: #B45309;">@harshityadu1c_</a></li>
                <li><strong>Snapchat:</strong> harshit-yadu1c</li>
            </ul>
            <hr>
            <h4>🔥 Core Trading Philosophy & Mindset:</h4>
            <blockquote style="border-left: 4px solid #D97706; padding-left: 10px; font-style: italic; font-size: 15px;">
                "Trust the Process. Trading is not about predicting the future; it is about managing risk, remaining disciplined, and executing your edge consistently without emotional noise."
            </blockquote>
        </div>
    """, unsafe_allow_html=True)
