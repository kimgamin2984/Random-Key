import streamlit as st
from datetime import datetime
import pytz
import random

# 1. 페이지 설정
st.set_page_config(page_title="🎸 랜덤 키 생성기 🎵", layout="wide")

# 2. 상수 및 날짜 설정
seoul_tz = pytz.timezone('Asia/Seoul')
today = datetime.now(seoul_tz).strftime('%Y-%m-%d')
keylist = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'B', 'E', 'A', 'D', 'G']

# 3. [저장 방식 변경] URL 파라미터 로드
params = st.query_params
url_date = params.get("date", "")

if "daily_data" not in st.session_state:
    # 날짜가 같으면 URL에서 데이터 복구, 다르면 초기화
    if url_date == today:
        done_str = params.get("done", "")
        done_keys = done_str.split(",") if done_str else []
        st.session_state.daily_data = {k: (k in done_keys) for k in keylist}
    else:
        st.session_state.daily_data = {k: False for k in keylist}

if "current_key" not in st.session_state:
    st.session_state.current_key = None

# 4. [기능] 완료 및 저장 함수
def complete_and_save(key):
    st.session_state.daily_data[key] = True
    # URL 파라미터 업데이트 (쿠키 대신 저장)
    done_list = [k for k, v in st.session_state.daily_data.items() if v]
    st.query_params.update(done=",".join(done_list), date=today)
    st.session_state.current_key = None

# 5. [기능] 초기화 함수
def reset_all_records():
    st.session_state.daily_data = {k: False for k in keylist}
    st.session_state.current_key = None
    st.query_params.clear()
    st.toast("기록이 초기화되었습니다.")

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
    
    st.button("🔄 기록 초기화", on_click=reset_all_records, use_container_width=True)

# --- 메인 화면 ---
st.markdown("""
    <h1 style="text-align: center;">🎸 랜덤 키 생성기 🎵</h1>
    """, unsafe_allow_html=True)

# [원래 로직 유지] 아직 완료하지 않은 키 필터링
remaining_keys = [k for k in keylist if not st.session_state.daily_data[k]]

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎲 랜덤 키 뽑기", use_container_width=True):
        # [원래 핵심 로직]
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