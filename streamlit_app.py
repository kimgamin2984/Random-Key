import streamlit as st
import extra_streamlit_components as stx
from datetime import date

# 1. 쿠키 매니저 초기화
st_common = stx.CookieManager()

st.title("📅 오늘의 일퀘 리스트")
today = str(date.today())

# 2. 쿠키 가져오기
saved_data = st_common.get(cookie="daily_quests")

# [중요] 쿠키를 아직 못 불러왔다면(None), 여기서 실행을 잠시 멈춤
if saved_data is None:
    st.info("데이터를 불러오는 중입니다...")
    st.stop()  # 데이터 올 때까지 아래 코드 실행 안 함

# 3. 데이터 초기화 로직 (날짜가 바뀌었거나 데이터가 비었을 때)
if not saved_data or saved_data.get("date") != today:
    saved_data = {
        "date": today, 
        "tasks": {k: False for k in ['C','F','Bb','Eb','Ab','Db','Gb','B','E','A','D','G']}
    }

st.subheader(f"오늘의 할 일: {today}")

# 4. 퀘스트 UI
updated_tasks = {}
# 순서 고정을 위해 keylist 기준으로 반복
keylist = ['C','F','Bb','Eb','Ab','Db','Gb','B','E','A','D','G']
for task in keylist:
    # saved_data에 해당 키가 없을 경우를 대비해 .get(task, False) 사용
    done = saved_data["tasks"].get(task, False)
    is_completed = st.checkbox(task, value=done, key=f"chk_{task}")
    updated_tasks[task] = is_completed

# 5. 변경사항 저장
if st.button("저장하기"):
    saved_data["tasks"] = updated_tasks
    # 쿠키 저장
    st_common.set("daily_quests", saved_data, key="save_logic")
    st.success("브라우저에 저장 완료! 새로고침해도 유지됩니다.")