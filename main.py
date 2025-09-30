import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 기본 설정
st.set_page_config(page_title="성별 출생자 수 시각화", layout="wide")

st.title("👶 시군구별 성별 출생자 수 시각화")

# 데이터 불러오기 (캐싱)
@st.cache_data
def load_data():
    df = pd.read_csv("행정안전부_지역별(법정동) 성별 출생등록자수_20250831.csv", encoding="euc-kr")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 시군구 선택
if "시군구" not in df.columns:
    st.error("⚠️ 데이터에 '시군구' 컬럼이 없습니다. CSV 컬럼명을 확인하세요.")
else:
    regions = df["시군구"].unique()
    selected_region = st.selectbox("시군구를 선택하세요:", regions)

    # 선택된 시군구 데이터 필터링
    region_df = df[df["시군구"] == selected_region]

    # --- 성별 출생자 수 막대그래프 ---
    st.subheader(f"📊 {selected_region}의 성별 출생자 수")
    if {"성별", "출생자수"}.issubset(region_df.columns):
        fig_bar = px.bar(
            region_df,
            x="성별",
            y="출생자수",
            color="성별",
            text="출생자수",
            labels={"출생자수": "출생자 수", "성별": "성별"},
            title=f"{selected_region} 성별 출생자 수",
            template="plotly_white"
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ '성별' 또는 '출생자수' 컬럼이 없어 막대그래프를 그릴 수 없습니다.")

    # --- 연도별 성별 출생자 수 추이 (라인차트) ---
    if {"연도", "성별", "출생자수"}.issubset(region_df.columns):
        st.subheader(f"📈 {selected_region}의 연도별 성별 출생자 수 추이")
        fig_line = px.line(
            region_df,
            x="연도",
            y="출생자수",
            color="성별",
            markers=True,
            labels={"출생자수": "출생자 수", "연도": "연도", "성별": "성별"},
            title=f"{selected_region} 연도별 성별 출생자 수 추이",
            template="plotly_white"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("ℹ️ 데이터에 '연도' 컬럼이 없어 연도별 추이를 표시할 수 없습니다.")

    # --- 데이터 미리보기 ---
    st.subheader("📋 데이터 미리보기")
    st.dataframe(region_df)

