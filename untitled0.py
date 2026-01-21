import streamlit as st
from datetime import datetime, timedelta
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

# --- 3. 時間與變色邏輯 ---
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz)
hm = now.strftime("%H:%M")

cur, rng, hi = "休息時間", "--:--", -1
is_urgent = False  # 是否進入最後10分鐘

for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']}-{x['e']}", i
        
        # 計算距離結束還有幾分鐘
        end_time = datetime.strptime(x["e"], "%H:%M").replace(year=now.year, month=now.month, day=now.day, tzinfo=tw_tz)
        time_diff = (end_time - now).total_seconds() / 60
        
        # 如果剩下不到 10 分鐘且大於 0 分鐘，開啟緊急模式
        if 0 <= time_diff <= 10:
            is_urgent = True
        break

# 設定顏色：緊急時用紅色 (#E63946)，平時用深灰色 (#5D5D5D) 或奶茶主題色 (#BC8F8F)
timer_color = "#E63946" if is_urgent else "#5D5D5D"
subject_color = "#E63946" if is_urgent else "#BC8F8F"

# --- 4. 響應式 HTML 樣式 ---
html = f"""
<style>
    .stApp {{ background:#fff; }}
    .main-container {{ background: #FDF5E6; padding: 2vw; border-radius: 30px; color: #5D5D5D; width: 95%; margin: auto; }}
    .header-box {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 20px; gap: 20px; }}
    .content-grid {{ display: flex; flex-wrap: wrap; gap: 20px; }}
    .card {{ background: white; padding: 25px; border-radius: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.02); flex: 1 1 350px; }}
    .status-box {{ display: flex; justify-content: space-around; background: #FDF5E6; padding: 15px; border-radius: 15px; margin-top: 20px; flex-wrap: wrap; }}
    
    /* 動態顏色類別 */
    .timer-text {{ color: {timer_color}; transition: color 0.5s; }}
    .subject-highlight {{ color: {subject_color}; transition: color 0.5s; }}

    @media (max-width: 600px) {{
        .time-display {{ font-size: 60px !important; }}
        .subject-display {{ font-size: 35px !important; }}
    }}
</style>

<div class="main-container">
    <div class="header-box">
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #BC8F8F;">{"⚠️ 考時將屆" if is_urgent else "當 前 時 間"}</div>
            <div class="timer-text time-display" style="font-size: 6rem; font-weight: bold; line-height: 1;">{now.strftime("%H:%M:%S")}</div>
        </div>
        <div style="background: white; padding: 20px 40px; border-radius: 20px; text-align: right; border: {"3px solid #E
