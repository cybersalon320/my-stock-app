import streamlit as st
from datetime import datetime, timedelta
import pytz
import time

# --- 1. 基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# 強制移除 Streamlit 預設的上邊距，讓看板頂天立地
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

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
            parts = line.split(',')
            name = parts[0].strip()
            times = parts[1].strip().split('-')
            sch.append({"n": name, "s": times[0].strip(), "e": times[1].strip()})
except:
    st.sidebar.error("格式錯誤，請檢查逗號")

# --- 3. 時間與變色邏輯 ---
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz)
hm = now.strftime("%H:%M")

cur, rng, hi = "休息時間", "-- : --", -1
is_urgent = False 

for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']} - {x['e']}", i
        try:
            end_dt = datetime.strptime(x["e"], "%H:%M").replace(year=now.year, month=now.month, day=now.day, tzinfo=tw_tz)
            remain = (end_dt - now).total_seconds() / 60
            if 0 < remain <= 10: is_urgent = True
        except: pass
        break

# 顏色與樣式定義
warn_red = "#E63946"
theme_brown = "#BC8F8F"
time_color = warn_red if is_urgent else "#5D5D5D"
box_border = f"3px solid {warn_red}" if is_urgent else "none"

# --- 4. 渲染畫面 ---

# 使用一個大容器包住所有內容
st.markdown(f"""
<div style="background-color: #FDF5E6; padding: 40px; border-radius: 30px; font-family: sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <div>
            <div style="font-size: 22px; font-weight: bold; color: {theme_brown}; margin-bottom: 5px;">
                {"⚠️ 考試即將結束" if is_urgent else "當 前 時 間"}
            </div>
            <div style="font-size: 100px; font-weight: bold; color: {time_color}; line-height: 1;">
                {now.strftime("%H:%M:%S")}
            </div>
        </div>
        <div style="background: white; padding: 25px 50px; border-radius: 25px; text-align: right; border: {box_border}; box-shadow: 2px 2px 15px rgba(0,0,0,0.02);">
            <div style="font-size: 50px; font-weight: bold; color: {warn_red if is_urgent else theme_brown};">
                {cur}
            </div>
            <div style="font-size: 26px; color: #888;">{rng}</div>
        </div>
    </div>

    <div style="display: flex; gap: 30px;">
        <div style="background: white; padding: 30px; border-radius: 25px; flex: 1; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <div style="color: {theme_brown}; font-size: 24px; font-weight: bold; margin-bottom: 15px;">📅 今日考程表</div>
            <div style="border-top: 2px solid #FDF5E6; padding-top: 10px;">
                {"".join([f'<div style="background: {"#A3B18A" if i==hi else "transparent"}; color: {"white" if i==hi else "#555"}; border-radius: 12px; padding: 15px; display: flex; justify-content: space-between; font-size: 20px; margin-bottom: 8px; border-bottom: {"none" if i==hi else "1px solid #eee"};"><span>{x["n"]}</span><span>{x["s"]} - {x["e"]}</span></div>' for i, x in enumerate(sch)])}
            </div>
        </div>

        <div style="background: white; padding: 30px; border-radius: 25px; flex: 1.6; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <div style="color: {theme_brown}; letter-spacing: 12px; font-size: 22px; font-weight: bold; margin-bottom: 20px;">考 場 規 範</div>
            <div style="margin: 40px 0;">
                <span style="font-size: 60px; font-weight: bold; color: #333;">🚫 考完請在位靜候</span><br>
                <span style="font-size: 36px; color: #666;">等監考老師收完卷</span>
            </div>
            
            <div style="display: flex; justify-content: space-around; background: #FDF5E6; padding: 25px; border-radius: 20px; margin-top: 30px;">
                <div style="flex: 1;"><small style="font-size: 18px; color: #888;">應到</small><br><b style="font-size: 55px; color: #333;">{st.session_state.t}</b></div>
                <div style="flex: 1; border-left: 2px solid #ddd;"><small style="font-size: 18px; color: #888;">實到</small><br><b style="font-size: 55px; color: #333;">{st.session_state.p}</b></div>
                <div style="flex: 1; border-left: 2px solid #ddd;"><small style="font-size: 18px; color: #888;">缺席</small><br><b style="font-size: 55px; color: {warn_red if absent > 0 else "#333"};">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 每秒自動重新整理
time.sleep(1)
st.rerun()
