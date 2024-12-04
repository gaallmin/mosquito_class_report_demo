import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="모기 지표 데이터 분석")

st.markdown("# 모기 지표 데이터 분석")
st.write("""
서울의 모기 지표 데이터를 분석합니다. 
업로드한 데이터를 바탕으로 기상값과 모기 발생량을 분석하는 웹앱
""")

# CSV 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 파일을 DataFrame으로 읽기
        df = pd.read_csv(uploaded_file)
        st.write("업로드된 데이터:")
        st.dataframe(df)

        # 사용자 선택 위젯 - 분석할 열 선택
        selected_columns = st.multiselect("분석할 열을 선택하세요", df.columns.tolist())
        if selected_columns:
            selected_data = df[selected_columns]
            st.write("선택된 지표의 데이터:")
            st.dataframe(selected_data)

            # 데이터 시각화
            st.write("### 선택된 데이터 시각화")
            chart_data = selected_data.reset_index().melt(id_vars=["index"]).rename(
                columns={"index": "Index", "variable": "Indicator", "value": "Value"}
            )
            chart = (
                alt.Chart(chart_data)
                .mark_line(point=True)
                .encode(
                    x="Index:O",
                    y="Value:Q",
                    color="Indicator:N"
                )
            )
            st.altair_chart(chart, use_container_width=True)

            # 상관관계 분석
            if len(selected_columns) == 2:
                st.write("### 선택된 지표 간의 상관관계 분석")
                correlation = selected_data.corr().iloc[0, 1]
                st.write(f"두 지표 간의 상관계수: {correlation:.2f}")
                if correlation > 0.7:
                    st.write("상관관계가 매우 높습니다.")
                elif correlation > 0.4:
                    st.write("상관관계가 중간 정도입니다.")
                elif correlation > 0:
                    st.write("상관관계가 낮습니다.")
                else:
                    st.write("음의 상관관계가 있습니다.")
            elif len(selected_columns) > 2:
                st.warning("상관관계 분석은 두 개의 열만 선택했을 때 수행됩니다.")
        else:
            st.error("분석할 열을 최소 하나 이상 선택해주세요.")

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")