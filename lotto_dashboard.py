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

## 역대 최다 1등 당첨자 수
st.subheader("🏆 역대 최다 1등 당첨자 수")

# 가장 많은 1등 당첨자 수 가진 회차 데이터 추출
max_row = df.loc[df["1등 당첨자 수"].idxmax()]
max_winners = int(max_row["1등 당첨자 수"])
max_round = int(max_row["회차"])
total_prize = int(max_row["1등 총 당첨금"])
per_person_prize = int(max_row["1등 당첨금"])

# 메인 숫자 강조 (전광판 스타일)
st.markdown(
    f"<h1 style='text-align:center; font-size:96px; margin-bottom:0px;'>{max_winners} 명</h1>",
    unsafe_allow_html=True
)

# 부가 정보 (중앙 정렬, 작게)
st.markdown(
    f"""
    <div style='text-align:center; font-size:18px; margin-top:5px; line-height:1.6;'>
        {max_round}회차<br>
        1등 총 당첨금: {total_prize:,}원<br>
        1인당 당첨금: {per_person_prize:,}원
    </div>
    """,
    unsafe_allow_html=True
)
###


st.subheader("📈 1등 당첨금 추이 (회차 기준)")
st.line_chart(df.set_index("회차")[["1등 당첨금"]])

st.subheader("🏆 1등 당첨자 수")
st.bar_chart(df.set_index("회차")[["1등 당첨자 수"]])

st.subheader("💰 총 판매금액")
st.line_chart(df.set_index("회차")[["총 판매금액"]])

st.subheader("🔢 당첨번호 분포 (출현 빈도순)")

# 문자열로 저장된 경우 리스트로 변환
import ast
if isinstance(df["numbers"].iloc[0], str):
    df["numbers"] = df["numbers"].apply(ast.literal_eval)

from collections import Counter
all_numbers = sum(df["numbers"], [])  # 리스트 평탄화
counter = Counter(all_numbers)

freq_df = pd.DataFrame(counter.items(), columns=["번호", "출현 빈도"]).sort_values(by="출현 빈도", ascending=False)
st.bar_chart(freq_df.set_index("번호"))



### 최다 출현번호
st.subheader("🔢 가장 많이 출현한 번호")

from collections import Counter
import ast

# 문자열로 저장된 경우 안전하게 변환
if "numbers" in df.columns and isinstance(df["numbers"].iloc[0], str):
    df["numbers"] = df["numbers"].apply(ast.literal_eval)

# numbers 필드가 제대로 있는지 체크
if "numbers" in df.columns and isinstance(df["numbers"].iloc[0], list):
    all_numbers = sum(df["numbers"], [])
    counter = Counter(all_numbers)
    most_common_num, count = counter.most_common(1)[0]

    # 숫자 크게 강조
    st.markdown(
        f"<h1 style='text-align:center; font-size:96px; margin-bottom:0px;'>{most_common_num}</h1>",
        unsafe_allow_html=True
    )

    # 설명
    st.markdown(
        f"""
        <div style='text-align:center; font-size:18px; margin-top:5px; line-height:1.6;'>
            총 출현 횟수: {count}회<br>
            분석 대상 회차: 최근 {len(df)}회차
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("numbers 데이터가 없거나 올바른 형식이 아닙니다.")
###

st.subheader("📋 전체 원시 데이터 보기")
st.dataframe(df, use_container_width=True)
