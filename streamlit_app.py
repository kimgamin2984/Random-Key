import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import pytz
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="🎸 랜덤 키 생성기 🎵", layout="wide")

# 2. 쿠키 매니저
if "cookie_manager" not in st.session_state:
    st.session_state.cookie_manager = stx.CookieManager()
cookie_manager = st.session_state.cookie_manager

# 3. 데이터 로드 및 초기화
seoul_tz = pytz.timezone('Asia/Seoul')
today = datetime.now(seoul_tz).strftime('%Y-%m-%d')
keylist = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'B', 'E', 'A', 'D', 'G']

if "daily_data" not in st.session_state:
    time.sleep(0.1)
    saved_cookie = cookie_manager.get(cookie="daily_quests")
    if saved_cookie and isinstance(saved_cookie, dict) and saved_cookie.get("date") == today:
        st.session_state.daily_data = saved_cookie["tasks"]
    else:
        st.session_state.daily_data = {k: False for k in keylist}

if "current_key" not in st.session_state:
    st.session_state.current_key = None

# --- [수정] 토스트 알림을 위한 초기화 로직 ---
def reset_all_records():
    st.session_state.daily_data = {k: False for k in keylist}
    st.session_state.current_key = None
    
    # KeyError 방지 및 쿠키 삭제
    try:
        all_cookies = cookie_manager.get_all()
        if "daily_quests" in all_cookies:
            cookie_manager.delete("daily_quests")
    except:
        pass
    
    # 토스트를 띄우기 위한 플래그 설정
    st.session_state.show_toast = True

# --- UI 레이아웃 ---
st.markdown("<h1 style='text-align: center;'>🎸 랜덤 키 생성기 🎵</h1>", unsafe_allow_html=True)

# 페이지 리런 시 토스트 띄우기
if st.session_state.get("show_toast"):
    st.toast("기록이 초기화되었습니다. 🔄")
    st.session_state.show_toast = False

# 사이드바
with st.sidebar:
    st.header("📊 오늘 달성도")
    done_count = list(st.session_state.daily_data.values()).count(True)
    st.progress(done_count / 12)
    st.write(f"**진행률: {done_count} / 12**")
    st.divider()
    
    cols = st.columns(2)
    for i, k in enumerate(keylist):
        status = "✅" if st.session_state.daily_data.get(k) else "⬜"
        cols[i % 2].write(f"{status} {k}")
    
    st.button("🔄 기록 초기화", on_click=reset_all_records, use_container_width=True)

# 메인 로직
remaining_keys = [k for k in keylist if not st.session_state.daily_data[k]]
current_key = st.session_state.current_key

c1, c2 = st.columns(2)
with c1:
    if st.button("🎲 랜덤 키 뽑기", use_container_width=True):
        st.session_state.current_key = random.choice(remaining_keys if remaining_keys else keylist)
        st.rerun()

with c2:
    if current_key:
        if st.button(f"🚩 {current_key} 완료!", type="primary", use_container_width=True):
            st.session_state.daily_data[current_key] = True
            cookie_manager.set(
                "daily_quests",
                {"date": today, "tasks": st.session_state.daily_data},
                key=f"save_{current_key}_{int(time.time())}",
                expires_at=datetime.now() + timedelta(days=1)
            )
            st.session_state.current_key = None
            st.rerun()

if current_key:
    is_done = st.session_state.daily_data.get(current_key, False)
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 50px; border-radius: 20px; text-align: center; border: 3px solid #ff4b4b; margin-top: 20px;">
            <p style="font-size: 20px; color: #666;">지금 연습할 키 { '(이미 완료)' if is_done else '' }</p>
            <h1 style="font-size: 100px; color: #ff4b4b; margin: 0;">{current_key}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if not remaining_keys and not is_done:
        st.balloons()