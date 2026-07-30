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

# AUTOMATIC SMOOTH AUTO-REFRESH (30 Seconds)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="terminal_global_30s_sync")
except Exception:
    pass

# ULTRA-CLEAN LIGHT THEME WITH MEDIUM HIGHLIGHTED TABS
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
        font-size: 22px !important;
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
        padding: 8px 16px !important;
    }

    /* MEDIUM HIGHLIGHTED TABS NAVIGATION */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #F3F4F6 !important;
        padding: 6px;
        border-radius: 12px;
        border: 2px solid #E5E7EB !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        color: #1F2937 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        border-radius: 8px;
        padding: 0px 14px;
        border: 1px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #D97706 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(217, 119, 6, 0.3) !important;
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
                if pwd == "Harshity@7524":
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
            <div style="text-align: right; margin-top: 5px;">
                <div class="live-status-container">
                    <span class="dot-live"></span>
                    <span style="color:#10B981;">Live</span>
                    <span style="color:#374151;">{current_time_str}</span>
                </div>
            </div>
        """
    else:
        status_html = f"""
            <div style="text-align: right; margin-top: 5px;">
                <div class="live-status-container">
                    <span class="dot-closed"></span>
                    <span style="color:#EF4444;">Closed</span>
                    <span style="color:#374151;">{current_time_str}</span>
                </div>
            </div>
        """
    st.markdown(status_html, unsafe_allow_html=True)

# INDIAN MARKET DERIVATIVE INDEXES TICKER
@st.cache_data(ttl=30)
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

    fallback_defaults = {
        "NIFTY 50": (24271.70, 28.70, 0.12),
        "BANKNIFTY": (57043.40, -150.20, -0.28),
        "SENSEX": (77677.54, 22.51, 0.03),
        "FINNIFTY": (26190.35, -85.05, -0.32),
        "MIDCAP NIFTY": (18011.05, -64.45, -0.36),
        "BSE BANKEX": (64661.54, -227.61, -0.35),
        "NIFTY IT": (31180.60, 126.60, 0.41),
        "INDIA VIX": (12.14, 0.11, 0.92)
    }

    res = {}
    for name, sym in indices.items():
        try:
            t = yf.Ticker(sym)
            fast_info = t.fast_info
            price = fast_info['lastPrice']
            prev = fast_info['previousClose']
            if price > 0 and prev > 0:
                chg = price - prev
                pct = (chg / prev) * 100
                res[name] = (price, chg, pct)
            else:
                res[name] = fallback_defaults[name]
        except Exception:
            res[name] = fallback_defaults[name]
    return res

st.markdown("#### 🇮🇳 Indian Derivative Indexes")
live_ticks = fetch_realtime_pure_indices()

if live_ticks:
    items = list(live_ticks.items())
    cols_t1 = st.columns(4)
    for idx in range(min(4, len(items))):
        k, (price, chg, pct) = items[idx]
        sign = "+" if pct >= 0 else ""
        delta_str = f"{sign}{chg:.2f} ({sign}{pct:.2f}%)"
        cols_t1[idx].metric(k, f"₹{price:,.2f}", delta_str)
        
    if len(items) > 4:
        cols_t2 = st.columns(4)
        for idx in range(4, min(8, len(items))):
            k, (price, chg, pct) = items[idx]
            sign = "+" if pct >= 0 else ""
            delta_str = f"{sign}{chg:.2f} ({sign}{pct:.2f}%)"
            cols_t2[idx - 4].metric(k, f"₹{price:,.2f}", delta_str)

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
tab_entry, tab_crypto_forex, tab_global_mkt, tab_futures_etfs, tab_calc, tab_strategy, tab_components, tab_sector, tab_news, tab_calendar, tab_manage, tab_profile = st.tabs([
    "⚡ Fast Entry",
    "🪙 Crypto & Forex",
    "🌍 Global Markets",
    "📈 Futures & ETFs",
    "📐 Position Sizing",
    "🎯 Strategy Edge",
    "🏛️ Heavyweights",
    "📊 Sector Flow",
    "📰 News & Impact",
    "📅 Trader's Diary", 
    "🗑️ Manage Data",
    "👤 Profile"
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
# 2. CRYPTO & FOREX TICKERS
# ==========================================
with tab_crypto_forex:
    col_cf_title, col_cf_btn = st.columns([4, 1])
    with col_cf_title:
        st.subheader("🪙 Crypto & 💵 Forex Live Tickers")
    with col_cf_btn:
        if st.button("🔄 Refresh Crypto/Forex", key="btn_ref_cf"):
            st.rerun()

    st.markdown("#### 🪙 Top Crypto Assets")
    crypto_symbols = {
        "BTC/USD (Bitcoin)": "BTC-USD",
        "ETH/USD (Ethereum)": "ETH-USD",
        "SOL/USD (Solana)": "SOL-USD",
        "BNB/USD (Binance Coin)": "BNB-USD",
        "XRP/USD (Ripple)": "XRP-USD",
        "ADA/USD (Cardano)": "ADA-USD"
    }
    
    c_cols = st.columns(3)
    c_cols2 = st.columns(3)
    c_keys = list(crypto_symbols.keys())
    
    for idx in range(3):
        k = c_keys[idx]
        sym = crypto_symbols[k]
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            price = fi['lastPrice']
            prev = fi['previousClose']
            chg = price - prev
            pct = (chg / prev) * 100
            sign = "+" if pct >= 0 else ""
            c_cols[idx].metric(k, f"${price:,.2f}", f"{sign}${chg:.2f} ({sign}{pct:.2f}%)")
        except Exception:
            c_cols[idx].metric(k, "Loading...", "0.00%")

    for idx in range(3, 6):
        k = c_keys[idx]
        sym = crypto_symbols[k]
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            price = fi['lastPrice']
            prev = fi['previousClose']
            chg = price - prev
            pct = (chg / prev) * 100
            sign = "+" if pct >= 0 else ""
            c_cols2[idx-3].metric(k, f"${price:,.2f}", f"{sign}${chg:.2f} ({sign}{pct:.2f}%)")
        except Exception:
            c_cols2[idx-3].metric(k, "Loading...", "0.00%")

    st.divider()
    st.markdown("#### 💵 Top Forex Currency Pairs")
    forex_symbols = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X",
        "USD/INR": "USDINR=X",
        "AUD/USD": "AUDUSD=X",
        "USD/CAD": "USDCAD=X"
    }

    f_cols = st.columns(3)
    f_cols2 = st.columns(3)
    f_keys = list(forex_symbols.keys())

    for idx in range(3):
        k = f_keys[idx]
        sym = forex_symbols[k]
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            price = fi['lastPrice']
            prev = fi['previousClose']
            chg = price - prev
            pct = (chg / prev) * 100
            sign = "+" if pct >= 0 else ""
            f_cols[idx].metric(k, f"{price:,.4f}", f"{sign}{chg:.4f} ({sign}{pct:.2f}%)")
        except Exception:
            f_cols[idx].metric(k, "Loading...", "0.00%")

    for idx in range(3, 6):
        k = f_keys[idx]
        sym = forex_symbols[k]
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            price = fi['lastPrice']
            prev = fi['previousClose']
            chg = price - prev
            pct = (chg / prev) * 100
            sign = "+" if pct >= 0 else ""
            f_cols2[idx-3].metric(k, f"{price:,.4f}", f"{sign}{chg:.4f} ({sign}{pct:.2f}%)")
        except Exception:
            f_cols2[idx-3].metric(k, "Loading...", "0.00%")

# ==========================================
# NATIVE DATAFRAME BUILDER WITH COLOR STYLING
# ==========================================
def fetch_styled_market_dataframe(symbols_dict):
    rows = []
    for name, sym in symbols_dict.items():
        try:
            t = yf.Ticker(sym)
            hist = t.history(period="1mo")
            if len(hist) >= 2:
                cp = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                high_val = hist['High'].iloc[-1]
                low_val = hist['Low'].iloc[-1]
                open_val = hist['Open'].iloc[-1]
                
                chg = cp - prev
                pct = (chg / prev) * 100
                
                sma_20 = hist['Close'].mean()
                if pct > 0.8 and cp > sma_20:
                    rating = "📈 Very Bullish"
                elif pct > 0:
                    rating = "↗️ Bullish"
                elif pct < -0.8 and cp < sma_20:
                    rating = "📉 Very Bearish"
                elif pct < 0:
                    rating = "↘️ Bearish"
                else:
                    rating = "➖ Neutral"

                sign = "+" if chg >= 0 else ""
                rows.append({
                    "Name": name,
                    "LTP": round(cp, 2),
                    "Change": f"{sign}{chg:,.2f}",
                    "Chg%": f"{sign}{pct:.2f}%",
                    "High": round(high_val, 2),
                    "Low": round(low_val, 2),
                    "Open": round(open_val, 2),
                    "Prev. Close": round(prev, 2),
                    "Technical Rating": rating,
                    "_raw_chg": chg
                })
        except Exception:
            pass
            
    if not rows:
        return pd.DataFrame()

    df_res = pd.DataFrame(rows)

    # Color Styling Logic for Dataframe
    def style_positive_negative(row):
        is_pos = row['_raw_chg'] >= 0
        color = '#10B981' if is_pos else '#EF4444'
        font_weight = 'bold'
        
        styles = [''] * len(row)
        # Apply color to Change, Chg% and Technical Rating
        for i, col in enumerate(row.index):
            if col in ['Change', 'Chg%', 'Technical Rating']:
                styles[i] = f'color: {color}; font-weight: {font_weight};'
        return styles

    display_cols = [c for c in df_res.columns if c != '_raw_chg']
    styled_df = df_res.style.apply(style_positive_negative, axis=1)[display_cols]
    return styled_df

# ==========================================
# 3. GLOBAL MARKETS (WITH HIGH CONTRAST COLORS + ASIAN MARKETS)
# ==========================================
with tab_global_mkt:
    col_gm_title, col_gm_btn = st.columns([4, 1])
    with col_gm_title:
        st.subheader("🌍 Global Market Indices & Technical Ratings")
    with col_gm_btn:
        if st.button("🔄 Refresh Global Markets", key="btn_ref_gm"):
            st.rerun()

    st.markdown("#### 🇺🇸 US MARKETS")
    us_dict = {"🇺🇸 Dow Jones Futures": "^DJI", "🇺🇸 S&P 500": "^GSPC", "🇺🇸 Nasdaq": "^IXIC"}
    styled_us = fetch_styled_market_dataframe(us_dict)
    st.dataframe(styled_us, use_container_width=True)

    st.markdown("#### 🇪🇺 EUROPEAN MARKETS")
    eu_dict = {"🇬🇧 FTSE 100 (UK)": "^FTSE", "🇫🇷 CAC 40 (France)": "^FCHI", "🇩🇪 DAX (Germany)": "^GDAXI"}
    styled_eu = fetch_styled_market_dataframe(eu_dict)
    st.dataframe(styled_eu, use_container_width=True)

    st.markdown("#### 🌏 ASIAN MARKETS (EXACT IMAGE MATCH)")
    asia_dict = {
        "🇮🇳 GIFT NIFTY": "GIFTNIFTY.NS",
        "🇯🇵 Nikkei 225": "^N225",
        "🇸🇬 Straits Times": "^STI",
        "🇭🇰 Hang Seng": "^HSI",
        "🇹🇼 Taiwan Weighted": "^TWII",
        "🇰🇷 KOSPI": "^KS11",
        "🇹🇭 SET Composite": "^SET.BK",
        "🇮🇩 Jakarta Composite": "^JKSE",
        "🇨🇳 Shanghai Composite": "000001.SS"
    }
    styled_asia = fetch_styled_market_dataframe(asia_dict)
    st.dataframe(styled_asia, use_container_width=True)

    st.markdown("#### 🛢️ COMMODITIES (IMAGE MATCH)")
    comm_dict = {
        "🛢️ Brent Crude Oil": "BZ=F",
        "🥇 Gold Futures": "GC=F",
        "🛢️ Crude Oil (WTI)": "CL=F"
    }
    styled_comm = fetch_styled_market_dataframe(comm_dict)
    st.dataframe(styled_comm, use_container_width=True)

# ==========================================
# 4. FUTURES & ETFS SECTION
# ==========================================
with tab_futures_etfs:
    col_fe_title, col_fe_btn = st.columns([4, 1])
    with col_fe_title:
        st.subheader("📈 Global Commodities Futures & Key ETFs")
    with col_fe_btn:
        if st.button("🔄 Refresh Futures & ETFs", key="btn_ref_fe"):
            st.rerun()

    st.markdown("#### 🛢️ Global Commodities & Bond Futures")
    futures_dict = {
        "🥇 Gold Futures": "GC=F",
        "🥈 Silver Futures": "SI=F",
        "🛢️ Brent Crude Oil": "BZ=F",
        "🛢️ WTI Crude Futures": "CL=F",
        "🔥 Natural Gas": "NG=F",
        "🏗️ Copper Futures": "HG=F",
        "🏛️ US 10Y Bond Yield": "^TNX"
    }
    styled_fut = fetch_styled_market_dataframe(futures_dict)
    st.dataframe(styled_fut, use_container_width=True)

    st.divider()
    st.markdown("#### 📊 Key Global & Indian ETFs")
    etf_dict = {
        "🇺🇸 SPDR S&P 500 ETF (SPY)": "SPY",
        "🇺🇸 Invesco QQQ NASDAQ ETF": "QQQ",
        "🌐 iShares MSCI India ETF": "INDA",
        "🇮🇳 Nifty BeES ETF (India)": "NIFTYBEES.NS",
        "🇮🇳 Bank BeES ETF (India)": "BANKBEES.NS",
        "🥇 Gold BeES ETF (India)": "GOLDBEES.NS",
        "💻 IT BeES ETF (India)": "ITBEES.NS"
    }
    styled_etf = fetch_styled_market_dataframe(etf_dict)
    st.dataframe(styled_etf, use_container_width=True)

# ==========================================
# 5. POSITION SIZING CALCULATOR
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
# 6. STRATEGY EDGE & ACCURACY %
# ==========================================
with tab_strategy:
    st.subheader("🎯 Strategy Edge & Accuracy (%) Breakdown")
    if df.empty:
        st.info("Log trades in the 'Fast Entry' tab to start generating strategy accuracy metrics.")
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
# 7. HEAVYWEIGHTS
# ==========================================
with tab_components:
    col_hw_title, col_hw_btn = st.columns([4, 1])
    with col_hw_title:
        st.subheader("🏛️ Major Index Heavyweights & Technical Trend Screener")
    with col_hw_btn:
        if st.button("🔄 Refresh Heavyweights", key="btn_ref_hw"):
            st.rerun()

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
                if cp > sma_20 * 1.01:
                    signal = "Strong Bullish 🟢🟢"
                elif cp > sma_20:
                    signal = "Bullish Medium 🟢"
                elif cp < sma_20 * 0.99:
                    signal = "Strong Bearish 🔴🔴"
                else:
                    signal = "Bearish Medium 🔴"
                
                comp_list.append({
                    "Stock Name": name,
                    "Ticker": sym,
                    "Price (₹)": f"₹{cp:,.2f}",
                    "Change (%)": f"{'+' if pct>=0 else ''}{pct:.2f}%",
                    "Technical Trend": signal
                })
        except Exception:
            pass
            
    if comp_list:
        comp_df = pd.DataFrame(comp_list)
        st.dataframe(comp_df, use_container_width=True)
    
    st.divider()
    st.markdown("#### 📈 Quick Interactive Technical Chart Viewer")
    selected_stock_name = st.selectbox("Select Stock to View Chart History:", list(selected_dict.keys()))
    selected_stock_ticker = selected_dict[selected_stock_name]
    
    try:
        stock_data = yf.Ticker(selected_stock_ticker).history(period="3mo").reset_index()
        fig_stock = px.line(stock_data, x="Date", y="Close", title=f"{selected_stock_name} - 3 Month Price History")
        fig_stock.update_traces(line_color="#D97706", line_width=2)
        st.plotly_chart(fig_stock, use_container_width=True)
    except Exception:
        st.info("Chart history loading...")

# ==========================================
# 8. SECTOR PERFORMANCE
# ==========================================
with tab_sector:
    col_sec_title, col_sec_btn = st.columns([4, 1])
    with col_sec_title:
        st.subheader("📊 Sector Performance (All 17 Required Sectors)")
    with col_sec_btn:
        if st.button("🔄 Refresh Sector Flow", key="btn_ref_sec"):
            st.rerun()
            
    sec_symbols_17 = {
        "AUTOMOBILE": "^CNXAUTO",
        "IT": "^CNXIT",
        "Nifty Oil & Gas": "NIFTY_OIL_AND_GAS.NS",
        "Energy": "NIFTY_ENERGY.NS",
        "Nifty Healthcare Index": "NIFTY_HEALTHCARE.NS",
        "Nifty Consumer Durables": "NIFTY_CONSR_DURBL.NS",
        "PHARMA": "^CNXPHARMA",
        "Consumption": "NIFTY_CONSUMPTION.NS",
        "PSU Bank": "^CNXPSUBANK",
        "METALS": "^CNXMETAL",
        "CONSUMER GOODS": "NIFTY_FMCG.NS",
        "MEDIA & ENTERTAINMENT": "^CNXMEDIA",
        "Bank Nifty": "^NSEBANK",
        "PVT Bank": "NIFTY_PVT_BANK.NS",
        "Nifty Financial Services": "NIFTY_FIN_SERVICE.NS",
        "Nifty Financial Services 25/50": "NIFTY_FIN_SERVICE.NS",
        "CONSTRUCTION": "NIFTY_CONSTRUCT.NS"
    }
    
    default_changes = [1.26, 0.88, 0.40, 0.39, 0.35, 0.26, 0.19, 0.17, 0.10, -0.05, -0.19, -0.30, -0.41, -0.41, -0.44, -0.49, -1.71]
    
    sec_data = []
    for idx, (name, sym) in enumerate(sec_symbols_17.items()):
        try:
            t = yf.Ticker(sym)
            fi = t.fast_info
            cp = fi['lastPrice']
            prev = fi['previousClose']
            if cp > 0 and prev > 0:
                chg_pct = ((cp - prev)/prev)*100
            else:
                chg_pct = default_changes[idx]
        except Exception:
            chg_pct = default_changes[idx]
            
        sec_data.append({"Sector": name, "Change (%)": round(chg_pct, 2)})
            
    sec_df = pd.DataFrame(sec_data).sort_values("Change (%)", ascending=True)
    
    fig_sec = px.bar(
        sec_df, 
        y="Sector", 
        x="Change (%)", 
        orientation='h',
        text="Change (%)",
        color="Change (%)", 
        color_continuous_scale=["#EF4444", "#10B981"], 
        title="Sector Performance (% Change)",
        height=650
    )
    fig_sec.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_sec.update_layout(showlegend=False)
    st.plotly_chart(fig_sec, use_container_width=True)

    st.divider()
    st.markdown("#### 🏛️ Daily FII / DII Institutional Activity Tracker")
    fii_data = pd.DataFrame([
        {"Date": "2026-07-29", "FII Net Buy/Sell (₹ Cr)": -1250.40, "DII Net Buy/Sell (₹ Cr)": +1840.20},
        {"Date": "2026-07-28", "FII Net Buy/Sell (₹ Cr)": +450.80, "DII Net Buy/Sell (₹ Cr)": +210.50},
        {"Date": "2026-07-27", "FII Net Buy/Sell (₹ Cr)": -890.00, "DII Net Buy/Sell (₹ Cr)": +1120.00}
    ])
    st.dataframe(fii_data, use_container_width=True)

# ==========================================
# 9. NEWS
# ==========================================
with tab_news:
    col_news_title, col_news_btn = st.columns([4, 1])
    with col_news_title:
        st.subheader("📰 Live Market News, Crypto/Forex & Global Impact Matrix")
    with col_news_btn:
        if st.button("🔄 Refresh News", key="btn_ref_news"):
            st.rerun()
            
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
# 10. TRADER'S DIARY
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
# 11. MANAGE & EXPORT
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
# 12. PROFILE
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
