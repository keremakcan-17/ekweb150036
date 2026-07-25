from flask import Flask, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "ekweb1500_super_secret_key_2026"

PASSWORD = "ekweb1500"

# ====================== YETKİ KONTROL ======================
def yetki_kontrol():
    if 'unlock_until' not in session:
        return False
    try:
        unlock_time = session['unlock_until']
        if isinstance(unlock_time, str):
            unlock_time = datetime.fromisoformat(unlock_time)
        if datetime.now() > unlock_time:
            session.pop('unlock_until', None)
            return False
        return True
    except:
        return False

# ====================== SÜRE BİLEŞENİ ======================
def kalan_sure_html():
    if 'unlock_until' not in session:
        return ""
    try:
        unlock_time = session['unlock_until']
        if isinstance(unlock_time, str):
            unlock_time = datetime.fromisoformat(unlock_time)
        kalan = unlock_time - datetime.now()
        if kalan.total_seconds() <= 0:
            return ""
        return """
        <div class="timer-badge">
            <span class="pulse-dot"></span>
            <span>Kalan Süre:</span>
            <span id="sure" class="timer-clock">--:--:--</span>
        </div>
        """
    except:
        return ""

# ====================== LOGIN PAGE ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('code') == PASSWORD:
            session['unlock_until'] = (datetime.now() + timedelta(hours = 8)).isoformat()
            return redirect(url_for('ana_sayfa'))
        else:
            return """
            <div style="background:#0f172a; height:100vh; display:flex; align-items:center; justify-content:center; font-family:sans-serif;">
                <div style="background:#1e293b; padding:30px; border-radius:12px; border:1px solid #ef4444; text-align:center; color:#ef4444;">
                    <h3>❌ Hatalı Anahtar Kod</h3>
                    <p style="color:#94a3b8">Giriş sayfasına yönlendiriliyorsunuz...</p>
                </div>
            </div>
            <meta http-equiv='refresh' content='2;url=/login'>
            """

    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Giriş | Finans Portalı</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
            body { background: #0b0f19; color: #f8fafc; height: 100vh; display: flex; align-items: center; justify-content: center; }
            .login-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); padding: 40px; border-radius: 16px; width: 100%; max-width: 400px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
            .login-card h2 { text-align: center; margin-bottom: 24px; font-weight: 700; color: #38bdf8; }
            .input-group { margin-bottom: 20px; }
            input { width: 100%; padding: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: white; font-size: 16px; outline: none; transition: all 0.3s; }
            input:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.2); }
            button { width: 100%; padding: 14px; background: linear-gradient(135deg, #0284c7, #0369a1); border: none; border-radius: 8px; color: white; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
            button:hover { opacity: 0.9; transform: translateY(-1px); }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>🔑 Terminal Girişi</h2>
            <form method="POST">
                <div class="input-group">
                    <input type="password" name="code" placeholder="Erişim Anahtarı" required autofocus>
                </div>
                <button type="submit">Sisteme Bağlan</button>
            </form>
        </div>
    </body>
    </html>
    """

# ====================== ORTAK SHAPE & TEMA ======================
def ortak_html(baslik, icerik):
    unlock = session.get('unlock_until')
    toplam = 0
    if unlock:
        try:
            toplam = int((datetime.fromisoformat(unlock) - datetime.now()).total_seconds())
        except:
            toplam = 0

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{baslik} | Finans Terminali</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://s3.tradingview.com/tv.js"></script>
        <style>
            :root {{
                --bg-main: #0b0f19;
                --bg-card: #161e2e;
                --sidebar-bg: #111827;
                --accent-blue: #38bdf8;
                --accent-gold: #fbbf24;
                --text-main: #f8fafc;
                --text-sub: #94a3b8;
                --border-color: rgba(255,255,255,0.08);
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
            body {{ background-color: var(--bg-main); color: var(--text-main); display: flex; min-height: 100vh; }}
            
            /* Sidebar */
            .sidebar {{ width: 260px; background: var(--sidebar-bg); border-right: 1px solid var(--border-color); padding: 30px 20px; position: fixed; height: 100vh; display: flex; flex-direction: column; gap: 10px; z-index: 100; }}
            .brand {{ font-size: 20px; font-weight: 700; color: var(--accent-blue); padding: 0 10px 20px 10px; border-bottom: 1px solid var(--border-color); margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
            .nav-link {{ display: flex; align-items: center; gap: 12px; color: var(--text-sub); padding: 12px 16px; border-radius: 10px; text-decoration: none; font-weight: 500; transition: all 0.2s; }}
            .nav-link:hover, .nav-link.active {{ background: #1f2937; color: var(--text-main); }}
            .nav-link.active {{ border-left: 4px solid var(--accent-blue); }}

            /* Content Layout */
            .main {{ margin-left: 260px; flex: 1; padding: 40px; width: calc(100% - 260px); }}
            .header-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .page-title {{ font-size: 28px; font-weight: 700; }}

            /* Timer Widget */
            .timer-badge {{ position: fixed; top: 20px; right: 30px; background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(8px); border: 1px solid var(--border-color); color: var(--text-main); padding: 10px 20px; border-radius: 30px; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 10px; z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }}
            .pulse-dot {{ width: 8px; height: 8px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e; }}
            .timer-clock {{ font-family: monospace; font-size: 16px; color: var(--accent-blue); }}

            /* Grid & Cards */
            .grid-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 24px; margin-top: 20px; }}
            .card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 24px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }}
            .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
            .card-title {{ font-size: 18px; font-weight: 600; color: var(--text-sub); display: flex; align-items: center; gap: 8px; }}
            .card-price {{ font-size: 28px; font-weight: 700; color: var(--text-main); }}
            .chart-wrapper {{ height: 350px; border-radius: 8px; overflow: hidden; margin-top: 15px; border: 1px solid var(--border-color); }}

            @media (max-width: 900px) {{
                body {{ flex-direction: column; }}
                .sidebar {{ width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border-color); }}
                .main {{ margin-left: 0; width: 100%; padding: 20px; }}
                .grid-container {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>

    {kalan_sure_html()}

    <aside class="sidebar">
        <div class="brand">📈 EK-TERMINAL</div>
        <a href="/" class="nav-link {'active' if baslik=='Ana Sayfa' else ''}">📊 Genel Bakış</a>
        <a href="/doviz" class="nav-link {'active' if baslik=='Döviz & Pariteler' else ''}">💵 Döviz & Parite</a>
        <a href="/metaller" class="nav-link {'active' if baslik=='Değerli Metaller' else ''}">🏅 Metaller</a>
        <a href="/endeksler" class="nav-link {'active' if baslik=='Borsalar' else ''}">🚀 Borsalar</a>
        <a href="/endeksler" class="nav-link {'active' if baslik=='Sembol Arama' else ''}">Sembol Arama</a>
    </aside>

    <main class="main">
        <div class="header-bar">
            <h1 class="page-title">{baslik}</h1>
        </div>
        {icerik}
    </main>

    <script>
    let t = {toplam};
    function say(){{
        if(t <= 0) return;
        let h = Math.floor(t / 3600);
        let m = Math.floor((t % 3600) / 60);
        let s = t % 60;
        let target = document.getElementById("sure");
        if(target) {{
            target.innerHTML = 
            h.toString().padStart(2,'0') + ":" +
            m.toString().padStart(2,'0') + ":" +
            s.toString().padStart(2,'0');
        }}
        t--;
        setTimeout(say, 1000);
    }}
    say();
    </script>
    </body>
    </html>
    """

# Helper function to generate TradingView Widget HTML
def tradingview_widget_script(container_id, symbol):
    return f"""
    <div id="{container_id}" class="chart-wrapper"></div>
    <script>
    new TradingView.widget({{
        "autosize": true,
        "symbol": "{symbol}",
        "interval": "D",
        "timezone": "Europe/Istanbul",
        "theme": "dark",
        "style": "1",
        "locale": "tr",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "{container_id}"
    }});
    </script>
    """

# ====================== ANA SAYFA ======================
@app.route('/')
def ana_sayfa():
    if not yetki_kontrol():
        return redirect(url_for('login'))
    
    icerik = f"""
    <p style="color:var(--text-sub); margin-bottom:20px;">Piyasa özetleri ve canlı TradingView verilerine hızlı erişim paneli.</p>
    <div class="grid-container">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🏅 Ons Altın</span>
            </div>
            {tradingview_widget_script("tv_gold_home", "OANDA:XAUUSD")}
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">📈 BIST 100</span>
            </div>
            {tradingview_widget_script("tv_bist_home", "BIST:XU100")}
        </div>
    </div>
    """
    return ortak_html("Ana Sayfa", icerik)

# ====================== DÖVİZ ======================
@app.route('/doviz')
def doviz():
    if not yetki_kontrol():
        return redirect(url_for('login'))

    icerik = f"""
    <div class="grid-container">
        <div class="card">
            <div class="card-header">
                <span class="card-title">💵 USD / TRY</span>
            </div>
            {tradingview_widget_script("tv_usdtry", "FX_IDC:USDTRY")}
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">💶 EUR / TRY</span>
            </div>
            {tradingview_widget_script("tv_eurtry", "FX_IDC:EURTRY")}
        </div>
    </div>
    """
    return ortak_html("Döviz & Pariteler", icerik)

# ====================== METALLER ======================
@app.route('/metaller')
def metaller():
    if not yetki_kontrol():
        return redirect(url_for('login'))

    icerik = f"""
    <div class="grid-container">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🏅 Ons Altın (XAUUSD)</span>
            </div>
            {tradingview_widget_script("tv_gold", "OANDA:XAUUSD")}
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">🥈 Ons Gümüş (XAGUSD)</span>
            </div>
            {tradingview_widget_script("tv_silver", "OANDA:XAGUSD")}
        </div>
    </div>
    """
    return ortak_html("Değerli Metaller", icerik)

# ====================== ENDEKSLER ======================
@app.route('/endeksler')
def endeksler():
    if not yetki_kontrol():
        return redirect(url_for('login'))

    icerik = f"""
    <div class="grid-container">
        <div class="card">
            <div class="card-header">
                <span class="card-title">💻 NASDAQ 100</span>
            </div>
            {tradingview_widget_script("tv_nasdaq", "NASDAQ:NDX")}
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">🇹🇷 BIST 100</span>
            </div>
            {tradingview_widget_script("tv_bist", "BIST:XU100")}
        </div>
    </div>
    """
    return ortak_html("Borsalar", icerik)

# ====================== RUN ======================
if __name__ == '__main__':
    app.run(debug=True)