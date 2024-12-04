import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("데이터 분석 보고서 작성")

# 데이터 출처 입력

data_source = st.text_input("데이터의 출처와 설명을 입력하세요.")
analysis_method = st.text_input("사용한 분석 방법을 설명하세요.")
st.subheader("분석 결과 요약")
analysis_summary = st.text_area("분석 결과를 요약하세요.")

# 최종 제언 입력
st.subheader("최종 제언")
final_recommendation = st.text_area("최종 결론 및 제언을 입력하세요.")

# 검증 데이터 입력
st.subheader("검증 데이터 및 시각화 파일 업로드")
validation_file = st.file_uploader("시각화 jpg 파일을 업로드하세요.", type=["jpg"], key="validation")
data_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if data_file is not None:
    # 데이터프레임 생성
    df = pd.read_csv(data_file)
    st.write("업로드된 데이터:")
    st.write(df)

    

# 보고서 제출 버튼
if st.button("보고서 제출"):
    st.success("보고서 제출되었습니다!")
