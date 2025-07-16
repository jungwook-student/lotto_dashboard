import streamlit as st
import pandas as pd
import json

# JSON 파일 불러오기
with open("lotto_100.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.set_page_config(page_title="로또 통계 대시보드", layout="wide")

st.title("🎯 로또 통계 대시보드")
st.caption("최근 100개 회차 기준 | 동행복권 API 기반")

# 회차 기준 내림차순 정렬
df = df.sort_values(by="round", ascending=False)

# 컬럼 한글명 매핑 (보기 편하게)
df.rename(columns={
    "round": "회차",
    "first_prize": "1등 당첨금",
    "first_total_prize": "1등 총 당첨금",
    "first_winner_count": "1등 당첨자 수",
    "sales": "총 판매금액"
}, inplace=True)

# 차트 탭 구성
tab1, tab2, tab3 = st.tabs(["📈 1등 당첨금 추이", "🏆 당첨자 수 및 판매금", "📋 데이터 테이블"])

with tab1:
    st.subheader("1등 당첨금 추이 (회차 기준)")
    st.line_chart(df.set_index("회차")[["1등 당첨금"]])

with tab2:
    st.subheader("1등 당첨자 수 & 총 판매금액 (회차 기준)")
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df.set_index("회차")[["1등 당첨자 수"]])
    with col2:
        st.line_chart(df.set_index("회차")[["총 판매금액"]])

with tab3:
    st.subheader("📋 전체 원시 데이터 보기")
    st.dataframe(df, use_container_width=True)