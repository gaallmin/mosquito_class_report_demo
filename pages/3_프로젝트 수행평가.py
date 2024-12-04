import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["user_database"]
users_collection = db["student"]
feedback_collection = db["teacher_feedbacks"] 

# Streamlit 앱 제목
st.title("Part III. 모기와 기후 데이터 분석 수행 평가")
st.write('본 파트에서는 수업의 목적에 맞는 데이터 분석을 잘 이해했는지를 확인합니다. 주어진 예시 데이터를 바탕으로 올바른 해석을 제시하세요😃')

st.write("---")

# 예시 데이터프레임
sample_data = {
    "date": ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04"],
    "temperature": [25.3, None, 27.8, 28.1],
    "humidity": [80, 85, None, 70],
    "mosquito_count": [15, 20, 30, None],
}
df = pd.DataFrame(sample_data)

# 데이터 샘플 표시
st.subheader("예시 데이터프레임")
st.write("""
아래는 모기 발생률과 기후 데이터를 포함한 예시 데이터프레임입니다.  
데이터는 `temperature` (기온), `humidity` (습도), `mosquito_count` (모기 발생 수)를 포함합니다.
""")
st.dataframe(df)
st.write("---")

# 데이터베이스에 저장 함수
def save_answer(question_number, answer):
    if not answer:
        st.error("답변을 입력해야 합니다!")
        return
    users_collection.update_one(
        {"student_id": st.session_state.get("student_id", "default")},
        {"$set": {f"q{question_number}_answer": answer}},
        upsert=True,
    )
    st.success(f"문제 {question_number} 답변이 성공적으로 저장되었습니다!")

# 문제 1
st.subheader("문제 1: 데이터 전처리 이해")
st.markdown("""
- 결측값(`None`)이 포함된 데이터를 적절히 처리하는 방법을 설명하세요.  
- `temperature`와 `mosquito_count` 열의 평균 값을 계산하는 코드를 작성하고 결과를 해석하세요.
""")
q1_answer = st.text_area("문제 1 답변을 작성하세요", key="q1_answer")
if st.button("문제 1 답변 제출"):
    save_answer(1, q1_answer)

st.write("---")

# 문제 2
st.subheader("문제 2: 데이터 시각화")
st.markdown("""
- `temperature`와 `mosquito_count` 간의 관계를 그래프로 표현하고, 해당 관계를 설명하세요.  
- 그래프 유형(예: scatter plot, line plot)을 선택한 이유를 작성하세요.
""")
q2_answer = st.text_area("문제 2 답변을 작성하세요", key="q2_answer")
if st.button("문제 2 답변 제출"):
    save_answer(2, q2_answer)

st.write("---")

# 문제 3
st.subheader("문제 3: 데이터 패턴 해석")
st.markdown("""
- 특정 조건을 만족하는 데이터를 필터링하는 코드를 작성하세요.  
- 조건: `temperature`가 27도 이상인 데이터만 추출하여 `mosquito_count`의 평균을 계산.  
- 결과를 해석하고, 이를 바탕으로 모기 발생률을 줄이기 위한 기후 관리 방안을 제안하세요.
""")
q3_answer = st.text_area("문제 3 답변을 작성하세요", key="q3_answer")
if st.button("문제 3 답변 제출"):
    save_answer(3, q3_answer)

st.write("---")

# 문제 4
st.subheader("문제 4: 데이터의 한계")
st.markdown("""
- 데이터 분석에서 발생할 수 있는 한계점을 2가지 작성하고, 이를 해결하기 위한 방법을 제안하세요.  
예) 데이터의 결측값, 이상치, 또는 시간대별 데이터 부족 등.
""")
q4_answer = st.text_area("문제 4 답변을 작성하세요", key="q4_answer")
if st.button("문제 4 답변 제출"):
    save_answer(4, q4_answer)

st.write("---")

# 교사용 데이터 확인 및 피드백 작성
st.header("교사용 데이터 확인 및 피드백")
if st.checkbox("학생 제출 데이터 보기"):
    submissions = list(users_collection.find())
    if submissions:
        df = pd.DataFrame(submissions)
        df.drop(columns="_id", inplace=True)  # MongoDB ObjectID 제거
        st.dataframe(df)

        student_id = st.selectbox("피드백을 작성할 학생을 선택하세요:", df["student_id"].unique())
        selected_student = df[df["student_id"] == student_id].iloc[0]

        st.subheader(f"{student_id} 학생의 제출물")
        for i in range(1, 5):
            st.write(f"**문제 {i} 답변**")
            st.write(selected_student.get(f"q{i}_answer", "답변 없음"))

        # 기존 피드백 표시
        existing_feedback = feedback_collection.find_one({"student_id": student_id})
        if existing_feedback:
            st.subheader("기존 피드백")
            st.write(existing_feedback["feedback"])
        else:
            st.write("기존 피드백이 없습니다.")

        # 새로운 피드백 입력
        st.subheader("피드백 작성")
        feedback = st.text_area("학생에게 제공할 피드백을 입력하세요:")
        if st.button("피드백 제출"):
            if feedback:
                feedback_collection.update_one(
                    {"student_id": student_id},
                    {"$set": {"feedback": feedback}},
                    upsert=True,
                )
                st.success(f"{student_id} 학생에게 피드백이 성공적으로 저장되었습니다!")
            else:
                st.error("피드백 내용을 입력해주세요.")
    else:
        st.write("아직 제출된 데이터가 없습니다.")