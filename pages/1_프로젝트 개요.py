import streamlit as st
import pandas as pd

def show_team_data():
    st.header('2. 우리 팀이 수집한 데이터를 소개해주세요')
    
    with st.form(key='data_input_form'):
        # Define empty lists to collect input data
        data_names = []
        data_sources = []
        data_purposes = []
        data_volumes = []
        data_collection_methods = []
        
        # Create 3 rows for data input
        for i in range(1):
            st.write(f'### 수집한 데이터 {i+1}')
            data_name = st.text_input(f'데이터 이름 ', key=f'data_name_{i}')
            data_source = st.text_input(f'데이터 출처 ', key=f'data_source_{i}')
            purpose = st.text_input(f'목적 ', key=f'purpose_{i}')
            volume = st.text_input(f'데이터의 양 (Volume) ', key=f'volume_{i}')
            collection_method = st.text_input(f'데이터 수집 방법', key=f'collection_method_{i}')
            
            data_names.append(data_name)
            data_sources.append(data_source)
            data_purposes.append(purpose)
            data_volumes.append(volume)
            data_collection_methods.append(collection_method)
        
        # Submit button
        submit_button = st.form_submit_button(label='입력 완료')
        
        # If the form is submitted, display the data in a DataFrame
        if submit_button:
            data = {
                '데이터 이름': data_names,
                '데이터 출처': data_sources,
                '목적': data_purposes,
                '데이터의 양 (Volume)': data_volumes,
                '데이터 수집 방법': data_collection_methods
            }
            df = pd.DataFrame(data)
            st.write('### 제출되었습니다!')
            st.dataframe(df)

def main():
    st.title("Part I. 데이터 수집 보고서 작성")
    st.write("이 파트에서는 우리 조가 수집한 데이터를 설명하고 이를 바탕으로 프로젝트의 가설을 제시해주세요 😃!")
    st.write("---")

    # 파일 업로드 위젯
    st.header("1. 먼저 CSV 파일을 업로드 해주세요")
    uploaded_file = st.file_uploader("csv 파일을 제출해주세요",type=["csv"])

    if uploaded_file is not None:
        try:
            # 파일을 DataFrame으로 읽기
            df = pd.read_csv(uploaded_file)
            
            # 데이터프레임 표시
            st.write("업로드된 데이터:")
            st.dataframe(df)
            # main 문 실행
            if show_team_data():
                st.write("제출되었습니다!")
            # 데이터 설명 입력란
                st.header("3. 프로젝트의 개요를 적어주세요")
                data_description = st.text_area("프로젝트 설명, 우리팀이 설정한 가설 (ex: 습도는 모기 지수에 어떤 영향을 미치는가?) 등 프로젝트를 자세히 기술해주세요.")
                if data_description:
                    st.write("제출되었습니다!")
                

        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()

