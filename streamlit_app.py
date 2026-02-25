import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime
import pytz
import random

# 1. 페이지 설정
st.set_page_config(page_title="🎸 랜덤 키 생성기 🎵", layout="wide")

# 2. 쿠키 매니저
with st.sidebar:
    cookie_manager = stx.CookieManager()

# 3. 상수 및 날짜 설정
seoul_tz = pytz.timezone('Asia/Seoul')
today = datetime.now(seoul_tz).strftime('%Y-%m-%d')
keylist = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'B', 'E', 'A', 'D', 'G']

# 4. 데이터 로드
saved_cookie = cookie_manager.get(cookie="daily_quests")

if "daily_data" not in st.session_state:
    if saved_cookie and isinstance(saved_cookie, dict) and saved_cookie.get("date") == today:
        st.session_state.daily_data = saved_cookie["tasks"]
    else:
        st.session_state.daily_data = {k: False for k in keylist}

# 5. 초기화 함수 (데이터 기록만 삭제)
def reset_all_records():
    st.session_state.daily_data = {k: False for k in keylist}
    st.session_state.current_key = None
    try:
        cookie_manager.delete("daily_quests")
    except:
        pass
    st.toast("기록이 초기화되었습니다.")

# 6. 완료 및 저장 함수
def complete_and_save(key):
    st.session_state.daily_data[key] = True
    cookie_manager.set(
        "daily_quests",
        {"date": today, "tasks": st.session_state.daily_data},
        key=f"save_{key}_{datetime.now().timestamp()}"
    )
    st.session_state.current_key = None

# --- 사이드바 ---
with st.sidebar:
    st.header("📊 오늘 달성도")
    current_tasks = st.session_state.daily_data
    done_count = list(current_tasks.values()).count(True)
    
    st.progress(done_count / 12)
    st.write(f"**진행률: {done_count} / 12**")
    
    st.divider()
    for k in keylist:
        status = "✅" if current_tasks.get(k) else "⬜"
        st.write(f"{status} {k} Key")
    
    # 별도의 기록 초기화 버튼
    st.button("🔄 기록 초기화", on_click=reset_all_records, use_container_width=True)

# --- 메인 화면: 랜덤 로직 설계 ---
st.markdown("""
    <h1 style="text-align: center;">🎸 랜덤 키 생성기 🎵</h1>
    """, unsafe_allow_html=True)

# 아직 완료하지 않은 키 필터링
remaining_keys = [k for k in keylist if not st.session_state.daily_data[k]]

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎲 랜덤 키 뽑기", use_container_width=True):
        # [핵심 로직]
        if remaining_keys:
            # 1. 12개를 다 채우기 전까지는 중복 없는 랜덤
            st.session_state.current_key = random.choice(remaining_keys)
        else:
            # 2. 12개를 다 채운 후에는 완전 랜덤 (무한 모드)
            st.session_state.current_key = random.choice(keylist)

with col2:
    current_key = st.session_state.get("current_key")
    if current_key:
        if st.button(f"🚩 {current_key} 완료!", type="primary", use_container_width=True):
            complete_and_save(current_key)
            st.rerun()

# 중앙 UI
if current_key:
    # 12개 완료 후 무한 모드일 때 이미 완료했는지 체크만 표시
    is_already_done = st.session_state.daily_data.get(current_key, False)
    badge = " (이미 완료함)" if is_already_done else ""
    
    # 12개 완주 시점에 축하 멘트 추가
    if not remaining_keys and not is_already_done:
        st.balloons()
        st.success("🎉 오늘 12키를 모두 완주하셨습니다! 이제부터는 완전 랜덤 모드입니다.")

    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 60px;
            border-radius: 20px;
            text-align: center;
            margin-top: 20px;
            border: 3px solid #ff4b4b;
        ">
            <p style="color: #555; font-size: 20px; margin-bottom: 10px;">지금 연습할 키는{badge}</p>
            <h1 style="font-size: 100px; color: #ff4b4b; margin: 0;">{current_key}</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    if not remaining_keys:
        st.success("✨ 1회차 완주 성공! 계속해서 완전 랜덤으로 연습할 수 있습니다.")