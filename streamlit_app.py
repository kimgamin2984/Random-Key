import streamlit as st
import extra_streamlit_components as stx
from datetime import date

keylist = ['C','F','Bb','Eb','Ab','Db','Gb','B','E','A','D','G']

st.title("📅 오늘의 일퀘 리스트")

today = str(date.today())
st_common = stx.CookieManager()
st.title('a')
# 로컬 스토리지에서 기존 데이터 가져오기 (JSON 형태 저장)
saved_data = st_common.get(cookie="daily_quests") or {}

# 날짜가 바뀌었으면 초기화 로직 (선택 사항)
if saved_data.get("date") != today:
    saved_data = {"date": today, "tasks": {"C": False, "F": False, "Bb": False, "Eb": False, "Ab": False, "Db": False, "Gb": False, "B": False, "E": False, "A": False, "D": False, "G": False}}

# 2. 퀘스트 UI 출력 및 상태 업데이트
st.subheader(f"오늘의 할 일: {today}")

updated_tasks = {}
for task, done in saved_data["tasks"].items():
    # 체크박스로 상태 변경
    is_completed = st.checkbox(task, value=done, key=task)
    updated_tasks[task] = is_completed

# 3. 변경사항 저장
if st.button("저장하기"):
    saved_data["tasks"] = updated_tasks
    st_common.set("daily_quests", saved_data, key="save_logic")
    st.success("브라우저에 저장 완료! 내일 와도 유지됩니다.")