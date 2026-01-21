import streamlit as st
from datetime import datetime, timedelta
import pytz
import time

# --- 1. 基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 2. 側邊欄設定 ---
st.sidebar.header("📝 考場設定")

if 't' not in st.session_state: st.session_state.t = 30
if 'p' not in st.session_state: st.session_state.p = 30
st.session_state.t = st.sidebar.number_input("應到人數", value=st.session_state.t, step=1)
st.session_state.p = st.sidebar.number_input("實到人數", value=st.session_state.p, step=1)
absent = st.session_state.t - st.session_state.p

st.sidebar.markdown("---")
# 手動輸入課表
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
    st.sidebar.error("格式有誤，請檢查逗號或橫槓")

# --- 3. 時間與變色邏輯 ---
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz)
hm = now.strftime("%H:%M")

cur, rng, hi = "休息時間", "-- : --", -1
is_urgent = False 

for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']} - {x['e']}", i
        # 判斷結束前 10 分鐘
        try:
            end_dt = datetime.strptime(x["e"], "%H:%M").replace(year=now.year, month=now.month, day=now.day, tzinfo=tw_tz)
            remain = (end_dt - now).total_seconds() / 60
            if 0 < remain <= 10: is_urgent = True
        except: pass
        break

# 顏色定義
warn_red = "#E63946"
theme_brown = "#BC8F8F"
time_color = warn_red if is_urgent else "#5D5D5D"
box_border = f"3px solid {warn_red}" if is_urgent else "none"
subj_color = warn_red if is_urgent else theme_brown

# --- 4. 渲染美感看板 ---
html_output = f"""
<style>
    .stApp {{ background-color: white; }}
    .main-board {{
        background-color: #FDF5E6;
        padding: 30px;
        border-radius: 25px;
        color: #5D5D5D;
        font-family: sans-serif;
        min-width: 900px;
        margin: auto;
    }}
</style>

<div class="main-board">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div>
            <div style="font-size: 20px; font-weight: bold; color: {theme_brown};">
                {"⚠️ 考試即將結束" if is_urgent else "當 前 時 間"}
            </div>
            <div style="font-size: 90px; font-weight: bold; color: {time_color}; line-height: 1;">
                {now.strftime("%H:%M:%S")}
            </div>
        </div>
        <div style="background: white; padding: 20px 40px; border-radius: 20px; text-align: right; border: {box_border};">
            <div style="font-size: 45px; font-weight: bold; color: {subj_color};">
                {cur}
            </div>
            <div style="font-size: 24px; color: #888;">{rng}</div>
        </div>
    </div>

    <div style="display: flex; gap: 20px;">
        <div style="background: white; padding: 25px; border-radius: 20px; flex: 1;">
            <b style="color: {theme_brown}; font-size: 22px;">📅 今日考程表</b><hr style="border: 0.5px solid #FDF5E6;">
"""

for i, x in enumerate(sch):
    row_bg = "background: #A3B18A; color: white; border-radius: 10px;" if i == hi else "border-bottom: 1px solid #eee;"
    html_output += f'<div style="{row_bg} padding: 12px; display: flex; justify-content: space-between; font-size: 18px; margin-top: 5px;"><span>{x["n"]}</span><span>{x["s"]} - {x["e"]}</span></div>'

html_output += f"""
        </div>
        <div style="background: white; padding: 25px; border-radius: 20px; flex: 1.5; text-align: center;">
            <b style="color: {theme_brown}; letter-spacing: 10px; font-size: 20px;">考 場 規 範</b>
            <h1 style="font-size: 48px; margin: 35px 0;">🚫 考完請在位靜候<br><span style="font-size: 32px; color: #666;">等監考老師收完卷</span></h1>
            <div style="display: flex; justify-content: space-around; background: #FDF5E6; padding: 20px; border-radius: 15px;">
                <div><small>應到</small><br><b style="font-size: 45px;">{st.session_state.t}</b></div>
                <div><small>實到</small><br><b style="font-size: 45px;">{st.session_state.p}</b></div>
                <div><small>缺席</small><br><b style="font-size: 45px; color: {warn_red if absent > 0 else "#5D5D5D"};">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
"""

st.markdown(html_output, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
