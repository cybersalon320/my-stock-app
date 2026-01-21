import streamlit as st
from datetime import datetime
import pytz

# --- 網頁設定 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 側邊欄：即時人數修正區 ---
st.sidebar.header("📝 人數即時修正")
if 'total' not in st.session_state:
    st.session_state.total = 30 # 初始應到
if 'present' not in st.session_state:
    st.session_state.present = 30 # 初始實到

# 使用數字選鈕，點一下就加減
st.session_state.total = st.sidebar.number_input("應到人數", value=st.session_state.total)
st.session_state.present = st.sidebar.number_input("實到人數", value=st.session_state.present)
absent = st.session_state.total - st.session_state.present

# --- 考程邏輯 (含下午時段) ---
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz)
current_hm = now.strftime("%H:%M")

schedule = [
    {"name": "第一節：自修", "start": "08:25", "end": "09:10"},
    {"name": "第二節：寫作", "start": "09:20", "end": "10:05"},
    {"name": "第三節：自修", "start": "10:15", "end": "11:00"},
    {"name": "第四節：數學", "start": "11:10", "end": "11:55"},
    {"name": "第五節：英文", "start": "13:10", "end": "14:40"}, # 現在時間會中！
]

current_period = "休息時間"
for item in schedule:
    if item["start"] <= current_hm <= item["end"]:
        current_period = item["name"]

# --- 畫面顯示 (這裡可以用美美的介面) ---
st.title(f"⏰ 當前時間：{now.strftime('%H:%M:%S')}")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📅 今日考程")
    for item in schedule:
        if item["name"] == current_period:
            st.success(f"**{item['name']} ({item['start']}-{item['end']})**")
        else:
            st.write(f"{item['name']} ({item['start']}-{item['end']})")

with col2:
    st.info(f"🚩 當前考科：{current_period}")
    st.warning("🚫 考完請在位靜候，等監考老師收完卷。")
    
    # 底部人數大看板
    c1, c2, c3 = st.columns(3)
    c1.metric("應到", st.session_state.total)
    c2.metric("實到", st.session_state.present)
    c3.metric("缺席", absent, delta="- 缺席" if absent > 0 else None, delta_color="inverse")
