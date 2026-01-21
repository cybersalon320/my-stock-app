import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 2. 側邊欄設定 ---
st.sidebar.header("📝 考場設定")
if 't' not in st.session_state: st.session_state.t = 30
if 'p' not in st.session_state: st.session_state.p = 30
st.session_state.t = st.sidebar.number_input("應到人數", value=st.session_state.t, step=1)
st.session_state.p = st.sidebar.number_input("實到人數", value=st.session_state.p, step=1)
absent = st.session_state.t - st.session_state.p

st.sidebar.markdown("---")
default_sch = """第一節：自修, 08:25-09:10
第二節：寫作, 09:20-10:05
第三節：自修, 10:15-11:00
第四節：數學, 11:10-11:55
第五節：英文, 13:10-15:00
第六節：社會, 15:10-16:10"""

st.sidebar.subheader("📅 手動輸入考程")
raw_input = st.sidebar.text_area("格式：科目, 開始-結束", value=default_sch, height=200)

# 解析課表
sch = []
try:
    for line in raw_input.strip().split('\n'):
        if ',' in line:
            name, times = line.split(',')
            s, e = times.strip().split('-')
            sch.append({"n": name.strip(), "s": s.strip(), "e": e.strip()})
except:
    st.sidebar.error("格式錯誤！請檢查逗號與橫槓。")

# 時間判斷
now = datetime.now(pytz.timezone('Asia/Taipei'))
hm = now.strftime("%H:%M")
cur, rng, hi = "休息時間", "--:--", -1
for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']}-{x['e']}", i
        break

# --- 3. 響應式 HTML 樣式 ---
# 使用了 calc() 和 flex-wrap 來達成自動縮放
html = f"""
<style>
    .stApp {{ background:#fff; }}
    .main-container {{
        background: #FDF5E6;
        padding: 2vw; /* 隨螢幕寬度調整間距 */
        border-radius: 30px;
        color: #5D5D5D;
        width: 95%;
        margin: auto;
    }}
    .header-box {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap; /* 寬度不夠時自動換行 */
        margin-bottom: 20px;
        gap: 20px;
    }}
    .content-grid {{
        display: flex;
        flex-wrap: wrap; /* 關鍵：寬度不足時自動上下排 */
        gap: 20px;
    }}
    .card {{
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.02);
        flex: 1 1 350px; /* 最小寬度 350px，超過則並排 */
    }}
    .status-box {{
        display: flex;
        justify-content: space-around;
        background: #FDF5E6;
        padding: 15px;
        border-radius: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }}
    @media (max-width: 600px) {{
        .time-text {{ font-size: 60px !important; }}
        .subject-text {{ font-size: 35px !important; }}
    }}
</style>

<div class="main-container">
    <div class="header-box">
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #BC8F8F;">當 前 時 間</div>
            <div class="time-text" style="font-size: 6rem; font-weight: bold; line-height: 1;">{now.strftime("%H:%M:%S")}</div>
        </div>
        <div style="background: white; padding: 20px 40px; border-radius: 20px; text-align: right;">
            <div class="subject-text" style="font-size: 3.5rem; font-weight: bold; color: #BC8F8F;">{cur}</div>
            <div style="font-size: 1.8rem; color: #888;">{rng}</div>
        </div>
    </div>

    <div class="content-grid">
        <div class="card">
            <b style="color: #BC8F8F; font-size: 1.5rem;">📅 今日考程表</b><hr>
"""

for i, x in enumerate(sch):
    bg = "background:#A3B18A; color:#fff; border-radius:10px;" if i == hi else "border-bottom:1px solid #eee;"
    html += f'<div style="{bg} padding:12px; display:flex; justify-content:space-between; font-size:1.2rem; margin-bottom:5px;"><span>{x["n"]}</span><span>{x["s"]}-{x["e"]}</span></div>'

html += f"""
        </div>
        <div class="card" style="text-align:center; flex: 1.5 1 450px;">
            <b style="color: #BC8F8F; letter-spacing: 10px; font-size: 1.5rem;">考 場 規 範</b>
            <h1 style="margin: 30px 0; font-size: 3.5rem;">🚫 考完請在位靜候<br><small style="font-size: 2rem; color: #666;">等監考老師收完卷</small></h1>
            <div class="status-box">
                <div><small>應到</small><br><b style="font-size: 3rem;">{st.session_state.t}</b></div>
                <div style="border-left: 1px solid #ddd; padding-left: 10px;"><small>實到</small><br><b style="font-size: 3rem;">{st.session_state.p}</b></div>
                <div style="border-left: 1px solid #ddd; padding-left: 10px;"><small>缺席</small><br><b style="font-size: 3rem; color: #BC8F8F;">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
time.sleep(1)
st.rerun()
