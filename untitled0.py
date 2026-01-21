import streamlit as st
from datetime import datetime
import pytz
import time

# 1. 基礎設定與人數修正 (側邊欄)
st.set_page_config(page_title="專業考場看板", layout="wide")
st.sidebar.header("📝 人數修正")

if 'total' not in st.session_state: st.session_state.total = 30
if 'present' not in st.session_state: st.session_state.present = 30

st.session_state.total = st.sidebar.number_input("應到人數", value=st.session_state.total, step=1)
st.session_state.present = st.sidebar.number_input("實到人數", value=st.session_state.present, step=1)
absent = st.session_state.total - st.session_state.present

# 2. 時間與課表
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

cur_p, cur_r, hi_idx = "休息時間", "-- : --", -1
for i, item in enumerate(schedule):
    if item["start"] <= current_hm <= item["end"]:
        cur_p, cur_r, hi_idx = item["name"], f"{item['start']} - {item['end']}", i
        break

# 3. 美感看板介面
html = f"""
<style> .stApp {{ background-color: white; }} </style>
<div style="background-color: #FDF5E6; padding: 40px; border-radius: 30px; font-family: sans-serif; color: #5D5D5D;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
        <div>
            <div style="font-size: 20px; font-weight: bold; color: #BC8F8F;">當 前 時 間</div>
            <div style="font-size: 100px; font-weight: bold;">{now.strftime("%H:%M:%S")}</div>
        </div>
        <div style="text-align: right; background: white; padding: 25px; border-radius: 20px;">
            <div style="font-size: 50px; font-weight: bold; color: #BC8F8F;">{cur_p}</div>
            <div style="font-size: 28px; color: #888;">{cur_r}</div>
        </div>
    </div>
    <div style="display: flex; gap: 20px;">
        <div style="background: white; padding: 30px; border-radius: 20px; flex: 1;">
            <h3 style="color: #BC8F8F; border-bottom: 2px solid #FDF5E6; padding-bottom: 10px;">📅 今日考程表</h3>
"""
for i, item in enumerate(schedule):
    style = "background:#A3B18A; color:white; border-radius:10px; padding:10px;" if i == hi_idx else "padding:10
