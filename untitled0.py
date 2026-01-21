import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 2. 側邊欄：人數即時修正功能 ---
# 使用 session_state 確保重新整理時數字不會跳掉
if 'total' not in st.session_state:
    st.session_state.total = 30
if 'present' not in st.session_state:
    st.session_state.present = 30

st.sidebar.header("📝 人數即時修正")
st.session_state.total = st.sidebar.number_input("應到人數", value=st.session_state.total, step=1)
st.session_state.present = st.sidebar.number_input("實到人數", value=st.session_state.present, step=1)

# 自動計算缺席人數
absent = st.session_state.total - st.session_state.present

# --- 3. 時間與課表判斷邏輯 ---
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz)
current_hm = now.strftime("%H:%M")

# 你可以隨時在這裡修改課表時間
schedule = [
    {"name": "第一節：自修", "start": "08:25", "end": "09:10"},
    {"name": "第二節：寫作", "start": "09:20", "end": "10:05"},
    {"name": "第三節：自修", "start": "10:15", "end": "11:00"},
    {"name": "第四節：數學", "start": "11:10", "end": "11:55"},
    {"name": "第五節：英文", "start": "13:10", "end": "15:00"},
    {"name": "第六節：社會", "start": "15:10", "end": "16:10"},
]

current_period = "休息時間"
current_range = "-- : --"
highlight_idx = -1

for i, item in enumerate(schedule):
    if item["start"] <= current_hm <= item["end"]:
        current_period = item["name"]
        current_range = f"{item['start']} - {item['end']}"
        highlight_idx = i
        break

# --- 4. 奶茶色美感 HTML 樣式注入 ---
html_template = f"""
<style>
    /* 強制修改 Streamlit 預設背景 */
    .stApp {{ background-color: white; }}
    /* 全域字體設定 */
    * {{ font-family: "Microsoft JhengHei", "Heiti TC", sans-serif; }}
</style>

<div style="background-color: #FDF5E6; padding: 40px; border-radius: 30px; color: #5D5D5D; max-width: 1200px
