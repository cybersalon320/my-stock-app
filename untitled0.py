import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 2. 側邊欄：人數即時修正功能 ---
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
# 注意：這裡就是報錯的地方，請務必確保從 f""" 到最後的 """ 都有複製到
html_template = f"""
<style>
    .stApp {{ background-color: white; }}
    * {{ font-family: "Microsoft JhengHei", "Heiti TC", sans-serif; }}
</style>

<div style="background-color: #FDF5E6; padding: 40px; border-radius: 30px; color: #5D5D5D; max-width: 1200px; margin: auto;">
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
        <div>
            <div style="font-size: 20px; font-weight: bold; letter-spacing: 4px; color: #BC8F8F;">當 前 時 間</div>
            <div style="font-size: 100px; font-weight: bold; line-height: 1; margin-top: 10px; color: #5D5D5D;">{now.strftime("%H:%M:%S")}</div>
        </div>
        
        <div style="text-align: right; background: white; padding: 25px 45px; border-radius: 25px; box-shadow: 5px 5px 15px rgba(0,0,0,0.02);">
            <div style="font-size: 56px; font-weight: bold; color: #BC8F8F; margin-bottom: 5px;">{current_period}</div>
            <div style="font-size: 32px; color: #888; font-weight: 500;">{current_range}</div>
        </div>
    </div>

    <div style="display: flex; gap: 30px;">
        <div style="background: white; padding: 35px; border-radius: 25px; flex: 1; box-shadow: 5px 5px 20px rgba(0,0,0,0.03);">
            <h3 style="color: #BC8F8F; margin: 0 0 20px 0; border-bottom: 2px solid #FDF5E6; padding-bottom: 15px; font-size: 28px;">📅 今日考程表</h3>
