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
# 讓你可以手動輸入考程
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

cur, rng, hi = "休息時間", "--:--", -1
is_urgent = False 

for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']}-{x['e']}", i
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

# --- 4. 渲染美感看板 (使用固定寬度避錯) ---
# 注意：這裡使用 f""" 開頭，務必確保結尾有 """
html_output = f"""
<style>
    .stApp {{ background-color: white; }}
    .main-board {{
        background-color: #FDF5E6;
        padding: 30px;
        border-radius: 25px;
        color: #5D5D5D;
        font-family: "Microsoft JhengHei", sans-serif;
        min-width: 900px;
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
        <div style="background: white; padding: 20px 40px; border-radius: 20px; text-align: right; border: {"3px solid "+warn_red if is_urgent else "none"};">
            <div style="font-size: 45px; font-weight: bold; color: {warn_red if is_urgent else theme_brown
