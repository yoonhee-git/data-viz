import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 인터랙티브 산불 데이터 시각화")

# 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 파일 확장자 구분하여 읽기
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 시점과 월별 NA 값이 있다면 forward fill 처리
    df[["시점", "월별"]] = df[["시점", "월별"]].fillna(method='ffill')

    # 시점 숫자로 변환
    df["시점"] = pd.to_numeric(df["시점"], errors='coerce')
    df = df.dropna(subset=["시점", "데이터"])  # 시점이나 데이터가 없는 행 제거
    df["시점"] = df["시점"].astype(int)

    # x축 선택 (월별 or 원인별)
    st.subheader("📊 x축을 선택하세요")
    x_axis = st.selectbox("x축 기준", ["월별", "원인별"])

    # 슬라이더로 연도 선택
    st.subheader("📅 연도를 선택하세요")
    selected_year = st.slider("시점을 선택하세요", min_value=df["시점"].min(), max_value=df["시점"].max(), value=df["시점"].min())

    # 시점별 정적 그래프
    st.subheader("📈 데이터 시각화 (선택된 연도)")
    filtered_df = df[df["시점"] == selected_year]
    fig_static = px.bar(filtered_df, x=x_axis, y="데이터", color=x_axis,
                        title=f"{selected_year}년 산불 발생 건수", labels={"데이터": "산불 건수"})
    st.plotly_chart(fig_static, use_container_width=True, key="static")

