import streamlit as st
from datetime import datetime
import pytz
import time

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="專業考場看板", layout="wide")

# --- 2. 側邊欄：手動輸入區 ---
st.sidebar.header("📝 考場設定")

# 人數修正
if 't' not in st.session_state: st.session_state.t = 30
if 'p' not in st.session_state: st.session_state.p = 30
st.session_state.t = st.sidebar.number_input("應到人數", value=st.session_state.t, step=1)
st.session_state.p = st.sidebar.number_input("實到人數", value=st.session_state.p, step=1)
absent = st.session_state.t - st.session_state.p

st.sidebar.markdown("---")
# 課表輸入：預設範例文字
default_sch = """第一節：自修, 08:25-09:10
第二節：寫作, 09:20-10:05
第三節：自修, 10:15-11:00
第四節：數學, 11:10-11:55
第五節：英文, 13:10-15:00
第六節：社會, 15:10-16:10"""

st.sidebar.subheader("📅 手動輸入考程")
raw_input = st.sidebar.text_area("格式：科目, 開始-結束", value=default_sch, height=200)

# --- 3. 解析輸入的課表 ---
sch = []
try:
    for line in raw_input.strip().split('\n'):
        if ',' in line:
            name, times = line.split(',')
            s, e = times.strip().split('-')
            sch.append({"n": name.strip(), "s": s.strip(), "e": e.strip()})
except:
    st.sidebar.error("課表格式錯誤，請檢查逗號或橫槓！")

# --- 4. 時間與課表邏輯 ---
now = datetime.now(pytz.timezone('Asia/Taipei'))
hm = now.strftime("%H:%M")
cur, rng, hi = "休息時間", "--:--", -1

for i, x in enumerate(sch):
    if x["s"] <= hm <= x["e"]:
        cur, rng, hi = x["n"], f"{x['s']}-{x['e']}", i
        break

# --- 5. 渲染美感畫面 ---
html = f"""
<style>.stApp {{ background:#fff; }}</style>
<div style="background:#FDF5E6; padding:30px; border-radius:20px; font-family:sans-serif; color:#5D5D5D;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <div><small style="color:#BC8F8F; font-weight:bold;">當 前 時 間</small><br><b style="font-size:80px;">{now.strftime("%H:%M:%S")}</b></div>
        <div style="background:#fff; padding:20px 40px; border-radius:15px; text-align:right; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <b style="font-size:45px; color:#BC8F8F;">{cur}</b><br><span style="color:#888; font-size:24px;">{rng}</span>
        </div>
    </div>
    <div style="display:flex; gap:20px;">
        <div style="background:#fff; padding:25px; border-radius:15px; flex:1; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <b style="color:#BC8F8F; font-size:22px;">📅 今日考程</b><hr>
"""
for i, x in enumerate(sch):
    bg = "background:#A3B18A; color:#fff; border-radius:8px;" if i == hi else "border-bottom:1px solid #eee;"
    html += f'<div style="{bg} padding:12px; display:flex; justify-content:space-between; font-size:18px;"><span>{x["n"]}</span><span>{x["s"]}-{x["e"]}</span></div>'

html += f"""
        </div>
        <div style="background:#fff; padding:25px; border-radius:15px; flex:1.5; text-align:center; box-shadow: 2px 2px 10px rgba(0,0,0,0.02);">
            <b style="color:#BC8F8F; letter-spacing:10px; font-size:20px;">考 場 規 範</b>
            <h1 style="margin:30px 0; font-size:48px;">🚫 考完請在位靜候<br><small style="color:#666; font-size:32px;">等監考老師收完卷</small></h1>
            <div style="display:flex; justify-content:space-around; background:#FDF5E6; padding:20px; border-radius:15px;">
                <div><small style="font-weight:bold;">應到</small><br><b style="font-size:45px;">{st.session_state.t}</b></div>
                <div><small style="font-weight:bold;">實到</small><br><b style="font-size:45px;">{st.session_state.p}</b></div>
                <div><small style="font-weight:bold;">缺席</small><br><b style="font-size:45px; color:#BC8F8F;">{absent}</b></div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
time.sleep(1)
st.rerun()
