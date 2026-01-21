import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# 這裡使用特殊的雙大括號 {{ }} 來避開 Python 語法衝突
st.markdown("""
<style>
    div.block-container { padding-top: 2rem; }
    .stApp { background-color: white; }
    .main-board {
        background-color: #FDF5E6;
        padding: 40px;
        border-radius: 30px;
        color: #5D5D5D;
        font-family: sans-serif;
        min-width: 900px;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 側邊欄設定 ---
st.sidebar.header("📝 考場設定")
t_num = st.sidebar.number_input("應到人數", value=30, step=1)
p_num = st.sidebar.number_input("實到人數", value=30, step=1)
absent = t_num - p_num

st.sidebar.markdown("---")
default_sch = """第一節：自修, 08:25-09:10
第二節：寫作, 09:20-10:05
第三節：自修, 10:15-11:00
第四節：數學, 11:10-11:55
第五節：英文, 13:10-15:00
第六節：社會, 15:10-16:10"""
raw_input = st.sidebar.text_area("📅 手動輸入考程 (科目, 開始-結束)", value=default_sch, height=200)

# 解析課表
sch = []
try:
    for line in raw_input.strip().split('\n'):
        if ',' in line:
            name, times = line.split(',')
            s, e = times.strip().split('-')
            sch.append({"n": name.strip(), "s": s.strip(), "e": e.strip()})
except:
    st.sidebar.error("格式錯誤")

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

# 定義動態顏色
warn_red = "#E63946"
theme_brown = "#BC8F8F"
time_color = warn_red if is_urgent else "#5D5D5D"
box_border = f"3px solid {warn_red}" if is_urgent else "none"
subj_color = warn_red if is_urgent else theme_brown

# --- 4. 渲染畫面 ---

# 組合考程清單的 HTML
list_items = ""
for i, x in enumerate(sch):
    bg = "#A3B18A" if i == hi else "transparent"
    color = "white" if i == hi else "#555"
    border = "none" if i == hi else "1px solid #eee"
    list_items += f"""
    <div style="background: {bg}; color: {color}; border-radius: 12px; padding: 15px; display: flex; justify-content: space-between; font-size: 20px; margin-bottom: 8px; border-bottom: {border};">
        <span>{x['n']}</span><span>{x['s']} - {x['e']}</span>
    </div>
    """

# 最終 HTML 輸出
full_html = f"""
<div class="main-board">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <div>
            <div style="font-size: 22px; font-weight: bold; color: {theme_brown};">
                {"⚠️ 考試即將結束" if is_urgent else "當 前 時 間"}
            </div>
            <div style="font-size: 100px; font-weight: bold; color: {time_color}; line-height: 1;">
                {now.strftime("%H:%M:%S")}
            </div>
        </div>
        <div style="background: white; padding: 25px 50px; border-radius: 25px; text-align: right; border: {box_border}; box-shadow: 2px 2px 15px rgba(0,0,0,0.02);">
            <div style="font-size: 50px; font-weight: bold; color: {subj_color};">{cur}</div>
            <div style="font-size: 26px; color: #888;">{rng}</div>
        </div>
    </div>

    <div style="display: flex; gap: 30px;">
        <div style="background: white; padding: 30px; border-radius: 25px; flex: 1; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <div style="color: {theme_brown}; font-size: 24px; font-weight: bold; margin-bottom: 15px;">📅 今日考程表</div>
            <div style="border-top: 2px solid #FDF5E6; padding-top: 10px;">
                {list_items}
            </div>
        </div>

        <div style="background: white; padding: 30px; border-radius: 25px; flex: 1.6; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <div style="color: {theme_brown}; letter-spacing: 12px; font-size: 22px; font-weight: bold; margin-bottom: 20px;">考 場 規 範</div>
            <div style="margin: 40px 0;">
                <span style="font-size: 60px; font-weight: bold; color: #333;">🚫 考完請在位靜候</span><br>
                <span style="font-size: 36px; color: #666;">等監考老師收完卷</span>
            </div>
            <div style="display: flex; justify-content: space-around; background: #FDF5E6; padding: 25px; border-radius: 20px; margin-top: 30px;">
                <div style="flex: 1;"><small style="color: #888;">應到</small><br><b style="font-size: 55px;">{t_num}</b></div>
                <div style="flex: 1; border-left: 2px solid #ddd;"><small style="color: #888;">實到</small><br><b style="font-size: 55px;">{p_num}</b></div>
                <div style="flex: 1; border-left: 2px solid #ddd;"><small style="color: #888;">缺席</small><br><b style="font-size: 55px; color: {warn_red if absent > 0 else "#333"};">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
"""

st.markdown(full_html, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
