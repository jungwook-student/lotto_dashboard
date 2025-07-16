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

st.subheader("📈 1등 당첨금 추이 (회차 기준)")
st.line_chart(df.set_index("회차")[["1등 당첨금"]])

st.subheader("🏆 1등 당첨자 수")
st.bar_chart(df.set_index("회차")[["1등 당첨자 수"]])

st.subheader("💰 총 판매금액")
st.line_chart(df.set_index("회차")[["총 판매금액"]])

st.subheader("🔢 당첨번호 분포 (출현 빈도순)")

# 모든 회차의 당첨번호를 하나의 리스트로 합치기
from collections import Counter
all_numbers = sum(df["numbers"], [])  # 리스트 안 리스트 → 평탄화
counter = Counter(all_numbers)

# 데이터프레임 변환 후 정렬
freq_df = pd.DataFrame(counter.items(), columns=["번호", "출현 빈도"]).sort_values(by="출현 빈도", ascending=False)

# 그래프 출력
st.bar_chart(freq_df.set_index("번호"))

st.subheader("📋 전체 원시 데이터 보기")
st.dataframe(df, use_container_width=True)
