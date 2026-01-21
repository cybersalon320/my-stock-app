import streamlit as st
from datetime import datetime
import pytz
import time

# 1. 介面配置與人數修正
st.set_page_config(page_title="考試看板", layout="wide")
if 't' not in st.session_state: st.session_state.t = 30
if 'p' not in st.session_state: st.session_state.p = 30

st.sidebar.header("📝 人數修正")
st.session_state.t = st.sidebar.number_input("應到", value=st.session_state.t, step=1)
st.session_state.p = st.sidebar.number_input("實到", value=st.session_state.p, step=1)
absent = st.session_state.t - st.session_state.p

# 2. 時間與課表
now = datetime.now(pytz.timezone('Asia/Taipei'))
hm = now.strftime("%H:%M")
sch = [
    {"n": "第一節：自修", "s": "08:25", "e": "09:10"},
    {"n": "第二節：寫作", "s": "09:20", "e": "10:05"},
    {"n": "第三節：自修", "s": "10:15", "e": "11:00"},
    {"n": "第四節：數學", "s": "11:10", "e": "11:55"},
    {"n": "第五節：英文", "s": "13:10", "e": "15:00"},
    {"n": "第六節：社會", "s": "15:10", "e": "16:10"},
]
cur, rng, hi = "休息時間", "--:--", -1
for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]: cur, rng, hi = x["n"], f"{x['s']}-{x['e']}", i

# 3. 渲染美感畫面
html = f"""
<style>.stApp {{ background:#fff; }}</style>
<div style="background:#FDF5E6; padding:30px; border-radius:20px; font-family:sans-serif; color:#5D5D5D;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <div><small style="color:#BC8F8F; font-weight:bold;">當 前 時 間</small><br><b style="font-size:80px;">{now.strftime("%H:%M:%S")}</b></div>
        <div style="background:#fff; padding:20px; border-radius:15px; text-align:right;">
            <b style="font-size:40px; color:#BC8F8F;">{cur}</b><br><span style="color:#888;">{rng}</span>
        </div>
    </div>
    <div style="display:flex; gap:20px;">
        <div style="background:#fff; padding:20px; border-radius:15px; flex:1;">
            <b style="color:#BC8F8F; font-size:20px;">📅 今日考程</b><hr>
"""
for i, x in enumerate(sch):
    bg = "background:#A3B18A; color:#fff; border-radius:8px;" if i == hi else "border-bottom:1px solid #eee;"
    html += f'<div style="{bg} padding:10px; display:flex; justify-content:space-between;"><span>{x["n"]}</span><span>{x["s"]}-{x["e"]}</span></div>'

html += f"""
        </div>
        <div style="background:#fff; padding:20px; border-radius:15px; flex:1.5; text-align:center;">
            <b style="color:#BC8F8F; letter-spacing:10px;">考 場 規 範</b>
            <h2 style="margin:30px 0;">🚫 考完請在位靜候<br><small style="color:#666;">等監考老師收完卷</small></h2>
            <div style="display:flex; justify-content:space-around; background:#FDF5E6; padding:15px; border-radius:10px;">
                <div><small>應到</small><br><b style="font-size:30px;">{st.session_state.t}</b></div>
                <div><small>實到</small><br><b style="font-size:30px;">{st.session_state.p}</b></div>
                <div><small>缺席</small><br><b style="font-size:30px; color:#BC8F8F;">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
time.sleep(1)
st.rerun()
